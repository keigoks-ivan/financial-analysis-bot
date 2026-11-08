你是 DD 管線 v20 的判斷層閘（gate），標的 FN（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（38 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1474.5 百萬美元｜期間與口徑：Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：FN Q1 FY27 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-25，公告於 2026-11-02））
  - 註記：新聞稿稱超出公司指引區間；共識數字未查證
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝158.5 百萬美元（利益率 10.8%）｜期間與口徑：Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：FN Q1 FY27 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-25，公告於 2026-11-02））
  - 註記：未查證
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝146.0 百萬美元（利益率 9.9%）｜期間與口徑：Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：FN Q1 FY27 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-25，公告於 2026-11-02））
  - 註記：未查證
- `f_kpi5_q2_fy2027_2026_12_25`（q1_business）｜下一季指引（Q2 FY2027，季末 2026-12-25）＝營收 1,600–1,650 百萬美元；GAAP EPS 3.81–3.96；non-GAAP EPS 4.77–4.92（約 36.2 百萬稀釋股） 區間｜期間與口徑：Q1 FY2027（公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：FN Q1 FY27 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（公告於 2026-11-02））
  - 註記：指引中點營收 1,625，約較 Q1 +10.2% QoQ；共識未查證
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-02 date｜期間與口徑：2026-11-02／距今 5 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-02）
- `f_peer_fn_gross_margin_pct`（q2_moat）｜FN 毛利率＝11.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fn_operating_margin_pct`（q2_moat）｜FN 營業利益率＝10.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fn_fcf_margin_pct`（q2_moat）｜FN FCF 利潤率＝-3.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cls_gross_margin_pct`（q2_moat）｜CLS 毛利率＝11.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cls_operating_margin_pct`（q2_moat）｜CLS 營業利益率＝8.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CLS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_jbl_gross_margin_pct`（q2_moat）｜JBL 毛利率＝9.23 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_jbl_operating_margin_pct`（q2_moat）｜JBL 營業利益率＝5.11 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_lite_gross_margin_pct`（q2_moat）｜LITE 毛利率＝45.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_operating_margin_pct`（q2_moat）｜LITE 營業利益率＝23.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_gross_margin_pct`（q2_moat）｜COHR 毛利率＝38.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_fcf_margin_pct`（q2_moat）｜COHR FCF 利潤率＝-23.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝19.72 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝24.11 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝29.74 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6596.57 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝8072.31 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（7 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_non_gaap_fcf`（q4_capital）｜自由現金流（non-GAAP FCF）＝-137.4 百萬美元｜期間與口徑：Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：FN Q1 FY27 新聞稿（營業現金流 21.3 − 資本支出 158.7）（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-25，公告於 2026-11-02））
  - 註記：n/a
- `f_kpi4_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝7.1 %（SBC 11.2 百萬；占營收 0.76%）｜期間與口徑：Q1 FY2027（季末 2026-09-25，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：FN Q1 FY27 新聞稿（SBC 11,225 千：銷貨成本 4,203＋SG&A 7,022；除以 non-GAAP 營業利益 158.5 自行計算）（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-25，公告於 2026-11-02））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-677.43 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 78.32、現金 755.75（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝11006.84 USD m｜期間與口徑：2026-11-08／市值 11684.27 ＋ 淨負債 -677.43｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝327.13 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.59 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 19.72，分子＝快照價 327.13｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝24.69 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝29.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝29.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.67 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.97 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（19.53 → 19.72）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝42.8 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 13.81 → 19.72（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-47.35 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝42.93｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 327.13 / W52 505.94 / W104 388.86 / W250 249.7 / W250 13週斜率 1.4%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝505.94 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝388.86 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝249.7 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：其他代工、ODM 或封測公司可能進入目標市場，產業整併可能產生更大對手；新競爭可能導致降價、毛利下降或失去份額
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-18）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素揭露：客戶整併在部分情況下已導致需求下降，因客戶取得自製產能（in-house）；未點名最大客戶正在自製或導入第二供應商。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-18）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K MD&A：公司依賴少數客戶，任一大客戶減單或流失會有重大不利影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 7（as_of 2026-08-18）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：公司10-K風險因素揭露：客戶集中增加應收帳款集中與客戶違約風險；許多客戶負債重或財務困難，部分客戶曾倒閉、破產或退出光學市場（為一般性揭露，未點名特定客戶惡化）。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-18）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：FN 財報 Q3 FY2026 call：Datacom 出貨受廣泛零組件短缺限制，儘管需求極強
  - 來源：Motley Fool FN Q3 2026 earnings transcript（as_of 2026-05-04）｜affects：thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2026 10-K Item 3 only discloses a PRC unjust-enrichment suit against Casix (RMB 400 million claimed); PRC Supreme Court accepted retrial on 2026-07-30, no merits determination, liability not quantifiable. No antitrust/DOJ/FTC matter listed.
  - 來源：SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings（as_of 2026-08-18）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 揭露公司與供應商可能受關稅、禁運等貿易限制影響，可能限制材料供應並推高成本，且已經歷較長交期與加急費。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-08-18）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：公司受泰國、中國、以色列、美國出口進口管制；美國對中國的技術出口禁令可能延伸至泰國，限制其製造某些產品。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-18）｜affects：thesis.R、decision_inputs.bear、triggers
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：關稅雖部分調降或延後，但再升級風險仍在；若無法轉嫁成本，毛利率與業績可能受重大不利影響。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-18）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q 稱多數資產與製造營運位於泰國，泰國政治、社會、經濟狀況對業務有重大影響；未來政治不穩可能阻礙出貨、中斷製造
  - 來源：Fabrinet Form 10-Q (SEC)（as_of 2026-09-25）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K 稱預期持續投資中國製造營運，須承擔當地經營風險；出口管制（泰國、中國、以色列、美國）與新增或提高關稅列為風險
  - 來源：Fabrinet Form 10-K FY2026 (SEC)（as_of 2026-06-26）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：早期 10-K（FY2019）稱關鍵材料依賴單一或有限供應商；10-Q 稱為某客戶採購的多數材料通常無法用於其他客戶產品
  - 來源：Fabrinet Form 10-K FY2019 / 10-Q (SEC)（as_of 2019-08-23）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：第三方 Porter 五力分析稱 CPO 等新技術可能改變價值鏈，且大客戶（如 NVIDIA）自行製造為持續風險；非公司一手文件。
  - 來源：dcf-analysis.com｜Fabrinet (FN): 5 FORCES Analysis [Apr-2026 Updated]（as_of 2026-04-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：第三方分析指出，若全電短距連結取代部分 AI 應用的光學，Fabrinet 可服務市場可能縮小；CPO 與 linear-drive pluggable 可能擾動現有組裝製程、需新能力或資本。
  - 來源：statementdog.com 與第三方個股分析（搜尋摘要）（as_of 2026-03-25）｜affects：moat_trend、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：子公司 Casix 的中國不當得利訴訟（求償 RMB 4 億）：2025-11 二審駁回，2026-04 原告上訴最高人民法院，2026-07-30 最高院裁定受理再審；受理不代表實體判斷，公司無法量化潛在負債。
  - 來源：SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings（as_of 2026-08-18）｜affects：decision_inputs.bear、triggers
- `ems_utilization_capex_cycle#1`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：Building 11（Chonburi）預計 Building 10 完工後（1 月）動工，約 150 萬平方呎、增約 $30 億營收產能，預計 FY2028 底前後完工；另有來源稱含潛在 Building 12 總產能目標由 $140 億升至 $160 億。
  - 來源：MarketBeat, Fabrinet Q1 earnings call highlights（as_of 2026-11-02）｜affects：thesis.R、decision_inputs.bear
