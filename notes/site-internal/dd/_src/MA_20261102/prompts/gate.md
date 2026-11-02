你是 DD 管線 v20 的判斷層閘（gate），標的 MA（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（43 條）
- `f_kpi0_net_revenue_gaap`（q1_business）｜Net revenue (GAAP)＝9807 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26 Earnings Release（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_adjusted_non_gaap_operat`（q1_business）｜Adjusted (non-GAAP) operating margin＝60.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26 Earnings Release（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝59.8 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26 Earnings Release（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi7_purchase_volume_cross_bo`（q1_business）｜Purchase volume / cross-border volume growth (local currency)＝9% / 11% YoY｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26 Earnings Release（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi6_management_guidance`（q1_business）｜Management guidance＝Q4 與全年淨營收（cc、不含 inorganic）成長 high end of low double digits text｜期間與口徑：Q3 FY2026 法說會（2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Q3 2026 earnings call transcript（CFO 準備稿）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026 法說會（2026-10-29））
- `f_peer_ma_gross_margin_pct`（q2_moat）｜MA 毛利率＝78.42 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_ma_operating_margin_pct`（q2_moat）｜MA 營業利益率＝60.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_v_operating_margin_pct`（q2_moat）｜V 營業利益率＝65.57 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.V.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ma_fcf_margin_pct`（q2_moat）｜MA FCF 利潤率＝42.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_v_fcf_margin_pct`（q2_moat）｜V FCF 利潤率＝44.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.V.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_v_gross_margin_pct`（q2_moat）｜V 毛利率＝79.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.V.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pypl_operating_margin_pct`（q2_moat）｜PYPL 營業利益率＝18.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pypl_gross_margin_pct`（q2_moat）｜PYPL 毛利率＝45.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pypl_fcf_margin_pct`（q2_moat）｜PYPL FCF 利潤率＝18.37 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_axp_fcf_margin_pct`（q2_moat）｜AXP FCF 利潤率＝19.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AXP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cof_fcf_margin_pct`（q2_moat）｜COF FCF 利潤率＝45.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COF.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.04 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝23.13 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝26.94 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.93 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 19.66 → 20.04（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_adjusted_diluted_eps`（q1_business）｜Adjusted diluted EPS＝5.31 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26 Earnings Release（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝37348.49 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（34 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝42060.51 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（34 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_9m_ytd`（q4_capital）｜SBC 占營業利益 (9M YTD)＝3.2 %｜期間與口徑：9M FY2026（至 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26（SBC 525M ÷ GAAP 營業利益 16,356M 推算）（numbers.latest_quarter_kpis.items[4]，as_of 9M FY2026（至 2026-09-30，公告於 2026-10-29））
- `f_kpi3_free_cash_flow_9m_ytd_q3`（q1_business）｜Free cash flow (9M YTD，Q3 單季未揭露)＝10718 USD M｜期間與口徑：9M FY2026（至 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 3Q26（OCF 11,859 − capex 1,141 推算）（numbers.latest_quarter_kpis.items[3]，as_of 9M FY2026（至 2026-09-30，公告於 2026-10-29））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.545 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝13474.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 23938.0、現金 10464.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝871.18 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝569293.07 USD m｜期間與口徑：2026-11-02／市值 555819.07 ＋ 淨負債 13474.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝638.01 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝31.84 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 20.04，分子＝快照價 638.01｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝33.39 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝15.32 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝15.69 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝29.18 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 638.01 / W52 538.68 / W104 542.77 / W250 451.48 / W250 13週斜率 0.94%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝538.68 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝542.77 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝451.48 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.94 %｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出競爭者含 Visa、AmEx、JCB、銀聯、Discover，並指即時帳戶對帳戶支付系統可能侵蝕 P2M/P2P 份額；部分對手在特定地區份額高於 MA
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：部分客戶與對手有近乎排他關係，且 MA 自這些客戶取得可觀營收，客戶可能將業務轉給對手
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因子：Mastercard 多數客戶關係非排他，客戶可依合約重新評估承諾，也可能自行開發競爭服務。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K 競爭段列出數位錢包等金融科技可用內部帳戶轉帳、帳戶對帳戶即時支付網路處理付款，不經卡網路。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-11）｜affects：moat_trend
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：Lloyds Banking Group 與 Visa 續約擴大，約 1000 萬張信用卡與簽帳卡由 Mastercard 轉至 Visa。
  - 來源：Banking Exchange: Lloyds to Transfer 10 Million Cards to Visa（as_of 2024-06-26）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：前五大客戶 2025 年淨營收約 69 億美元，占總淨營收 21%；失去任一客戶或其重要卡方案可能衝擊營收。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因子揭露營收集中於前五大客戶，失去其中任一家可能有重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Mastercard 10-K FY2025 披露其為多起民事訴訟及監管調查的被告，包括指控違反競爭與反壟斷法者；若在反壟斷主張下敗訴可能面臨三倍賠償，對業務與經營成果造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：DOJ 反壟斷司對 Mastercard 美國簽帳金融卡業務發出 CID，Mastercard 配合調查；10-Q 列示 ATM 附加費訴訟與歐盟執委會資訊請求
  - 來源：Mastercard 10-Q 2026-03-31（as_of 2026-03-31）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Visa/Mastercard 與商家和解：平均有效信用卡交換費降低10bp五年，並限制附加費；參議員 Durbin 稱其不足，信用卡競爭法案2026-01重新提出
  - 來源：Digital Transactions / Payment Expert（as_of 2025-11-18）｜affects：valuation、triggers、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：MA 10-K 風險因子將關稅相關的不確定全球貿易政策列為可能對業務（含消費與企業支出）及利害關係人關係產生不利影響的因素；屬間接暴露，未量化。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：MA 10-K 指出地緣事件、OFAC 制裁與不利貿易政策可能引發相關司法管轄區報復行動而不利業務；OFAC 制裁限制與特定國家／實體往來。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026 財報電話會議（2026-07-30）：管理層指中東衝突造成的地緣不確定性趨緩但仍壓抑跨境旅遊與支出。
  - 來源：GuruFocus, Q2 2026 Mastercard Inc Earnings Call Transcript（as_of 2026-07-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Marqeta 狀態頁記錄 2026-09-03 Mastercard 端平台故障，使其整合服務降級約 7.5 小時；根因是否共用未見揭露。
  - 來源：isdown.app Marqeta incident 648879（as_of 2026-09-03）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 自述：即時帳戶對帳戶支付成熟後，國內 P2M/P2P 市佔競爭可能增加，跨境市佔也可能被基礎設施互連所擾動；多項產業倡議在試驗帳戶型全球機制，可能擾動清算結算選項。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 自述：穩定幣與加密貨幣可能隨監管（如 GENIUS Act）更普及，加密原生業者有能力擾動傳統金融市場；對公司既是機會也可能與其產品競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-11）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：新技術可能優於或使現有技術過時，並促使使用其技術的客戶（含金融科技與科技公司）改用自有技術與之競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：10-K 指出 fintech 與新興支付業者可能以內部帳戶轉帳、即時帳戶對帳戶網路等非卡軌處理支付，對客戶與資料構成競爭
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：Macquarie 曾因中東衝突總經影響下調目標價至 $665；Raymond James 下調目標價至 $631（自 $707）。
  - 來源：Munich startup insights feed; TipRanks/The Fly（as_of 2026-07-01）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露英國集體訴訟（索賠逾 £10 億英鎊）及美國 EMV 責任轉移集體訴訟（原告主張單一損害逾 $10 億）。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-11）｜affects：decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：英國集體訴訟索賠逾 £10 億英鎊；美國 EMV 責任轉移集體訴訟原告主張單一損害逾 $10 億。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-11）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1302.0,"bear_5y_price":456.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":57.9,"ev5y_pct":43.5,"irr_base_pct":9.6,"asym_ratio":3.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.04,"pe":31.84,"basis":"2026年度共識EPS（FY1）；判斷日已過該年10個月，終端同樣用2031年度EPS乘倍數，口徑一致"},"eps":{"bull":[23.5,27.6,32.0,36.8,42.0],"base":[23.0,26.5,30.0,33.6,37.3],"bear":[21.2,20.3,20.9,21.8,22.8]},"pe":{"bull":31,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.545,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12.0,"base_cagr_pct":9.5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MA_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Sachin Mehra｜guidance：CFO 給 Q3 淨收入成長指引：幣別中性、排除併購後落在低雙位數區間的高端（原話："expected to be at the high end of low double-digit"）
- 2026-07-30｜Sachin Mehra｜guidance：全年淨收入指引區間不變，但表示因上半年較強，預期落在區間內較高位置（原話："we now expect to be higher within the range than"）
- 2026-07-30｜Sachin Mehra｜guidance：Q3 營業費用成長指引為低雙位數，並有 0.5 ppt 併購逆風（原話："Q3 growth to be at the low double-digits range versus"）
- 2026-07-30｜Sachin Mehra｜guidance：Q3、Q4 非 GAAP 稅率預期 20%–21%（原話："20% to 21% for both Q3 and Q4."）
- 2026-07-30｜Sachin Mehra｜guidance：全年外匯對淨收入預期為約 1 ppt 順風；Q3 則為約 0.5 ppt 逆風（原話："a tailwind of approximately 1 ppt from foreign exchange."）
- 2026-07-30｜Sachin Mehra｜guidance：下半年基本情境假設消費維持健康，且中東衝擊維持 Q2 末水準（原話："our base case continues to assume spending remains healthy."）
- 2026-07-30｜Sachin Mehra｜guidance：Q3 回扣與誘因占網路評估費的比率預期略高於 Q2（原話："slightly higher than it was in Q2."）
- 2026-07-30｜Sachin Mehra｜guidance：BVNK 收購預期 Q3 完成，淨收入影響極小、營業費用有些影響，皆已納入指引（原話："Minimal impact from a net revenue standpoint."）
- 2026-07-30｜Sachin Mehra｜margin：Q2 營業費用成長 10%（含處分 1 ppt 效益），營業利益成長 14%，淨利 16%、EPS 19%（原話："Operating expenses increased 10%, including a 1 ppt benefit"）
- 2026-07-30｜Sachin Mehra｜margin：費用成長主因為執行策略優先事項的支出：強化基礎設施、地理擴張、產品創新（原話："to further harden our infrastructure, geographic expansion"）
- 2026-07-30｜Sachin Mehra｜margin：Q2 EPS 5.04 美元，含 0.14 美元回購貢獻（原話："EPS was $5.04, which includes a $0.14 contribution from"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：國內評估費成長 10% 對 GDV 成長 8%，差距主要來自定價（原話："The 2 ppt difference is primarily"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：跨境評估費成長 20% 對跨境量 12%，差距 8 ppt 主要來自國際市場定價與組合（原話："The 8 ppt difference is driven primarily by pricing in"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：交易處理評估費 12% 對交易筆數 9%，差距來自組合與定價，部分被 FX 波動帶來的較低收入抵銷（原話："due to favorable mix and pricing, partially offset by lower"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：美國借記 GDV 成長 1%，剔除 Capital One 遷移後為 8%（原話："our U.S. debit GDV growth would have been 8%."）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：網路評估淨收入成長 8%，VAS 成長 18%（原話："Payment network net revenue increased 8%,"）
- 2026-07-30｜Michael Miebach｜margin：數字口徑：VAS 約 60% 淨收入與網路連結（network linked）（原話："about 60% of our value-add services and solutions net"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：Q2 上行來源含委內瑞拉跨境支出回升（中東衝擊較預期輕、VAS 需求強）（原話："an uptick in cross-border spend out of Venezuela"）
- 2026-07-30｜Sachin Mehra｜margin：數字口徑：美國排除 Capital One 後交換量成長 10%，較上季高 2 ppt，歸因於燃油支出與整體消費（原話："U.S. switched volume growth was 10% or 2 ppt"）
- 2026-07-30｜Sachin Mehra｜capital_allocation：Q2 回購 49 億美元，另至 7/27 再回購約 7 億美元（原話："we repurchased $4.9 billion worth of stock and approximately"）
- 2026-07-30｜Michael Miebach｜capital_allocation：預期本季完成 BVNK 收購，定位為可信的互通層（原話："We expect to close the BVNK acquisition this quarter."）
- 2026-07-30｜Devin Corr｜capital_allocation：IR 宣布 Ling Hai 8/3 起接任 CFO（Sachin Mehra 轉任 Chief Business Officer）（原話："incoming CFO effective August 3."）
- 2026-07-30｜Sachin Mehra｜commitment：管理層表示不追求無利潤的量；舉放棄 Lloyds Credit 為例（原話："Volume for the sake of volume is not what this company"）
- 2026-07-30｜Sachin Mehra｜commitment：管理層稱只追求能提高淨收入收益率（net revenue yield）的量（原話："Profitable volume, which is"）
- 2026-07-30｜Michael Miebach｜commitment：對在地交換合作設定條件：須技術可行、經濟上合理（原話："the give and take has to work for us."）
- 2026-07-30｜Michael Miebach｜commitment：Open USD 預計年內上線，且 Mastercard 稱會同時支援多種幣別（原話："Open USD is set to go live later this year."）
- 2026-07-30｜Michael Miebach｜competition：交換滲透率升至 72%，管理層歸因於相對在地網路的價值主張（原話："switching penetration now reaching 72%."）
- 2026-07-30｜Michael Miebach｜competition：阿聯酋：與央行子公司合作建置國內交換，Mastercard 為 Jaywan 聯名信用卡的主要國際品牌，屬增量交易（原話："These transactions are incremental to what we process"）
- 2026-07-30｜Michael Miebach｜competition：歐洲被描述為高度競爭市場，數位歐元在籌備；目前以卡片主張為主，保留彈性（原話："Europe it's a very competitive market"）
- 2026-07-30｜Sachin Mehra｜competition：歐洲購買量成長從 2024 Q2 的 16% 放緩，管理層歸因於先前大型贏單的基期效應與放棄部分交易（原話："back in Q2 of"）
- 2026-07-30｜Michael Miebach｜competition：管理層稱 Mastercard 是唯一能做機器對機器支付的網路（原話："Mastercard is the only network enabling"）
- 2026-07-30｜Michael Miebach｜product：穩定幣定位：對 B2B 與 P2P 有明確效用，P2M 無待解問題（原話："but no problem to solve"）
- 2026-07-30｜Michael Miebach｜product：代理式商務：管理層預期卡片在代理世界仍佔優（原話："we expect cards will prevail in an agentic world"）
- 2026-07-30｜Michael Miebach｜product：加密聯名卡量兩年增逾三倍（原話："Our crypto co-brand"）
- 2026-07-30｜Michael Miebach｜product：Threat Intelligence 前三季辨識逾 700 萬筆卡片測試交易，估計阻止 1.72 億美元詐欺（原話："prevented an estimated $172 million in fraud linked to"）
- 2026-07-30｜Sachin Mehra｜product：代幣滲透率逾 40%（非接觸 80%，卡片成長 5%）（原話："token penetration reached over 40% of all switched"）
- 2026-07-30｜Michael Miebach｜customer：上半年贏得數百筆轉換與擴約，預期未來十年帶來數兆美元增量交易量（原話："which are expected to drive trillions of dollars in"）
- 2026-07-30｜Michael Miebach｜customer：續約 JPMorgan Chase Freedom Flex 與 Banamex（原話："renewed a key partnership"）
- 2026-07-30｜Michael Miebach｜customer：過去 12 個月淨新增逾 2.3 億張 Mastercard（原話："added over 230 million net new Mastercards"）
- 2026-07-30｜Michael Miebach｜customer：商用借貸記量成長 12%（原話："commercial debit and credit volumes grew at 12%"）
- 2026-07-30｜Sachin Mehra｜customer：美國消費廣泛健康，涵蓋信用與借記、消費與商用，大眾與富裕客群皆穩，富裕端成長較高（原話："it's broad-based. We see it across credit and debit."）
- 2026-07-30｜Michael Miebach｜risk：管理層持續監控地緣政治與其潛在經濟影響（原話："monitor geopolitical uncertainty and its potential"）
- 2026-07-30｜Sachin Mehra｜risk：中東情勢仍具動態性，管理層以多元化業務作為緩衝（原話："the environment in the Middle East remains dynamic."）
- 2026-07-30｜Sachin Mehra｜risk：Q2 跨境強勁部分來自委內瑞拉美元可得性提高（2018 年已解併）（原話："increased availability of U.S. dollars"）
- 2026-07-30｜Sachin Mehra｜risk：美國成長受惠於較高燃油價格；世界盃可能有貢獻但無法量化（原話："a tailwind, which has come on account of higher fuel prices"）

### 問答異常語氣（迴避／改口／保留）
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Sanjay Sakhrani 問跨境 4–6 月加速的幅度是否受世界盃影響、是否會回落｜答法：未直接回答世界盃占比與是否回落；稱「難以辨識是否與世界盃有關」，改談中東復甦與委內瑞拉
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Tien-Tsin Huang 問美國 10% 成長是否有持續力、是否廣泛｜答法：承認燃油價格與世界盃有貢獻但稱無法量化，未給持續性判斷，轉述基本面健康
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Andrew Jeffrey 問阿聯酋式國內交換還會鎖定哪些市場、歐洲是否適用｜答法：未點名其他目標市場，稱各地有「不同版本」，並強調須符合經濟原則；歐洲「目前」以卡片為主但保留彈性
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Harshita Rawat 問歐洲購買量成長減速的原因與未來成長｜答法：以基期效應與放棄 Lloyds 等交易解釋，未給歐洲未來成長數字或區域指引
- MA_Q2_2026_Earnings_Call_20260730.md｜問：Tim Chiodo 問 VAS 中安全類占比是否更新（先前約 40%）｜答法：未提供安全類占比數字，只重申約 60% 網路連結並說收購不會顯著改變

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 3 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 4 | 1 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260703","verdict":"進場","role":"核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"無現金化 secular 滲透持續 + V/MA 雙寡頭定價權維持（卡網路仍是陌生人信任層的主軌）","columns":{"2Y 驗證點":"GDV YoY lc &ge; +7%、switched txns &ge; +9%","5Y 驗證點":"MA 處理筆數複合 &ge; +8%/yr；net take rate 不下滑","10Y 驗證點":"穩定幣/A2A 占 MA 可及流量 &lt; 5%（繞道未跨門檻）","具體數字門檻":"Q1 FY26：GDV +7%lc、switched txns +9%（達標）","信息來源":"MA FY26 Q1 法說（2026-04-30）、MA Investor Day 2025","漂移觸發條件":"net take rate 連 4 季下滑 或 A2A 占比 &ge; 5% → 反轉（5Y 假設，QC-35 連 4 季）"}},{"id":"H2","text":"跨境復甦 + VAS/Move 高速成長兌現 15-16% EPS CAGR（三引擎接力）","columns":{"2Y 驗證點":"跨境 YoY cc &ge; +10%；VAS cc &ge; +15%；Move &ge; +30%","5Y 驗證點":"VAS 占 Rev &ge; 40%；Move 年化 &ge; $8T","10Y 驗證點":"VAS 占 incremental revenue &ge; 55%；Move $15T+","具體數字門檻":"Q1 FY26：跨境 +13%cc、VAS +18%cc、Move +32%（達標）","信息來源":"MA FY26 Q1 法說、MA Investor Day 2025、Mastercard Move whitepaper","漂移觸發條件":"跨境連 2 季 &lt; +8% 或 VAS 連 4 季 cc &lt; +15% → 削弱（QC-34/35）"}},{"id":"H3","text":"估值從 5Y 低位（Fwd PE 23.7x）修復（板塊 de-rate 過度、基本面加速被錯殺）","columns":{"2Y 驗證點":"Fwd PE 分位回升至 5Y 中段（&ge; 40th）","5Y 驗證點":"倍數回到 26-30x（A 級複利應得）","10Y 驗證點":"非依賴 re-rate；EPS 複利本身即達標","具體數字門檻":"當前 Fwd PE FY27 23.7x = 5Y ~5th 分位（5Y 區間 24-40x）","信息來源":"yfinance / GuruFocus 5Y forward PE band、本報告 §11.1","漂移觸發條件":"此為市場假設，非動作觸發；若倍數不修復但 EPS 複利，報酬仍 12-13%（§11.6 非估值依賴）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"全球旅遊 + 跨境放緩（MA 比 V 對跨境更敏感；管理層 Q1 已示警 4 月起 YTD cross-border 減速）","columns":{"對應假設":"H1/H2","時間尺度":"⚡→🔥 短中期（1-2 季可觸發，4-6 季確認）","監測指標":"MA 跨境體積 YoY cc、UNWTO 國際旅客增速、單月消費信心","警戒閾值":"連 2 季跨境 YoY cc &lt; +8% → 削弱"}},{"id":"R2","text":"DOJ v Visa（借記壟斷案）連帶 + FTC 對 MA 推 consent decree / interchange 監管收緊","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"DOJ v Visa 進度（fact discovery 2026-10-16 截止、expert discovery 至 2027-04-08 → 裁決預估 2027-2028；惟 2026-06 已有法院初步核准的 Equitable Relief 和解對 V/MA 皆具約束，近期訴訟尾部偏降溫）；FTC 是否啟動 MA inquiry；CCCA 2026（Durbin/Marshall 重提、傳獲行政部門支持，歷來最接近通過）；歐盟 interchange 上限","警戒閾值":"① V 遭強制拆分/重大和解 → MA 連帶 reprice 向 18x；② FTC 對 MA 啟動 inquiry → 立即重評"}},{"id":"R3","text":"穩定幣 / A2A / Capital One-Discover 三軌結構替代（繞卡去中介化）","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數，需 &ge; 50% 機率才砍倉）","監測指標":"① 穩定幣（USDC/USDT）商戶結算量；② A2A（Pix/UPI/FedNow/Wero）在主力市場的消費滲透；③ Capital One 把 credit 卡量遷至 Discover 網路的比例；④ MA net take rate 趨勢","警戒閾值":"① 穩定幣/A2A 結算量達 MA 可及流量 5%；② Capital One 把 &gt; 20% credit 卡轉至 Discover；③ MA net take rate 連 4 季結構下滑"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.0,"ev5y_pct":75.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心持倉","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":7.0,"ev5y_pct":75.0,"irr_base_pct":13.0,"max_dd_pct":-45.0,"bull_5y_price":1310.0,"bear_5y_price":405.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":539.39,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MA","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Mastercard Incorporated"},"oneliner":"卡網路量價與加值服務雙引擎仍穩（Q3淨營收+14%、調整後EPS+21%），但半年漲29%後本益比約32倍、五年年化只剩約10%；美國強制信用卡路由立法是最大單一風險，不追，等580美元以下","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MA_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺全球每筆卡片交易的網路評估費與加值服務費，錢卡在發卡行選網路與商店受理兩個節點；Q3淨營收98.07億美元、調整後營益率60.5%","reasoning":"賺誰的錢：發卡行與商店為每筆交易付網路評估費（國內、跨境、交易處理），MA另向銀行、商店與企業賣加值服務（詐欺與身分、數據分析、行銷、代幣化、資安）。Q3淨營收98.07億美元，其中支付網路約57億美元（+11%）、加值服務40.6億美元（+19%，約60%與網路量連動）（3Q26財報新聞稿，2026-10-29）；GAAP營益率59.8%、調整後60.5%，TTM毛利率78.4%。錢卡在兩個節點：發卡行選哪個網路（前五大客戶占2025年淨營收21%，單一客戶都不到10%——集中度是風險，不是護城河證據），以及商店受理（逾2億個受理點）。量價：購買量+9%、跨境+11%、交易筆數+9%；國內評估費+13%對GDV+7%。產業時鐘II（擴張）：GDV與交易筆數穩定成長，管理層描述勞動市場平衡、家庭資產負債表強、薪資續增。供需持久性：結構性持久，現金數位化與受理擴張仍在延伸，週期性部分主要是跨境旅遊。產業態勢：雙向拉鋸——結構轉好（受理點上半年+20%、加值服務+19%）對上其他結構變動（監管：和解費率上限、信用卡競爭法案重提、DOJ調查令；替代技術：A2A與穩定幣）。","fact_refs":["f_kpi0_net_revenue_gaap","f_kpi1_adjusted_non_gaap_operat","f_kpi2_gaap_operating_income_ma","f_kpi7_purchase_volume_cross_bo","f_kpi6_management_guidance","f_peer_ma_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"高：按交易量與筆數計費的經常性收入；扣分處是回扣與誘因（抵減收入）+18%快於淨營收+14%，且Q3含服務專案與簽約從Q4提前（管理層稱Q4回吐）","unit_econ_note":"Q3每單位量的收費持續上升：國內評估費+13%對GDV+7%、跨境評估費+16%對跨境量+11%、交易處理評估費+14%對交易筆數+9%，差距來自定價與組合（2026-10-29法說）","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"雙邊網路收費、資產輕、營益率約60%、FCF高於淨利、EPS年增15%以上且持續回購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：受理點上半年年增20%、店內非接觸占81%、過去12個月淨增逾2.3億張卡（Q2與Q3法說）；週期性部分主要是跨境旅遊","bargaining":{"up":"事實表未涵蓋供應商集中度；前九個月資本支出11.41億美元、只占FCF約11%，上游投入規模小","down":"發卡行議價最強：前五大客戶占2025年淨營收21%、多數關係非排他、回扣與誘因+18%；商店端以訴訟與立法施壓（和解費率上限、信用卡競爭法案）","geo":"印度、巴西的政府主導A2A壓縮國內卡片份額；中國正擴大發卡與受理；中東衝突壓抑跨境旅遊"},"profit_pool_dir":"利潤池往加值服務（安全、代幣化、數據）與跨境移動；國內網路費受監管上限與A2A夾擊","tam_table":{"expanded":false,"reason":"事實表未涵蓋全球消費支出的卡片滲透率與利潤池占比；本案成長承重在已揭露的量價與加值服務成長率，不靠TAM外推"}}}},"q2_moat":{"verdict":"護城河穩定（→）、等級B：定價權仍在擴大，但美國份額小輸Visa、發卡行分走更多回扣、監管上限逼近，三者抵銷","reasoning":"機制：雙邊網路（38億張卡×逾2億受理點）加上代幣化、詐欺偵測與加值服務把發卡行綁住，與Visa共享雙寡頭結構租金。方向：定價面Q3國內評估費比GDV多6pp、跨境多5pp、交易處理比筆數多5pp，仍在擴大；執行面贏單（Pinnacle 2027年整批轉入、印度HDFC、德國DSGV與DZ Bank續約、北歐Handelsbanken與Swedbank續約、中國銀行簽帳卡）與失單（Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出使美國簽帳卡只+1%、2025年美國購買量成長6.3%略低於Visa的6.8%）互抵；加上社會容忍度上限壓住定價延續性，綜合判為穩定（→）。同業比較：TTM營益率60.1%比Visa 65.6%低約5.5pp、FCF利潤率42.5%對44.9%，差距反映Visa的規模份額，兩家吃的是同一塊結構租金；對PayPal（營益率18.5%）等其他支付同業大幅領先。與Visa差距的兩年趨勢事實表未涵蓋，但MA自身營益率2022至2025年由57.2%升到59.5%，沒有證據顯示差距在擴大，因此不另扣分。評分：執行8（美國份額小輸、失單）、定價8（提價仍強但碰到監管上限），等級B；A2A列生態攻擊，扣分後仍不低於7分、等級不變。當期報酬：高利益率×高周轉；稅後營業利益率約47.8%，投入資本口徑事實表未涵蓋。","fact_refs":["f_peer_ma_operating_margin_pct","f_peer_v_operating_margin_pct","f_peer_ma_fcf_margin_pct","f_peer_v_fcf_margin_pct","f_peer_ma_gross_margin_pct","f_peer_v_gross_margin_pct","f_peer_pypl_operating_margin_pct","f_peer_pypl_gross_margin_pct","f_peer_pypl_fcf_margin_pct","f_peer_axp_fcf_margin_pct","f_peer_cof_fcf_margin_pct","f_kpi1_adjusted_non_gaap_operat"],"verdict_values":{"moat":{"mechanism":"雙邊網路效應：38億張卡×逾2億受理點，加上代幣化、詐欺偵測與加值服務綁定發卡行；與Visa雙寡頭共享","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價：Q3國內評估費比GDV多成長6pp、跨境多5pp→擴大；執行：美國簽帳卡因Capital One轉移只+1%、2025年美國購買量MA+6.3%對Visa+6.8%、Lloyds約1000萬張卡轉Visa，對上Pinnacle、HDFC、德國與北歐續約→穩定；監管上限與回扣誘因+18%壓住定價延續性→綜合穩定","competitor_notes":[{"name":"V","strategy_note":"最強同業：營益率65.6%比MA高約5.5pp、FCF利潤率44.9%；美國購買量份額約70%，2025年成長6.8%略快於MA，並從MA拿走Lloyds"},{"name":"AXP","strategy_note":"閉環發卡兼網路，FCF利潤率19.8%（截至2026-06）；爭奪高端消費者，與MA富裕客群（支出成長為整體信用卡2倍）正面重疊"},{"name":"COF","strategy_note":"併入Discover網路後把簽帳卡從MA移走（美國簽帳卡Q3僅+1%），是美國能垂直整合的大型發卡行；FCF利潤率45.0%屬銀行口徑，不可直接比"},{"name":"PYPL","strategy_note":"錢包業者，營益率18.5%、毛利率45.8%；多數交易仍跑卡網路，MA稱錢包與先買後付業者最後多選擇合作，屬合作兼競爭"}],"spread_notes":{"vs_strongest_peer":"營益率比Visa低約5.5pp、FCF利潤率低約2.4pp（TTM）；兩年趨勢事實表未涵蓋","vs_others":"營益率比PayPal高約41.6pp；AXP、COF為發卡銀行，口徑不可比"},"peer_na_reason":"同業ROIC事實表未涵蓋，以營益率與FCF利潤率代替；AXP、COF為發卡銀行，利潤率口徑不可直接比","threats":[{"level":"🟡","text":"Visa點對點搶單：Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出；部分客戶與對手近乎排他、多數關係非排他，續約時可整包換網路","p":"40%","evidence_refs":["customer_second_source#2","competitive_share_entrants#1","customer_second_source#0"]},{"level":"🔴","text":"A2A即時帳戶支付與金融科技內部轉帳的生態攻擊：10-K自述A2A成熟後國內P2M／P2P份額競爭可能增加、互連後也可能擾動跨境；印度UPI已成規模，MA以在地錢包嵌卡與簽帳卡競爭回應","p":"35%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#1","channel_business_model_shift#1"]},{"level":"🟡","text":"穩定幣與加密原生業者：10-K稱可能與產品競爭、新技術可能讓現有技術過時；目前MA以BVNK參與、P2M用途未見量，暫列點狀；若穩定幣商戶結算占可及流量達5%升為生態攻擊","p":"30%","evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（持卡人）、決策者（發卡行選網路、商店決定受理）、付款者（商店付手續費、發卡行付評估費）三方都成立：38億張卡、逾2億受理點、受理點上半年+20%、店內非接觸占81%；電子支付是需要不是想要，延後的代價是退回現金"},{"item":"決策層級","level":"🟡","text":"替代發生在發卡行的卡組合層級，不在持卡人：Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出、Pinnacle 2027年整批轉入MA——多年合約到期時整包換網路；前五大客戶占21%營收，代理變數是續約與回扣條件"},{"item":"價值鏈分配","level":"🟡","text":"和解上限針對的是發卡行的交換費，MA收網路評估費與服務費；但回扣與誘因+18%快於淨營收+14%、Q4占總評估費比率再升，代表發卡行在續約時分走更多；淨營收仍+14%，MA這一節點目前仍最難被取代"},{"item":"社會容忍度","level":"🔴","text":"商家和解平均交換費降0.1pp五年、標準消費信用卡費率上限1.25%八年；信用卡競爭法案2026-01重提、DOJ對簽帳卡發調查令、歐盟資訊請求；評估費每季比量多成長5–6pp，政治上限已在視線內，實際定價上限由社會容忍度決定"}],"roiic":"公式值無意義：2022至2025年淨利由99.3億增至149.7億美元（+50.4億），同期FCF/淨利維持0.97–1.10，新增獲利幾乎不需新增投入資本，增量報酬遠高於資金成本；投入資本口徑事實表未涵蓋，無法給精確數字","reinvest_rate":"約10%：前九個月資本支出11.41億美元（D&A事實表未涵蓋，淨額視為接近零）＋BVNK收購14億美元，對照稅後營業利益約155億美元（2025年營業利益約195億×(1−20.5%)）；其餘FCF以回購與股息配回","endo_ceiling":12.5,"formula_note":"增量報酬×再投資率對資產輕的網路不適用（增量報酬趨近無限、再投資率低），改以有機營運上限代替：量8–9%（購買量、交易筆數皆+9%）＋價格組合約4pp，營益率持平→有機淨營收與營業利益約12–13%，取12.5%，不含回購。稅後營業利益率約47.8%（TTM營益率60.07%×(1−20.5%)），投入資本周轉率未涵蓋，當期ROIC無法算出"}}}},"q3_growth":{"verdict":"五年後跑道寬（🟢）：量、價、加值服務三條線都有財報證據；共識EPS年增約16%中約3pp靠回購與營益率","reasoning":"成長來源：量（購買量、交易筆數各+9%）＋價與組合（評估費比量多成長5–6pp）＋加值服務（+19%），回購墊高EPS（Q3回購貢獻0.16美元，約3%），收購影響極小。共識EPS：2026年20.04、2027年23.13、2028年26.94美元（Koyfin快照，家數未標；營收共識34位），前瞻兩年年增約15.9%；若以2025年GAAP稀釋EPS 16.52美元為基期，三年約17.7%，但基期與共識口徑可能不同，以前者為準。再投資報酬檢核的有機上限約12.5%（不含回購），缺口約3.4pp：淨回購約2–2.5pp、營益率擴張約1pp（Q3營業利益+15%對淨營收+14%），可歸因，不依賴重估。跑道：卡片滲透率事實表未涵蓋，無法換算年數；但第二曲線有財報證據——加值服務占淨營收約41%、前九個月+20%，另有商務虛擬卡、代理式商務與BVNK穩定幣基礎設施，五年後跑道判寬（🟢）。十類衰退信號亮2項（美國簽帳卡份額、倍數4年下移），長期成長性與陷阱風險皆為中。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi7_purchase_volume_cross_bo","f_kpi6_management_guidance","f_kpi5_adjusted_diluted_eps","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量約8–9%（購買量、交易筆數各+9%）＋價格與組合約4pp＋加值服務組合上移；回購每年約2–3%墊高EPS（Q3回購貢獻0.16美元）；收購影響極小","runway_years":"事實表未涵蓋卡片滲透率，無法換算達30%滲透率的年數","runway_post_y5":"🟢","endo_ceiling_basis":"有機上限約12.5%（量8–9%＋價格組合約4pp、營益率持平、不含回購）；前瞻兩年共識EPS年增約15.9%，缺口約3.4pp歸因淨回購約2–2.5pp與營益率擴張約1pp，可歸因、非依賴重估","segments":[{"item":"支付網路淨營收（Q3 2026）","value":"約57億美元，+11%：量與定價，已扣回扣與誘因"},{"item":"加值服務淨營收（Q3 2026）","value":"40.6億美元，+19%，約占淨營收41%；前九個月113.34億美元、+20%；約60%與網路量連動"},{"item":"跨境（Q3 2026）","value":"跨境量+11%、跨境評估費+16%；非旅遊線上交易由Q2的20%降到15%，歐洲內部跨境由16%降到10%"}],"decay_signals":[{"item":"毛利率連2季年減","lit":false,"note":"季度毛利率事實表未涵蓋；年度由76.3%升到77.9%"},{"item":"核心市占近12個月縮減","lit":true,"note":"美國簽帳卡因Capital One轉移Q3只+1%；2025年美國購買量MA+6.3%略低於Visa+6.8%；Lloyds約1000萬張卡轉Visa"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"評估費比量多成長5–6pp，交易筆數仍+9%"},{"item":"EPS年複合高於營收年複合逾5pp","lit":false,"note":"2022至2025年GAAP EPS年複合約17.4%、營收約13.8%，差3.6pp"},{"item":"FCF/淨利連2年低於0.75","lit":false,"note":"2024年1.06、2025年1.10"},{"item":"SBC/營收逾5%且逐年上升","lit":false,"note":"前九個月SBC占營業利益3.2%，換算約占營收2%"},{"item":"TAM萎縮或被替代技術壓縮","lit":false,"note":"10-K只是潛在風險敘述；印度、巴西的A2A屬既有格局，未見全球卡片可及流量萎縮的量化證據，改列護城河威脅"},{"item":"估值倍數近3年系統性下移","lit":true,"note":"落後本益比33.4倍、市銷率15.3倍皆為4個年度端點中最低"},{"item":"維持性資本支出占FCF逾60%","lit":false,"note":"前九個月資本支出11.41億美元對FCF 107.18億美元，約11%"},{"item":"停止投資新產能且收入3年內下滑","lit":false,"note":"收入2023至2025年各+12.9%、+12.2%、+16.4%"}],"trap_rating":"價值陷阱風險中、長期成長性中（亮2項）"}}},"q4_capital":{"verdict":"資本配置中等：SBC稀釋極低、FCF高於淨利，但以30倍以上本益比回購的報酬偏低，收購報酬尚未證實","reasoning":"現金品質：FCF高於淨利，2024年FCF/淨利1.06、2025年1.10；前九個月FCF 107.18億美元，資本支出11.41億美元只占約11%。SBC占營業利益3.2%（前九個月），年化約7億美元，對市值稀釋約0.13%。股東回饋：Q2回購49億美元、Q3回購30億美元、10月至26日再6.48億美元，股息殖利率0.55%；在30倍以上本益比回購，盈餘殖利率只有約3.1–3.7%，報酬偏低。收購：BVNK 14億美元8月完成，管理層稱收入基期小、影響極小。負債：淨負債134.7億美元，穆迪Aa3／標普A+、展望穩定。計分：SBC稀釋過、回購收益率不過、收購報酬未能衡量，判B。現金去向三年四分、債務到期結構與加權利率事實表未涵蓋。","fact_refs":["f_kpi4_sbc_9m_ytd","f_kpi3_free_cash_flow_9m_ytd_q3","f_dividend_yield_ttm","f_net_debt_m","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"BVNK於2026-08-03以現金14億美元收購（另有最高3億美元或有對價），管理層稱對加值服務成長影響極小、基期小；收購兩個月，已實現增量報酬無法衡量；更早的收購事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q2回購49億、Q3回購30億美元；回購均價事實表未涵蓋，以期間股價約540–640美元對2026年共識EPS 20.04推算盈餘殖利率約3.1–3.7%；10年期殖利率事實表未涵蓋，只要高於1.7%即不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九個月SBC 5.25億美元（占營業利益3.2%），年化約7億美元，約為市值5558億美元的0.13%，遠低於每年1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：管理層稱收購對淨營收影響極小、BVNK基期小；現金去向三年四分資料事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求五年EPS年增約13%且本益比只降到27倍，才換到約10%年化；EPS路徑可信，倍數沒有再上行空間——合理但不追","reasoning":"現價638.01美元＝2026年度共識EPS的31.8倍、2027年度27.6倍、2028年度23.7倍。市場要的是：五年EPS年增約13%（2031年約37美元）且本益比只從31.8倍降到27倍，換到約10%年化。EPS路徑我信——Q3淨營收+14%、2026年度共識近3個月上修1.9%；倍數再往上我不信——26週已漲29%，Q3有時點提前、Q4定價開始滿年。落後本益比33.4倍、市銷率15.3倍是4個年度端點中最低，代表相對自身近年不貴，但這不是5年連續分位。PEG約2.0（31.84÷15.9），在合理與偏貴的邊界。同業前瞻本益比事實表未涵蓋，終端倍數只能以自身2027年度27.6倍對照。短期（12個月）約+11%、中期（3年）約+36%：EPS走基本情境、本益比由31.8倍線性降到27倍。結論合理但空間窄，不追；580美元以下（2027年度約25倍）基本情境年化升到約12%才加碼。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2026年度共識EPS）＋PEG，輔以2027年度倍數","tier":"支付網路雙寡頭","peers":{"expanded":false,"reason":"事實表同業表只有利潤率、沒有同業前瞻本益比；終端倍數改以自身現值（2027年度共識EPS約27.6倍）與前份判斷記載的5年前瞻本益比區間24–40倍對照"},"fwd_pe":31.84,"peg":2.0,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比31.8倍（2026年度）／27.6倍（2027年度）；PEG約2.0；落後本益比在4個年度端點中最低（5年連續分位事實表未涵蓋，不以此代替）；基本情境5年年化約10%落在8–12%中段→合理（🟡），較前份539美元時空間明顯變窄","upside_short_pct":11,"upside_mid_pct":36,"denominator_disputed":false,"denominator_note":"2026年度分母含Q3服務專案提前認列（管理層稱Q4回吐，全年不變）；GAAP含2.02億美元重組費（每股0.18美元），不在調整後口徑；分母不構成爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在監管：美國若立法強制信用卡第二網路路由，定價權與本益比會同時下修；路徑風險中等（−30%～−45%），陷阱風險中","reasoning":"看錯的三條路見反證紀錄：監管把定價上限壓下來（與唯一致命點重疊）、A2A與穩定幣繞卡、發卡行分走增量。路徑風險中等：歷史最大回撤事實表未涵蓋，以情境推估−30%～−45%——一般衰退或監管驚嚇時EPS照共識、本益比回到約22倍本年EPS（約441美元，接近250週均線451美元）；深度情境EPS谷底約20.3美元×17倍約345美元。成長熄火壓力測試：2028年後成長降到15%／10%／5%、本益比對應28／22／17倍，五年終點約1147／789／530美元，三種中兩種高於現價。週線上股價高於52、104、250週均線，250週均線13週斜率+0.94%，屬中性。陷阱風險中：不是便宜股陷阱，亮的是美國份額與倍數下移兩項。RSI標記不可用，不作動能判斷。","fact_refs":["f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_pe_percentile","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"非價值陷阱，但兩項衰退信號亮燈（美國簽帳卡份額、倍數4年下移）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.04,"pe":31.84,"basis":"2026年度共識EPS（FY1）；判斷日已過該年10個月，終端同樣用2031年度EPS乘倍數，口徑一致"},"eps":{"bull":[23.5,27.6,32.0,36.8,42.0],"base":[23.0,26.5,30.0,33.6,37.3],"bear":[21.2,20.3,20.9,21.8,22.8]},"pe":{"bull":31,"base":27,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.55,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12.0,"base_cagr_pct":9.5},"max_dd":{"lo":-45,"hi":-30,"basis":"歷史最大回撤事實表未涵蓋。上緣−30%：一般衰退或監管驚嚇，EPS照共識、本益比回到約22倍本年EPS（約441美元，接近250週均線451美元）；下緣−45%：深度情境，衰退谷底EPS約20.3美元×17倍約345美元（約−46%）；兩者都比空頭情境終點（約−29%）深，反映途中超跌","trigger_time":null},"basis":{"bull":"加值服務維持17%以上、跨境回到13%以上，代理式商務與商務虛擬卡帶來增量，EPS年增約16%（2031年42美元），本益比維持31倍（約等於現值）","base":"量8–9%＋價格組合約4pp、營益率小升，EPS年增由約15%逐年降到11%（2031年37.3美元，五年約13.2%），本益比降到27倍（約等於現價對2027年度共識EPS的27.6倍）；每股EPS已含回購增厚，淨回購殖利率填0以免重複計算","bear":"美國強制信用卡路由或DOJ起訴，疊加2027年衰退壓跨境、回扣與誘因吃掉定價：EPS在2028年跌回約20美元、2031年22.8美元（不高於2027年共識23.13美元），本益比20倍（成長降到10%情境約22倍再折價，因EPS成長低於10%）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"信用卡競爭法案2026-01重提、參議員公開批評商家和解不足；DOJ對簽帳卡業務發調查令；10-K自述A2A成熟後國內P2M／P2P份額競爭可能增加","assumption":"評估費每季比量多成長5–6pp的定價能延續五年","consequence":"美國強制信用卡路由＋衰退＋A2A在歐洲擴張：EPS五年停在約23美元、本益比降到約20倍，股價約450美元（約−29%），深度情境−45%","ruling":"部分採納：列為空頭情境（30%）；不採為基本情境，因Q3量價仍強、法案過去多次未過。與唯一致命點部分重疊（法案是觸發點），本條補上衰退與A2A的共振","watch":"法案表決進度、DOJ動向、國內評估費減GDV差距（每季）","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#1","substitute_technology#0"],"fact_refs":["f_kpi7_purchase_volume_cross_bo","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"10-K稱穩定幣可能隨GENIUS Act普及並與產品競爭、新技術可能讓現有技術過時；代理式商務目前由處理商以一次性虛擬卡墊在中間，MA表態長期不支援","assumption":"代理式商務與穩定幣最後仍跑卡網路代幣","consequence":"若代理平台改走帳戶直付或穩定幣結算，新增線上流量繞過MA，淨營收成長由低雙位數降到個位數","ruling":"暫不採納：MA已併入BVNK、與OpenAI和Shopify簽約使用Agent Pay，管理層稱代理交易量仍小；但這是十年尺度的架構風險，併入繞卡替代監測","watch":"穩定幣商戶結算占可及流量（資料缺口）、Agent Pay採用方數、管理層是否揭露代理交易量","evidence_refs":["substitute_technology#1","substitute_technology#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"回扣與誘因+18%快於淨營收+14%，Q4占總評估費比率預期再升；前五大客戶占21%營收、多數關係非排他；以30倍以上本益比回購的盈餘殖利率約3%；BVNK收入基期小","assumption":"量價成長能轉成每股價值，而不是被發卡行分走或被高價回購稀釋","consequence":"營收年增12%但淨收費率下降、回購報酬低於資金成本，EPS年增掉到10%以下，股價只跟EPS走，五年年化約6–7%","ruling":"採納為監測：目前淨營收仍+14%、調整後營益率60.5%，尚未發生；以回扣與誘因比率和淨收益率當早期指標","watch":"回扣與誘因占總評估費比率年增超過2pp連2季→停止加碼","evidence_refs":["customer_concentration_credit#0","customer_second_source#0","competitive_share_entrants#1"],"fact_refs":["f_kpi1_adjusted_non_gaap_operat","f_fwd_pe_latest"]},{"view":"價格已反映太多","evidence":"26週漲29%、2026年度前瞻本益比31.8倍；Q3淨營收含服務專案與簽約從Q4提前、Q4定價開始滿年；賣方Q3前平均目標價約660美元只高3%，Raymond James曾下調到631美元","assumption":"市場會繼續給約32倍","consequence":"若一年後倍數回到27倍、EPS照2027年共識，股價約624美元，一年報酬約−2%","ruling":"採納：已持有者續抱不加碼，新資金不追，等580美元以下","watch":"股價對2027年共識EPS倍數、Q4淨營收成長（2027-01公布）","evidence_refs":["capital_markets_pricing#5"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 539.39 → 本次 638.01（+18.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=539.39","side_b":"本次 price_at_dd=638.01","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 539.39 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 539.39 美元：Bull 價 1,310、Bear 價 405，五年期望值 +75.0%，基準年化 13.0%，不對稱比 7.0","side_b":"本次情境、股價仍用 539.39 美元：Bull 價 1,302、Bear 價 456，五年期望值 +69.7%，基準年化 13.3%，不對稱比 7.62","ruling":"先換情境、股價不動：五年期望值少 5.3 個百分點，基準年化多 0.3 個百分點。不對稱比由 7.0 變為 7.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 539.39 美元：五年期望值 +69.7%，基準年化 13.3%，不對稱比 7.62","side_b":"本次情境、股價 638.01 美元：五年期望值 +43.5%，基準年化 9.6%，不對稱比 3.04","ruling":"再換股價、情境不動：起點價上漲 18.3%，五年期望值少 26.2 個百分點，基準年化少 3.7 個百分點，不對稱比由 7.62 降到 3.04。合計五年期望值比前份少 31.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：整體訊號","cause":"新證據","prior_field":["signal"],"side_a":"前份（2026-07-03，股價539.39美元）：整體訊號A；護城河趨勢↑、陷阱風險低（🟢）、估值合理（🟡）","side_b":"本次（股價638.01美元）：整體訊號B；護城河趨勢→、陷阱風險中（🟡）；估值仍判合理（🟡），但空間變窄","ruling":"整體訊號是基本面評級，這次降級來自新證據，不是價格。①護城河趨勢由↑改→：Q3美國簽帳卡因Capital One轉移只+1%，2025年美國購買量MA+6.3%略低於Visa+6.8%，Lloyds約1000萬張卡轉Visa。②陷阱由🟢改🟡：十類衰退信號亮2項，分別是美國份額縮減與倍數4年下移。③前份只把監管列為Visa連帶，本次納入2026年Q1 10-Q揭露的DOJ對MA簽帳卡業務調查令；另外回扣與誘因+18%，快於淨營收+14%。量價引擎沒壞：Q3淨營收+14%、調整後EPS+21%、全年指引維持，所以只降一級到B，不到C。股價上漲18%只影響估值空間：估值判讀前後都是合理（🟡），基本情境5年年化由約13%降到約10%，價格效果已在上方程式拆解的股價變動一條另列。這是新資金等580美元以下的理由，不是訊號降級的理由。裁決與角色變動由程式另列多欄共同歸因，不併入本條","evidence_level":"硬數據＋第三方統計＋公司申報","settle_metric":"美國購買量成長MA對Visa、美國簽帳卡GDV成長、回扣與誘因占總評估費比率、DOJ程序狀態","if_then":["若2027年上半年美國簽帳卡GDV回到+6%以上、美國購買量成長不低於Visa，且回扣與誘因比率未再升→護城河趨勢可回↑，整體訊號可回A","若再有前五大客戶轉出或DOJ正式起訴→護城河趨勢改↓，整體訊號檢討是否降為C並重跑DD"],"evidence_refs":["customer_second_source#2","competitive_share_entrants#2","customer_second_source#0","regulatory_antitrust#1"]},{"axis":"前份漂移：護城河與陷阱","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河趨勢↑、陷阱風險低（🟢）、五年後跑道寬（🟢）","side_b":"本次：護城河趨勢→、陷阱風險中（🟡）、五年後跑道仍寬（🟢）","ruling":"趨勢由↑改→：Q3美國簽帳卡因Capital One轉移只+1%、2025年美國購買量MA+6.3%略低於Visa+6.8%、Lloyds約1000萬張卡轉Visa，大客戶份額有下滑證據就不能標↑；定價面仍強所以不到↓。陷阱改🟡：十類衰退信號亮2項（美國份額、倍數4年下移）。跑道維持：加值服務+19%、占淨營收約41%，是有財報證據的第二曲線","evidence_level":"硬數據＋第三方統計","settle_metric":"美國購買量成長MA對Visa、美國簽帳卡GDV成長（2026年Q4起Capital One轉移滿年）","if_then":["若2027年上半年美國簽帳卡GDV回到+6%以上且美國購買量成長不低於Visa→趨勢可回↑","若再有前五大客戶轉出→趨勢改↓並重跑DD"],"evidence_refs":["customer_second_source#2","competitive_share_entrants#2","customer_second_source#0"]},{"axis":"前份漂移：情境機率與分類","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：未標公司類型與循環位置；多頭30%、空頭25%；最大回撤−45%單點","side_b":"本次：品質複利成長、非循環股不標位置；多頭25%、基本45%、空頭30%；最大回撤改為−30%至−45%區間","ruling":"空頭機率上調來自本次加做的再投資報酬檢核：前瞻兩年共識EPS年增約15.9%高於有機上限約12.5%（差額為回購與營益率，可歸因），按框架空頭不得低於30%；另有新證據（法案重提、DOJ調查令）支持不下修。回撤改區間是寫法改變，下緣沿用−45%","evidence_level":"推論","settle_metric":"有機淨營收成長對12.5%","if_then":["若2027年財測有機淨營收成長≥13%且法案未過任一院→空頭機率下修到25%","若有機淨營收成長連2季低於10%→空頭機率上調到35%並下修基本情境"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟條件：null（前份為進場，未設）","side_b":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）才恢復加碼","ruling":"本次結論改為不追，唯一約束是價格，重啟條件就是價格約束的否定；不用事件錨，因生意本身沒有待決證據","evidence_level":"推論","settle_metric":"股價","if_then":["若股價≤580美元且Q4淨營收成長≥11%→分三批加碼","若股價≤580美元但跌因是法案或DOJ起訴→不加碼，依唯一致命點處理"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉／減碼門檻（null）","side_b":"減碼：跨境本幣成長連2季低於8%、DOJ對MA正式起訴、股價≥765美元且共識未上修；清倉：國內評估費成長連4季低於GDV成長且淨營收成長低於8%，或美國強制路由立法涵蓋全部發卡行且無過渡期","ruling":"前份只寫假設門檻、沒寫動作；本次補上具體動作，跨境8%沿用前份削弱門檻，未放寬","evidence_level":"推論","settle_metric":"季報評估費與量","if_then":["若觸發任一減碼條件→減碼三分之一並重跑DD","若觸發清倉條件→清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"新證據","prior_field":["single_thing"],"side_a":"前份唯一致命點：未設（null）","side_b":"Single Thing：美國立法強制大型發卡行的信用卡支援第二家非關聯網路路由（信用卡競爭法案）","ruling":"法案在2026-01重新提出，參議員公開批評商家和解不足；它同時壓美國網路費與本益比，是情境樹中單一敏感度最大的二元事件（失去一家前五大客戶平均約影響4%營收，英國與EMV訴訟是10億級一次性金額，都小於它）","evidence_level":"立法紀錄與新聞","settle_metric":"法案表決進度","if_then":["若法案通過任一院→減碼至原倉位三分之二","若簽署成法→減碼至半倉並重跑DD；涵蓋全部發卡行且無過渡期→清倉"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"監管風險門檻","cause":"新證據","prior_field":["thesis.R2"],"side_a":"前份：V遭強制拆分或重大和解→MA連帶下修向18倍；FTC對MA啟動調查→立即重評","side_b":"本次：DOJ對MA美國簽帳卡業務由調查令轉為正式起訴→減碼三分之一並重跑DD；信用卡競爭法案通過任一院→減碼至原倉位三分之二","ruling":"2026年Q1 10-Q揭露DOJ反壟斷司已對MA簽帳卡業務發出調查令，風險從Visa連帶變成MA直接當事人，門檻改盯MA自己的案子；FTC條件沒有新證據，併入此條","evidence_level":"公司申報","settle_metric":"10-Q法律程序揭露","if_then":["若DOJ正式起訴→減碼三分之一","若調查結案未起訴→回到前份監測強度"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"假設三撤換","cause":"價格變動","prior_field":["thesis.H3"],"side_a":"前份H3：估值從5年低位修復（前瞻本益比23.7倍，2年內回到5年中段40分位以上）","side_b":"本次撤下，改為營益率與EPS成長假設：股價已漲18%、2026年度前瞻本益比31.8倍，重估大致發生，不能再當報酬來源","ruling":"前份的重估論點已兌現；本次報酬只算EPS複利，終端倍數下修到27倍，所以不是估值依賴型","evidence_level":"硬數據","settle_metric":"股價對2027年共識EPS倍數","if_then":["若倍數回到25倍以下而EPS照共識→重估論點重新成立，分批加碼","若倍數升破33倍→減碼四分之一"],"evidence_refs":[]},{"axis":"Q2指引與Q3實績","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO Sachin Mehra：Q3淨營收成長落在低雙位數高端；Q3回扣與誘因比率略高於Q2；全年落在區間較高處","side_b":"2026-10-29 新任CFO Ling Hai：Q3淨營收+14%高於預期，部分是服務專案與簽約時點從Q4挪到Q3，Q4會回吐；回扣與誘因大致持平、Q4比率預期升高；全年維持低雙位數高端","ruling":"兌現且略優，沒有改口；CFO更替是內部輪調（Mehra轉任商務長），口徑一致。但Q3超額有一部分是時點，Q4淨營收成長落在9–11%不算轉弱，低於9%才算","evidence_level":"管理層原話","settle_metric":"Q4淨營收成長（匯率中性、不含收購），2027-01公布","if_then":["若Q4淨營收成長低於9%→停止加碼並下修基本情境2027年EPS","若Q4≥12%且2027年指引不低於低雙位數高端→維持基本情境"],"evidence_refs":[]},{"axis":"跨境放緩的一次性歸因","cause":null,"prior_field":null,"side_a":"管理層（2026-10-29 Ling Hai）：歐洲內部跨境放緩來自歐盟新海關費、大型促銷時點、去年加密貨幣購買高基期，非結構性；高收益的其他跨境穩定","side_b":"數據：跨境非旅遊線上交易成長由Q2的20%降到15%、歐洲內部跨境由去年同期16%降到10%；Q2跨境強勢含委內瑞拉美元一次性；中東衝突仍壓抑旅遊","ruling":"不採信也不否定，標未證、監測。預先登記：加密高基期過後的2027年Q1，若歐洲內部跨境仍≤10%且整體跨境低於10%，視為歸因證偽，跨境成長假設下修1pp","evidence_level":"管理層原話＋季報數據","settle_metric":"跨境量成長（本幣）、跨境評估費成長","if_then":["若2027年Q1整體跨境低於10%→跨境假設下修1pp、停止加碼","若跨境連2季低於8%→減碼至原倉位三分之二"],"evidence_refs":["geo_supply_chain#0","reg_tariff_export#1"]},{"axis":"定價權與社會容忍度","cause":null,"prior_field":null,"side_a":"Q3國內評估費+13%對GDV+7%、跨境評估費+16%對量+11%：定價與組合每季多貢獻5–6pp；管理層稱依價值定價、Q4起部分定價開始滿年","side_b":"商家和解平均交換費降0.1pp五年、標準消費信用卡費率上限1.25%八年；信用卡競爭法案2026-01重提；DOJ對簽帳卡發調查令；英國集體訴訟逾10億英鎊、美國EMV訴訟主張逾10億美元，反壟斷敗訴可能三倍賠償","ruling":"可調和（程度差異）：和解上限落在發卡行的交換費，不直接碰MA網路費；MA的定價多來自國際、代幣與加值服務。但兩邊疊加會壓縮未來提價空間，所以定價只給8分、社會容忍度給紅燈，空頭機率維持30%","evidence_level":"季報數據＋公司申報","settle_metric":"國內評估費成長減GDV成長","if_then":["若差距連2季低於3pp→停止加碼","若信用卡競爭法案通過任一院→減碼至原倉位三分之二"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","end_markets#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣：26週漲29%、2026年度前瞻本益比31.8倍；Q3有時點提前、Q4定價開始滿年、回扣與誘因比率升高；法案與DOJ在路上；賣方Q3前平均目標價約660美元只高3%，Raymond James曾下調到631美元","side_b":"續抱：Q3淨營收+14%、EPS+21%、全年指引維持；2026年度共識近3個月上修1.9%；落後本益比33.4倍仍是4個年度端點中最低；基本情境5年年化約10%","ruling":"續抱、不加碼、不賣：賣的理由都是價格與時點，不是生意變差；但價格理由足以停止加碼，新資金等580美元以下","evidence_level":"硬數據","settle_metric":"股價對2027年共識EPS倍數、Q4淨營收成長","if_then":["若股價≥765美元且2027年共識EPS未上修→減碼四分之一","若股價≤580美元且Q4淨營收成長≥11%→分三批加碼"],"evidence_refs":["capital_markets_pricing#5","capital_markets_pricing#0"]},{"axis":"回扣與誘因對不為量而量","cause":null,"prior_field":null,"side_a":"2026-07-30 Sachin Mehra：不為量而量，只追能提高淨收益率的量，舉放棄Lloyds信用卡為例","side_b":"Q3回扣與誘因+18%快於淨營收+14%，Q4占總評估費比率預期再升；新任CFO（2026-10-29）不給回扣指引，改稱淨收益率才是最終指標；外部報導Lloyds約1000萬張卡是轉到Visa","ruling":"目前說法與數字一致：淨營收仍+14%、國內評估費仍快於量。但Lloyds案外部報導寫的是Lloyds與Visa擴大合作，不完全是MA主動放棄，續約成本在升高","evidence_level":"管理層原話＋第三方報導","settle_metric":"回扣與誘因占總評估費比率、淨收益率","if_then":["若比率年增超過2pp連2季→停止加碼","若任一前五大客戶轉出→趨勢改↓並重跑DD"],"evidence_refs":["customer_second_source#2","customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"國內評估費成長減本幣GDV成長連2季低於3個百分點，代表定價權轉弱","type":"假設驗證","maps_to":"H1","metric":"國內評估費成長−本幣GDV成長","threshold":"連2季低於3pp","action":"停止加碼","source_freq":"季報（每季）","date":null,"evidence_refs":[]},{"n":2,"text":"加值服務成長連4季低於15%","type":"假設驗證","maps_to":"H2","metric":"加值服務淨營收成長（匯率中性）","threshold":"連4季低於15%","action":"停止加碼，基本情境EPS下修","source_freq":"季報（每季）","date":null,"evidence_refs":[]},{"n":3,"text":"跨境量本幣成長連2季低於8%","type":"減碼","maps_to":"R1","metric":"跨境量成長（本幣）","threshold":"連2季低於8%","action":"減碼至原倉位三分之二","source_freq":"季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","reg_tariff_export#0"]},{"n":4,"text":"DOJ對MA美國簽帳卡業務由調查轉為正式起訴","type":"減碼","maps_to":"R2","metric":"DOJ程序狀態","threshold":"提起正式訴訟","action":"減碼三分之一並重跑DD","source_freq":"8-K、10-Q（事件）","date":null,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#0"]},{"n":5,"text":"信用卡競爭法案（強制信用卡第二網路路由）簽署成法","type":"Single Thing","maps_to":"R2","metric":"法案立法進度","threshold":"簽署成法","action":"減碼至半倉並重跑DD；涵蓋全部發卡行且無過渡期則清倉","source_freq":"國會紀錄（每月）","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":6,"text":"回扣與誘因占總評估費比率年增超過2個百分點且連2季，或任一前五大客戶宣布主要卡組合轉網路","type":"風險","maps_to":"R4","metric":"回扣與誘因占總評估費比率；前五大客戶轉換公告","threshold":"年增超過2pp連2季；或一家轉出","action":"停止加碼；連4季則減碼三分之一","source_freq":"季報、新聞稿","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#2"]},{"n":7,"text":"國內評估費成長連4季低於GDV成長，且淨營收成長低於8%：淨收費率結構性下滑","type":"清倉","maps_to":"R3","metric":"國內評估費成長−GDV成長；淨營收成長（匯率中性）","threshold":"連4季低於0且淨營收低於8%","action":"清倉","source_freq":"季報（每季）","date":null,"evidence_refs":["substitute_technology#0","channel_business_model_shift#1"]},{"n":8,"text":"股價回到580美元以下","type":"估值rearm","maps_to":null,"metric":"股價","threshold":"≤580美元（2027年共識EPS約25倍）","action":"分三批加碼","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":9,"text":"股價升破765美元而2027年共識EPS未上修","type":"減碼","maps_to":null,"metric":"股價對2027年共識EPS倍數","threshold":"≥765美元（約33倍）","action":"減碼四分之一","source_freq":"每日收盤＋共識快照","date":null,"evidence_refs":[]},{"n":10,"text":"Q4財報與2027年度財測","type":"複審日期","maps_to":"H3","metric":"2027年淨營收成長指引、Q4淨營收成長","threshold":"指引低於低雙位數或Q4低於9%→基本情境下修","action":"依財測更新情境樹後重跑DD","source_freq":"法說（每季）","date":"2027-01","evidence_refs":[]},{"n":11,"text":"MA核心網路公開揭露的大範圍服務中斷","type":"風險","maps_to":"H1","metric":"網路中斷時數與影響範圍","threshold":"單次≥4小時且影響多家發卡或收單方","action":"停止加碼至原因揭露","source_freq":"公司公告、發卡與收單方狀態頁（事件）","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":12,"text":"加密高基期過後歐洲內部跨境仍≤10%且整體跨境低於10%","type":"假設驗證","maps_to":"R1","metric":"跨境量成長（本幣）","threshold":"2027年Q1整體低於10%","action":"跨境成長假設下修1pp、停止加碼","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["geo_supply_chain#0"]}],"kill_metrics":[{"metric":"淨營收成長（匯率中性、不含收購）","bear_threshold":"連2季低於9%","window":"2季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"國內評估費成長減本幣GDV成長","bear_threshold":"連2季低於3個百分點；連4季低於0且淨營收低於8%即清倉","window":"2至4季","source":"季度財報新聞稿與法說簡報","last_status":"ok"},{"metric":"跨境量成長（本幣）","bear_threshold":"連2季低於8%（沿用前份）","window":"2季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"加值服務淨營收成長（匯率中性）","bear_threshold":"連4季低於15%（沿用前份）","window":"4季","source":"季度財報新聞稿","last_status":"ok"},{"metric":"回扣與誘因占總評估費比率","bear_threshold":"年增超過2個百分點且連2季","window":"2季","source":"10-Q與法說","last_status":"warning"},{"metric":"A2A與穩定幣占MA可及流量","bear_threshold":"≥5%（沿用前份）","window":"年度","source":"資料缺口：事實表未涵蓋","last_status":"unknown"},{"metric":"Capital One信用卡轉至Discover網路比例","bear_threshold":"超過20%（沿用前份）","window":"年度","source":"資料缺口：事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）","exec_line":"已持有者續抱、不加碼；新資金等580美元以下分三批；破765美元且共識未上修減碼四分之一；美國強制路由立法減至半倉","holding_cap":"單一個股上限6%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=29.18, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到580美元以下（2027年共識EPS約25倍、基本情境5年年化約12%）'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"雙寡頭卡網路的量價引擎延續：交易量穩定成長，評估費成長持續高於量","2y":"本幣GDV≥+7%、交易筆數≥+9%、國內評估費成長減GDV成長≥3pp","5y":"淨營收（匯率中性）年複合≥11%，淨收費率不下滑","10y":"A2A與穩定幣占MA可及流量低於5%","threshold":"Q3 2026：GDV+7%、交易筆數+9%、國內評估費+13%（差6pp）","source":"季度財報新聞稿與法說簡報（3Q26，2026-10-29）","drift_rule":"5年假設：淨營收TTM成長連4季比11%低5%以上（低於10.45%）削弱，連6季低10%以上（低於9.9%）反轉"},{"id":"H2","text":"加值服務成為第二引擎：安全、數據、代幣化與代理式商務帶動加值服務成長高於整體","2y":"加值服務淨營收（匯率中性）≥+15%","5y":"加值服務占淨營收≥45%（Q3約41%）","10y":null,"threshold":"Q3 2026：加值服務40.6億美元、+19%；前九個月113.34億美元、+20%","source":"3Q26財報新聞稿、10-Q；Q2法說（約60%與網路量連動）","drift_rule":"5年假設：加值服務TTM成長連4季低於14.25%削弱，連6季低於13.5%反轉（沿用前份15%基準）"},{"id":"H3","text":"營運槓桿加回購：調整後營益率守住58%以上，EPS年增≥13%","2y":"2027年調整後EPS≥22.7美元（共識23.13美元的98%）、調整後營益率≥58%","5y":null,"10y":null,"threshold":"Q3 2026：調整後營益率60.5%、調整後EPS 5.31美元（+21%，回購貢獻0.16美元）","source":"季度財報新聞稿、2027年度財測（2027-01法說）","drift_rule":"2年假設：EPS年增連2季比13%低5%以上（低於12.35%）削弱，連3季低10%以上（低於11.7%）反轉"}],"R":[{"id":"R1","text":"跨境放緩：歐洲內部跨境降溫、中東衝突壓抑旅遊、委內瑞拉一次性因素退去，關稅與制裁等貿易政策壓抑消費與企業支出","h_ref":"H1","clock":"⚡","threshold":"跨境量成長（本幣）連2季低於8%→減碼至原倉位三分之二（沿用前份門檻）","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R2","text":"監管與訴訟：DOJ對美國簽帳卡業務發調查令、信用卡競爭法案2026-01重提、商家和解平均交換費降0.1pp五年且標準信用卡費率上限1.25%八年；英國集體訴訟逾10億英鎊、美國EMV集體訴訟主張逾10億美元，反壟斷敗訴可能三倍賠償","h_ref":"H1","clock":"🔥","threshold":"DOJ轉正式起訴→減碼三分之一；法案通過任一院→減碼至原倉位三分之二；單一訴訟判決或和解超過20億美元→重跑DD","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#1"]},{"id":"R3","text":"繞卡替代：A2A即時支付、金融科技內部轉帳、穩定幣與加密原生業者，以及代理式商務若改走帳戶直付","h_ref":"H1","clock":"🐢","threshold":"A2A與穩定幣占MA可及流量≥5%、Capital One信用卡轉Discover網路超過20%、或國內評估費成長連4季低於GDV成長（沿用前份三門檻，前兩項資料缺口）；機率≥50%才砍倉","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","customer_second_source#1","channel_business_model_shift#1","competitive_share_entrants#0"]},{"id":"R4","text":"發卡行議價與客戶流失：前五大客戶占2025年淨營收21%、多數關係非排他、部分客戶與對手近乎排他；Lloyds約1000萬張卡轉Visa、Capital One簽帳卡移出；回扣與誘因+18%快於淨營收","h_ref":"H3","clock":"🔥","threshold":"回扣與誘因占總評估費比率年增超過2pp連2季，或任一前五大客戶宣布主要卡組合轉網路→停止加碼；連4季→減碼三分之一","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#0","customer_second_source#2","competitive_share_entrants#1"]}],"single_thing":{"description":"美國立法強制大型發卡行的信用卡支援第二家非關聯網路路由（信用卡競爭法案，2026-01重新提出）","why_fatal":"美國是最大市場，美國信用卡GDV Q3+10%是增量主力；強制路由把選網路的權力交給收單與商店端，直接壓網路評估費，同時坐實社會容忍度上限，本益比會一起下修——EPS與倍數雙殺。失去一家前五大客戶平均約影響4%營收、英國與EMV訴訟是10億級一次性金額，都小於它","if_happens":"通過任一院減碼至原倉位三分之二；簽署成法減碼至半倉、空頭機率上調到40%以上並重跑DD；涵蓋全部發卡行且無過渡期則清倉","how_monitor":"國會表決與行政部門表態（每月）；季報美國信用卡GDV成長與國內評估費減GDV差距","probability":"約15%（12–24個月）：過去多次重提未過，但2026-01再提且參議員公開批評商家和解不足"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"高","fpe_fy2":27.58,"peg_fy2":1.73,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":16.52,"FY2026E":20.04,"FY2027E":23.13,"FY2028E":26.94},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（年度財報，調整後口徑事實表未涵蓋）；FY2026E至FY2028E為Koyfin共識（快照未標口徑，推定為調整後）；兩者口徑可能不同，三年年複合約17.7%可能偏高，以前瞻兩年共識年增約15.9%為準"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年度財測","impact":"高","watch":"淨營收成長指引是否維持低雙位數高端、回扣與誘因比率、Q4時點回吐幅度"},{"date":"2026-12","date_precision":"month","type":"product","event":"年末購物季代理式商務交易（Agent Pay、Shop Pay、OpenAI合作）","impact":"低","watch":"管理層是否揭露代理交易量與採用方數"},{"date":"2027-04","date_precision":"month","type":"other","event":"Q1 2027財報：加密高基期過後的歐洲內部跨境","impact":"中","watch":"整體跨境是否回到10%以上，驗證管理層一次性歸因"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
