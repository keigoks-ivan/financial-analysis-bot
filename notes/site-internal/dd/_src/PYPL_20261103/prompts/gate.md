你是 DD 管線 v20 的判斷層閘（gate），標的 PYPL（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_revenues_gaap`（q1_business）｜Net revenues (GAAP)＝8584 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：第三方媒體報 consensus 約 $8.71B、未達（僅單一媒體、未經一手來源驗證）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝18.8 %（營業利益 $1,613M）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未查得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝16.3 %（營業利益 $1,402M）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未查得
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝1431 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未查得
- `f_kpi6_active_accounts_12_mau`（q1_business）｜Active accounts（12 個月基礎，非 MAU）＝440 M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未查得
- `f_kpi7_total_payment_volume_tpv`（q1_business）｜Total payment volume（TPV）＝487.1 USD B｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release 摘要（YoY +6%）（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未查得
- `f_peer_pypl_gross_margin_pct`（q2_moat）｜PYPL 毛利率＝45.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pypl_operating_margin_pct`（q2_moat）｜PYPL 營業利益率＝18.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 5 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
- `f_peer_pypl_fcf_margin_pct`（q2_moat）｜PYPL FCF 利潤率＝18.37 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PYPL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_xyz_gross_margin_pct`（q2_moat）｜XYZ 毛利率＝46.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XYZ.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_xyz_operating_margin_pct`（q2_moat）｜XYZ 營業利益率＝12.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XYZ.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_v_operating_margin_pct`（q2_moat）｜V 營業利益率＝65.57 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.V.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_afrm_operating_margin_pct`（q2_moat）｜AFRM 營業利益率＝20.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AFRM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_afrm_fcf_margin_pct`（q2_moat）｜AFRM FCF 利潤率＝23.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AFRM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.55 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.88 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝6.4 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝34540.98 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（35 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝35976.46 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝14.4 %（SBC $233M ÷ non-GAAP 營業利益 $1,613M；占營收 2.7%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：PayPal Q3 2026 earnings release（8-K 附件），占比為本 agent 換算（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3971.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 14251.0、現金 10280.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.956 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝830.66 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝52626.81 USD m｜期間與口徑：2026-11-03／市值 48655.81 ＋ 淨負債 3971.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝10.55 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.55，分子＝快照價 58.57｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝58.58 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝11.18 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝2.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝2.1 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.42 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.53 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.52 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.16 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 5.38 → 5.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_guidance_q4_fy2026`（q1_business）｜Guidance（Q4 與 FY2026，皆為點估非區間）＝Q4 non-GAAP EPS 約 $1.43、GAAP EPS 約 $1.37；FY non-GAAP EPS 約 $5.60、GAAP EPS 約 $5.07 USD/share｜期間與口徑：Q3 FY2026（公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：PayPal Q3 2026 earnings release（8-K 附件）；FY non-GAAP TM$ 同步上調（第三方報約 $15.6–15.7B，未經一手驗證）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-27））
  - 註記：dd_numbers_extra.py consensus_revision：FY1 EPS 5.55（2026-10-31 快照），指引 $5.60 略高於共識
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 58.7 / W52 51.71 / W104 62.4 / W250 69.07 / W250 13週斜率 -2.71%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝51.71 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝62.4 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝69.07 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-2.71 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_rsi14`（q5_valuation）｜RSI(14)＝63.94｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝16.86 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（23 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出的競爭者包含銀行、支付網路、數位錢包、BNPL、即時支付、加密貨幣與穩定幣等，並稱新競爭者可能出現、競爭可能加劇。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-03）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：PayPal 線上結帳帝國遭對手擠壓；Q1 品牌結帳僅成長2%
  - 來源：AP via NY1（as_of 2026-05-26）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Seeking Alpha：品牌結帳流失份額，Apple Pay、Google Pay、Shop Pay 搶份額
  - 來源：Seeking Alpha（as_of 2026-03-01）｜affects：moat_trend、thesis.R
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Q3 2026：線上品牌結帳 TPV 成長連四季維持 1%–2%，管理層預期 Q4 同為 1%–2%；歐盟取消小額免稅造成約 70bp 逆風；2026 非 GAAP EPS 指引上調至約 $5.60
  - 來源：MarketBeat, Transcript: PayPal Q3 earnings call highlights（as_of 2026-10-27）｜affects：moat_trend、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Morgan Stanley 重申 Sell，理由為 take rate 持續承壓與品牌結帳再加速速度；2027 將加碼投資（約三分之二投向品牌結帳與 BNPL）
  - 來源：Zacks, PayPal Q3 earnings call highlights growth and 2027 investments（as_of 2026-10-28）｜affects：decision_inputs.bear、valuation
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K FY2025 風險因素載明 PayPal 受美國及國際反壟斷／競爭法主管機關審視，可能面臨訴訟、罰款與被迫改變業務做法。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：英國 FCA 對 PayPal、Visa、Mastercard 展開競爭法調查，涉及 PayPal 數位錢包的資金來源與使用相關合約條款。
  - 來源：PYMNTS：PayPal, Visa and Mastercard Face UK Competition Investigation（as_of 2026-05-06）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：PayPal 10-Q（2026Q3）揭露 FTC CID、CFPB CID（PayPal Credit）、德國 Bundeskartellamt 程序與英國調查。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-11-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：跨境交易是重要營收與獲利來源，且可能受新增或變動關稅、貿易爭端、制裁、進出口管制影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K MD&A：關稅等因素造成的總體環境惡化可能影響消費與信用損失，公司無法合理估計對財務的總影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-03）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Truist 調降 PayPal 目標價，理由為跨境交易量疲弱。
  - 來源：247wallst: Truist Cuts PayPal Price Target as Cross-Border Volume Weakness Bites（as_of 2026-05-12）｜affects：decision_inputs.bear、valuation
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 品牌結帳 TPV 幣別中性成長約 1%，連續第四季維持 1–2%；歐盟取消 de minimis 免稅約拖累 70bp
  - 來源：MarketBeat/PayPal Q3 2026 earnings call highlights（as_of 2026-10-27）｜affects：moat_trend、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Apple Pay 等對手侵蝕 PayPal 品牌結帳；Q1 品牌結帳僅成長 2%
  - 來源：AP: PayPal's online checkout empire is under siege as rivals squeeze its core business（as_of 2026-05-26）｜affects：moat_trend、decision_inputs.bear
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：品牌結帳 TPV 連四季 1–2% 成長
  - 來源：PayPal 3Q26 IR Newsletter（as_of 2026-10-27）｜affects：moat_trend
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：PayPal 10-K 自述：生成式 AI 與自主 AI agent 等新技術可能優於或使其現有技術過時；第三方可能以降低客戶對其產品需求的方式部署 AI。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：PayPal 10-K 列出瀏覽器儲存卡資訊、即時支付、代幣化、虛擬貨幣/區塊鏈、NFC 等顛覆性支付技術變動。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：moat_trend、thesis.R
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：Q3 2026 財報簡報：品牌結帳 TPV 按固定匯率成長 1%，已部署 playbook 的商家趨勢改善。
  - 來源：PYPL 3Q 26 Earnings Presentation（as_of 2026-10-28）｜affects：moat_trend、thesis.R
- `channel_business_model_shift#3`（channel_business_model_shift｜方向 -｜狀態 ok）：無品牌結帳（Braintree、PayPal Complete Payments）為策略重點，但獲利低於品牌按鈕。
  - 來源：Digital Transactions（as_of 2023-05-09）｜affects：moat_trend、valuation
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 後分析師預測仍受弱品牌結帳成長與 2027 投資計畫限制
  - 來源：Beinsure search snippet（as_of 2026-10-28）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年初共識 EPS 於財測偏弱後下修（Zacks 2026 共識 $5.38，近一週下修）；Zacks Rank #4/#5
  - 來源：Zacks/Nasdaq - PYPL Falls 9.6% Despite Earnings Growth（as_of 2026-02-28）｜affects：valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：In re PayPal Branded Checkout Securities Litigation：Darcy 案（2026-02-24 提起）與 Norfolk 案（2026-04-02）於 2026-05-21 合併，指稱誤導投資人關於品牌結帳改善；衍生訴訟 2026-07 合併並暫停。
  - 來源：PayPal 10-Q FY2026（經搜尋摘要）／Labaton 新聞稿（as_of 2026-05-21）｜affects：thesis.R、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：10-10Q 揭露 2026年3月收到英國 FCA 依 Competition Act 1998 的調查通知與資訊要求，公司配合中。
  - 來源：PayPal 10-Q（搜尋摘要轉述）（as_of 2026-03-31）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：In re PayPal Branded Checkout Securities Litigation 於 2026-05-21 合併，class period 最長 2024-02-08 至 2026-02-02，指稱 Section 10(b)/20(a) 違法。
  - 來源：Labaton 新聞稿／PayPal 10-Q（as_of 2026-05-21）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":135.8,"bear_5y_price":43.2,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":54.0,"ev5y_pct":41.5,"irr_base_pct":9.0,"asym_ratio":2.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.55,"pe":10.55,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-31，與公司非 GAAP 指引 5.60 同口徑）；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[6.0,6.7,7.6,8.6,9.7],"base":[5.9,6.4,7.0,7.6,8.2],"bear":[5.6,5.5,5.4,5.4,5.4]},"pe":{"bull":14,"base":11,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.956,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PYPL_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：CEO表示上調全年交易毛利金額與非GAAP EPS財測（原話："raising our full year guidance for transaction margin"）
- 2026-07-28｜CFO｜guidance：CFO給出全年TM美元約156億（扣除客戶餘額利息為145億）（原話："approximately $15.6 billion or $14.5 billion"）
- 2026-07-28｜CFO｜guidance：CFO給出非交易營運費用成長7%-8%與EPS 5.38美元（原話："approximately 7% to 8% growth in non-transaction operating"）
- 2026-07-28｜CFO｜guidance：CFO給出第三季非交易費用高個位數成長、EPS低個位數衰退（原話："non-GAAP earnings per share to decline"）
- 2026-07-28｜CFO｜guidance：CFO表示第四季TM美元成長略為正（原話："transaction margin dollar growth to be slightly positive."）
- 2026-07-28｜CFO｜guidance：CFO上調全年品牌結帳TPV預期至低個位數（原話："For online branded checkout, we now expect low single-"）
- 2026-07-28｜CFO｜guidance：CFO預期第三季品牌結帳成長約2%（原話："branded checkout growth at about 2%"）
- 2026-07-28｜CFO｜guidance：CFO表示成長投資對全年TM美元的拖累小於原先3個百分點（原話："a modestly lower headwind to transaction margin dollars"）
- 2026-07-28｜CFO｜guidance：CFO表示FCF與買回財測維持（原話："at least $6 billion of adjusted free cash flow"）
- 2026-07-28｜CFO｜guidance：CFO表示不預期年內再有利率變動（原話："we're not expecting or not planning, I should say, any more"）
- 2026-07-28｜CFO｜margin：CFO說明交易take rate下滑7bp至1.61%（原話："Transaction take rate declined by 7 basis points to 1.61%."）
- 2026-07-28｜CFO｜margin：CFO說明交易費用占TPV 90bp，因Braintree占比上升而略增（原話："expense as a percentage of TPV was 90 basis points"）
- 2026-07-28｜CFO｜margin：CFO說明TM美元表現受外匯有利與損失降低貢獻（原話："FX favorability and lower losses across PayPal and Venmo"）
- 2026-07-28｜CFO｜margin：CFO說明部分費用增加屬時間差，先投資再享節省（原話："It's important to note that part of the increase is timing."）
- 2026-07-28｜CFO｜margin：CFO說明非GAAP營業利益年減8%（原話："income was down 8% in the quarter to $1.5 billion."）
- 2026-07-28｜CFO｜commitment：CFO表示至少15億美元成本節省目標維持（原話："achieve at least $1.5 billion in gross run rate cost"）
- 2026-07-28｜CFO｜commitment：CFO表示年底前已識別約4億美元新增節省（原話："identified actions to unlock approximately $400"）
- 2026-07-28｜CFO｜guidance：CFO預告下半年轉型相關費用約1.2億至1.4億美元（原話："approximately $120 million to $140 million during the second"）
- 2026-07-28｜CFO｜commitment：CFO表示成本節省第四季起更顯著（原話："cost savings initiatives to become more meaningful"）
- 2026-07-28｜CFO｜commitment：CFO表示將把大部分節省再投資於策略領域（原話："we do expect to reinvest much of those"）
- 2026-07-28｜CEO｜commitment：CEO表示多數投資由節省自行支應（原話："will be self-funded with the savings that Jamie described."）
- 2026-07-28｜CFO｜commitment：CFO表示若未達ROI門檻將重新配置資金（原話："even more focused with Enrique on redeployment of those"）
- 2026-07-28｜CEO｜commitment：CEO表示成長動能預計2027下半年起累積（原話："momentum expected to build in the second half of 2027"）
- 2026-07-28｜CEO｜product：CEO表示2028年後代理支付與數位身分預期更具貢獻（原話："agentic payments and digital identity"）
- 2026-07-28｜CFO｜capital_allocation：CFO表示本季買回15億美元（原話："we completed $1.5 billion in share repurchases,"）
- 2026-07-28｜CFO｜capital_allocation：CFO說明過去12個月買回60億美元與期末現金（原話："trailing 12-month total to $6 billion."）
- 2026-07-28｜CEO｜capital_allocation：CEO談M&A傳聞：不評論，但保持開放（原話："remain open and objective in evaluating opportunities."）
- 2026-07-28｜CEO｜capital_allocation：CEO在Q&A表示目前聚焦執行自身策略（原話："our focus is on executing our own strategic"）
- 2026-07-28｜CFO｜competition：CFO提到歐洲成長正常化且競爭強度上升（原話："certainly, there's more competitive intensity as"）
- 2026-07-28｜CFO｜risk：CFO提到旅遊類別季初出現壓力（原話："We saw some pressure in the travel vertical that was"）
- 2026-07-28｜CEO｜product：CEO說明Venmo多產品使用者ARPA高於純P2P用戶（原話："more than 9x higher ARPA than peer-to-peer only users"）
- 2026-07-28｜CFO｜product：CFO說明Venmo TPV連續七季雙位數成長（原話："seventh consecutive quarter of double-digit growth."）
- 2026-07-28｜CFO｜product：CFO說明Pay with Venmo與BNPL優於市場（原話："continue to outpace the market"）
- 2026-07-28｜CFO｜product：CFO表示金融服務營收今年成長至少為整體兩倍（原話："at least twice as fast as the total company"）
- 2026-07-28｜CEO｜product：CEO表示金融服務占TM近20%（原話："part of the transaction margin of the company, close to 20%"）
- 2026-07-28｜CEO｜customer：CEO提到與Amazon在德國與奧地利的消費信貸合作（原話："consumer lending partnership with Amazon for"）
- 2026-07-28｜CEO｜customer：CEO舉社群電商平台整合計畫後量與TM成長50%（原話："we saw 50% growth in volume and transaction margin"）
- 2026-07-28｜CEO｜customer：CEO舉時尚零售商簽獨家BNPL後TPV由下滑轉為成長（原話："signed an exclusive BNPL agreement during the last month"）
- 2026-07-28｜CFO｜customer：CFO表示策略將帶來雙位數獲利成長輪廓（原話："attractive double-digit earnings growth profile"）

### 問答異常語氣（迴避／改口／保留）
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Wells Fargo：再投資有多少在交易利潤線之上、多久才見效於TM美元成長｜答法：CFO與CEO談再投資方向與自籌資金，未給出占比或見效時間
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：JPMorgan：潛在控制權變動是否影響商家合作｜答法：CEO先指出問題實為兩題，對傳聞不評論，只講董事會會客觀評估並聚焦自身計畫，未直接回答商家張力
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Wolfe：第四季品牌結帳成長預期（較易比較基期）｜答法：CFO未給第四季數字，僅稱假期競爭且財測審慎
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：RBC：美國以外品牌結帳動態與結構性或地緣因素｜答法：CFO與CEO描述歐洲略改善、競爭加劇，未給海外數字
- PYPL_Q2_2026_Earnings_Call_20260728.md｜問：Cantor：7月品牌結帳相對6月退出率的趨勢｜答法：CFO只給第三季約2%，未直接回答7月對6月

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：PayPal Braintree largest merchant customer moves volume to Adyen OR in-house processing 2026；PayPal Braintree merchant loses OR moves processing volume Adyen OR Stripe OR in-house 2026；PayPal 10-K customer concentration largest merchant dependence risk factor 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"品牌結帳於 FY2026 下半年觸底並回升至低個位數 YoY（+2~4%），停止份額流失","columns":{"2Y 驗證點":"Q3/Q4 2026 branded YoY ≥+2%","5Y 驗證點":"Fastlane＋agentic commerce 使 branded 重回 5-8%","具體數字門檻":"branded YoY，Q4 FY2025 僅 +1%；FY2026 guidance transaction margin dollars 持平","信息來源":"PayPal 季度法說 branded/unbranded 拆分（Q1 FY2026 IR，2026-05-05）","漂移觸發":"連 2 季 branded YoY &lt;0% → 反轉、moat_trend 下修 ↓、thesis 削弱至 X"}},{"id":"H2","text":"FY2026-27 調整後 FCF 年化維持 ≥$5.5B，回購 ~$6B 不靠大幅舉債","columns":{"2Y 驗證點":"滾動 TTM FCF ≥$5.5B、FCF/NI ≥0.90","5Y 驗證點":"FCF 隨 margin 擴張與 Venmo 貨幣化維持","具體數字門檻":"FY2025 FCF $5.56B（yfinance）；FY2026「約 $6B 回購」（管理層 Q4 FY2025 法說）","信息來源":"PayPal FY2025 10-K；yfinance cashflow","漂移觸發":"滾動 TTM FCF 連 2 季 &lt;$5.0B → H2 削弱、重評估值錨；&lt;$4.0B → thesis 根本動搖"}},{"id":"H3","text":"total transaction take rate 年降幅收窄至 &lt;3bps/年（定價壓力趨穩）","columns":{"2Y 驗證點":"連 2 年降幅 &lt;3bps","5Y 驗證點":"Venmo／信貸／高毛利 VAS 佔比上升抵住 mix shift","具體數字門檻":"現約 6bps/年降幅（Rev +7% vs TPV +11%，Q1 FY2026）；transaction take rate ~1.66%","信息來源":"PayPal 10-K TPV／Revenue 自算；Q1 FY2026 IR","漂移觸發":"連 2 年降幅 &gt;7bps 且 Braintree 佔比續升 → mix 結構性惡化、定價能力消失確認"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"品牌結帳份額加速流失給 Apple Pay／Shop Pay／卡網直連（產業態勢競爭惡化回填）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"branded checkout YoY、branded TPV 佔比","警戒閾值":"連 2 季 branded YoY &lt;0%"}},{"id":"R2","text":"take rate 壓縮加速（unbranded/Braintree 負向 mix shift 結構化）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"Rev÷TPV 年降幅、branded/unbranded TPV mix","警戒閾值":"連 2 年降幅 &gt;7bps"}},{"id":"R3","text":"agentic commerce 去中介：AI agent 在 API 層直接調用卡網／穩定幣結算，繞過 PayPal 錢包 UI（比「品牌結帳被 Apple Pay 搶」更根本）。三方軌道戰 Visa Intelligent Commerce／Mastercard Agent Pay／Coinbase x402（Circle/Stripe/AWS/Cloudflare 背書、首年 ~1.69 億筆）主導，PayPal 不在核心玩家名單；且最大落地案例 Shopify×ChatGPT 原生軌是 Shop Pay 非 PayPal（產業態勢其他結構變數）","columns":{"對應假設":"H1＋第二曲線","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"PayPal 在 agentic 結帳份額、ACP 採用 vs Shop Pay/卡網/x402 軌道、PYUSD agentic TPV","警戒閾值":"agent 支付軌道主導權落 Visa/MA/Coinbase/Shop Pay 而 PayPal 錢包被架空"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","irr_base_pct":9.2,"ev5y_pct":48.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.3,"ev5y_pct":48.0,"irr_base_pct":9.2,"max_dd_pct":-55.0,"bull_5y_price":109.0,"bear_5y_price":35.0,"p_bull_pct":25.0,"p_bear_pct":40.0,"rearm_trigger":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","price_at_dd":45.32,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"PYPL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"PayPal Holdings, Inc."},"oneliner":"PayPal 靠成本與回購撐住 EPS，品牌結帳連四季只長 1–2%；股價已逼近傳聞收購價，Fwd P/E 10.5 倍不再明顯便宜，等品牌結帳回升與 2027 指引再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是線上付款抽成：毛利最高的品牌按鈕只長 1–2%，錢卡在「消費者每筆結帳選不選 PayPal」這一節點；成長改由 Venmo、Braintree 與金融服務補位","reasoning":"Q3 FY2026 營收 $8,584M（現貨 +2%、幣別中性 +1%），非 GAAP 營業利益率 18.8%、GAAP 16.3%，FCF $1,431M；TPV $487.1B（+6%），活躍帳戶 4.4 億。錢分三塊：品牌結帳（PayPal 按鈕，毛利最高，幣別中性 +1%）、無品牌收單（Braintree TPV +10%，量大利薄）、Venmo 與金融服務（BNPL +25%、Pay with Venmo +43%，金融服務占 TM$ 逾 20%）。營收分部金額與各段毛利事實表未涵蓋。總 take rate 約 1.76%（營收 8,584 ÷ TPV 487,100），TM$ 約 $4.0B，只占 TPV 約 0.82%。產業時鐘判在擴張期：數位支付量仍在長（TPV +6%、BNPL 與 Venmo 雙位數），但利潤池正從品牌按鈕移向裝置錢包與商家自有結帳。單點依賴：無客戶占營收逾 10%，但兩家支付處理商占交易費用 56%（2024 年 48%），集中度上升；應收帳款有一家夥伴機構占 23%（10-K FY2025 附註）。","fact_refs":["f_kpi0_net_revenues_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow","f_kpi6_active_accounts_12_mau","f_kpi7_total_payment_volume_tpv","f_peer_pypl_gross_margin_pct","f_peer_pypl_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"以 TPV 抽成的交易營收為主體，另有客戶餘額利息約 $1.1B／年（全年 TM$ 指引 $15.7B 減去不含利息的 $14.6B）與信貸收入；毛利最高的品牌結帳成長最慢，營收組合往低毛利的 Braintree 與利率敏感的利息收入偏移","unit_econ_note":"Q3 總 take rate 約 1.76%，TM$ 約占 TPV 0.82%；Q2 交易 take rate 1.61%、年降 7bp（2026-07-28 CFO）；Q3 交易費用率因組合與夥伴激勵下降、交易與信用損失下降（含信用準備迴轉），TM$ +2%（不含客戶餘額利息 +3%）","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"新任執行長重組、五項變革、2027 定為投資年；核心品牌結帳低成長但自由現金流強、每年回購約市值 12%；2026-07 傳出私募收購要約"},"industry":{"clock_phase":"II","sd_verdict_source":"數位支付需求結構性持久，但線上錢包供給可逆性高：Apple Pay、Shop Pay、卡網代幣化都能提供同樣的結帳功能，PayPal 的需求要在每一筆結帳重新贏回；依據是品牌結帳連四季 1–2%（2026-10-27 法說）對比總 TPV +6%","bargaining":{"up":"上游為卡網、發卡行與處理商；兩家支付處理商占交易費用 56%（2024 年 48%），議價集中度上升","down":"下游大型商家（Amazon 德國、DICK'S 等）談判力強，PayPal 以 contra revenue 讓利換結帳頁曝光；無單一客戶占營收逾 10%","geo":"跨境交易是重要營收與獲利來源（10-K 風險因素）；Q3 國際營收幣別中性約 −4%（法說問答，CFO 歸因歐盟取消小額免稅）"},"profit_pool_dir":"利潤池從品牌按鈕往裝置錢包、商家自有結帳與卡網代幣化移動；PayPal 以 BNPL、信貸與 Venmo 變現在消費金融端找新池子","tam_table":{"expanded":false,"reason":"利潤池遷移是爭點，但事實表未涵蓋線上結帳 TAM、品牌結帳份額與五年營業利益池占比，無數可填；改以品牌結帳 TPV 成長率（連四季 1–2%）對比總 TPV（+6%）作為份額代理"}}}},"q2_moat":{"verdict":"→：執行面因成本重整與 playbook 早期成效變強，定價面因 take rate 續降、讓利換曝光變弱，兩者抵銷；等級 C","reasoning":"機制是雙邊網路加信任品牌。可證方向改用營業利益率：PYPL TTM 18.5%，高於 Block 12.5%，略低於 Affirm 20.4%，遠低於 Visa 65.6%；自身營業利益率 FY2022 14.7% → FY2025 19.3%，TTM 回到 18.5%，擴張已停。評分：執行 7（裁員逾 2,000 人、Q3 非交易費用僅 +1%、美國品牌結帳連三季改善），定價 5（take rate 續降、以 contra revenue 讓利、處理商集中度上升），綜合 6，扣裝置錢包生態攻擊一分仍在 C。產業態勢三軸：競爭惡化中（Apple Pay、Shop Pay 擠壓品牌結帳，AP 2026-05）；結構轉好有限（BNPL +25%、Venmo 變現雙位數，但占比仍小）；其他結構變動中（英國 FCA、德國反壟斷機關、歐盟取消小額免稅）。裁決：雙向拉鋸、偏競爭惡化。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 算不出；四檢查點一紅三黃，紅在決策層級（每筆結帳都可換按鈕）。再投資：FCF 幾乎全數回購，淨再投資接近零，內生成長上界以有機 TM$ 成長約 3% 代理。","fact_refs":["f_peer_pypl_gross_margin_pct","f_peer_pypl_operating_margin_pct","f_peer_pypl_fcf_margin_pct","f_peer_xyz_gross_margin_pct","f_peer_xyz_operating_margin_pct","f_peer_v_operating_margin_pct","f_peer_afrm_operating_margin_pct","f_peer_afrm_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"雙邊網路加信任品牌：4.4 億活躍帳戶、商家端整合與買賣雙方保障；轉換成本在商家端（Braintree 留存高、加值服務附加率 6%）大於消費者端（每筆結帳都能換按鈕）","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行：裁員逾 2,000 人、管理職減少逾四分之一、Q3 非交易費用僅 +1%、美國品牌結帳連三季改善、Venmo 連八季雙位數。定價：Q2 交易 take rate 1.61% 年降 7bp、Q3 營收 +2% 落後 TPV +6%、Q3 加大 contra revenue、兩家處理商占交易費用由 48% 升至 56%。外部報導品牌結帳份額仍在流失，所以不給上升","competitor_notes":[{"name":"V","strategy_note":"網路層收費、不承擔商家風險，營業利益率 65.6% 對 PYPL 18.5%；PayPal 的交易費用多付給這一層，價值鏈位置比 PayPal 強"},{"name":"XYZ","strategy_note":"毛利率 46.4% 與 PYPL 相近、營業利益率 12.5% 較低；Cash App 與 Venmo 在轉帳與消費金融正面競爭"},{"name":"AFRM","strategy_note":"BNPL 專業對手，營業利益率 20.4%、FCF 利潤率 23.3% 都高於 PYPL；PayPal BNPL +25% 說明可以分食，但定價空間有限"},{"name":"ADYEN.AS","strategy_note":"事實表無財務數字；在大型企業收單直接對打 Braintree，Braintree 目前強調獲利成長而非搶量"},{"name":"Apple Pay／Shop Pay","strategy_note":"事實表無財務數字；以裝置與平台入口搶品牌結帳，是份額流失的主要來源（AP、Seeking Alpha 報導）"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改以營業利益率對照；ADYEN 無財務數字","threats":[{"level":"🔴","text":"Apple Pay、Google Pay、Shop Pay 以裝置與平台入口搶品牌結帳（生態攻擊）；品牌結帳連四季 1–2%","p":60,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","end_markets#2"]},{"level":"🟡","text":"AI agent 支付可能在 API 層直接調用卡網或穩定幣，繞過錢包介面；PayPal 已接入 OpenAI 與 Google 的協定並與 Meta 合作，目前未見被排除。若主要 agent 平台預設軌道不含 PayPal，升為架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"英國 FCA、德國反壟斷機關、美國 FTC 與 CFPB 程序，可能迫使修改錢包資金來源條款或罰款","p":30,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2"]},{"level":"🟡","text":"Affirm、Klarna 在 BNPL 點對點競爭；Block 的 Cash App 與 Venmo 正面競爭","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"無法判定：營業利益率 18.5% 屬中等，投入資本事實表未涵蓋，周轉率算不出","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是消費者，決策者是消費者加上決定結帳頁擺放的商家，付款者是商家。客戶要解決的問題（安全快速付款）持久，但 PayPal 按鈕只是解法之一；品牌結帳 +1% 對總 TPV +6%，需求在、解法被分食"},{"item":"決策層級","level":"🔴","text":"替代發生在每一次結帳：消費者換按鈕沒有成本，商家常同時掛多種錢包；代理變數是品牌結帳成長落後總量約 5pp。商家端較黏（Braintree 留存高、加值服務附加率由 5% 升至 6%），但那是低毛利段"},{"item":"價值鏈分配","level":"🟡","text":"上游卡網與兩家處理商（占交易費用 56%）、下游大商家（以 contra revenue 換曝光）、入口端裝置錢包三方擠壓；PayPal 營業利益率 18.5% 對 Visa 65.6%，價值多被網路層拿走。BNPL 與信貸讓 PayPal 在消費金融端多拿一層"},{"item":"社會容忍度","level":"🟡","text":"英國 FCA、德國反壟斷機關、美國 FTC 與 CFPB（PayPal Credit）同時有程序；BNPL 與信貸擴張提高消費金融監管曝險。目前在調查階段，未見處分金額"}],"roiic":"事實表未涵蓋投入資本與資本支出，無法計算","reinvest_rate":"接近 0：FY2025 FCF 5,564 約等於淨利 5,233，TTM 回購 $6B 約等於全年 FCF，淨再投資極少（資本支出與折舊事實表未涵蓋，無法精算）","endo_ceiling":3.0,"formula_note":"內生成長率＝增量 ROIC × 再投資率；兩項輸入缺，改用實際有機成長代理：Q3 TM$ 不含客戶餘額利息 +3%（2026-10-27 法說），取 3% 為上界"}}}},"q3_growth":{"verdict":"🟡：Y5 之後跑道中等。主力品牌結帳已成熟，第二曲線（金融服務、Venmo 變現）有成長但占比仍小；EPS 成長多半來自回購，不是內生","reasoning":"成長組成：量為主（TPV +6%），價為負（Q3 營收 +2% 落後 TPV），併購可忽略，EPS 多出來的部分靠淨回購與成本節省。共識 EPS FY2026E 5.55 → FY2027E 5.88 → FY2028E 6.40，年增約 7.4%（Koyfin 快照，EPS 家數未在事實表；營收共識 35～40 位分析師）。內生上界 3%，缺口約 4.4pp：Q3 非 GAAP EPS +8% 對非 GAAP 營業利益 +3%，約 5pp 來自縮股與財務項目；另有至少 $1.5B 成本節省支撐營運槓桿。缺口可歸因，不依賴重新評價。跑道：滲透率事實表未涵蓋，無法換算年數；第二曲線（金融服務、Venmo 每用戶收入 4–5 倍空間、agentic 支付）由管理層提出，只有 BNPL 與 Venmo 有數據佐證，所以給中等。衰退訊號十類亮 2 項（核心份額、替代技術），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_total_payment_volume_tpv","f_kpi0_net_revenues_gaap"],"verdict_values":{"growth":{"driver_mix":"量（TPV +6%，Venmo、Braintree 雙位數）為主，價為負（take rate 下滑），EPS 主要靠淨回購與成本節省，併購可忽略","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界 3%：再投資率接近零，以 Q3 有機 TM$（不含客戶餘額利息）+3% 代理；共識 EPS 年增 7.4% 超出部分歸因於淨回購（約 5pp）與成本節省","segments":[{"item":"品牌結帳 TPV（幣別中性）","value":"+1%，連四季 1–2%；Q4 指引 1–2%（2026-10-27 法說）"},{"item":"Braintree TPV","value":"+10%；PSP 量 +8%，加值服務附加率 6%（去年 5%）"},{"item":"Venmo","value":"TPV 連八季雙位數，ARPA 雙位數；Venmo 簽帳卡月活 670 萬（+55%）"},{"item":"BNPL／Pay with Venmo","value":"+25%／+43%"},{"item":"金融服務占 TM$","value":"逾 20%，雙位數成長"},{"item":"國際營收（幣別中性）","value":"約 −4%（法說問答，CFO 歸因歐盟取消小額免稅）"},{"item":"各段營收金額與毛利","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":null,"evidence":"資料不足：TTM 毛利率 45.76% 低於 FY2025 的 46.62%，顯示 2026 年有季度下滑，但事實表無季度拆分；Q3 TM$ 與營收同為 +2%，不足以判定連兩季"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"品牌結帳連四季 1–2%，同期總 TPV +6%；AP 與 Seeking Alpha 報導份額流向 Apple Pay、Shop Pay"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"未見提價，反而以 contra revenue 讓利換曝光"},{"signal":"EPS 年增顯著高於營收年增（差逾 5pp）","lit":false,"evidence":"前瞻口徑：共識 EPS FY2026E→FY2028E 年增約 7.4%，FY2027E 共識營收 +4.2%，差約 3pp；歷史 GAAP 口徑 2023→2025 為 18.7% 對 5.6%，若採歷史口徑此項亮起"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FY2024 1.63、FY2025 1.06"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":false,"evidence":"Q3 為 2.7%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"裝置錢包、商家自有結帳、瀏覽器存卡與 AI agent 支付壓縮品牌按鈕可得市場（10-K FY2025 風險因素）"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"資料不足：PYPL 自身 P/S、EV/S 在四個年度端點最低（分位 0），同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":null,"evidence":"資本支出事實表未涵蓋；FCF 利潤率 18.4%，商業模式輕資產"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"evidence":"營收 FY2023～FY2025 年增 8.2%、6.8%、4.3%，2027 反而加碼投資"}],"trap_rating":"價值陷阱風險中（亮 2 項，另 3 項資料不足）"}}},"q4_capital":{"verdict":"現金幾乎全數拿去回購，在約 10.5 倍本益比買回是合理用法；SBC 年化約市值 1.9% 偏高，吃掉約六分之一回購效果","reasoning":"FCF／淨利：FY2022 2.11、FY2023 0.99、FY2024 1.63、FY2025 1.06，轉換率健康。Q3 FCF $1,431M，調整後（排除 BNPL 應收款時間差）$2.0B；全年調整後 FCF 指引至少 $6.5B。SBC Q3 $233M，占營收 2.7%、占非 GAAP 營業利益 14.4%。現金去向：回購 TTM $6B（約市值 12.3%）為絕對大宗，股息殖利率 0.96%，併購只有小額（2026-01 收購 Cymbio，金額未在事實表），淨負債 $3,971M、維持投資等級。資本支出、債務到期結構與回購均價事實表未涵蓋。三項評分：併購報酬不適用（無重大併購）；回購買在約 10.5 倍本益比，盈餘殖利率約 9.5%，只要 10 年期公債殖利率低於 7.5% 即過（殖利率事實表未涵蓋）；SBC 年化 $932M ÷ 市值 $48,656M 約 1.9%，高於 1.5% 不過。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_non_gaap","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年無重大收購；2026-01 收購 Cymbio，金額與報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"回購時本益比約 10.5 倍，盈餘殖利率約 9.5%（1 ÷ 10.55）；10 年期殖利率事實表未涵蓋，低於 7.5% 即過"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"Q3 SBC $233M，年化約 $932M，÷ 市值 $48,656M 約 1.9%／年，高於 1.5%"}],"grade":null},"governance":{"capital_returns":[{"item":"TTM 回購","value":"$6B（2026-10-27 CFO）"},{"item":"FY2026 回購指引","value":"約 $6B"},{"item":"FY2026 調整後 FCF 指引","value":"至少 $6.5B"},{"item":"Q3 回購加股息","value":"逾 $1.6B"},{"item":"股息殖利率（TTM）","value":"0.96%"},{"item":"淨負債","value":"$3,971M，維持投資等級"}],"sbc":{"q3_sbc_usd_m":233,"pct_revenue":2.7,"pct_nongaap_oi":14.4,"annualized_pct_mktcap":1.9}}}},"q5_valuation":{"verdict":"現價要的是 EPS 每年約 7–8% 成長、本益比守在 10–11 倍；靠回購做得到，但前提是品牌結帳不轉負。我只信一半，估值合理不便宜","reasoning":"現價 58.58，FY2026E 共識 EPS 5.55，Fwd P/E 10.55；對 FY2027E 5.88 為 9.96 倍。Trailing P/E 11.18 落在四個年度端點的最低區（分位 2.1），P/S 1.42、EV/S 1.53 都在端點最低（分位 0），但這只有四個點，不是五年連續序列。PEG 以 FY2026E→FY2028E 共識年增 7.4% 算約 1.43。調整後 FCF 指引至少 $6.5B，約占市值 13.4%，絕對值便宜；但便宜的原因是成長低，不是市場算錯。外部對照：Q3 後賣方平均目標約 $57.19（Citi 由 $61 降到 $58），傳聞私募出價 $60.50 約為 FY2026E 的 10.9 倍，現價已在私募買方願付價位附近。一年上檔：FY2027E 基本情境 5.90 × 11 倍約 $64.9（+10.8%）；三年：FY2029E 7.00 × 11 倍約 $77.0（+31.4%）。分母：GAAP 全年 EPS 指引 5.07 比非 GAAP 5.60 低約 10%，Q3 另含信用準備迴轉；用 GAAP 算 Fwd P/E 約 11.6 倍，結論不變。同業本益比事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi5_guidance_q4_fy2026"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2026E 共識）為主，自由現金流殖利率為輔","tier":"成熟期數位支付","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比；改以自身年度端點、賣方目標價與傳聞私募出價對照"},"fwd_pe":10.55,"peg":1.43,"percentile_5y":2.1,"val_light":"🟡","val_light_derivation":"Fwd P/E 10.55 落在四個年度端點最低區（分位 2.1，非五年連續序列），歷史面便宜；PEG＝10.55 ÷ 7.4 約 1.43，落在 1～2 的合理帶；股價 58.58 已高於賣方平均目標約 $57.19、距傳聞收購價 $60.50 僅 3%。綜合判為合理，不是便宜","upside_short_pct":10.8,"upside_mid_pct":31.4,"denominator_disputed":false,"denominator_note":"非 GAAP 與 GAAP FY2026 EPS 差約 10%（5.60 對 5.07），Q3 含信用準備迴轉；以 GAAP 算 Fwd P/E 約 11.6 倍，估值結論不變，不列為爭議"}}},"q6_how_wrong":{"verdict":"最可能看錯在把品牌結帳四季維持 1–2% 當成止跌；若 2027 投資年後仍在 1% 以下，回購撐出來的 EPS 會被本益比下修抵銷","reasoning":"衰退訊號十類亮 2 項（核心份額縮減、替代技術壓縮），毛利率、產業倍數、維護性資本支出三項資料不足；若改用 2023→2025 GAAP 口徑，EPS 年增 18.7% 對營收 5.6%，第三項亮起就升為高風險。壓力三測只過一項：成長降到 5% 加本益比 9 倍，FY2031 EPS 約 7.41、價值約 $66.7，高於現價；共識到 FY2028 後零成長加 8 倍約 $51.2，不過；空頭路徑約 $43.2，不過。技術面：股價 58.7 低於 250 週均線 69.07，該均線 13 週斜率 −2.71%，長線趨勢仍向下；高於 52 週均線 51.71；RSI 63.9 未過熱，26 週漲 16.9%。","fact_refs":["f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_rsi14","f_week26_return_pct","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"低成長折價，核心按鈕份額仍在流失"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.55,"pe":10.55,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-31，與公司非 GAAP 指引 5.60 同口徑）；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[6.0,6.7,7.6,8.6,9.7],"base":[5.9,6.4,7.0,7.6,8.2],"bear":[5.6,5.5,5.4,5.4,5.4]},"pe":{"bull":14,"base":11,"bear":8},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.96,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-45,"hi":-30,"basis":"空頭終點約 −26%；路徑上可能同時遇到兩件事：收購想像退場（回到前份 2026-07-10 的 45.32，約 −23%），以及品牌結帳轉負使市場對 EPS 5.4 只給 6–7 倍（約 $32–38，−35%～−45%）。淨負債僅 $4.0B、投資等級信評、每年回購約 $6B 提供承接，所以上緣取 −30%、下緣 −45%","trigger_time":null},"basis":{"bull":"品牌結帳 2027 下半年回到 3–5%，TM$ 2028 起中個位數，成本節省部分落到利潤，加上每年約 5% 淨縮股，EPS 年增約 12%；本益比回到 14 倍","base":"品牌結帳維持 1–3%，TM$ 由 2% 爬到 4%；EPS 前兩年照共識、之後每年約 8–9%，多數來自回購；本益比 11 倍，約等於傳聞私募出價對 FY2026E 的 10.9 倍。EPS 為每股口徑已含回購，淨回購殖利率填 0 以免重複計算","bear":"品牌結帳轉負、2027 投資沒有回收、take rate 續降，淨利逐年下滑被回購抵銷，EPS 卡在 5.4；本益比 8 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"品牌結帳連四季 1–2%，同期總 TPV +6%；Apple Pay、Shop Pay 擠壓（AP 2026-05）；10-K 自承 AI agent 可能使現有技術過時","assumption":"2027 投資能把品牌結帳拉回 3% 以上","consequence":"投資年後品牌結帳若轉負，TM$ 回到零成長，回購撐的 EPS 遇上本益比壓到 6–7 倍，5 年後股價約 $32–38（−35%～−45%）；要到 −50% 還需信用損失或監管處分疊加","ruling":"採納：這是最可能的虧損路徑，空頭機率給 35%；與唯一致命點是同一條路（品牌結帳轉負是第一張骨牌），不另立","watch":"每季品牌結帳 TPV 幣別中性成長；歐洲 playbook 導入進度","evidence_refs":["competitive_share_entrants#1","end_markets#2","substitute_technology#0"],"fact_refs":["f_kpi7_total_payment_volume_tpv","f_consensus_eps_fy1"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收只長 2%，同時加大 contra revenue 投資；2027 要再投資 TM$ 與費用；Morgan Stanley 認為 take rate 持續承壓；SBC 年化約 $0.93B，約抵掉回購的六分之一","assumption":"品牌結帳回升不需要大幅讓利","consequence":"TPV 回來但 take rate 與 TM 率繼續掉，EPS 成長仍只靠回購；若股價升到 14 倍，每塊錢回購的縮股效果比現在少約四分之一","ruling":"部分採納：多頭機率只給 20%，多頭終端倍數不超過 14 倍","watch":"TM$ ÷ TPV 年變化、財報中 contra revenue 的揭露","evidence_refs":["supply_demand_durability#1","channel_business_model_shift#3"],"fact_refs":["f_kpi4_sbc_non_gaap"]},{"view":"價格已反映太多","evidence":"股價由前份 45.32 漲到 58.58（+29%），26 週 +16.9%；高於 Q3 後賣方平均目標約 $57.19；距 2026-07 傳聞收購價 $60.50 只差 3%；分析師預測仍受品牌結帳與 2027 投資壓抑","assumption":"現價沒有計入收購想像","consequence":"收購可能性若歸零，股價可能回吐部分漲幅；以前份價位計約 −23%","ruling":"採納：估值結論由偏便宜改為合理，等事件不追價","watch":"收購要約後續、賣方目標價變化","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"Q3 EPS 超標部分來自交易損失下降與預期信用外部化帶來的準備迴轉（2026-10-27 CFO）；同季營收 $8.58B 低於第三方共識 $8.71B","assumption":"2026 年的 EPS 超標可以延續","consequence":"準備迴轉不再時，Q4 與 2027 EPS 的基期偏高，2027 共識 5.88 有下修壓力","ruling":"不採信也不否定，列為待驗：若 2027 上半年信用損失率回升而 EPS 落後 5.88 路徑，判定 2026 超標屬一次性","watch":"交易與信用損失占 TPV 比率","evidence_refs":[],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi5_guidance_q4_fy2026"]},{"view":"論點失敗","evidence":"英國 FCA 對 PayPal、Visa、Mastercard 錢包資金來源條款展開競爭法調查；10-Q 揭露 FTC、CFPB 調查令與德國反壟斷程序","assumption":"監管只會帶來罰款，不改變商業條款","consequence":"若被迫改變錢包資金來源條款，資金來源組合變貴，交易費用率上升","ruling":"反駁其致命性：調查對象是條款，最壞情境是改約加罰款，不改變雙邊網路本身；保留為威脅並設觸發","watch":"FCA 與德國程序的處分內容","evidence_refs":["regulatory_antitrust#2","major_events#2"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 45.32 → 本次 58.58（+29.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=45.32","side_b":"本次 price_at_dd=58.58","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 45.32 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 45.32 美元：Bull 價 109、Bear 價 35，五年期望值 +48.0%，基準年化 9.2%，不對稱比 4.3","side_b":"本次情境、股價仍用 45.32 美元：Bull 價 135.8、Bear 價 43.2，五年期望值 +82.9%，基準年化 14.8%，不對稱比 24.39","ruling":"先換情境、股價不動：五年期望值多 34.9 個百分點，基準年化多 5.6 個百分點。不對稱比由 4.3 變為 24.39。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 45.32 美元：五年期望值 +82.9%，基準年化 14.8%，不對稱比 24.39","side_b":"本次情境、股價 58.58 美元：五年期望值 +41.5%，基準年化 9.0%，不對稱比 2.87","ruling":"再換股價、情境不動：起點價上漲 29.3%，五年期望值少 41.4 個百分點，基準年化少 5.7 個百分點，不對稱比由 24.39 降到 2.87。合計五年期望值比前份少 6.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論、機率與回撤範圍","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-07-10：股價 45.32，估值偏便宜；多頭機率 25%、空頭 40%；最大回撤 −55%","side_b":"本次：股價 58.58（+29%），Fwd P/E 10.55，估值改判合理；多頭 20%、空頭 35%；最大回撤 −30%～−45%","ruling":"估值結論轉中性的主因是股價上漲（7 月收購傳聞加上 Q3 上調指引），不是基本面變差。空頭機率降 5pp：TM$ 已恢復成長、全年 EPS 指引由 5.38 上調到 5.60。多頭機率降 5pp：起點價高 29%，品牌結帳仍未回升。回撤改成範圍並收窄，因為起點本益比已在端點最低區、淨負債僅 $4.0B 且維持投資等級。裁決與角色若有變動，同屬這次價位與估值改判的結果","evidence_level":"高","settle_metric":"股價對 FY2026E EPS 的本益比","if_then":["若股價回到 9 倍（約 $50）而品牌結帳 ≥+1%、TM$ 仍成長：估值恢復偏便宜，分批建首倉","若股價升破 $66（約 11.9 倍）而品牌結帳仍 1–2%：不追"],"evidence_refs":[]},{"axis":"護城河方向、Y5 後跑道、陷阱風險、整體評級","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","signal"],"side_a":"前份：護城河方向 →、Y5 後跑道中等、陷阱風險中、整體評級 C","side_b":"本次四欄維持：→、中等、中、C","ruling":"新證據兩邊都有。負面：品牌結帳 Q3 幣別中性 +1%，前份要求的 Q3／Q4 ≥+2% 沒達到；Q2 交易 take rate 年降 7bp。正面：TM$ +2%（不含利息 +3%）、Venmo 連八季雙位數、金融服務占 TM$ 逾 20%、非交易費用僅 +1%。品牌結帳沒有轉負，衰退訊號仍只亮兩項，所以四欄不動；降級條件寫在唯一致命點與減碼觸發","evidence_level":"中","settle_metric":"品牌結帳 TPV 幣別中性成長、TM$ 年增","if_then":["若品牌結帳連兩季 <+1%：護城河方向下修為 ↓，陷阱風險升為高","若品牌結帳連兩季 ≥+3%：Y5 後跑道與整體評級重評上調"],"evidence_refs":["end_markets#0"]},{"axis":"公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"品質複利成長","side_b":"轉機/特殊情境","ruling":"改判依據是本季逐字稿與事件：新執行長提出五項變革、裁員逾 2,000 人並砍三層組織，自稱多年期轉型；2027 定為投資年；7 月傳出私募收購要約。營收年增由 8.2% 一路降到 4.3%，Q3 只 +2%，不再符合複利成長型的成長條件。現金流面仍有複利特徵，列為次要類型","evidence_level":"中","settle_metric":"TM$ 能否回到中個位數","if_then":["若 2028 年 TM$ 年增 ≥4% 且品牌結帳 ≥+3%：轉型完成，改回複利成長型評估"],"evidence_refs":[]},{"axis":"景氣循環位置","cause":"方法變動","prior_field":["cycle_position"],"side_a":"前份：不適用（空值）","side_b":"本次：仍不適用（空值）","ruling":"支付業務不是景氣循環型，前後都不套循環位置判斷，欄位沒有變化","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件（進場首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","side_b":"品牌結帳 TPV 幣別中性連兩季 ≥+2%，且 2027 非 GAAP EPS 指引 ≥$5.88；兩者都到才重跑判斷、定首倉","ruling":"舊條件後半句「TM$ 重回成長」已在 Q3（+2%）達成，但這次成長來自 Venmo、Braintree、交易損失下降與信用準備迴轉，不代表品牌結帳止穩；用「或」連接讓條件太鬆。本次改成兩項都要，並把 2027 指引納入，因為 2027 是投資年，EPS 能否守住是另一個獨立約束。觸發後重跑判斷，進場首倉上限 2%","evidence_level":"中","settle_metric":"Q4 FY2026 與 2027 各季品牌結帳；2027-02 指引","if_then":["兩項同時達成：重跑判斷，進場首倉 ≤2%","只達成一項：維持觀望，不建倉"],"evidence_refs":["end_markets#0"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場門檻（空值）","side_b":"品牌結帳 TPV 任一季 <0% 清倉；連兩季 <+1% 減碼；TM$ 連兩季 <0% 減碼；FY2027 調整後 FCF <$5.0B 減碼；2027 指引 EPS <$5.60 減碼","ruling":"前份只有重啟條件、沒有出場門檻；本次補齊，門檻取自品牌結帳現值（+1%）與公司自己的 FCF、EPS 指引，讓清倉與減碼都對到每季可檢查的數字","evidence_level":"中","settle_metric":"每季財報","if_then":["任一清倉門檻觸發：不論持倉多少，清倉","減碼門檻同時觸發兩項以上：比照清倉"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"Single Thing：品牌結帳 TPV 幣別中性年增任一季轉負，不建倉、已持有則清倉","ruling":"新證據讓這一點成為最大敏感項：Q3 只 +1%，低於前份要求的 +2%；歐盟取消小額免稅的逆風（約 70bp）管理層預期延續整個 Q4；2027 新增投資約三分之二押在品牌結帳與 BNPL。前份把同一風險放在中期風險而未設二元門檻，本次改成二元事件","evidence_level":"中","settle_metric":"每季品牌結帳 TPV 幣別中性成長","if_then":["任一季 <0%：清倉／不建倉","2027 下半年連兩季 ≥+3%：唯一致命點機率下修，改盯 agentic 支付軌道"],"evidence_refs":["supply_demand_durability#0","end_markets#4"]},{"axis":"前份假設門檻對帳","cause":"新證據","prior_field":["thesis.H1","thesis.H3"],"side_a":"前份 H1：Q3／Q4 2026 品牌結帳 ≥+2%；H3：take rate 年降幅收窄至 <3bp","side_b":"實際：Q3 品牌結帳幣別中性 +1%；Q2 交易 take rate 1.61%、年降 7bp（2026-07-28 CFO）；Q3 營收 +2% 對 TPV +6%，降幅未收窄","ruling":"兩條前份假設的兩年驗證點都沒過，但都還沒到前份的反轉條件（品牌結帳轉負、連兩年降幅逾 7bp）。本次 H1 期限延到 2027 下半年（CFO 自承大商家投資回收期約三年），take rate 改放進風險 R2，因為公司已明說以 TM$ 為主指標","evidence_level":"高","settle_metric":"品牌結帳 TPV、總 take rate","if_then":["若 2027 下半年品牌結帳仍 <+2%：H1 判定失敗，整體評級下修"],"evidence_refs":["end_markets#0","supply_demand_durability#1"]},{"axis":"管理層前後說法（2026-07-28 法說對 2026-10-27 法說）","cause":null,"prior_field":null,"side_a":"2026-07-28 CFO：Q3 品牌結帳約 2%、全年非交易費用 +7–8%、全年非 GAAP EPS 約 5.38、TM$ 約 $15.6B；同場 CEO：成長動能 2027 下半年起累積。同場五個問題未正面回答（再投資占比與見效時間、控制權變動對商家影響、Q4 品牌結帳數字等）","side_b":"2026-10-27：Q3 品牌結帳幣別中性 +1%（含歐盟小額免稅約 70bp 拖累）；費用改為中個位數成長；EPS 上調到約 5.60、TM$ 約 $15.7B；2027 定為投資年，EPS 成長目標與 2026 相近；補上 Q4 品牌結帳 1–2% 的數字","ruling":"可調和，屬程度差異：成本與 EPS 交付優於承諾，核心品牌結帳比承諾低 1pp。EPS 超標靠費用、交易損失下降與信用準備迴轉，營收 $8.58B 還低於第三方共識 $8.71B。採信成本面，成長面列待驗","evidence_level":"中","settle_metric":"Q4 品牌結帳是否守住 1–2%；2027-02 指引","if_then":["若 Q4 品牌結帳 <+1% 且管理層再歸因外部逆風：歸因證偽，H1 削弱","若 Q4 ≥+2%：管理層成長面說法可信度上調"],"evidence_refs":[]},{"axis":"品牌結帳份額：改善還是流失","cause":null,"prior_field":null,"side_a":"管理層（2026-10-27 CEO、CFO）：導入完整 playbook 的商家群相對份額明顯改善，美國連三季改善，相對市場有進步","side_b":"外部：AP（2026-05）與 Seeking Alpha（2026-03）報導品牌結帳被 Apple Pay、Google Pay、Shop Pay 搶份額；品牌結帳 1–2% 遠落後總 TPV +6%","ruling":"可調和：改善只出現在已導入 playbook 的商家群，整體份額仍在流失。整體判斷採外部說法，管理層的改善列為待驗；管理層沒有量化份額，簡報只給趨勢","evidence_level":"中","settle_metric":"整體品牌結帳幣別中性成長","if_then":["若 2027 年 playbook 推到歐洲後整體品牌結帳仍 ≤+2%：管理層的改善只在局部成立","若整體 ≥+3%：外部份額流失說法失效"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"axis":"收購要約與現價","cause":null,"prior_field":null,"side_a":"2026-07 報導 Stripe 與 Advent 每股 $60.50 要約（未經證實）；2026-10-27 CEO：會客觀評估所有選項，目前最佳選項是執行自身計畫","side_b":"現價 58.58，距傳聞價只差 3%，且高於賣方平均目標約 $57","ruling":"現價含部分收購想像，不把 $60.50 當地板；另一面，私募買方願付約 FY2026E 的 10.9 倍，作為基本情境終端 11 倍的外部對照","evidence_level":"低","settle_metric":"要約後續公告","if_then":["若正式確認要約落空、股價回到 $50 以下而基本面無損：依重啟條件分批建首倉","若出現正式收購協議：視為事件交易，不另建倉"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：Fwd P/E 10.55；調整後 FCF 指引至少 $6.5B，約市值 13.4%；每年回購約 $6B；管理層目標中期 TM$ 中個位數、EPS 穩定雙位數；董事會沒有接受 $60.50 傳聞要約，代表經營層認為價值更高","side_b":"不買：品牌結帳未回升；2027 是投資年；股價已到傳聞收購價與賣方目標附近；股價在 250 週均線之下、長線趨勢仍向下","ruling":"觀望。綁住的約束是品牌結帳證據未到（事件錨），不是價格；估值合理只是讓我們不急。價格先走、證據未到，不追；股價下跌而基本面無損，分批建首倉","evidence_level":"中","settle_metric":"品牌結帳幣別中性成長；2027 EPS 指引","if_then":["品牌結帳連兩季 ≥+2% 且 2027 EPS 指引 ≥$5.88：重跑判斷，首倉 ≤2%","股價升破 $66 而證據未到：不追","股價跌到 $50 以下而品牌結帳 ≥+1%、TM$ 仍成長：分批建首倉，第一批 1%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"品牌結帳回升驗證","type":"假設驗證","maps_to":"H1","metric":"品牌結帳 TPV 幣別中性年增率","threshold":"連兩季 ≥+2%；2027 下半年任兩季 ≥+3% 視為成立","action":"連兩季 ≥+2% 且 2027 指引達標：重跑判斷，評估首倉 ≤2%","source_freq":"每季財報、法說與 IR newsletter","date":"2027-02 起每季","evidence_refs":["end_markets#0","end_markets#4"]},{"n":2,"text":"品牌結帳轉負","type":"Single Thing","maps_to":"Single Thing","metric":"品牌結帳 TPV 幣別中性年增率","threshold":"任一季 <0%","action":"未持有：不建倉、改為迴避；已持有：清倉","source_freq":"每季","date":"每季財報日","evidence_refs":["supply_demand_durability#0"]},{"n":3,"text":"take rate 壓縮加速","type":"風險","maps_to":"R2","metric":"總 take rate（營收 ÷ TPV）年降幅","threshold":"連兩年逾 10bp 且 TM$ 年增 <2%","action":"護城河方向下修為 ↓，重跑判斷","source_freq":"年度","date":"2027-02、2028-02","evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"價格回到偏便宜區","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2026E 共識 EPS 的本益比","threshold":"≤9 倍（約 $50），且品牌結帳 ≥+1%、TM$ 仍正成長","action":"分批建首倉，第一批 1%","source_freq":"每日股價、每季財報","date":null},{"n":5,"text":"2027 指引複審","type":"複審日期","maps_to":"H3","metric":"2027 非 GAAP EPS 全年指引","threshold":"≥$5.88 維持；<$5.60（零成長）視為投資拖垮 EPS","action":"重跑判斷；低於 $5.60 依出場門檻減碼","source_freq":"一次","date":"2027-02"},{"n":6,"text":"交易毛利額轉負","type":"減碼","maps_to":"H2","metric":"TM$ 年增率","threshold":"連兩季 <0%","action":"已持有減碼一半；未持有則延後重啟","source_freq":"每季","date":null},{"n":7,"text":"國際業務持續萎縮","type":"風險","maps_to":"R4","metric":"國際營收幣別中性年增率","threshold":"歐盟小額免稅逆風滿週年後（2027 第三季）仍 ≤−2%","action":"空頭機率上調 5pp，重跑情境","source_freq":"每季","date":"2027-10","evidence_refs":["reg_tariff_export#2"]},{"n":8,"text":"監管處分或訴訟升級","type":"風險","maps_to":"R5","metric":"英國 FCA、德國反壟斷程序結果；證券集體訴訟是否通過集體認證","threshold":"處分要求修改錢包資金來源條款，或集體認證後出現不利和解","action":"已持有減碼至半倉；未持有則延後重啟","source_freq":"事件","date":null,"evidence_refs":["regulatory_antitrust#1","lawsuit_class_action#0"]},{"n":9,"text":"收購溢價回吐","type":"風險","maps_to":"R6","metric":"收購要約狀態","threshold":"出價方或公司正式確認不再進行","action":"不追價；股價若因此回到 $50 以下，依第 4 條評估","source_freq":"事件","date":null}],"kill_metrics":[{"metric":"品牌結帳 TPV 幣別中性年增率","bear_threshold":"任一季 <0% 清倉；連兩季 <+1% 減碼","window":"每季，至 2028 年第四季","source":"公司季度財報、法說與 IR newsletter","last_status":"warning"},{"metric":"交易毛利額（TM$）年增率","bear_threshold":"連兩季 <0% 減碼","window":"每季","source":"公司季度財報","last_status":"ok"},{"metric":"調整後自由現金流（年度）","bear_threshold":"FY2027 <$5.0B 減碼","window":"年度，2028-02 驗證","source":"公司年度財報","last_status":"ok"},{"metric":"2027 非 GAAP EPS 全年指引","bear_threshold":"<$5.60（零成長）減碼","window":"2027-02 法說","source":"Q4 FY2026 財報","last_status":"unknown"},{"metric":"總 take rate（營收 ÷ TPV）年降幅","bear_threshold":"連兩年逾 10bp 且 TM$ <+2% 減碼","window":"年度","source":"公司財報營收與 TPV","last_status":"warning"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#3","reason":"這是 2026-02 的舊時點資料，描述的方向已被較新數據反轉：其後 FY1 共識在近三個月由 5.38 上修到 5.55，公司全年 EPS 指引由 5.38 上調到 5.60；以此證據判斷目前共識趨勢會用錯時點"}],"action_conditions":{"rearm_trigger":"品牌結帳 TPV 幣別中性連兩季 ≥+2%，且 2027 非 GAAP EPS 指引 ≥$5.88；兩者都到才重跑判斷、定首倉","exec_line":"觀望不建倉；重啟後首倉 ≤2%，分兩批、間隔一季；不因收購傳聞追價；價格先漲而證據未到不追","holding_cap":"3%（重啟後上限；品牌結帳連兩季 ≥+3% 才可放寬）"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件：2027-02 法說的 2027 指引與 Q4 品牌結帳；或股價回到 FY2026E 本益比 9 倍（約 $50）且品牌結帳 ≥+1%","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=16.86, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"品牌結帳在 2027 年 playbook 擴大後由 1–2% 回升，止住份額流失","2y":"2027 下半年任兩季幣別中性 ≥+3%","5y":null,"10y":null,"threshold":"每季幣別中性 ≥+1% 為底線；2027 下半年 ≥+3%","source":"公司季度法說與 IR newsletter 的品牌結帳 TPV 幣別中性成長","drift_rule":"連兩季 <+1% 削弱；任一季 <0% 反轉並觸發唯一致命點"},{"id":"H2","text":"交易毛利額成長由 2% 走到中個位數，靠 Venmo、PSP 與金融服務各自雙位數成長，不需要品牌結帳回到歷史水準","2y":null,"5y":"2028～2031 年 TM$ 年增 4–6%，金融服務占 TM$ 由逾 20% 升到 30% 以上","10y":null,"threshold":"TM$ 年增：2027 ≥+2%、2028 ≥+4%","source":"季度財報 TM$（含與不含客戶餘額利息）與法說金融服務占比","drift_rule":"TTM TM$ 連四季低於路徑 5% 以上削弱；連六季低於 10% 以上反轉"},{"id":"H3","text":"自由現金流維持每年 $6B 以上並大致全數回饋，回購讓每股盈餘在投資年仍成長","2y":"FY2026 調整後 FCF ≥$6.5B、FY2027 ≥$6.0B；2027 非 GAAP EPS ≥$5.88","5y":null,"10y":null,"threshold":"調整後 FCF 每年 ≥$6.0B；每年回購 ≥$5B","source":"季度財報現金流量表、法說回購金額、2027-02 全年指引","drift_rule":"TTM FCF 連兩季低於門檻 5% 以上削弱；連三季低於 10% 以上反轉"}],"R":[{"id":"R1","text":"品牌結帳份額持續流失給裝置錢包與商家自有結帳，playbook 推到歐洲也拉不回","h_ref":"H1","clock":"🔥","threshold":"品牌結帳幣別中性連兩季 <+1%","evidence_refs":["supply_demand_durability#0","end_markets#0","end_markets#4","channel_business_model_shift#2","competitive_share_entrants#1"]},{"id":"R2","text":"take rate 與 TM 率被讓利和 Braintree 組合拖累，量回來但錢沒回來","h_ref":"H2","clock":"🐢","threshold":"總 take rate 連兩年年降逾 10bp 且 TM$ 年增 <2%","evidence_refs":["supply_demand_durability#1","channel_business_model_shift#3"]},{"id":"R3","text":"agentic commerce 支付軌道落在卡網代幣化或穩定幣，錢包被架空","h_ref":"H1","clock":"🐢","threshold":"主要 AI agent 平台預設支付不含 PayPal，或兩年內公司仍未揭露有量的 agentic 交易","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"跨境與歐洲逆風延長：歐盟取消小額免稅、關稅與貿易爭端壓低國際營收","h_ref":"H2","clock":"⚡","threshold":"國際營收幣別中性在 2027 第三季滿週年後仍 ≤−2%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"監管與訴訟：英國 FCA、德國反壟斷、FTC 與 CFPB 程序，以及品牌結帳證券集體訴訟","h_ref":"H1","clock":"🐢","threshold":"處分要求修改錢包條款，或集體訴訟通過集體認證後出現不利和解","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"id":"R6","text":"收購溢價回吐：傳聞每股 $60.50 要約若正式落空，現價少了支撐想像","h_ref":"H3","clock":"⚡","threshold":"公司或出價方正式確認不再進行","evidence_refs":[]}],"single_thing":{"description":"品牌結帳 TPV 幣別中性年增率任一季轉負","why_fatal":"品牌結帳是毛利最高的業務，2027 新增投資約三分之二押在品牌結帳與 BNPL；投資年後若反而轉負，代表 playbook 失效，TM$ 中個位數目標失去最大支撐，EPS 只剩回購，本益比會往空頭的 8 倍走。品牌結帳占 TM$ 的確切比重事實表未涵蓋，這是依毛利排序推定的最大敏感項","if_happens":"不建倉、改為迴避；若已持有則清倉；護城河方向下修為 ↓","how_monitor":"每季財報與 IR newsletter 的品牌結帳 TPV 幣別中性成長；Q3 為 +1%，Q4 指引 1–2%","probability":"20%（12–24 個月）：Q3 已貼近底線且歐盟逆風延續到 Q4，但美國連三季改善、2027 下半年比較基期轉易"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":9.96,"peg_fy2":1.35,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":5.41,"FY2026E":5.55,"FY2027E":5.88,"FY2028E":6.4},"fy_end_month":12,"eps_basis":"FY2025A 用 GAAP 稀釋 EPS 5.41（年度財報，事實表沒有 FY2025 非 GAAP 實際值）；FY2026E～FY2028E 為 Koyfin 共識（2026-10-31），與公司非 GAAP 指引 5.60 同口徑。基期與共識口徑不同，三年年增率以 FY2026E→FY2028E 的 7.4% 為準"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 全年指引","impact":"高","watch":"2027 非 GAAP EPS 指引是否 ≥$5.88；Q4 品牌結帳是否守住 1–2%"},{"date":"2027-04","date_precision":"month","type":"product","event":"Q1 FY2027 財報：playbook 開始推到歐洲後的第一季","impact":"中","watch":"歐洲品牌結帳與國際營收幣別中性成長"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"英國 FCA 對 PayPal、Visa、Mastercard 錢包條款的競爭法調查進展","impact":"中","watch":"是否要求修改錢包資金來源或使用條款"},{"date":null,"date_precision":null,"type":"other","event":"Stripe 與 Advent 收購要約後續","impact":"中","watch":"正式確認或撤回"},{"date":"2027-10","date_precision":"month","type":"macro","event":"歐盟取消小額免稅約滿週年，比較基期轉易","impact":"中","watch":"品牌結帳與國際營收能否回升"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。plan 時 archetype 為「品質複利成長」、判斷者歸「轉機/特殊情境」，轉機/特殊情境 的專屬核心軸未採證（不計燈號）：turnaround_catalyst_timeline、turnaround_liquidation_floor。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
