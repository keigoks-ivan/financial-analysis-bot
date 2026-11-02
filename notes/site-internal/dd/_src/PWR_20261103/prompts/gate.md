你是 DD 管線 v20 的判斷層閘（gate），標的 PWR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（40 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝12014.9 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝1026.5 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝8.5 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 non-GAAP 營業利益，以此代）＝1448.9 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi6_2026`（q1_business）｜全年 2026 指引（上修）＝營收 $41.3–41.6B；adj. EPS $17.90–18.30；adj. EBITDA $4.40–4.49B；FCF $2.50–3.00B；GAAP EPS $12.57–12.97 range｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi7_backlog`（q1_business）｜總 backlog＝63731.7 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_pwr_gross_margin_pct`（q2_moat）｜PWR 毛利率＝15.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_pwr_operating_margin_pct`（q2_moat）｜PWR 營業利益率＝6.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_fcf_margin_pct`（q2_moat）｜PWR FCF 利潤率＝8.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mtz_operating_margin_pct`（q2_moat）｜MTZ 營業利益率＝4.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTZ.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mtz_fcf_margin_pct`（q2_moat）｜MTZ FCF 利潤率＝2.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTZ.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_operating_margin_pct`（q2_moat）｜EME 營業利益率＝9.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_dy_operating_margin_pct`（q2_moat）｜DY 營業利益率＝7.78 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DY.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_operating_margin_pct`（q2_moat）｜FIX 營業利益率＝16.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_fcf_margin_pct`（q2_moat）｜FIX FCF 利潤率＝19.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝17.44 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝20.52 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝23.94 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝41492.91 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝46363.8 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_fcf`（q4_capital）｜自由現金流（FCF）＝1199.4 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝6.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，IR 稿原文）https://www.sec.gov/Archives/edgar/data/0001050915/000119312526436949/d77812dex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝5196.63 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 7511.9、現金 2315.27（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝150.68 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.07 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝625.48 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝35.86 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 17.44，分子＝快照價 625.48｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝56.6 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝67.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝67.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.53 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.67 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.4 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-17.38 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝49.97｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝24.39 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 14.02 → 17.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ma_w52`（q5_valuation）｜52 週均線＝591.63 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝2.7 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K：多數業務進入門檻低，任何有資金與技術者都可能成為競爭者；分包商可能發展能力直接競標主合約；公用事業客戶有自有內部團隊，可能增加內製。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K：公司自述近期在較小規模專案已遇到更競爭的定價。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素：客戶的內部服務組織可自行施作，客戶可能被迫增加自行施作而減少外包給 PWR；MSA 下客戶無義務指派特定工作量。未找到具體客戶已導入第二供應商或自製的新聞。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因素揭露：大客戶可能減少業務、被併購或遭遇財務困難乃至破產，可能對公司造成重大不利影響（一般性揭露）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：ECMWeb：2027 北美建築展望偏謹慎（2026 末放緩），2028 起多年回升
  - 來源：ECMWeb: Navigating Construction Growth in 2027 Amid Economic Uncertainty（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素提到對併購的反壟斷審查加嚴（FTC/DOJ、HSR 法等），可能影響部分潛在收購的成本、時程或完成能力；屬一般性風險揭露，非針對 Quanta 的調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：野火事件：Quanta 營運公司曾收到辯護通知、文件保全要求與傳票，未來可能有更多相關求償（產業特定責任風險，非反壟斷）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：關稅、關稅稅負或採購限制可能墊高客戶專案成本、影響專案時程；貿易政策已影響部分元件（如太陽能板）供應鏈。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：EPC／固定價合約下負責採購銅、鋼、鋁、變壓器等材料，價格與可得性可能受關稅等全球貿易關係影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險揭露：電力變壓器可得性受製造商無法滿足需求影響，且需求預期持續上升
  - 來源：Quanta Services Form 10-K FY2025 (SEC)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：全球貿易關係（關稅、制裁性採購限制）與地緣衝突可能影響設備交付與價格
  - 來源：Quanta Services Form 10-K FY2025 (SEC)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：分析稱勞動力緊俏（尤其資料中心市場）為限制，另有許可延遲與供應鏈執行風險；E&C 毛利本質偏薄（TipRanks 空方論點）
  - 來源：Nasdaq 分析文章 / TipRanks（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Skanska 2026 春季報告：開關櫃與油浸式變壓器交期 60–100 週，2026 年電氣設備價格預期上漲 5–8%；S&P 稱銅線纜、電氣設備、變壓器漲幅最大，2026-06 更新顯示成本動能放緩但交期延長
  - 來源：Skanska Spring 2026 Supply Chain; S&P Global Market Intelligence E&C costs June 2026（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1290.0,"bear_5y_price":320.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":24.3,"ev5y_pct":22.8,"irr_base_pct":4.4,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":17.44,"pe":35.86,"basis":"FY2026E 共識調整後 EPS（Koyfin 2026-10-31），前瞻一年口徑；終端倍數同樣套在終端年當年的調整後 EPS"},"eps":{"bull":[22.0,26.5,31.5,37.0,43.0],"base":[20.8,24.0,27.4,30.7,33.8],"bear":[18.0,17.0,17.5,18.8,20.0]},"pe":{"bull":30,"base":23,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.07,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PWR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：CFO 上調 2026 全年營收指引區間（原話："revenues to range between $39.3 billion and $39.7 billion"）
- 2026-07-30｜CFO｜guidance：CFO 給出全年調整後 EPS 指引區間（原話："adjusted EPS to range between $16.45 and $16.95"）
- 2026-07-30｜CFO｜guidance：新指引內含四家併購的營收貢獻（原話："$1.2 billion to $1.4 billion of revenues"）
- 2026-07-30｜CFO｜guidance：新指引內含四家併購的調整後 EBITDA 貢獻（原話："$120 million to $140 million of adjusted EBITDA"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明負債對 EBITDA 比率自 2025 年底 1.95 降至 1.7（原話："our debt-to-EBITDA ratio improved to 1.7,"）
- 2026-07-30｜CEO｜margin：CEO 表示下半年毛利率仍有上行空間，且指引採保守做法（原話："So yes, I think there's upside in the back."）
- 2026-07-30｜CEO｜margin：CEO 重申電力部門利潤率能力的口徑（10 至 12，12 為上限）（原話："the electric segment has the ability to operate 10 to 12"）
- 2026-07-30｜CEO｜margin：CEO 答覆地下與基礎建設部門利潤率可能追上電力部門，先求達雙位數（原話："let me get to double digits first"）
- 2026-07-30｜CEO｜margin：CEO 稱地下部門有機會與電力部門持平，取決於工作組合（原話："I do think we have opportunities to get at parity"）
- 2026-07-30｜CFO｜margin：CFO 答覆本季無一次性項目（回應 SunZia 結算問題）（原話："There was nothing onetime in our quarterly"）
- 2026-07-30｜CFO｜guidance：CFO 稱自由現金流轉換率口徑約 55%（Investor Day 提過 55% 至 60%），並認為今年可達區間高端（原話："rate of around 55%."）
- 2026-07-30｜CFO｜customer：CFO 稱合約條款對現金流與營運資金有利，且遍及各業務（原話："We are getting favorable contracting terms"）
- 2026-07-30｜CEO｜competition：CEO 回應部分公用事業自建燃氣發電的趨勢（原話："Yes, it sounds easy. It's not."）
- 2026-07-30｜CEO｜risk：CEO 說明對複循環與單循環燃氣機組 EPC 的風險立場（原話："not willing to take the risk on the combined cycle side"）
- 2026-07-30｜CEO｜commitment：CEO 稱 NiSource 相關工作大部分將於第三季進入在手訂單（原話："a significant amount of that will go into backlog"）
- 2026-07-30｜CEO｜commitment：CEO 預期第三季甚至第四季在手訂單續創新高（原話："record backlog into the third and probably even into"）
- 2026-07-30｜CEO｜customer：CEO 描述傳統輸配電業務成長口徑（原話："upper single-digit growth in the business as it sits"）
- 2026-07-30｜CEO｜customer：CEO 說明大型輸電專案預計進場施工的時間點（原話："second half of '27, you'll start to see us go to the field"）
- 2026-07-30｜CEO｜customer：CEO 給出科技業務占整體營收比重的口徑（原話："15% of the business is technology, call it, 15% to 20%"）
- 2026-07-30｜CFO｜risk：CFO 說明資料中心專案列入在手訂單的規則（原話："we tend to put in things that have only LNTPs"）
- 2026-07-30｜CEO｜risk：CEO 回應紐約州資料中心暫停令對公司影響（原話："having a moratorium in New York doesn't bother me at all"）
- 2026-07-30｜CEO｜customer：CEO 否認本季有訂單提前拉貨（原話："nothing pulled in at all that I'm aware of"）
- 2026-07-30｜CEO｜risk：CEO 稱產能充足、無人力吃緊（原話："we're nowhere near capacity"）
- 2026-07-30｜CEO｜competition：CEO 稱近期不會看到技術工人供給過剩（原話："we're not seeing any oversupply of craft-skilled"）
- 2026-07-30｜CEO｜capital_allocation：CEO 稱每年訓練支出約 2.5 億美元（原話："we spend about $250 million a year in training"）
- 2026-07-30｜CEO｜capital_allocation：CEO 說明併購節奏不均：上季 0 件、本季 4 件（原話："Last quarter, we did zero. This quarter, we did 4."）
- 2026-07-30｜CEO｜capital_allocation：CEO 表示不看 EBOS 類公司（原話："I'm not looking at EBOS companies"）
- 2026-07-30｜CEO｜capital_allocation：CEO 說明垂直供應鏈投資將選擇性進行（原話："We'll be selective in how we invest there."）
- 2026-07-30｜CEO｜product：CEO 說明預製與整合製造面積擴增（原話："talked about having 7 million square feet"）
- 2026-07-30｜CEO｜product：CEO 答覆 800 伏特架構相關招標尚未出現（原話："We haven't seen it show up."）
- 2026-07-30｜CEO｜guidance：CEO 說明管線業務預算內部設定的口徑，並稱已超過（原話："we kind of put $500 million in our head"）
- 2026-07-30｜CFO｜guidance：CFO 答覆併購貢獻約為半年份，可自行年化（原話："It's about 6, 7 months worth of what we gave you."）

### PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md
- 2026-03-31｜Jayshree Desai｜guidance：2030 目標：有機營收 CAGR 7%–10%（原話："grow organic revenue by 7% to 10% CAGR"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 目標：調整後 EBITDA 利潤率 10%–11%（原話："the ability to generate 10% to 11% adjusted EBITDA margins"）
- 2026-03-31｜Jayshree Desai｜margin：利潤率擴張幅度相對 2026 財測高標的口徑（原話："an 80 basis point expansion against the high end"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 調整後 EPS 目標區間（原話："targeting an EPS and adjusted EPS range of $21.60 to $26.75"）
- 2026-03-31｜Jayshree Desai｜guidance：EPS 複合成長率目標（含資本配置）（原話："grow 15% to 20% compound annual"）
- 2026-03-31｜Jayshree Desai｜guidance：管理層稱不含併購的有機 EPS 可達雙位數成長，未給具體有機 EPS 目標（原話："achieve a double-digit EPS growth organically"）
- 2026-03-31｜Jayshree Desai｜guidance：全部機會疊加時 EPS CAGR 可超過 20%（原話："we should see an adjusted EPS CAGR of north of 20%"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 營收區間 440–490 億美元（原話："organic revenue CAGR, $44 billion to $49 billion"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 ROIC 目標 12%–15%（原話："we now expect a 12% to 15% by the end of 2030"）
- 2026-03-31｜Jayshree Desai｜guidance：2030 自由現金流轉換率目標 55%–60%（原話："we will be able to achieve a 55% to 60% conversion ratio"）
- 2026-03-31｜Jayshree Desai｜risk：管理層提到製造擴張對自由現金流轉換率的壓力（原話："free cash flow conversion given the manufacturing expansion"）
- 2026-03-31｜Jayshree Desai｜guidance：五年累計自由現金流預期（原話："$10 billion to $12 billion of free cash flow in this time"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：槓桿目標區間（原話："We're targeting a leverage ratio of 1.5 to 2x"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：管理層稱不被槓桿區間綁住（原話："But we don't feel any pressure to force"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：併購時槓桿可拉高的上限（Blattner 為例）（原話："You could see us pushing closer to 3"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：併購與回購以報酬率高低擇優（原話："buy a great company versus buying our shares back"）
- 2026-03-31｜Jayshree Desai｜capital_allocation：過去四年併購金額相對自由現金流（原話："bought $6 billion worth of companies"）
- 2026-03-31｜Jayshree Desai｜commitment：股利承諾：持續成長（原話："We're going to continue to grow our dividend"）
- 2026-03-31｜Earl Austin｜commitment：CEO 稱這些數字對他是個人承諾（原話："I don't view it goes away today. I view it last."）
- 2026-03-31｜Earl Austin｜commitment：CEO 稱不會放上自己不相信的計畫（原話："we would not put a plan up here that we didn't believe in"）
- 2026-03-31｜Earl Austin｜guidance：CEO 稱財測屬審慎（原話："Our guidance is prudent."）
- 2026-03-31｜Jayshree Desai｜guidance：管理層稱規劃以約 80% 效率率計，預留專案遞延（原話："ourselves at an efficiency rate of around 80%"）
- 2026-03-31｜Earl Austin｜guidance：CEO 稱寬幅財測約 80% 會如期落實（原話："you can expect about 80% of it to be right"）
- 2026-03-31｜Jayshree Desai｜margin：管理層要求勿過度解讀分部數字（原話："directional, directional"）
- 2026-03-31｜Jayshree Desai｜margin：利潤率擴張來源之一：企業整體績效改善（原話："performance improvements across the enterprise"）
- 2026-03-31｜Jayshree Desai｜margin：CFO 承認部分營運未達預期（原話："We haven't performed as well as we'd like"）
- 2026-03-31｜Jayshree Desai｜margin：CFO 稱可能為長期可見度讓出部分利潤率（原話："there may be times when we will give up some margin"）
- 2026-03-31｜Earl Austin｜margin：預製化／AI 帶來的利潤率貢獻量級（原話："it gives you some margin expansion, albeit small"）
- 2026-03-31｜Earl Austin｜margin：技術端客戶若要更快或承擔風險，定價可含風險溢價（原話："if there's risk to it, yes, you can expect more margins"）
- 2026-03-31｜Earl Austin｜margin：受管制業務端定價預期（原話："on our regulated side of the business"）
- 2026-03-31｜Jayshree Desai｜risk：固定價格大型合約佔比（原話："less than 15% of our revenues comes from fixed"）
- 2026-03-31｜Earl Austin｜customer：資料中心／大型負載佔積壓訂單比重（原話："while we talk about this, it's only 10%"）
- 2026-03-31｜Jayshree Desai｜customer：技術與大型負載為最快成長市場（原話："That will be our fastest-growing market as we see it today."）
- 2026-03-31｜Jayshree Desai｜customer：電力生成與儲能 CAGR 中點約雙位數（原話："At the midpoint, we're seeing about double-digit growth"）
- 2026-03-31｜Earl Austin｜customer：總可及市場規模（原話："we think it's around $2.4 trillion"）
- 2026-03-31｜Earl Austin｜customer：資料中心可及範圍占比（原話："it's about 50% to 60% of that"）
- 2026-03-31｜Earl Austin｜customer：需求展望延伸至 2030 年後（原話："This business has not stopped at 2030."）
- 2026-03-31｜Earl Austin｜customer：NiSource 機會規模（原話："$5 billion to $7 billion type opportunity"）
- 2026-03-31｜Jayshree Desai｜customer：NiSource 已計入預測（原話："that is baked into our projections"）
- 2026-03-31｜Earl Austin｜customer：客戶詢案頻率（原話："there's not a week that goes by, something doesn't"）
- 2026-03-31｜Earl Austin｜product：變壓器投資金額（CEO 先說錯後更正）（原話："million to $700 million investment"）
- 2026-03-31｜Earl Austin｜product：765kV 變壓器廠擴產（原話："where that factory will double in"）
- 2026-03-31｜Earl Austin｜product：管理層稱不承擔大宗商品風險（原話："We don't take commodity risk."）
- 2026-03-31｜Karl Studer｜product：整合式預製廠面積目標（原話："looking to grow to over 5 million this year"）
- 2026-03-31｜Earl Austin｜product：機械（MEP）平台併購（原話："DSI was kind of a platform acquisition we made last year"）
- 2026-03-31｜Earl Austin｜product：人力與營收成長關係不宜放進財務模型（原話："something that you can put in a financial model"）
- 2026-03-31｜Earl Austin｜product：CEO 估計所需人力成長（原話："you need to grow 7,000 to 10,000 a year"）
- 2026-03-31｜Jayshree Desai｜product：CFO 要求勿把人力成長當建模依據（原話："I don't want you guys to take that as a modeling exercise."）
- 2026-03-31｜Earl Austin｜competition：多數工作為議價而非競標（原話："the negotiations are around 75%"）
- 2026-03-31｜Earl Austin｜competition：電信與大型管線缺乏規模（原話："we don't have scale there in places"）
- 2026-03-31｜Earl Austin｜competition：聯合循環電廠風險態度（原話："take that risk of a combined cycle as it stands today"）
- 2026-03-31｜Earl Austin｜competition：對同業承擔 CCGT 勞力風險的看法（原話："I'm unwilling to take those risks of the past"）
- 2026-03-31｜Earl Austin｜capital_allocation：不買押注單一題材的公司（原話："I'm really concerned with these hockey stick companies"）
- 2026-03-31｜Earl Austin｜capital_allocation：併購模型不內建綜效（原話："we don't build synergies in our models to"）
- 2026-03-31｜Earl Austin｜capital_allocation：併購估值壓力看法（原話："acquire great companies at this kind of framework"）
- 2026-03-31｜Earl Austin｜guidance：全疊加情境營收預期落在區間高端（原話："full stack will be at the high end of the range."）
- 2026-03-31｜Jayshree Desai｜guidance：大型機會時程尚未確定，不在目標內（原話："the timing of those things can be still a little bit"）
- 2026-03-31｜Jayshree Desai｜risk：管理層列舉監管與許可風險（原話："have to get through the regulatory process"）
- 2026-03-31｜Jayshree Desai｜risk：稅務抵減（48E）不確定性，管理層稱是風險（原話："that is out there and that is a risk"）
- 2026-03-31｜Jayshree Desai｜risk：管理層稱目前對電力生成成長無疑慮（原話："we do not see any concerns"）
- 2026-03-31｜Jayshree Desai｜commitment：管理層稱 2026 目標將超標（原話："We now expect to exceed our targets on"）
- 2026-03-31｜Jayshree Desai｜commitment：EPS 加倍承諾（原話："we can double that over the next 5 years"）

### 問答異常語氣（迴避／改口／保留）
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Steven Fisher (UBS) 問長期利潤率上行空間，管理層過去對利潤率上行訊息偏保守｜答法：CEO 說下半年有 room、指引 prudent，但未給具體利潤率數字或長期目標
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Chad Dillard (Bernstein) 問預製業務占 RFP 比重、5 年展望、勞動成本節省與價值定價｜答法：CEO 談面積與協作，未回答 RFP 占比、5 年展望，也未直接回答價值定價
- PWR_Q2_2026_Earnings_Call_20260730.md｜問：Chris Tsung (Wolfe) 問收購標的年化 EBITDA 與購買倍數｜答法：CFO 要求分析師自行計算，未給年化數字與倍數
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：Wolfe：電力生成 CAGR 內含多少 NiSource 類專案｜答法：CFO 答 NiSource 已計入；CEO 改談『若不是 NiSource 就會是別家』，未給專案數量
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：ROTH：48E 稅務抵減與 FEOC 指引延遲對再生能源業務的影響｜答法：CFO 稱『沒有疑慮』並承認是風險，未給具體曝險或數字
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：UBS：人力成長與 7–10% 有機成長的橋接｜答法：CEO 給 7,000–10,000 人/年，CFO 隨即說別當建模依據，口徑收回
- PWR_Analyst_Investor_Day_Quanta_Services_Inc_20260331.md｜問：Goldman：活躍市場機會是否含在財測內｜答法：CFO 以多種方式回答（可疊加亦可降低目標風險），未直接答含或不含，並稱時程仍不確定

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 2 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 1 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260731","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國電網與發電資本支出超級週期在 2026-2031 不中斷，且規劃額能實際轉為核准與開工"},{"id":"H2","text":"craft 工班稀缺使 Quanta 保有工程選擇權與利益率結構——Electric 分部守在 10-12%、Underground 由 9.1% 升向雙位數"},{"id":"H3","text":"市場願意持續給 Quanta 26 倍以上的 FY+2 遠期本益比（現為 32.9x）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"固定價格／EPC 專案成本超支。Primoris 於 2026 年 6 月因六個再生能源固定價格專案超支，全年淨利指引由 $2.23-2.34 億砍至 $0.71-1.01 億、營運長離職。Quanta 的 10-K 只把合約分成單價／成本加成／固定價格三類，未揭露固定價格佔營收比重（數據限制）。發電 EPC 與資料中心整體工程正是固定價格風險最集中的型態，而 Quanta 正在往這兩塊擴張。"},{"id":"R2","text":"費率端政治反彈使資本支出「規劃」無法轉「核准」。EEI／S&amp;P 的 $1.3-1.4 兆是規劃額；零售電價因資料中心負荷上升而走高已引發州級審查壓力，費率案審批放緩會直接拖慢那 95% 尚未進入在手訂單的大型專案。併網佇列改革（PJM 的 first-ready, first-served 群組研究）同向延後發電專案成熟時點。執行長本人反覆強調「公司高度專注於把成本壓低給費率支付者」——這正是議價權被封頂的機制。"},{"id":"R3","text":"資料中心州級禁令擴散 ＋ 再生能源稅負優惠限縮，同時壓縮技術／大負載與再生能源兩條腿。紐約州已通過全美首例：2026-06-04 州議會通過 Responsible Data Center Development Act、州長簽署行政命令暫停超大規模資料中心一年；2026 年共 11 州提出州級暫停法案，數十個地方政府已自行凍結。喬治亞州 S.B. 476 擬取消幾乎全部州級稅負抵免。技術業務目前佔 PWR 營收 15-20%（執行長 2026-07-30）。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY+2 遠期本益比回落至 26x（約 $520）；或管理層正式將 2030 adj EPS 目標重設至 ≥$29 並經一季驗證","irr_base_pct":5.6,"ev5y_pct":19.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.36,"ev5y_pct":19.9,"irr_base_pct":5.6,"max_dd_pct":-60.0,"bull_5y_price":1168.0,"bear_5y_price":324.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"FY+2 遠期本益比回落至 26x（約 $520）；或管理層正式將 2030 adj EPS 目標重設至 ≥$29 並經一季驗證","price_at_dd":657.98,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"PWR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Quanta Services, Inc."},"oneliner":"美國電網與大型負載建設中規模最大的自營施工商。在手訂單 637 億美元，全年財測第三度上修，生意比 7 月更強。但前瞻本益比 35.9 倍，五年基準年化報酬約 4.5%。等價格回到 535 美元附近，或 2027 財測確認後再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PWR_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是公用事業與科技業電力建設的施工錢，靠長約框架合約加自營工班。錢卡在技術工班與關鍵設備兩個節點，Quanta 兩個都在補位。","reasoning":"最新一季（2026 Q3）營收 120.1 億美元、年增 57%；GAAP 營業利益 10.3 億美元，利益率 8.5%；調整後 EBITDA 14.5 億美元，利潤率 12.1%（CFO）。TTM 毛利率 15.76%。全年財測第三度上修，營收 413–416 億美元，調整後 EPS 17.90–18.30 美元。分部數字事實表未涵蓋，只能用法說給的量級：電力部門裡的公用事業業務約 200 億美元、利潤率 10–12%（Q3 法說 CEO）；科技相關約占 15–20%（2026-07-30 法說 CEO）；再生能源 50–100 億美元（Q3 法說 CEO）。收錢方式以框架合約與議價合約為主，投資人日 CEO 說議價約占 75%；投資人日 CFO 說 >3 億美元的固定價格合約占營收不到 15%。單點依賴：沒有。最大客戶占 2025 年營收 8%，前十大占 30%，2023–2025 年沒有任何客戶超過 10%（10-K）。產業處於擴張期：在手訂單 637 億美元、年增約 63%，大型 765kV 輸電與發電專案都還沒入帳。供需持久性分兩塊看：電網屬結構性持久，資料中心與再生能源屬週期性。技術工班要多年才養得出來，供給的可逆性低。產業態勢判為結構性轉好中：在手訂單季增 100 億美元，各主要市場都在增（Q3 CFO）。競爭面只在小型案惡化（10-K 自述定價更競爭）。其他結構變數（關稅、變壓器交期、野火責任）偏負面，但還沒反映到毛利率。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_adjusted_ebitda_non_gaap","f_kpi6_2026","f_kpi7_backlog","f_peer_pwr_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"以框架合約與議價合約為主。在手訂單約為 2026 營收財測中點的 1.5 倍（637 ÷ 414.5 億美元）。合約預收款改善了營運資金（Q3 CFO），收入能見度高。但 CEO 說沒簽約就不入帳，訂單數字會跳動。","unit_econ_note":"利潤率被費率支付者封頂，公用事業段刻意守在 10–12%（Q3 CEO）。成長主要來自工作量，以及每 MW 擷取金額提高：資料中心由每 MW 3–4 百萬美元升到 5–7 百萬美元（Q3 CEO 粗估）。2026 調整後 EBITDA 利潤率中點 10.7%。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"屬資本支出建設循環型：營收跟著公用事業與超大型科技公司的資本支出走。但 2009 年營收 −12.2% 時，毛利率反升到 17.9%，可見景氣循環中仍能賺錢。公用事業框架合約這塊底盤有長期複利性質；資料中心、再生能源與管線屬循環部分。"},"industry":{"clock_phase":"II","sd_verdict_source":"電網部分結構性持久，大型負載部分週期性。CEO 說客戶要的方案延伸到 2030 年後，公用事業規模要長大一倍（Q3 法說），在手訂單年增約 63%。資料中心這塊有渠道調查稱工程延後（Q3 法說 ROTH 提問），ECMWeb 也預期 2027 北美建築偏謹慎。","bargaining":{"up":"上游設備商目前議價力較強：變壓器、開關櫃交期 60–100 週（Skanska），CEO 說成長取決於 OEM。Quanta 是高壓設備前五大買家，並投入 5–7 億美元自建變壓器與斷路器產能，又併購電桿廠反制。","down":"對公用事業的議價受費率封頂，刻意守 10–12% 利潤率。對科技客戶可以就速度與確定性收溢價（投資人日 CEO）。議價合約約占 75%。","geo":"海外營收占 7.0%，主要在加拿大、澳洲，其餘在美國。關稅主要經由材料與客戶專案成本間接影響。"},"profit_pool_dir":"利潤池正往上游關鍵設備與工期確定性移動。Quanta 用垂直整合與預製產能（約 670 萬平方英尺）跟進，把利潤往自己這一節點拉。","tam_table":[{"item":"可及市場（投資人日 CEO）","value":"約 2.4 兆美元，期間口徑未說明"},{"item":"2026 營收財測中點占可及市場","value":"約 1.7%（414.5 億 ÷ 2.4 兆美元；分母期間不明，只看量級）"},{"item":"資料中心每 MW 擷取金額","value":"每 MW 約 1500 萬美元的機電支出中，一年前拿 3–4 百萬，現在拿 5–7 百萬，目標 7–10 百萬（Q3 CEO 粗估）"},{"item":"資料中心與大型負載占在手訂單","value":"約 10%（2026-03-31 投資人日 CEO）"},{"item":"營業利益池占比，5 年前與現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河 B 級，方向向上。技術工班規模大（自營比率 85%），又能跨工種調度，所以 Quanta 賣得出工期確定性。定價權被費率封頂，優勢主要表現在量與執行，不在價格。","reasoning":"機制能驗證的部分在執行面。GAAP 營業利益率由 2022 年 4.91% 升到 2025 年 5.57%，TTM 再到 6.81%；FCF 利潤率由 4.12% 升到 TTM 8.46%。同期營收由 170.7 億升到 284.8 億美元，規模放大時利潤率同步改善，表示新增工作的報酬高於舊工作。同業對照：TTM 營業利益率高於最直接的對手 MTZ（4.85%），低於建物機電的 EME（9.88%）與 FIX（16.66%），DY 為 7.78%。FCF 利潤率 8.46% 僅次於 FIX。同業的投入資本報酬差距事實表未涵蓋，所以綜合分不給到 8。定價面：CEO 明說公用事業段不會超過 10–12%（Q3 法說回答 Truist 提問），10-K 也說小型案定價更競爭，因此定價力給 6 分，執行力給 9 分。當期投入資本報酬與再投資率事實表未涵蓋，下面用管理層目標與併購金額估量級。","fact_refs":["f_peer_pwr_gross_margin_pct","f_peer_pwr_operating_margin_pct","f_peer_pwr_fcf_margin_pct","f_peer_mtz_operating_margin_pct","f_peer_mtz_fcf_margin_pct","f_peer_eme_operating_margin_pct","f_peer_dy_operating_margin_pct","f_peer_fix_operating_margin_pct","f_peer_fix_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"三件事合起來就是工期確定性：技術工班的規模與跨工種流動性（今年新增約 2.6 萬人，每年訓練支出約 2.5 億美元）、嵌入公用事業資本計畫的長期框架合約、關鍵設備的垂直整合。新進者能接小案，接不了多年、多州、跨工種的計畫型工作。","execution":9,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"執行面在擴大：GAAP 營業利益率由 2022 年 4.91% 升到 2025 年 5.57%，TTM 6.81%，Q3 單季 8.5%。資料中心每 MW 擷取金額由 3–4 百萬美元升到 5–7 百萬美元（Q3 CEO）。CSIMarket 也顯示 PWR 占同業合計營收的比重上升。定價面持平：公用事業段刻意守 10–12%，小型案定價更競爭（10-K）。兩者合起來，方向向上。","competitor_notes":[{"name":"MTZ","strategy_note":"最直接的電力與管線施工對手。TTM 營業利益率 4.85%、FCF 利潤率 2.34%，都低於 PWR。同樣在擴變壓器與預製產能，但規模與現金轉換都落後。"},{"name":"EME","strategy_note":"以建物機電為主，營業利益率 9.88%，高於 PWR。PWR 往機電與資料中心延伸時，EME 是利潤率標竿；大型輸電上兩家沒有直接競爭。"},{"name":"DY","strategy_note":"以電信與公用事業配線為主，營業利益率 7.78%，略高於 PWR。業務重疊在配電與地下工程。"},{"name":"FIX","strategy_note":"資料中心機械空調承包商，營業利益率 16.66%、FCF 利潤率 19.46%。Truist 拿它質疑 PWR 的利潤率天花板，CEO 回答公用事業段的 10–12% 是刻意設計。"}],"peer_na_reason":"同業的投入資本報酬與投入資本事實表未涵蓋，只能用營業利益率與 FCF 利潤率對照。","threats":[{"level":"🟡","text":"10-K 自述部分業務進入門檻低，小型案已見更競爭的定價。屬點對點競爭，大型計畫型工作未受影響。","p":"25%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"公用事業客戶可能擴大內部施工，或自己併購施工商；框架合約沒有最低工作量。目前沒有具名客戶這樣做。","p":"15%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"變壓器等上游設備產能吃緊，價值鏈利潤往設備商移。Quanta 以自建製造部分反制。","p":"30%","evidence_refs":["geo_supply_chain#0"]}],"roic_durability":{"quadrant":"低利益率、高周轉：TTM 營業利益率 6.81%；投入資本事實表未涵蓋，周轉率算不出來。判斷偏高周轉，依據有三：合約預收、DSO 改善（Q3 CFO）、FCF 高於淨利（2024–2025 年約 1.6 倍）。這種結構容易被誤判成薄利的爛生意。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是電網與資料中心，決策者是公用事業與科技公司的資本規劃部門，付款者是費率支付者與超大型科技公司。電網可靠度與負載成長是必要支出，延後的代價是停電與無法併網。代理讀數：在手訂單 637 億美元、年增約 63%，12 個月以外的部分也在增（Q3 CEO）。"},{"item":"決策層級","level":"🟡","text":"在多年、多州的計畫型工作上，替代者少：議價約占 75%、自營 85%，而且嵌入客戶的長期資本計畫。但在單一小型案上替代者多：10-K 自述進入門檻低、小型案定價更競爭，客戶也有內部施工團隊。代理讀數：前十大客戶占 30%，沒有單一客戶超過 10%；續約率與漲價後的流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"變壓器、開關櫃、電桿是瓶頸，交期 60–100 週，價值往設備商移，CEO 也說成長取決於 OEM。Quanta 以高壓設備前五大買家的身分談長約，並投入 5–7 億美元自建製造、併購電桿廠，把一部分瓶頸收回自己手上。"},{"item":"社會容忍度","level":"🟡","text":"電價上漲與資料中心的政治爭議是一道看得見的天花板。CEO 主動把公用事業利潤率守在 10–12%，說要對費率支付者負責（Q3 法說）；紐約州已有資料中心暫停令（2026-07-30 法說 CEO 回應不在意）。管理層刻意不把價格推到經濟上限，等於繳保費換長期關係。"}],"roiic":"事實表未涵蓋，缺投入資本、資本支出、折舊與收購淨額。只能給量級：2022→2025 年營業利益增加約 7.5 億美元（838→1586 百萬），同期併購約 60 億美元（投資人日 CFO）。但營業利益的增量含有機成長，拆不出併購本身的增量報酬；CFO 在 2026-07-30 法說也拒絕給收購倍數。","reinvest_rate":"量級為 100% 以上：2022–2025 年併購約 60 億美元，已經超過同期稅前營業利益合計約 48.2 億美元，差額靠舉債與預收款支應。這還沒算製造擴產的資本支出。","endo_ceiling":15,"formula_note":"內生成長上限＝增量報酬 × 再投資率。增量報酬用管理層 2030 年投入資本報酬目標 12–15% 的上緣代理（這是目標，不是實績）。可持續的再投資率封頂在 100%，因為槓桿目標是 1.5–2 倍，不能長期超額舉債。兩者相乘約 15%/年。2026 年營收約 +46%，遠超這個上限，來源是需求暴衝、訓練支出走費用而非資本、以及預收款。這屬一次性加速，不外推。"}}}},"q3_growth":{"verdict":"跑道寬：765kV 大型輸電與發電 EPC 還沒進在手訂單，公用事業這塊底盤延伸到 2030 年後。但共識 2026→2028 年 EPS 年增 17.2%，超過約 15% 的內生上限，超出的部分要靠利潤率改善來補。","reasoning":"成長以量為主。2026 年新增約 2.6 萬名員工，其中有機約 1.2 萬人（Q3 CEO）。營收財測中點較 2025 年增約 46%，其中四家併購貢獻 12–14 億美元營收（2026-07-30 CFO），約占 3%。價格貢獻小，也沒有回購。共識 EPS：FY2026 17.44、FY2027 20.52、FY2028 23.94 美元，兩年年增 17.2%。若以投資人日數字反推的 2025 年調整後 EPS 約 10.75 美元為基期，三年年增 30.6%；但 2026 年只剩兩個月，這段加速多半已經實現。共識 FY2027 營收 463.6 億美元，只比 FY2026 多 11.7%，表示市場已預期營收放慢、改靠利潤率撐 EPS。管理層說法前後一致：投資人日給出 2030 調整後 EPS 21.60–26.75 美元，年增 15–20%（含資本配置），有機部分為雙位數；Q3 法說則說 2027 年仍會強勁雙位數成長，進度已超前投資人日計畫。FY2028 共識 23.94 美元已經落在 2030 目標區間內，這代表目標可能提前上調，也代表市場預期已經拉高。跑道方面，客戶要的方案延伸到 2030 年後，765kV 計畫 2027 年上半年才開始入帳（Q3 CEO），第二、第三條成長曲線都有出處。十類衰退信號只亮一個：EPS 成長明顯快過營收成長（2022–2025 年 GAAP EPS 年增約 27%，營收約 18.6%），來源是利潤率擴張。管理層自己說這不是利潤率的故事，所以後段的 EPS 成長應該會收斂回營收成長的速度。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_2026","f_kpi7_backlog"],"verdict_values":{"growth":{"driver_mix":"量為主（員工與工作量增加），加上利潤率擴張與小型併購；價格貢獻小，沒有回購。","runway_years":"10 年以上。事實表未涵蓋滲透率序列，這是依客戶規劃延伸到 2030 年後、765kV 尚未入帳所做的判斷。","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河題的再投資推導，內生上限約 15%/年（增量報酬以管理層 2030 年投入資本報酬目標上緣代理，乘上 100% 的可持續再投資率）。與共識的缺口：FY2026→FY2028 年增 17.2%，超出約 2pp；若從反推的 2025 年基期算三年 30.6%，超出約 16pp，且主要集中在 2026 年。缺口來源以利潤率擴張為主（GAAP 營業利益率由 2025 年 5.57% 升到 Q3 8.5%，地下部門往雙位數走），併購為輔（四家併購約 12–14 億美元營收），可以歸因。Base 情境五年年增約 14%，在上限之內。","segments":{"expanded":false,"reason":"事實表未收錄分部營收與利潤率。法說只有 CEO 口頭給的量級（公用事業約 200 億美元、科技 15–20%、再生能源 50–100 億美元），口徑與期間都不一致，撐不起判斷，所以成長判斷改用在手訂單與共識。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"TTM 毛利率 15.76%，高於 2022–2025 年的 14.07–15.01%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"CSIMarket 顯示占同業合計營收的比重上升"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"不適用：公用事業利潤率封頂，沒有主動提價"},{"signal":"EPS 成長比營收快 5pp 以上","lit":true,"evidence":"2022–2025 年 GAAP EPS 年增約 27%，營收約 18.6%；以反推基期計，2026 財測調整後 EPS 約 +68%，營收約 +46%"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 1.63，2025 年 1.58"},{"signal":"SBC／營收超過 5% 且逐年上升","lit":false,"evidence":"SBC 占 GAAP 營業利益 6.6%，約占營收 0.6%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"10-K 列出的智慧電網、地下化、燃氣發電與儲能都是新增的工作來源"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數序列"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":null,"evidence":"事實表未涵蓋資本支出拆分"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"正在擴充製造與預製產能，營收連年成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換好、稀釋輕、不回購，錢主要拿去併購與自建製造。併購報酬管理層不給，事實表也算不出來，這是本題最大的空白。","reasoning":"Q3 單季 FCF 12.0 億美元，創季度紀錄。2026 FCF 財測 25–30 億美元，中點約為調整後 EBITDA 的 62%；CFO 說長期仍以 55–60% 看待。年度 FCF 對淨利：2024 年 1.63 倍，2025 年 1.58 倍。SBC 占 GAAP 營業利益 6.6%，換算約占營收 0.6%。稀釋股數由 2022 年約 1.479 億股增到 2025 年約 1.512 億股，年增約 0.7%。現金去向：2022–2025 年併購約 60 億美元（投資人日 CFO），超過同期 FCF 合計的 49.4 億美元；2026 年前九個月又完成 5 件。股息殖利率只有 0.07%，事實表沒有回購資料。資產負債表：8 月發行 20 億美元公司債，9 月提前還清定期貸款，循環信用額度擴大到 29.8 億美元並延到 2031 年。銀行口徑槓桿約 1.3 倍，淨負債 52.0 億美元。債務到期結構與利率事實表未涵蓋。","fact_refs":["f_kpi4_fcf","f_kpi5_sbc_gaap","f_kpi6_2026","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"併購標的的年化 EBITDA 與收購倍數，CFO 在 2026-07-30 法說拒答。事實表未涵蓋投入資本，算不出已實現的增量報酬。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表沒有回購金額。股息殖利率 0.07%，股數三年小增，回購不是主要的資本去向。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數由 2022 年約 1.479 億（淨利 4.912 億 ÷ EPS 3.32）增到 2025 年約 1.512 億（10.284 億 ÷ 6.80），年增約 0.7%，低於 1.5%。"}]},"governance":{"capital_returns":[{"item":"2022–2025 年併購","value":"約 60 億美元（投資人日 CFO），超過同期 FCF 合計約 49.4 億美元"},{"item":"2026 年前九個月併購","value":"5 件；Q2 之後的 2 件約 2.45 億美元（Q3 CFO）"},{"item":"自建製造","value":"未來數年投入 5–7 億美元於變壓器、斷路器與電桿等產能"},{"item":"股息","value":"殖利率 0.07%"},{"item":"債務","value":"8 月發行 20 億美元公司債，9 月提前還清定期貸款；銀行口徑槓桿約 1.3 倍，流動性 52 億美元"}]}}},"q5_valuation":{"verdict":"現價要成立，得五年 EPS 年增約 20%（全疊加情境），而且 2031 年市場還願意給 23 倍，才換得 10% 的年報酬。我相信的是 14% 左右，對應年化約 4.5%，所以不付現價。","reasoning":"現價 625.48 美元，是 FY2026 共識 EPS 17.44 美元的 35.9 倍、FY2027 20.52 美元的 30.5 倍、FY2028 23.94 美元的 26.1 倍。若 2031 年終端給 23 倍，又要拿到 10% 年報酬，FY2031 EPS 得到約 43.8 美元（625.48 × 1.61 ÷ 23），等於五年年增約 20%，也就是全疊加情境。我的基準是年增 14% 左右，到 33.8 美元，對應 777 美元，年化約 4.5%。賣方目標價（約 2026-08 的資料）平均 692–762 美元，中位 790 美元，區間 410–976 美元，高低差 2.4 倍，接近分歧過大的界線，不拿來當支撐。同業前瞻倍數事實表未涵蓋，終端倍數沒有同業現值可對照，改用自身成長換檔推算：成長 15% 給 27 倍、10% 給 21 倍、5% 給 15 倍。調整後與 GAAP 差距大：2026 財測 GAAP EPS 12.57–12.97 美元，以 GAAP 計前瞻本益比約 49 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_kpi6_2026"],"verdict_values":{"valuation":{"basis":"以前瞻一年調整後 EPS 本益比為主，EV/S 作對照","tier":"電力與公用事業基建承包商，對照 MTZ、DY；EME、FIX 是建物機電，不同層級，不拿來當錨","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比或 EV/S，無法做倍數對照；終端倍數改用自身成長換檔推算"},"fwd_pe":35.86,"peg":2.09,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 35.9 倍（FY2026 共識 17.44 美元），FY2027 30.5 倍，FY2028 26.1 倍。P/S 2.53 倍、EV/S 2.67 倍，都是 4 個年度端點中最高的（只有 4 點，不是五年分位）。前瞻 PEG 約 2.1（35.9 ÷ FY2026→FY2028 共識年增 17.2%）。若用反推的 2025 年基期 10.75 美元算，三年年增 30.6%，PEG 約 1.2；但 2026 年只剩兩個月，那段加速已經實現，不拿來撐估值。基準五年年化約 4.5%，低於 8%。價格偏貴，但有 17% 的獲利成長撐著，不到泡沫，結論是偏貴。短期（12 個月）：FY2027 基準 EPS 20.8 美元 × 30 倍＝約 624 美元，約 0%。中期（3 年）：FY2029 基準 27.4 美元 × 26 倍＝約 712 美元，約 +14%。","upside_short_pct":0,"upside_mid_pct":14,"denominator_disputed":false,"denominator_note":"調整後與 GAAP 差距大：2026 財測 GAAP EPS 12.57–12.97 美元，調整後 17.90–18.30 美元，約差 29%，以 GAAP 計前瞻本益比約 49 倍。調整項目明細事實表未涵蓋。本次不主張便宜，所以這不構成爭點；但若併購持續，這個差距值得每季追。"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩個方向。一是資料中心與大型負載同時延後，35.9 倍的倍數先崩，路徑最深約 −57%，這邊我給 30% 機率。二是我低估了 765kV 與發電 EPC 疊上來的速度，錯過一段漲幅，這邊給 25%。","reasoning":"成長熄火壓力測試：以共識 FY2027 20.52 美元、FY2028 23.94 美元為底，2029 年起成長率換檔，倍數同步調整。維持 15%、給 27 倍，約 743 美元（+19%）；降到 10%、給 21 倍，約 553 美元（−12%）；降到 5%、給 15 倍，約 377 美元（−40%）。三種情況只有一種站得住現價。管理層迴避的問題有三個：投資人日被問到 48E 稅負抵減的曝險，只說是風險、沒給數字；2026-07-30 法說不給收購標的的年化 EBITDA 與倍數；Q3 法說被問到 >3 億美元固定價格合約是否仍低於營收 15%，沒有確認數字。近 26 週報酬 −17.4%，RSI 50，不算過熱。同一段時間 FY2026 共識 EPS 上修 24.4%、股價卻下跌，代表市場在降倍數，而不是質疑獲利，倍數還有往下的空間。週線方面，股價在 52 週均線之上，但 250 週均線斜率只有 +2.7%，長期趨勢走平。EV/S 與 P/S 貼著 4 個年度端點的最高點，循環位置雖在中段，倍數不支持現在新建部位。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ev_s_percentile","f_ps_percentile","f_ma_w52","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率帶動 EPS 成長超前，不是價值陷阱，但後段會收斂回營收成長"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":17.44,"pe":35.86,"basis":"FY2026E 共識調整後 EPS（Koyfin 2026-10-31），前瞻一年口徑；終端倍數同樣套在終端年當年的調整後 EPS"},"eps":{"bull":[22.0,26.5,31.5,37.0,43.0],"base":[20.8,24.0,27.4,30.7,33.8],"bear":[18.0,17.0,17.5,18.8,20.0]},"pe":{"bull":30,"base":23,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.07,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-40,"basis":"Bear 情境把倍數從 35.9 倍壓到 16 倍，EPS 在 2028 年回落到 17 美元：16 × 17＝272 美元（−57%），是路徑最深點。較溫和的版本是成長熄火到 10%、倍數 21 倍、EPS 約 19 美元，約 400 美元（−36%）。2009 年金融海嘯時營收 −12.2%，毛利率反而上升，表示回撤主要來自倍數而非虧損，所以下緣取 −60%，不再更深。近 26 週已經跌了 17.4%。","trigger_time":null},"basis":{"bull":"765kV 與發電 EPC 從 2027 上半年起入帳，資料中心每 MW 擷取升到 7–10 百萬美元，地下部門利潤率進雙位數：EPS 年增 16–21%，2031 年市場仍給 30 倍（成長約 16% 的溢價）。","base":"2027 年照管理層說的強勁雙位數（約 +15%），之後隨基期變大降到 10–14%，調整後 EBITDA 利潤率守在 10.5–11%。2031 年成長約 10%，給 23 倍（成長 10% 換檔情境的 21 倍，再加跑道溢價）。","bear":"2027–2028 年資料中心與大型負載專案延後，出現固定價格專案虧損，設備交期又拖慢訂單轉營收：EPS 2028 年回落到 17 美元，2031 年才回到 20 美元；倍數 16 倍（成長 5–10% 的換檔區間）。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 法說 ROTH 提問：渠道調查顯示部分資料中心工作延後，甚至停工。ECMWeb 預期 2027 年北美建築偏謹慎，2028 年才回升。分析文章指出勞動力、許可與供應鏈是執行瓶頸。10-K 也提醒大客戶可能因資金成本而縮減發包。投資人日時，資料中心與大型負載只占在手訂單約 10%，但 2026 年營收增量有相當部分來自這塊。","assumption":"大型負載與公用事業的資本計畫在 2027–2028 年照規劃執行，費率案照常核准。","consequence":"五年後虧 50% 最可能的劇本：2027 年科技客戶延後，又碰上一兩個固定價格專案虧損，2027 財測成長低於 10%。倍數由 35.9 倍降到 16 倍，EPS 2028 年回落到 17 美元，股價約 270–340 美元。","ruling":"部分採納。在手訂單 Q3 季增 100 億美元，12 個月以外的部分也在增，目前沒有否證；但這個劇本成立的機率不低，Bear 機率給 30%。它與唯一致命點部分重疊：2027 財測是這個劇本最早露出跡象的時點。","watch":"總在手訂單連 2 季季減；2027 財測調整後 EPS 中點成長低於 10%；CEO 口徑中的科技業務占比回落。","evidence_refs":["supply_demand_durability#3","end_markets#4","customer_concentration_credit#2"],"fact_refs":["f_kpi7_backlog","f_fwd_pe_latest"]},{"view":"論點成功但股東經濟變差","evidence":"管理層 2030 年 15–20% 的 EPS 年複合含資本配置。2022–2025 年併購約 60 億美元，超過同期 FCF 合計 49.4 億美元，CFO 也不給收購標的的年化 EBITDA 與倍數。自建變壓器、斷路器、電桿製造讓業務變重。10-K 還提到，反壟斷審查加嚴會拉高併購的成本與時程。","assumption":"成長能繼續用同樣的報酬率，靠投入資本買到。","consequence":"EPS 照共識走，但每一塊新增資本的報酬下降：FCF 轉換跌回 55% 以下，投入資本報酬停在 12% 以下，市場不再給成長股的倍數。","ruling":"目前未證實。2026 年 FCF 轉換約 62%，稀釋每年約 0.7%；製造投資 5–7 億美元，相對 2026 FCF 財測 25–30 億美元不算大。但併購報酬完全無法驗證，列入監測，不扣分。","watch":"年度 FCF ÷ 調整後 EBITDA 低於 55%；單筆併購超過市值 5%（約 47 億美元）；2030 年投入資本報酬目標下修。","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi4_fcf","f_kpi6_2026"]},{"view":"價格已反映太多","evidence":"前瞻本益比 35.9 倍，FY2027 30.5 倍。P/S 2.53 倍與 EV/S 2.67 倍都在 4 個年度端點的最高。FY2026→FY2028 共識 EPS 年增 17.2%，前瞻 PEG 約 2.1。","assumption":"市場到 2030 年後仍給 30 倍上下。","consequence":"就算 EPS 照基準走到 2031 年 33.8 美元，倍數回到 23 倍，五年年化也只有約 4.5%；要拿到 10%，EPS 得年增約 20%。","ruling":"採納。這是本次不追的主因，價格是唯一的約束。","watch":"價格 ≤535 美元，或 2027 財測調整後 EPS 中點 ≥22 美元。","fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 657.98 → 本次 625.48（-4.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=657.98","side_b":"本次 price_at_dd=625.48","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 657.98 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 657.98 美元：Bull 價 1,168、Bear 價 324，五年期望值 +19.9%，基準年化 5.6%，不對稱比 1.36","side_b":"本次情境、股價仍用 657.98 美元：Bull 價 1,290、Bear 價 320，五年期望值 +16.8%，基準年化 3.4%，不對稱比 1.56","ruling":"先換情境、股價不動：五年期望值少 3.1 個百分點，基準年化少 2.2 個百分點。不對稱比由 1.36 變為 1.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 657.98 美元：五年期望值 +16.8%，基準年化 3.4%，不對稱比 1.56","side_b":"本次情境、股價 625.48 美元：五年期望值 +22.8%，基準年化 4.4%，不對稱比 1.81","ruling":"再換股價、情境不動：起點價下跌 4.9%，五年期望值多 6.1 個百分點，基準年化多 1.1 個百分點，不對稱比由 1.56 升到 1.81。合計五年期望值比前份多 2.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：生意變強，價格仍貴","cause":null,"prior_field":null,"side_a":"管理層、在手訂單與共識三方一致：Q3 營收年增 57%，在手訂單 637 億美元，FY2026 共識 EPS 近 3 個月上修 24.4%。","side_b":"三種估值指標一致偏貴：前瞻本益比 35.9 倍，P/S 與 EV/S 都在 4 個年度端點最高。","ruling":"兩者不衝突：好生意，價格已經先反映。結論是等價格，不是質疑生意。","evidence_level":"事實表數字","settle_metric":"FY2027 共識前瞻本益比","if_then":["若 FY2027 前瞻本益比 ≤26 倍：重跑研究，通過才建首倉"]},{"axis":"資料中心需求：管理層說詢案史上最快，渠道調查說部分工程延後","cause":null,"prior_field":null,"side_a":"CEO（Q3 法說）：詢案速度是職業生涯最快，客戶要的方案延伸到 2030 年後；在手訂單季增 100 億美元，12 個月以外的部分也在增。","side_b":"ROTH（Q3 法說提問）：渠道調查顯示部分資料中心工作延後甚至停工；ECMWeb 預期 2027 年北美建築偏謹慎。","ruling":"方向相反、不可調和，暫時採 A 側。硬數據站在管理層這邊（在手訂單 637 億美元，FY2026 共識 3 個月上修 24.4%），B 側是沒有量化的渠道說法。但 CEO 自己也承認訓練型資料中心可能放緩，所以 B 側不歸零，Bear 機率給 30%。現在就買的最強論證：公司 2026 財測中點 18.10 美元已高於共識 17.44 美元，管理層承諾 2027 強勁雙位數；若 2027 年 EPS 到 22 美元、市場給 30 倍，就是 660 美元，再加上 765kV 入帳，而且股價已跌 17%，消化了部分恐慌。反駁：即使如此，基準五年年化只有約 4.5%，現價沒有替看錯留下空間。","evidence_level":"A 側是公司財報數字；B 側是賣方渠道調查的口述，未量化","settle_metric":"2027 年 2 月 Q4 財報的總在手訂單與 2027 調整後 EPS 財測","if_then":["若 Q4 在手訂單 ≥650 億美元且 2027 財測中點 ≥22 美元：符合重新觸發條件，重跑研究，通過以 2% 首倉進場","若在手訂單季減且 2027 財測中點低於 20 美元：渠道調查成立，不碰，反彈也不追","價格先走、證據未到：價格續漲但 Q4 數據還沒出，不追；價格跌破 535 美元但在手訂單仍季增，分批反買，不當作停損訊號"],"evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"axis":"大宗商品風險：投資人日說不承擔，10-K 與 Q3 法說顯示要承擔","cause":null,"prior_field":null,"side_a":"CEO（2026-03-31 投資人日）：『We don't take commodity risk.』","side_b":"10-K：EPC 與固定價格合約下由公司採購銅、鋼、鋁、變壓器，價格與可得性受關稅影響。CEO（Q3 法說）說擔心銅價，要用資產負債表替客戶承擔供應鏈風險。","ruling":"程度差異，可以調和。多數合約有價格轉嫁或議價機制，公司承擔的主要是交期與可得性，不是全面的價格風險。但承擔範圍在變大，而且 Q3 被問到 >3 億美元固定價格合約的占比時，沒有確認低於 15%。裁定為部分曝險，列入固定價格專案虧損的監測。","evidence_level":"雙方都是公司揭露原文","settle_metric":"單季專案損失認列金額；TTM GAAP 營業利益率","if_then":["若單季認列專案損失超過 1 億美元，或 TTM GAAP 營業利益率跌回 6% 以下：持有時減碼一半，未持有則不建"],"evidence_refs":["reg_tariff_export#1","end_markets#4"]},{"axis":"利潤率目標：投資人日 2030 目標 10–11%，2026 年已達 10.7%","cause":null,"prior_field":null,"side_a":"投資人日 CFO：2030 年調整後 EBITDA 利潤率 10–11%。","side_b":"Q3 單季調整後 EBITDA 利潤率 12.1%，2026 全年財測中點 10.7%，四年目標第一年就達到。CEO 同時說公用事業段刻意不超過 10–12%，這不是利潤率的故事。","ruling":"可以調和。目標偏保守（投資人日 CEO 自稱財測審慎，規劃以約 80% 的效率計），但上限是管理層主動設的。基準情境只給 10.5–11%，利潤率再擴張只放在 Bull 情境。","evidence_level":"公司法說與財報","settle_metric":"2027 財測隱含的調整後 EBITDA 利潤率","if_then":["若 2027 財測隱含利潤率 ≥11.5%：上調 Base EPS 路徑後重算報酬，不直接加碼"]},{"axis":"2030 EPS 目標與共識：共識已提前進入目標區間","cause":null,"prior_field":null,"side_a":"投資人日 2030 調整後 EPS 目標 21.60–26.75 美元。","side_b":"共識 FY2028 EPS 23.94 美元已在區間內；CEO（Q3）說進度超前計畫，可能不到 5 年就得改口。","ruling":"可以調和。目標會提前重設，這個條件的資訊量變低，所以把重新觸發條件裡的『2030 目標重設到 ≥29 美元』，改成時間較近、有確定日期的 2027 財測。","evidence_level":"投資人日與 Q3 法說原文；事實表共識","settle_metric":"2027 年 2 月公布的 2027 財測；任何新的長期目標","if_then":["若管理層 2027 年公布新的 2030 目標、中點 ≥30 美元，並經一季驗證：上調 Base 路徑後重算"]},{"axis":"前份漂移：估值結論、裁決與角色","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-31）：價格 657.98 美元，FY2027 前瞻本益比 32.9 倍，估值偏貴，裁決觀望。","side_b":"本次：價格 625.48 美元（−4.9%），對應 FY2027 共識 20.52 美元為 30.5 倍，仍偏貴；裁決與角色依本輪輸入重算。","ruling":"估值結論不變。股價小跌加上共識上修，FY2027 倍數降了 2.4 倍；但前瞻一年仍有 35.9 倍，P/S 與 EV/S 貼著 4 年端點最高，五年基準年化約 4.5%，仍低於 8%。我的判斷是不追，等價格。","evidence_level":"事實表價格與共識","settle_metric":"FY2027 共識前瞻本益比","if_then":["若 FY2027 前瞻本益比 ≤26 倍（約 535 美元）：重跑研究"]},{"axis":"前份漂移：護城河方向、跑道、訊號、分類、循環位置","cause":"新證據","prior_field":["moat_trend","runway_post_y5","signal","archetype","cycle_position"],"side_a":"前份：護城河方向向上、跑道寬、訊號等級 B、分類為循環/商品、循環位置中段。","side_b":"本次全部維持。Q3 在手訂單年增約 63%、季增 100 億美元，營業利益率續升，765kV 尚未入帳；員工仍在增加，CEO 說離滿載還遠，循環位置維持中段。","ruling":"新證據都在強化原判斷，沒有改變任何一欄。循環位置沒有往後段移：訂單領先、客戶信用強、量增領先價格。但客戶資本支出已在高檔，所以也不判早循環。","evidence_level":"公司 Q3 財報與法說","settle_metric":"在手訂單年增率、員工增減"},{"axis":"前份漂移：價值陷阱判斷、情境機率與最大回撤","cause":"方法變動","prior_field":["trap","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：陷阱風險低；Bull 25%、Bear 28%；最大回撤單點 −60%。","side_b":"本次：陷阱風險中（十類衰退信號亮一個）；Bull 25%、Base 45%、Bear 30%；最大回撤改為區間 −60%～−40%。","ruling":"這次逐項檢查十類衰退信號，其中『EPS 成長明顯快過營收』亮燈（2022–2025 年 27% 對 18.6%），陷阱風險由低改為中。共識成長超過約 15% 的內生上限，所以 Bear 機率拉到 30%。最大回撤改填區間。這些都是方法調整，不是新的壞消息。","evidence_level":"事實表財務歷史與共識","settle_metric":"EPS 與營收成長差距是否收斂"},{"axis":"重新觸發條件變動（首倉前提）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"FY+2 遠期本益比回落至 26x（約 $520）；或管理層正式將 2030 adj EPS 目標重設至 ≥$29 並經一季驗證","side_b":"價格 ≤535 美元（FY2027 共識 EPS 20.52 美元的 26 倍）；或 2027 財測調整後 EPS 中點 ≥22 美元且在手訂單 ≥650 億美元","ruling":"倍數門檻 26 倍不變；FY2027 共識由約 20.0 升到 20.52 美元，對應價位由 520 升到約 535 美元。第二個條件改為 2027 財測：FY2028 共識已落在 2030 目標區間，目標重設的資訊量變低，而 2027 年 2 月有確定的公布日期。觸發後重跑研究，通過才建首倉，不直接買進。","evidence_level":"事實表共識 EPS；投資人日與 Q3 法說","settle_metric":"股價；2027 財測"},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（空白）","side_b":"2027 年 2 月 Q4 財報給出的 2027 全年調整後 EPS 財測，中點較 2026 年實際成長低於 10%","ruling":"前份沒有設定，本次依格式補上。選的是數學上最大的單一敏感度：現價倍數綁在 15–20% 的複利上，財測一旦跌破 10%，倍數與 EPS 會同時被壓。發生時不碰；若已持有則清倉。","evidence_level":"事實表估值與 Q3 法說","settle_metric":"2027 財測調整後 EPS 中點"},{"axis":"淘汰指標新增","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定淘汰指標（空白）","side_b":"總在手訂單連 2 季季減或年增低於 10%；TTM GAAP 毛利率低於 14.0%；FCF ÷ 調整後 EBITDA 低於 50%；2027 財測 EPS 中點年增低於 10%","ruling":"前份沒有設定，本次補上四條。持有時任一條觸發就減碼一半，兩條同時觸發則清倉。","evidence_level":"事實表財務歷史與公司財測","settle_metric":"四條指標每季讀數"}],"triggers":[{"n":1,"text":"價格回到 FY2027 共識 EPS 的 26 倍以下，五年基準年化報酬升到 8% 以上","type":"估值rearm","maps_to":"rearm_trigger","metric":"股價 ÷ FY2027 共識調整後 EPS","threshold":"≤26 倍（約 ≤535 美元）","action":"重跑研究，通過才以 2% 首倉分兩批進場","source_freq":"股價每日；共識每月","date":null},{"n":2,"text":"2027 全年調整後 EPS 財測中點成長低於 10%","type":"Single Thing","maps_to":"single_thing","metric":"2027 財測調整後 EPS 中點 ÷ 2026 實際 −1","threshold":"低於 10%","action":"不碰；若已持有則清倉","source_freq":"年度財測（Q4 財報）","date":"2027-02"},{"n":3,"text":"大型輸電入帳、在手訂單續增，驗證成長能疊加","type":"假設驗證","maps_to":"H1","metric":"季末總在手訂單；765kV 計畫是否入帳","threshold":"Q4 在手訂單 ≥650 億美元；2027-06-30 前至少一個 765kV 計畫入帳","action":"達標則維持成長假設；若同時 2027 財測 ≥22 美元，重跑研究","source_freq":"每季 8-K 新聞稿","date":"2027-02"},{"n":4,"text":"固定價格與 EPC 專案虧損","type":"風險","maps_to":"R1","metric":"單季專案損失認列；TTM GAAP 營業利益率","threshold":"超過 1 億美元；或低於 6.0%","action":"持有時減碼一半；未持有則延後一季再重跑研究","source_freq":"每季 10-Q","date":null,"evidence_refs":["reg_tariff_export#1","end_markets#4"]},{"n":5,"text":"設備與材料瓶頸拖慢訂單轉營收","type":"風險","maps_to":"R4","metric":"營收年增率與在手訂單年增率","threshold":"營收年增低於 15% 而在手訂單年增超過 30%，連 2 季","action":"下修 Base 路徑前兩年 EPS 後重算；持有時停止加碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","cyclical_inventory_price_position#2","reg_tariff_export#0"]},{"n":6,"text":"小型案競爭與客戶自建侵蝕毛利","type":"風險","maps_to":"R2","metric":"TTM GAAP 毛利率","threshold":"低於 14.0%，連 2 季","action":"持有時減碼一半，護城河方向改判持平","source_freq":"每季","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#1"]},{"n":7,"text":"資料中心與大型負載發包放緩","type":"風險","maps_to":"R3","metric":"總在手訂單季變動","threshold":"連 2 季季減","action":"持有時減碼一半；未持有則維持不碰，價格再低也等訂單止跌","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"n":8,"text":"野火責任求償","type":"風險","maps_to":"R5","metric":"揭露的野火相關求償或提列","threshold":"單一事件超過 2 億美元，或被列為重大野火集體訴訟被告","action":"持有時減碼一半，等釐清訴訟性質是個案還是集體","source_freq":"10-Q、10-K、8-K","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":9,"text":"Q4 財報與 2027 財測公布後複審","type":"複審日期","maps_to":"H3","metric":"全部假設與觸發條件","threshold":"財報公布即複審","action":"重跑完整研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"季末總在手訂單","bear_threshold":"連 2 季季減，或年增低於 10%","window":"每季，2027 全年","source":"公司季度 8-K 新聞稿","last_status":"ok"},{"metric":"TTM GAAP 毛利率","bear_threshold":"低於 14.0%（2022–2025 年下緣 14.07%），連 2 季","window":"每季","source":"10-Q 與季報","last_status":"ok"},{"metric":"年度 FCF ÷ 調整後 EBITDA","bear_threshold":"低於 50%（管理層口徑 55–60%）","window":"FY2027","source":"年度財報、CFO 法說","last_status":"ok"},{"metric":"2027 財測調整後 EPS 中點年增","bear_threshold":"低於 10%（相對 FY2026 實際）","window":"2027-02 Q4 財報","source":"Q4 2026 8-K 新聞稿","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"價格 ≤535 美元（FY2027 共識 EPS 20.52 美元的 26 倍）；或 2027 財測調整後 EPS 中點 ≥22 美元且在手訂單 ≥650 億美元","exec_line":"現在不買。重新觸發後重跑研究，通過才以個股部位 2% 首倉、分兩批進場，第二批等 765kV 計畫入帳。建倉前若任一淘汰指標觸發，延後一季再看。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"價格 ≤535 美元（FY2027 共識 EPS 的 26 倍），或 2027 年 2 月財測調整後 EPS 中點 ≥22 美元且在手訂單 ≥650 億美元","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"qc48_result":"pass","qc48_note":"Bull 情境有量乘價的方向，也有具名的管理層說法支撐跑道，但分部營收、MW 量與 765kV 金額都沒有推到數字，同業高估值進場後 5 年報酬的案例也不足，所以 Bull 依據只能算部分成立，不算已經驗證。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-17.38, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 情境有量乘價的方向，也有具名的管理層說法支撐跑道，但分部營收、MW 量與 765kV 金額都沒有推到數字，同業高估值進場後 5 年報酬的案例也不足，所以 Bull 依據只能算部分成立，不算已經驗證。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='價格 ≤535 美元（FY2027 共識 EPS 的 26 倍），或 2027 年 2 月財測調整後 EPS 中點 ≥22 美元且在手訂單 ≥650 億美元'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"電網、發電與大型負載的資本計畫持續轉成 Quanta 已簽約的在手訂單，765kV 大型輸電與發電 EPC 從 2027 年起疊加到公用事業底盤上","2y":null,"5y":"2031 年前總在手訂單維持年增 10% 以上；2027-06-30 前至少一個 765kV 計畫入帳（Q3 法說 CEO：德州、俄亥俄州先行）","10y":null,"threshold":"季末總在手訂單 ≥550 億美元且年增 ≥10%；2027 上半年有 765kV 計畫入帳","source":"公司季度 8-K 新聞稿與 10-Q 的在手訂單、剩餘履約義務；每季法說","drift_rule":"在手訂單年增連 4 季低於 10% 為削弱；連 2 季季減，或連 6 季年增 ≤0%，為反轉"},{"id":"H2","text":"自營工班規模與跨工種調度把成長轉成利潤率與現金：調整後 EBITDA 利潤率守在 10.5% 以上，FCF 轉換 55% 以上","2y":null,"5y":"FY2027–FY2030 每年調整後 EBITDA 利潤率 ≥10.5%（2026 財測中點 10.7%，投資人日 2030 目標 10–11%），FCF ÷ 調整後 EBITDA ≥55%","10y":null,"threshold":"年度調整後 EBITDA 利潤率 ≥10.5%；FCF 轉換 ≥55%；TTM GAAP 毛利率 ≥14.0%","source":"年度與季度財報、CFO 法說","drift_rule":"TTM 調整後 EBITDA 利潤率連 4 季低於 10.0%（偏離門檻 5% 以上）為削弱；連 6 季低於 9.5% 為反轉"},{"id":"H3","text":"2027 年 EPS 照管理層說的強勁雙位數兌現，而且不靠大型併購補洞","2y":"FY2027 調整後 EPS ≥20.5 美元（共識 20.52），較 FY2026 實際年增 13% 以上","5y":null,"10y":null,"threshold":"2027 財測中點 ≥20.5 美元；FY2027 實際 ≥20.5 美元","source":"2027 年 2 月 Q4 財報與全年財測；之後每季更新","drift_rule":"TTM 調整後 EPS 連 2 季落後共識路徑 5% 以上為削弱；連 3 季落後 10% 以上為反轉"}],"R":[{"id":"R1","text":"固定價格與 EPC 專案虧損：業務組合往發電 EPC、機電與大型輸電移動，由公司自行採購銅、鋼、鋁與變壓器的部分變大。Q3 法說被問到 >3 億美元固定價格合約是否仍低於營收 15% 時，CEO 沒有確認數字，只說風險狀況比以往好","h_ref":"H2","clock":"🔥","threshold":"單季認列專案損失超過 1 億美元，或 TTM GAAP 營業利益率跌回 6.0% 以下","evidence_refs":["reg_tariff_export#1","end_markets#4"]},{"id":"R2","text":"小型案競爭與客戶自建：10-K 自述部分業務進入門檻低，小型案已見更競爭的定價；公用事業客戶有內部施工團隊，框架合約也沒有最低工作量","h_ref":"H2","clock":"🐢","threshold":"TTM GAAP 毛利率連 2 季低於 14.0%，或前十大客戶公開擴大自營施工","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#1"]},{"id":"R3","text":"大型負載與資料中心資本支出放緩：渠道調查已見部分工程延後，2027 年北美建築展望偏謹慎；大客戶資金成本上升，會直接減少發包","h_ref":"H1","clock":"🔥","threshold":"總在手訂單連 2 季季減，或 2027 財測調整後 EPS 中點成長低於 10%","evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"id":"R4","text":"設備與材料瓶頸拖慢在手訂單轉成營收：變壓器、開關櫃交期 60–100 週，2026 年電氣設備漲價 5–8%，關稅又墊高客戶的專案成本。CEO 自己也說成長取決於 OEM","h_ref":"H1","clock":"🔥","threshold":"營收年增低於 15% 而在手訂單年增超過 30%，連 2 季","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","cyclical_inventory_price_position#2","reg_tariff_export#0"]},{"id":"R5","text":"野火責任：營運子公司曾在野火事件調查中收到辯護通知、文件保全要求與傳票，10-K 說未來可能有更多求償","h_ref":"H2","clock":"🐢","threshold":"單一野火事件揭露的求償或提列超過 2 億美元，或被列為重大野火集體訴訟被告","evidence_refs":["regulatory_antitrust#2"]}],"single_thing":{"description":"2027 年 2 月 Q4 財報給出的 2027 全年調整後 EPS 財測，中點較 2026 年實際成長低於 10%","why_fatal":"現價是 FY2026 共識的 35.9 倍、FY2027 的 30.5 倍，倍數綁在 15–20% 的複利上。財測一旦低於 10%，倍數會先換到成長 10% 那一檔的 21 倍上下，EPS 路徑同時下移，股價約 −30%～−40%（21 倍 × 約 19.9 美元＝約 418 美元）。情境樹裡倍數是最大的單一敏感度，這個事件是它最直接的開關。","if_happens":"不碰；若屆時已持有則清倉，等在手訂單止跌後才重跑研究","how_monitor":"看 2027 年 2 月的 Q4 財報與法說；在那之前，看 Q4 在手訂單，以及 CEO 對 2027 的措辭（Q3 法說說的是強勁雙位數）","probability":"12–24 個月內約 15%。CEO 已公開說 2027 會強勁雙位數成長，在手訂單 637 億美元，要跌破 10% 得多個大客戶同時延後"}},"appendix_a":{"growth_durability":8,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":30.5,"peg_fy2":1.8,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":10.75,"FY2026E":17.44,"FY2027E":20.52,"FY2028E":23.94},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（Koyfin 共識）。FY2025A 的 10.75 美元事實表沒有直接收錄，是由 2026-03-31 投資人日 CFO 的 2030 目標 21.60–26.75 美元與 15–20% 年複合反推而得（21.60 ÷ 1.15^5 ≈ 10.74，26.75 ÷ 1.20^5 ≈ 10.75）。同年 GAAP 稀釋 EPS 為 6.80 美元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年財測","impact":"高","watch":"調整後 EPS 財測中點是否 ≥20.5 美元（共識），或 ≥22 美元（重新觸發）；在手訂單是否 ≥650 億美元"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"Q1 2027 財報，看季節性人力下滑後的利潤率","impact":"中","watch":"地下部門利潤率是否往雙位數走；FCF 轉換"},{"date":"2027-06","date_precision":"quarter","type":"other","event":"德州、俄亥俄州 765kV 大型輸電計畫入帳（CEO 預期 2027 上半年）","impact":"高","watch":"新聞稿是否點名大型輸電入帳與金額"},{"date":null,"date_precision":null,"type":"regulatory","event":"48E 稅負抵減與外國關注實體指引落地（影響再生能源業務）","impact":"中","watch":"再生能源訂單與營收是否轉弱"}]}
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