- `ems_utilization_capex_cycle#2`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：FY2026 營收 +36% 至 $46 億，營運現金流 $2.57 億、自由現金流僅 $400 萬，因持續投入產能；capex 季度升至 $1.69 億（含 $7,700 萬 Santa Clara 第二園區收購），FY2027 計畫提高資本支出。
  - 來源：Nasdaq, Fabrinet Q4 Earnings Call Highlights; MarketBeat Q1 call highlights（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear、valuation
- `ems_roic_asset_turnover_benchmark#2`（ems_roic_asset_turnover_benchmark｜方向 -｜狀態 ok）：FY2026 營運現金流 256.7M（FY2025 為 328.4M）；季度（截至 2026-09-25）營運現金流 21.3M 對去年同期 102.6M，公司歸因於應收帳款增加；現金及短投 875.1M、無負債。第三方 VCP Scanner 列 CCC 約 62–82 天、最新約 65.45（欄位期間未標，未核）。
  - 來源：Fabrinet 10-K FY2026、10-Q 2026-09-25；VCP Scanner（as_of 2026-11-05）｜affects：moat_trend、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：唯一重大訴訟為子公司 Casix 的中國不當得利案（非集體訴訟）；2026-07-30 最高院受理再審，公司無法量化潛在負債。搜尋未見近 12 個月證券集體訴訟（僅 2014 年律所調查公告）。
  - 來源：SEC EDGAR 10-K FY2026 Item 3 Legal Proceedings（as_of 2026-08-18）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":846.0,"bear_5y_price":204.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":55.9,"ev5y_pct":53.5,"irr_base_pct":9.3,"asym_ratio":3.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":19.72,"pe":16.59,"basis":"FY2027E 共識 non-GAAP EPS 19.72（不含 Pillar 2 補足稅），現價 327.13；終端倍數同樣乘第五年 non-GAAP EPS。"},"eps":{"bull":[20.8,27.5,34.5,41.0,47.0],"base":[19.9,24.0,28.0,31.0,34.0],"bear":[19.0,20.5,17.0,15.5,17.0]},"pe":{"bull":18,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FN_Q4_2026_Earnings_Call_20260817.md
- 2026-08-17｜Csaba Sverha｜guidance：FQ1'27營收財測區間（原話："revenue to be between $1.375 billion and $1.425 billion"）
- 2026-08-17｜Csaba Sverha｜guidance：FQ1'27 EPS財測區間（原話："we anticipate EPS to be between $4.10 and $4.25"）
- 2026-08-17｜Csaba Sverha｜guidance：管理層稱只按季給財測，但客戶提供延伸至FY27之後的能見度（原話："we are more confident than ever in our longer-term outlook"）
- 2026-08-17｜Csaba Sverha｜guidance：管理層說明客戶長期預測並非訂單承諾（原話："customer forecasts are not order commitments"）
- 2026-08-17｜Seamus Grady｜guidance：被問FY27成長是否再加速，管理層表示有可能（原話："we could see another year of accelerating growth"）
- 2026-08-17｜Csaba Sverha｜margin：Q4毛利率12.2%（原話："Gross margin in the fourth quarter was 12.2%"）
- 2026-08-17｜Csaba Sverha｜margin：Q4營業利益率10.9%（原話："operating margin of 10.9%, our highest level in three years"）
- 2026-08-17｜Csaba Sverha｜margin：Q1費用季節性造成暫時性利潤率逆風（原話："expense seasonality will create a temporary margin headwind"）
- 2026-08-17｜Csaba Sverha｜margin：成長模式不需大幅增加營業費用（原話："growth model does not require significant incremental"）
- 2026-08-17｜Csaba Sverha｜margin：Raytek重新衡量利得依一致處理方式排除於non-GAAP（原話："We intend to apply the same treatment consistently"）
- 2026-08-17｜Csaba Sverha｜margin：泰國OECD補足稅準備列為non-GAAP排除項（原話："$57.4 million provision related to Thailand's top-up tax"）
- 2026-08-17｜Csaba Sverha｜margin：新營收分類僅為呈現方式變更（原話："This change is purely presentational"）
- 2026-08-17｜Csaba Sverha｜margin：新分類依產品最終部署處歸類（原話："everything else goes into the communication infrastructure"）
- 2026-08-17｜Csaba Sverha｜margin：資料中心Q4營收與成長（原話："Data center revenue was $669 million in the fourth quarter"）
- 2026-08-17｜Csaba Sverha｜margin：DCI年化營收運行率超過10億美元（原話："annualized revenue run rate exceeding $1 billion"）
- 2026-08-17｜Csaba Sverha｜margin：通訊基礎設施Q4營收與年增率（原話："Revenue was $413 million, an increase of 40% from a year ago"）
- 2026-08-17｜Csaba Sverha｜customer：FY26十%以上客戶占比（原話："Cisco at 20%, NVIDIA at 16%, Nokia at 11%"）
- 2026-08-17｜Seamus Grady｜customer：Nokia升為10%以上客戶（原話："Yes, they rose to be more than a 10% customer."）
- 2026-08-17｜Seamus Grady｜customer：資料中心客戶供應：部分零組件需求高於供給（原話："certain components is higher than the available supply"）
- 2026-08-17｜Seamus Grady｜customer：管理層稱已把供應缺口納入財測（原話："taken any potential gaps in supply into account"）
- 2026-08-17｜Seamus Grady｜customer：HPC表現優於預期（原話："continues to perform, I would say, ahead of expectations"）
- 2026-08-17｜Seamus Grady｜customer：系統整合業務盼未來數季新增1至2案（原話："we hope to have 1 or 2 to add in the coming quarters"）
- 2026-08-17｜Seamus Grady｜product：新收發器專案時程：一個merchant專案12月季開始（原話："merchant programs to begin in the December quarter"）
- 2026-08-17｜Seamus Grady｜product：NPO被視為較CPO近期的機會（原話："probably represents a more near-term opportunity than CPO"）
- 2026-08-17｜Seamus Grady｜product：積極參與多條multi-rail專案（原話："heavily engaged with number of customers on these programs"）
- 2026-08-17｜Seamus Grady｜product：OCS目前規模仍小（原話："OCS is quite small today"）
- 2026-08-17｜Seamus Grady｜competition：中國收發器禁令尚未定案，公司不為中國業者製造（原話："We don't manufacture for any Chinese providers"）
- 2026-08-17｜Seamus Grady｜competition：對中國收發器禁令的說法（原話："The proposed ban on new transceivers from China"）
- 2026-08-17｜Csaba Sverha｜risk：存貨增加歸因於成長與為後續ramp備料（原話："the inventory increase has to do with our growth"）
- 2026-08-17｜Csaba Sverha｜risk：Q4資料中心中datacom子類持平（新分類下）（原話："our datacom was somewhat flat"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：Q4自由現金流為流出（原話："Free cash flow was an outflow of $37 million in the quarter"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：回購額度剩餘約1.69億美元（原話："approximately $169 million available at the end of"）
- 2026-08-17｜Csaba Sverha｜capital_allocation：再投資於業務是最具吸引力的現金用途之一（原話："reinvesting in the business remains one of the most"）
- 2026-08-17｜Seamus Grady｜commitment：Building 10預計2027年初完工（原話："we remain on track to complete Building 10 by early 2027"）
- 2026-08-17｜Seamus Grady｜commitment：產能規劃上看125億至140億美元營收（原話："between $12.5 billion and $14 billion over the coming years"）
- 2026-08-17｜Seamus Grady｜commitment：Building 10新增產能30至35億美元（原話："Building 10 will add $3 billion to $3.5 billion of capacity"）
- 2026-08-17｜Seamus Grady｜commitment：未來數年持續積極擴產（原話："continuing to expand aggressively over the next few years"）
- 2026-08-17｜Seamus Grady｜commitment：每平方呎營收提升（原話："We are actually increasing our revenue per square foot."）

### 問答異常語氣（迴避／改口／保留）
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Tim Long問NVIDIA業務年度下滑與競爭格局｜答法：不談單一客戶細節，改談資料中心整體與供應鏈管理，未直接回答競爭格局
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Amol問最大datacom客戶1.6T營收時程｜答法：拒絕更新，請分析師去問NVIDIA
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Karl Ackerman問是否有支撐1.6T ramp的雷射供應承諾｜答法：未給具體答案，只說零組件供應已納入財測
- FN_Q4_2026_Earnings_Call_20260817.md｜問：Yash Shah問datacom單季下滑原因（供應、轉換或需求時序）｜答法：改以新分類下datacom持平回應，未拆解各因素占比

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 3 | 2 |
| customer_concentration_credit | found | 3 | 0 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 5 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 5 |
| ems_utilization_capex_cycle | found | 5 | 3 |
| ems_roic_asset_turnover_benchmark | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","irr_base_pct":8.8,"ev5y_pct":46.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟡","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.8,"ev5y_pct":46.4,"irr_base_pct":8.8,"max_dd_pct":-45,"bull_5y_price":1012.0,"bear_5y_price":227.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","price_at_dd":407.4,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Fabrinet"},"oneliner":"Fabrinet 營收年增 51%，營益率守住 10.8%，股價卻跌掉近一半，預估本益比剩 16.6 倍；但自由現金流轉負、補足稅沒算進 EPS，現價合理，還稱不上便宜。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FN_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是精密光電的量產代工費：客戶掌握設計與品牌，FN 拿製造環節約 12% 毛利，錢主要卡在元件與設計端。","reasoning":"最新一季（季末 2026-09-25）營收 14.745 億美元，年增 51%。依 2026-11-02 法說，三個分部都超過一成：資料中心 7.77 億（占 53%，年增 78%）、通訊基礎設施 4.44 億（年增 35%）、車用工業與其他 2.53 億（年增 20%）。non-GAAP 毛利率 12.1%，營益率 10.8%。產業處於擴張期，依據是連續 14 季成長、零組件全面偏緊，尚未看到砍單或庫存反轉。客戶集中是單點依賴：10-K FY2026 前四大客戶合計 57.4%（Cisco 19.9%、NVIDIA 16.3%、Nokia 10.7%、Amazon 10.5%）。NVIDIA 占比兩年由 35.1% 降到 16.3%，以總營收換算，金額約由 10.1 億美元降到 7.6 億美元。AI 熱潮中金額反而縮小，是本輪最需要解釋的數字，管理層 2026-08-17 法說沒有正面回答。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_q2_fy2027_2026_12_25","f_earnings_recency"],"verdict_values":{"revenue_quality":"收入來自需要驗證的長週期製造案，可見度高但約束力低，財務長 2026-08-17 明說客戶預測不是訂單。","unit_econ_note":"財務長 2026-11-02 稱固定成本約占成本 5%，毛利率缺乏規模槓桿，營益率靠 1.3% 的費用率帶動；每平方呎營收上升，使 Building 11 產能由 21 億上修到 30 億美元。","archetype":{"primary":"EMS/ODM","secondary":"品質複利成長","confidence":"中","fingerprint":"約 12% 毛利、代工收費、客戶集中、需求跟著 AI 資本支出，但資本報酬高於一般代工。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求疊加週期斜率：資料中心光互連需求持久，但付款者是 AI 資本支出，客戶預測不是訂單；FN 新增產能在 2027-01 達約 100 億美元，廠房建成後不可逆。來源為 2026-11-02 與 2026-08-17 法說。","bargaining":{"up":"雷射、記憶體、ASIC 偏緊，上游較強；管理層 2026-11-02 稱拿到公平甚至超額的配額。","down":"前四大客戶占 57.4%，對代工議價強，毛利率四年由 12.71% 降到 11.99%。","geo":"多數資產與製造在泰國，北美以外出貨占 77.3%，並受出口管制外溢影響。"},"profit_pool_dir":"利潤留在元件與設計端，LITE 與 COHR 毛利率 45.91%、38.16%，FN 為 11.95%；未見利潤往代工端移動，五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM、滲透率與利潤池占比，無可引用來源；成長判斷改以客戶、產能與分部數字為依據，屬已知資料缺口。"}}}},"q2_moat":{"verdict":"護城河持平：製程與量產良率的優勢還在，客戶分散抵銷了最大資料中心客戶金額縮小的負面，還不能說擴大。","reasoning":"機制是精密光電的量產知識：10-K 稱許多產品 FN 是客戶唯一的外包製造商，新案重新驗證時間長，管理層也稱已在概念階段參與設計。定價權只到製造費：毛利率 11.95%、營益率 10.04%，高於 CLS 的 11.46%／8.29% 與 JBL 的 9.23%／5.11%，但遠低於 LITE 的 45.91%／23.35%。ROIC 來源不一致：opencapital 23.7%、stockanalysis 30.53%，管理層稱 30% 以上；事實表沒有投入資本，無法自算。CLS 同一來源為 39.5%，期間不同，因此看不到對最強同業的正向差距。增量報酬用營業利益×96%（Q1 FY27 non-GAAP 稅率 4%）估 NOPAT，FY2024 到 FY2026 增加 1.78 億美元，同期再投資以 NOPAT 減 FCF 近似為 5.48 億，增量 ROIC 約 32.5%，再投資率約 72.3%，內生成長上界約 23.5%。Building 10 的資本已投入但營收尚未完全反映，這個數字會受落後效應影響。可能看錯之處：若 Building 10 未滿載，下一段增量 ROIC 會明顯低於此值。","fact_refs":["f_peer_fn_gross_margin_pct","f_peer_fn_operating_margin_pct","f_peer_fn_fcf_margin_pct","f_peer_cls_gross_margin_pct","f_peer_cls_operating_margin_pct","f_peer_jbl_gross_margin_pct","f_peer_jbl_operating_margin_pct","f_peer_lite_gross_margin_pct","f_peer_lite_operating_margin_pct","f_peer_cohr_gross_margin_pct","f_peer_cohr_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"精密光電的量產製程與良率知識，加上新案重新驗證的轉換成本。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：Q1 FY27 營收高於指引，Nokia、Amazon 升為一成以上客戶，多家收發器新客戶爬坡。定價面穩定：毛利率四年略降，營益率回升。反向證據是 NVIDIA 金額兩年約減 25%，管理層 2026-08-17 對此與 1.6T 時程未正面回答，所以不標擴大。","competitor_notes":[{"name":"CLS","strategy_note":"毛利率與 FN 接近，FCF 利潤率 2.99%；同一資料站 ROIC 39.5%，是最強的代工對照，也被 10-K 列為光學製造對手。"},{"name":"JBL","strategy_note":"毛利率 9.23%、營益率 5.11%，被 10-K 列為對手，威脅在爭取新案，現有案轉移的證據事實表未涵蓋。"},{"name":"LITE","strategy_note":"既是長期客戶也是上游，毛利率 45.91%；2026-11-02 傳出與 Marvell 的併購後，委外比例可能改變，需要觀察。"},{"name":"COHR","strategy_note":"毛利率 38.16%、FCF 利潤率 −23.28%，上游同樣大舉投資，顯示擴產不只 FN 一家；與 FN 的直接重疊程度事實表未涵蓋。"},{"name":"InnoLight／Eoptolink","strategy_note":"10-K 列為光學製造對手，事實表沒有財務數字，威脅程度只能定性。"}],"threats":[{"level":"🟡","text":"客戶自製或導入第二供應商：10-K 揭露客戶整併後曾因自製而減少需求，少數客戶流失會造成重大影響；具名的第二供應商報導未找到。","p":30,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"level":"🟡","text":"CPO 與全電短距連結可能改變組裝製程，封測廠也可能進入；證據來自第三方與風險因子，FN 已有 NPO 與 CPO 案但尚無營收。若量產案流向封測廠，升級為架構替代。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"level":"🟡","text":"其他代工與 ODM 進入目標市場，或產業整併產生更大對手，可能帶來降價與份額流失。","p":25,"evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心與電信網路，決策者是設備 OEM 與雲端業者，付款者是它們的資本支出。連接需求是真的，資料中心營收年增 78%；但客戶預測不是訂單，需求持久，金額節奏不持久。"},{"item":"決策層級","level":"🟡","text":"替代要看單一產品案：10-K 稱許多產品 FN 是唯一外包製造商，新案又要重新驗證，短期難換。但 NVIDIA 金額兩年約減 25%，顯示份額可能在產品世代切換時移走，原因事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的利潤留在元件與設計端：LITE 毛利率 45.91%、COHR 38.16%，FN 11.95%。前四大客戶占 57.4%，部分有自製能力。FN 毛利率四年約降 0.7 個百分點，沒有多分到，也沒有被明顯擠壓。"},{"item":"社會容忍度","level":"🟢","text":"FN 是企業間製造服務，不面對消費者定價，沒有社會定價上限；政策風險在出口管制與關稅，已列入風險。"}],"roiic":32.5,"reinvest_rate":72.3,"endo_ceiling":23.5,"formula_note":"事實表缺折舊與營運資金變動，再投資以 NOPAT 減 FCF 近似。NOPAT＝營業利益×(1−4%)；FY2025 與 FY2026 再投資 5.48 億÷NOPAT 合計 7.575 億＝72.3%；增量 ROIC＝FY2024 到 FY2026 NOPAT 增加 1.782 億÷5.48 億＝32.5%。若稅率改 15%，增量 ROIC 約 34.2%，再投資率約 68.8%，內生上界仍為 23.5%。"}}}},"q3_growth":{"verdict":"五年後仍有跑道：資料中心光互連加上尚未出貨的 OCS、NPO 與 CPO 構成下一條成長曲線，但證據目前只有管理層說法與案件數量。","reasoning":"成長以量為主，價格貢獻事實表未涵蓋，回購與併購可忽略。共識三年 EPS 由 FY2026 的 13.05（GAAP）到 FY2029E 的 29.74，CAGR 31.6%；基期是 GAAP、共識是 non-GAAP，若用 2026-08-13 快照 13.81 推估 non-GAAP 基期則為 29.1%。FY2027E 到 FY2029E 兩年 CAGR 22.8%。內生上界 23.5%，缺口 8.1 個百分點：約 2.5 個是基期口徑，其餘約 5.6 個來自 Building 10 已投入資本的釋放與營益率擴張，兩者無法再拆，視為無法完全歸因；共識路徑依賴這段缺口，Base 路徑不採用。產能規劃為 2027-01 約 100 億、Building 11 後 130 億、含 Building 12 為 160 億美元，FY2028 共識營收 80.7 億只用到 2027-01 產能的八成。TAM 與滲透率事實表未涵蓋，跑道判斷只靠下一條曲線有管理層來源這一項；若 FY2030 前 OCS、NPO、CPO 沒有達到管理層說的數億美元規模，下修為中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主：客戶新案與產能爬坡；價格貢獻事實表未涵蓋；併購與回購貢獻可忽略。","runway_years":"事實表未涵蓋 TAM，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段的增量 ROIC 32.5%×再投資率 72.3%＝23.5%，不另算。","segments":[{"item":"資料中心（Q1 FY27）","value":"7.77 億美元，占 53%，年增 78%，季增 16%"},{"item":"通訊基礎設施（Q1 FY27）","value":"4.44 億美元，占 30%，年增 35%，季增 8%"},{"item":"車用、工業與其他（Q1 FY27）","value":"2.53 億美元，占 17%，年增 20%，季增 8%"}],"decay_signals":["亮：毛利率年度連續下滑，12.71%、12.35%、12.09%、11.99%，Q1 FY27 年減 20 個基點。","亮：FCF 對淨利連兩年低於 0.75，FY2025 為 0.62，FY2026 為 0.01。","未亮：FY2023 到 FY2026 EPS 與營收 CAGR 差 4.1 個百分點，低於 5。","未亮：SBC 占營收 0.76%。","未亮：仍在擴產，沒有停止投資。","未定：CPO 是否壓縮可服務市場，證據只有第三方分析。","無資料：核心市占、維修性資本支出、產業倍數三年走勢事實表未涵蓋。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金優先投產能，短期現金轉換很差；SBC 低，回購規模小，且買在比現價高的位置。","reasoning":"FY2026 FCF 304 萬美元，對淨利 4.73 億幾乎為零。Q1 FY27 營運現金流 2,130 萬、資本支出 1.587 億，其中 7,700 萬是 Santa Clara 園區，FCF −1.374 億。現金及短投 7.57 億，淨現金約 6.77 億，占市值 5.8%。SBC 單季 1,120 萬，占營收 0.76%，年化約占市值 0.4%。回購 7.7 萬股、均價約 380 美元，比現價高 16%；董事會把額度增至 2 億美元，財務長明說優先序是先投資成長。管理層說擴產用自有資金，同季在泰國借入約 7,500 萬美元，財務長解釋為當地借款比動用美國投資便宜，金額不大，不視為資金壓力。Building 11 與潛在新廠將把資本支出推高。近三年現金去向四分與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi3_non_gaap_fcf","f_kpi4_sbc_non_gaap","f_net_debt_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"沒有大型併購；Raytek 16% 股權約 3,240 萬美元，Q1 FY27 認列 2,100 萬美元未實現損失，規模不足以計算已實現報酬。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q1 FY27 均價約 380 美元，以 FY2027E EPS 19.72 計買入收益率 5.2%，計入補足稅約 4.5%；事實表未涵蓋 10 年期公債殖利率，無法比較。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 4,490 萬美元，占市值約 0.38%，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能與新案，不靠併購支撐；併購與回購金額都小，展開也不改變判斷。"}}}},"q5_valuation":{"verdict":"現價要靠 FY2031 EPS 約 35 美元配 15 倍才有年化 10%，這個要求我相信，但回報只算合理，算不上便宜。","reasoning":"現價 327.13 美元，FY2027E 本益比 16.59 倍，FY2028E 13.57 倍，預估 EV/S 1.67 倍。要年化 10%，FY2031 EPS 需約 35 美元配 15 倍；Base 路徑 34 美元，幾乎剛好，所以回報只算合理。PEG 0.73 用 FY2027E 到 FY2029E 兩年 CAGR 22.8%，三年口徑缺 non-GAAP 基期。一年上檔用 FY2028E Base EPS 24.0×16 倍＝384 美元（+17.4%），三年用 FY2029E 28.0×15 倍＝420 美元（+28.4%）。真正的五年分位算不出來，事實表只有四個年度端點，trailing 本益比落在 29.4%。同業 Fwd P/E 事實表未涵蓋，無法做同業倍數對照。賣方平均目標價 624.33 美元比現價高 91%，全距 385–800 美元，來源日期不一，只視為賣方尚未下修，不當估值依據。共識 FY1 三個月上修 42.8% 很可能是財年切換造成，最新一次修正只有 +0.97%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"以 FY2027E non-GAAP EPS 的 Forward P/E 為主，計入 Pillar 2 補足稅後的倍數作對照；同業 Fwd P/E 事實表未涵蓋。","tier":"光通訊代工（低毛利、高資本報酬）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業 Fwd P/E，無法當估值錨；估值改用自身現值與情境路徑。"},"fwd_pe":16.59,"peg":0.73,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"名目 16.59 倍看起來便宜，但分母排除了經常性的補足稅，計入後約 19 倍，用 Q2 指引 GAAP 與 non-GAAP 差距換算約 20.7 倍；FCF 為負，PEG 0.73 只在 FY2029 共識成立時有效。真正五年分位無法計算，只有四個年度端點的 29.4%。綜合為合理，不到便宜。","upside_short_pct":17.4,"upside_mid_pct":28.4,"denominator_disputed":true,"denominator_note":"non-GAAP EPS 排除 Pillar 2 補足稅，Q1 FY27 為 2,000 萬美元，約占 non-GAAP EPS 12.7%，泰國抵減尚未實施。市場同時質疑 FY2028–29 EPS 能否實現，所以不採用 16.59 倍的便宜論證。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 AI 建置高峰的 EPS 當成常態；目前還不是價值陷阱，但兩項衰退訊號已亮。","reasoning":"衰退訊號亮兩項：毛利率連續下滑、FCF 對淨利連兩年低於 0.75，價值陷阱風險屬中度。三個假設的量化衝擊：補足稅若照 Q1 FY27 計，EPS 約少 12.7%；Cisco 若流失，營收少 19.9%；資料中心需求反轉，FY2031 EPS 由 Base 34 美元降到 Bear 17 美元。股價 26 週跌 47.35%，原因事實表未涵蓋，法說只看到投資人擔心 CPO 蠶食，不能把跌幅當安全邊際。2026-08-17 法說有四題管理層沒有正面回答：NVIDIA 下滑與競爭、1.6T 時程、雷射供應承諾、datacom 單季下滑原因，都視為資料缺口。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_peer_fn_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"現金轉換與毛利率兩項訊號亮起，尚未到陷阱。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":19.72,"pe":16.59,"basis":"FY2027E 共識 non-GAAP EPS 19.72（不含 Pillar 2 補足稅），現價 327.13；終端倍數同樣乘第五年 non-GAAP EPS。"},"eps":{"bull":[20.8,27.5,34.5,41.0,47.0],"base":[19.9,24.0,28.0,31.0,34.0],"bear":[19.0,20.5,17.0,15.5,17.0]},"pe":{"bull":18,"base":15,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-55,"hi":-35,"basis":"過去 26 週已跌 47.35%，顯示基本面未壞時也能深跌。深的一端：Bear 谷底 FY2030 EPS 15.5 美元×10 倍＝155 美元，較現價 −52.6%，加少量超跌取 −55%。淺的一端：Bear 終點 204 美元為 −37.6%，取 −35% 作為需求轉弱但未到谷底的回檔。","trigger_time":null},"basis":{"bull":"OCS、NPO、CPO 在 FY2029 前各達數億美元，產能 130–160 億美元接近滿載，FY2031 營收約 150 億美元，淨利率約 11.3%，給 18 倍。","base":"FY2028 前貼近共識，之後 AI 資本支出成長放緩，FY2031 營收約 115 億美元，淨利率約 10.7%；15 倍低於現行 16.59 倍，反映補足稅未決與成長放緩。同業 Fwd P/E 事實表未涵蓋，對照只有 FN 自身現值。","bear":"FY2029 資料中心需求反轉，營收回到約 60 億美元，新廠閒置，FY2031 EPS 17 美元，給成長熄火到 10% 時的 12 倍。機率 30% 依據是共識路徑超過內生上界，且客戶預測不是訂單。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"AI 資本支出是占營收 53% 的資料中心業務的共同來源；Building 11 動工，總產能規劃上修到 160 億美元。第三方分析另指 CPO 與全電短距連結可能縮小可服務市場，客戶整併也曾帶來自製。","assumption":"管理層看到的客戶預測能轉成訂單，且架構改變時 FN 仍是製造方。","consequence":"FY2029 起營收回到約 60 億美元，FY2031 EPS 17 美元×12 倍＝204 美元，比現價低 37.6%；谷底給 10 倍時約低 52.6%。","ruling":"採納為 Bear 情境，機率 30%，與 Single Thing 是同一個故事。CPO 替代部分反駁：證據只來自第三方網站，FN 已有 NPO 與 CPO 案，但尚無營收，無法排除。","watch":"資料中心營收 QoQ、年化營收÷產能、10-K 重要客戶表。","evidence_refs":["ems_utilization_capex_cycle#1","customer_second_source#0","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_week26_return_pct","f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 營收增 36%，FCF 只有 304 萬美元；Q1 FY27 FCF −1.374 億，營運現金流 2,130 萬對去年同期 1.026 億，公司歸因應收帳款增加。客戶集中也使應收集中。Non-GAAP EPS 又未計補足稅。","assumption":"Building 10 完工後資本支出回落，營運資金增速放緩，現金轉換恢復。","consequence":"Building 11、12 與新址接續投入，營收達標但現金長期被吃掉，EPS 複利無法變成股東現金，合理倍數應低於名目 EPS 所示。","ruling":"採納：這是目前最接近事實的風險。Base 給 15 倍而非現行倍數，並把 FY2028 全年 FCF 為負列為減碼條件。反駁部分：淨現金 6.77 億，短期沒有資金壓力。","watch":"單季 FCF、營運現金流對淨利、應收帳款增速對營收增速、單季補足稅金額。","evidence_refs":["ems_utilization_capex_cycle#2","ems_roic_asset_turnover_benchmark#2","customer_concentration_credit#2"],"fact_refs":["f_kpi3_non_gaap_fcf","f_peer_fn_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價跌 47.35% 後名目本益比 16.59 倍，但計入補足稅約 19 倍，用 Q2 指引 GAAP 差距換算約 20.7 倍；trailing 24.69 倍。","assumption":"一般直覺認為跌近一半就便宜。","consequence":"用 15 倍與 Base 路徑，年化回報約 10%，只算中等；要更好的回報必須相信共識 FY2029 EPS 29.74 能實現，而這段超過內生上界。","ruling":"部分採納：價格沒有貴到反映過度，但跌幅本身不是安全邊際，只支持分批，不支持一次買足。","watch":"股價÷當年度共識 EPS，以及補足稅抵減是否實施。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 407.4 → 本次 327.13（-19.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=407.4","side_b":"本次 price_at_dd=327.13","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 407.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 407.4 美元：Bull 價 1,012、Bear 價 227.5，五年期望值 +46.4%，基準年化 8.8%，不對稱比 2.8","side_b":"本次情境、股價仍用 407.4 美元：Bull 價 846、Bear 價 204，五年期望值 +23.3%，基準年化 4.6%，不對稱比 1.8","ruling":"先換情境、股價不動：五年期望值少 23.1 個百分點，基準年化少 4.2 個百分點。不對稱比由 2.8 變為 1.8。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 407.4 美元：五年期望值 +23.3%，基準年化 4.6%，不對稱比 1.8","side_b":"本次情境、股價 327.13 美元：五年期望值 +53.5%，基準年化 9.3%，不對稱比 3.51","ruling":"再換股價、情境不動：起點價下跌 19.7%，五年期望值多 30.2 個百分點，基準年化多 4.7 個百分點，不對稱比由 1.8 升到 3.51。合計五年期望值比前份多 7.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面結論五項未變的原因","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5"],"side_a":"前份：評級 B、估值中性、陷阱中度、護城河持平、五年後跑道寬，股價 407.4 美元。","side_b":"本次：五項結論不變，股價 327.13 美元。新證據包括 Q1 FY27 超出指引、Building 11 上修、FCF −1.374 億、補足稅持續。","ruling":"好消息與壞消息互相抵銷。營收與產能證據改善，現金轉換與 EPS 品質轉差，所以五項都不動。估值倍數雖降，但分母有爭議，不升為便宜。","evidence_level":"一手財報與法說","settle_metric":"Q2 FY27 的資料中心 QoQ 與營運現金流","if_then":["若 Q2 FY27 營收≥1,600M 且營運現金流轉正，則加碼第二筆。","若毛利率連 2 季低於 11.5%，則減碼三分之一。"],"evidence_refs":["ems_utilization_capex_cycle#2"]},{"axis":"公司分類與循環位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份分類為品質複利成長，循環位置未填。","side_b":"本次主分類改為 EMS/ODM，次分類為品質複利成長，循環位置為中循環。","ruling":"改分類是因為本輪明確採代工視角，生意本身沒變。倍數與情緒偏買，需求與擴產不在低點，訊號矛盾，判為中循環、未觸發循環買點。循環讀數只作平行參考，不改長期判斷。","evidence_level":"財報結構與法說","settle_metric":"客戶庫存資料，目前事實表未涵蓋","if_then":["若資料中心營收連兩季環比下滑，循環位置改判晚循環以後，清倉。","若需求回落後股價跌破 249.7 美元且 ROIC 維持 25% 以上，再分批反買。"],"evidence_refs":[]},{"axis":"裁決、機率與回撤區間","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：觀望，機率 25／45／30，最大回撤 −45%，股價 407.4 美元。","side_b":"本次：機率維持 25／45／30，回撤區間 −35% 到 −55%，股價 327.13 美元，下跌 19.7%；裁決與角色由本次輸入重新產生。","ruling":"股價下跌改變進場條件，不改變情境機率。Bear 30% 是共識超過內生上界後的下限，新證據正負相抵，不調整。","evidence_level":"價格資料與判斷","settle_metric":"Q2 FY27 財報","if_then":["若股價續漲而財報未驗證，則不追。","若股價下跌而基本面無損，則分批反買。"],"evidence_refs":[]},{"axis":"重新進場與加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"11 月 Q1 FY27 財報總資料中心 QoQ >0 且 datacom QoQ ≥0；或回檔至 ≤$350（FY2027 本益比約 19x）且 H1-H3 檢核無損","side_b":"Q2 FY27 營收≥1,600M、資料中心 QoQ≥8% 且營運現金流轉正；或週收盤站回 104 週均線 388.86 且營收條件成立","ruling":"舊門檻已發火：股價 327.13 低於 350，資料中心 QoQ +16%。datacom 自 FY2026 第四季起不再單獨揭露，只有管理層質化說法。舊條件已用完，新門檻改看現金流，因為這是目前尚未驗證的環節，前份裁決不沿用。","evidence_level":"一手財報與法說","settle_metric":"Q2 FY27 財報","if_then":["若新門檻全部成立，則加碼第二筆。","若營收低於 1,600M，則停止加碼。"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未提供（null）。","side_b":"資料中心營收連兩季環比下滑則清倉；FY2028 全年 FCF 利潤率為負或毛利率連 2 季低於 11.5% 則減碼。","ruling":"前份門檻在摘要中缺失，無法比對，本次重新設定，理由是資料中心占營收 53%，且現金轉換是目前最弱的一環。","evidence_level":"判斷","settle_metric":"每季財報","if_then":["若資料中心營收連兩季環比下滑，則清倉。"],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未提供（null）。","side_b":"資料中心營收連兩季環比下滑（2028 年中前）。","ruling":"前份內容缺失，無法比對。本次選最大敏感項：資料中心占營收 53%，並貢獻最新一季年增金額的 69%。","evidence_level":"判斷","settle_metric":"資料中心營收 QoQ","if_then":["若事件發生，第一季停止加碼，第二季清倉。"],"evidence_refs":[]},{"axis":"客戶整併對 FN 是利多還是利空","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：過去整併（Lumentum 併 NeoPhotonics、Infinera 併 Coriant、Nokia 併 Infinera）事後都讓 FN 業務成長。","side_b":"10-K FY2026：部分情況下客戶整併後取得自製產能，FN 需求下降。","ruling":"可調和，兩者描述不同案例。Lumentum 與 Marvell 的影響未知，管理層也說尚未與雙方談過；賣方模型應未反映，第一個驗證點是後續兩季法說。","evidence_level":"管理層原話對 10-K 風險因子","settle_metric":"10-K 重要客戶表與法說對 Lumentum 的說法","if_then":["若合併後宣布把 FN 現有案轉自製，則停止加碼。","若合併公司占比升破 10%，則維持原計畫，不因此減碼。"],"evidence_refs":["customer_second_source#0"]},{"axis":"需求能見度與訂單約束力","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：客戶讓 FN 看到的需求遠到看不見盡頭，成長看來可持續。","side_b":"財務長 Sverha 2026-08-17：客戶預測不是訂單承諾。","ruling":"可調和：能見度高，約束力低。FN 擴產依據的是沒有約束力的預測，這段風險落在股東身上，所以 Bear 取 30%。","evidence_level":"管理層原話","settle_metric":"年化營收÷總產能","if_then":["若 Building 10 完工後連 4 季低於 65%，則減碼一半。","若比率升破 80% 且現金流轉正，則加碼。"],"evidence_refs":["ems_utilization_capex_cycle#1"]},{"axis":"資產輕的說法與現金流","cause":"新證據","prior_field":null,"side_a":"執行長 Grady 2026-11-02：資產輕、固定成本低，即使景氣反轉也沒有增加重大固定成本。","side_b":"FY2026 FCF 幾乎為零，連兩季 FCF 為負，Building 10、11 共 350 萬平方呎屬自有廠房。","ruling":"可調和：損益面成立，固定成本約占成本 5%；現金面不成立，資本已經投下去。評價上採用現金面。","evidence_level":"法說與財報","settle_metric":"FY2028 FCF 利潤率","if_then":["若 FY2028 FCF 利潤率低於 0，則減碼三分之一。","若連 2 季 FCF 為正，則加碼。"],"evidence_refs":["ems_utilization_capex_cycle#2"]},{"axis":"EPS 分母的品質","cause":"新證據","prior_field":null,"side_a":"Non-GAAP EPS 4.34，有效稅率 4%，FY2027E 本益比 16.59 倍。","side_b":"Q1 FY27 另有 2,000 萬美元補足稅被排除，約占 EPS 12.7%；財務長稱泰國抵減尚未實施，FY2026 也有 5,740 萬美元。","ruling":"管理層的排除未證、需監測。若 FY2027 底仍未實施，且單季補足稅仍達 non-GAAP 淨利 10% 以上，排除的說法即視為不成立，改用含稅 EPS。","evidence_level":"法說原話","settle_metric":"泰國抵減實施與否、單季補足稅金額","if_then":["若 FY2027 底仍未實施，則停止加碼，估值改用含稅 EPS。","若抵減實施且單季補足稅低於淨利 5%，則恢復使用 non-GAAP 倍數。"],"evidence_refs":[]},{"axis":"三個月共識上修是否真實","cause":"方法變動","prior_field":null,"side_a":"共識 FY1 三個月上修 42.8%，由 13.81 到 19.72。","side_b":"最新一次修正只有 +0.97%。8 月 13 日的 13.81 比 Northland 2026-05 對 FY2027 的 17.23 低約 20%，當時 FY2026 尚未公布，應是財年切換所致。","ruling":"不把 42.8% 當真實上修。真實方向是小幅上修，FY1 +0.97%、FY2 +1.56%、FY3 持平。無法從事實表直接確認快照對應財年，這是推論。","evidence_level":"快照資料與推論","settle_metric":"以同一財年比對快照","if_then":["若同財年比對仍顯示大幅上修，則上調 Base 路徑前兩年。"],"evidence_refs":[]},{"axis":"現在買與現在賣的最強論證","cause":"新證據","prior_field":null,"side_a":"買：營收加速到 51%，Q2 指引年增 43%，名目 16.59 倍，淨現金占市值 5.8%，固定成本低，前份進場門檻已到。","side_b":"賣：股價在 52 週與 104 週均線之下，FCF 連兩季為負，EPS 未計補足稅，AI 資本支出週期未知，此刻大幅擴產正是週期後段常見的動作。","ruling":"可調和：基本面支持小量建立，價格與現金流證據不支持一次買足。","evidence_level":"財報與價格資料","settle_metric":"Q2 FY27 財報與週收盤對 104 週均線","if_then":["若 Q2 FY27 營收≥1,600M 且資料中心 QoQ≥8%，則加碼第二筆。","若股價續漲但財報未驗證，則不追。","若股價跌破 249.7 美元而論點無損，則分批反買。","若資料中心營收連兩季環比下滑，則清倉。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭與替代：10-K 提醒代工、ODM、封測可能進入，第三方指 CPO 改變價值鏈，NVIDIA 金額縮小。","side_b":"結構轉好：資料中心年增 78%，OCS 與 NPO 開始，雷射客戶轉向委外。其他結構變數：Lumentum 與 Marvell 併購、Pillar 2、關稅。","ruling":"雙向拉鋸：需求結構轉好，競爭與客戶結構的不確定同時上升。","evidence_level":"10-K、法說、第三方","settle_metric":"客戶占比與新案營收揭露","if_then":["若前四大客戶任一營收金額年減≥25%，則減碼三分之一。"],"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"axis":"管理層上季承諾對帳","cause":"新證據","prior_field":null,"side_a":"2026-08-17 財務長 Sverha 指引 FQ1 營收 13.75–14.25 億美元、EPS 4.10–4.25；執行長 Grady 稱總產能規劃 125–140 億美元、Building 11 為 21 億美元。","side_b":"2026-11-02 實際營收 14.74 億、EPS 4.34，均高於指引；執行長把總產能改為 160 億美元，Building 11 改為 30 億美元。","ruling":"財測兌現，可信度加分。但產能目標 11 週內上修 14% 到 28%，部分來自每平方呎營收上升，上修速度快於可驗證的訂單。","evidence_level":"逐字稿","settle_metric":"Building 10 完工後年化營收÷產能","if_then":["若下季再度上修產能而資料中心 QoQ 低於 8%，則停止加碼。"],"evidence_refs":["ems_utilization_capex_cycle#1"]}],"triggers":[{"n":1,"text":"Q2 FY27 營收與資料中心成長驗證第一個論點。","type":"假設驗證","maps_to":"H1","metric":"Q2 FY27 營收；資料中心 QoQ","threshold":"營收≥1,600M 且資料中心 QoQ≥8%","action":"達標則加碼第二筆；營收低於 1,600M 則停止加碼","source_freq":"季報，每季","date":"2027-02"},{"n":2,"text":"資料中心營收連兩季環比下滑。","type":"Single Thing","maps_to":"Single Thing","metric":"資料中心營收 QoQ","threshold":"連 2 季低於 0","action":"第一季停止加碼；第二季清倉","source_freq":"季報，每季","date":"2028-06 前"},{"n":3,"text":"新產能沒有被填滿。","type":"風險","maps_to":"R1","metric":"年化營收÷總產能","threshold":"Building 10 完工後連 4 季低於 65%","action":"減碼一半","source_freq":"季報與法說，每季","date":"2027-03 起","evidence_refs":["ems_utilization_capex_cycle#1","ems_utilization_capex_cycle#2"]},{"n":4,"text":"零組件短缺導致營收落空。","type":"風險","maps_to":"R2","metric":"季營收對指引下緣","threshold":"低於下緣且管理層歸因供應","action":"停止加碼一季，供應改善才恢復","source_freq":"季報，每季","date":"每季","evidence_refs":["supply_demand_durability#0"]},{"n":5,"text":"關稅成本轉嫁失敗。","type":"風險","maps_to":"R4","metric":"non-GAAP 毛利率","threshold":"連 2 季低於 11.5% 且管理層歸因關稅或貿易限制","action":"減碼三分之一","source_freq":"季報，每季","date":"每季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":6,"text":"美國把出口管制延伸到泰國。","type":"風險","maps_to":"R4","metric":"出口管制適用範圍","threshold":"正式延伸到泰國且涵蓋 FN 主力產品","action":"清倉","source_freq":"美國商務部公告與 10-K，事件驅動","date":"未定","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"Pillar 2 補足稅抵減沒有落地。","type":"風險","maps_to":"R5","metric":"泰國抵減實施與否；單季補足稅÷non-GAAP 淨利","threshold":"FY2027 底未實施且比率≥10%","action":"停止加碼，估值改用含稅 EPS","source_freq":"季報，每季","date":"2027-08"},{"n":8,"text":"子公司 Casix 的中國不當得利案（民事、個案）由最高院再審，求償 RMB 4 億，受影響營收事實表未涵蓋。","type":"風險","maps_to":"R4","metric":"再審判決","threshold":"判決 Casix 須賠償且金額≥RMB 2 億","action":"計入一次性損失重算淨現金；若同時引發中國業務限制則減碼三分之一","source_freq":"10-K、10-Q，每季","date":"判決日未定","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0"]},{"n":9,"text":"重新進場條件。","type":"估值rearm","maps_to":"H1","metric":"Q2 FY27 營收、資料中心 QoQ、營運現金流；週收盤對 104 週均線","threshold":"營收≥1,600M、QoQ≥8%、營運現金流>0；或站回 388.86 且營收條件成立","action":"重跑研究後建首筆，不直接買足","source_freq":"季報與週線，每季","date":"2027-02"},{"n":10,"text":"現金流證實擴產回本。","type":"加碼","maps_to":"H3","metric":"單季 FCF；non-GAAP 營益率","threshold":"FCF 連 2 季為正且營益率≥10.5%","action":"加碼到計畫部位上限","source_freq":"季報，每季","date":"2027-08 起"},{"n":11,"text":"倍數回到透支水準而現金流未改善。","type":"減碼","maps_to":"H3","metric":"股價÷當年度共識 EPS；FCF","threshold":"≥25 倍且 TTM FCF 仍為負","action":"減碼三分之一","source_freq":"每日價格與季報","date":"持續"},{"n":12,"text":"Q2 FY27 財報後全面複審。","type":"複審日期","maps_to":"H1","metric":"H1 到 H3 檢核","threshold":"財報公布","action":"依檢核結果執行加碼或停止加碼","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心營收環比","bear_threshold":"連 2 季低於 0","window":"2028-06 前每季","source":"季報營收分類","last_status":"ok"},{"metric":"年化營收÷總產能","bear_threshold":"Building 10 完工後連 4 季低於 65%","window":"2027-03 起 4 季","source":"法說揭露的產能與季度營收","last_status":"unknown"},{"metric":"自由現金流利潤率","bear_threshold":"FY2028 全年低於 0","window":"FY2028","source":"10-K 現金流量表","last_status":"warning"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季低於 11.5%","window":"每季","source":"季度法說","last_status":"ok"},{"metric":"前四大客戶營收金額","bear_threshold":"任一客戶年減≥25%","window":"FY2027 與 FY2028","source":"10-K 重要客戶表","last_status":"warning"}],"action_conditions":{"rearm_trigger":"Q2 FY27 營收≥1,600M、資料中心 QoQ≥8% 且營運現金流轉正；或週收盤站回 104 週均線 388.86 且營收條件成立","exec_line":"2027-02 財報前最多建首筆（計畫部位三分之一）；股價續漲而財報未驗證則不追，跌破 250 週均線 249.7 美元但論點無損則分批反買。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 CPO 當成對 FN 的替代，但 FN 同時承接 pluggable、NPO 與 CPO 案，架構改變換的是產品，不一定換掉製造商；週期高點的疑慮反駁不了，已放進 Bear 情境。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"資料中心需求把營收帶到 FY2028 約 80 億美元，Building 10 的新產能能被填滿。","2y":"FY2028 營收≥76.7 億美元（共識 80.72 億的 95%）","5y":null,"10y":null,"threshold":"FY2028 營收≥76.7 億美元；Q2 FY27 資料中心 QoQ≥8%","source":"季報營收分類與法說；共識來自 Koyfin 與 yfinance 快照","drift_rule":"TTM 營收落後路徑連 2 季≥5% 為削弱，連 3 季≥10% 為反轉"},{"id":"H2","text":"客戶與產品持續分散：NVIDIA 下滑由 Cisco、Amazon、Nokia 與新收發器客戶補上，OCS、NPO、CPO 成為下一條曲線。","2y":null,"5y":"FY2030 前 OCS、NPO、CPO 合計年營收≥10 億美元，且單一客戶占比≤25%","10y":null,"threshold":"管理層或 10-K 揭露的新案營收≥10 億美元；單一客戶≤25%","source":"10-K 重要客戶表與法說","drift_rule":"連 4 季偏離路徑≥5% 為削弱，連 6 季≥10% 為反轉；若新案營收始終未揭露，視為無法驗證並下修跑道判斷"},{"id":"H3","text":"擴產不稀釋資本報酬：ROIC 維持 25% 以上，Building 10 後自由現金流轉正。","2y":"FY2028 FCF 利潤率≥3%，non-GAAP 營益率≥10.5%","5y":"同一口徑 ROIC≥25%","10y":null,"threshold":"FY2028 FCF 利潤率≥3%；non-GAAP 營益率≥10.5%","source":"10-K 現金流量表、季度法說、第三方 ROIC 資料","drift_rule":"TTM 偏離連 2 季≥5% 為削弱，連 3 季≥10% 為反轉"}],"R":[{"id":"R1","text":"擴產走在需求前面：2027-01 產能約 100 億美元，Building 11 動工，客戶預測卻不是訂單。","h_ref":"H1","clock":"🔥","threshold":"Building 10 完工後連 4 季，年化營收÷總產能低於 65%","evidence_refs":["ems_utilization_capex_cycle#1","ems_utilization_capex_cycle#2"]},{"id":"R2","text":"零組件短缺壓住出貨，雷射、記憶體、ASIC 偏緊，為特定客戶採購的料也難轉用。","h_ref":"H1","clock":"⚡","threshold":"季營收低於指引下緣，且管理層歸因供應","evidence_refs":["supply_demand_durability#0","geo_supply_chain#2"]},{"id":"R3","text":"客戶自製、第二供應商或 CPO 把製造環節拿走。","h_ref":"H2","clock":"🐢","threshold":"任一前四大客戶營收金額年減≥25%；或 FY2029 前 NPO 與 CPO 營收仍接近零","evidence_refs":["customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"泰國集中與貿易限制：出口管制可能延伸到泰國，關稅再升級時成本未必能轉嫁，中國營運也要承擔當地風險。","h_ref":"H3","clock":"🔥","threshold":"non-GAAP 毛利率連 2 季低於 11.5%，且管理層歸因關稅或貿易限制","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"Pillar 2 補足稅落地：泰國抵減若未實施，non-GAAP EPS 約高估 12.7%。","h_ref":"H3","clock":"🔥","threshold":"FY2027 底未實施抵減，且單季補足稅≥non-GAAP 淨利 10%","evidence_refs":[]}],"single_thing":{"description":"資料中心營收連兩季環比下滑（2028 年中前）。","why_fatal":"資料中心占營收 53%，貢獻最新一季年增金額的 69%；一旦反轉，Bear 的 FY2031 EPS 17 美元只有 Base 34 美元的一半，而 Building 11 已開工，資本收不回來，是模型中最大的單一敏感項。","if_happens":"第一季環比下滑就停止加碼；連兩季下滑則清倉，不等 Building 11 完工。","how_monitor":"每季法說的營收分類，比較資料中心營收對上季，同時看年化營收÷產能。","probability":"約 25%（12–24 個月，判斷值，假設 Bear 機率 30% 中多數落在 FY2028–29，沒有統計基礎）"}},"appendix_a":{"growth_durability":7,"quality_score":6.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.57,"peg_fy2":0.6,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":13.05,"FY2027E":19.72,"FY2028E":24.11,"FY2029E":29.74},"fy_end_month":6,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS 13.05，事實表未涵蓋 FY2026 non-GAAP EPS；FY2027E 到 FY2029E 為 Koyfin 共識，由上半年 EPS 與指引推斷為 non-GAAP，家數事實表未涵蓋（營收共識為 7 位分析師）。財年於 6 月底結束。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"capacity","event":"Building 10 完工，Building 11 動工，總產能約 100 億美元","impact":"中","watch":"完工後第一個完整季的年化營收÷產能"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 財報與 Q3 指引","impact":"高","watch":"資料中心 QoQ、營運現金流、毛利率是否如指引改善"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"泰國 Pillar 2 抵減是否實施（管理層未給時點，以 FY2027 底為觀察點）","impact":"中","watch":"單季補足稅金額"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"NPO 與 CPO 案開始貢獻營收","impact":"中","watch":"管理層是否量化 OCS、NPO、CPO 營收"},{"date":"2028-06","date_precision":"quarter","type":"capacity","event":"Building 11 預計完工，新增約 30 億美元產能","impact":"中","watch":"完工時年化營收是否已超過 100 億美元產能的八成"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 CPO 當成對 FN 的替代，但 FN 同時承接 pluggable、NPO 與 CPO 案，架構改變換的是產品，不一定換掉製造商；週期高點的疑慮反駁不了，已放進 Bear 情境。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-47.35, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
