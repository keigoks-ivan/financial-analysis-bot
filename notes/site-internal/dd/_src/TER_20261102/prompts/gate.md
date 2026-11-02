你是 DD 管線 v20 的判斷層閘（gate），標的 TER（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（48 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1306.0 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益＝412.9 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝31.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝402.0 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝30.8 %｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi8_q4_fy2026_1_300`（q1_business）｜管理層 Q4 FY2026 指引：營收區間（中值 1,300）＝1,250–1,350 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
- `f_peer_ter_gross_margin_pct`（q2_moat）｜TER 毛利率＝59.41 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ter_operating_margin_pct`（q2_moat）｜TER 營業利益率＝33.17 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ter_fcf_margin_pct`（q2_moat）｜TER FCF 利潤率＝21.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_6857_t_gross_margin_pct`（q2_moat）｜6857.T 毛利率＝65.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6857.T.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6857_t_operating_margin_pct`（q2_moat）｜6857.T 營業利益率＝45.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6857.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6857_t_fcf_margin_pct`（q2_moat）｜6857.T FCF 利潤率＝31.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6857.T.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_form_gross_margin_pct`（q2_moat）｜FORM 毛利率＝44.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FORM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_form_operating_margin_pct`（q2_moat）｜FORM 營業利益率＝15.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FORM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohu_operating_margin_pct`（q2_moat）｜COHU 營業利益率＝-6.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHU.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_keys_gross_margin_pct`（q2_moat）｜KEYS 毛利率＝64.69 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KEYS.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_keys_operating_margin_pct`（q2_moat）｜KEYS 營業利益率＝20.25 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KEYS.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝9.44 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝11.9 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝15.92 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5230.16 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6518.41 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝10.28 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 8.56 → 9.44（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_313_6_86_3_agent`（q4_capital）｜自由現金流（營業現金流 313.6 − 資本支出 86.3，本 agent 自算）＝227.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi6_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝5.4 %｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi7_non_gaap_eps`（q4_capital）｜Non-GAAP 稀釋 EPS＝2.29 USD｜期間與口徑：Q3 FY2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Exhibit 99.1（8-K，teradyne.com/investors 發布）https://www.sec.gov/Archives/edgar/data/0000097210/000119312526434981/ter-ex99_1.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-27，公告於 2026-10-27））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-329.47 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 137.12、現金 466.59（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.186 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝156.12 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝274.37 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝29.06 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 9.44，分子＝快照價 274.37｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.54 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝26.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝26.6 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝8.57 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝67.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝67.3 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝8.5 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝67.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝67.4 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.13 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝42506.48 USD m｜期間與口徑：2026-11-02／市值 42835.95 ＋ 淨負債 -329.47｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-20.51 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.85｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝316.39 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝211.64 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝149.55 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝1.83 %｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（9.44 → 9.44）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.25 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（11.87 → 11.9）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：面臨新興亞洲公司及數家客戶內部開發的競爭，且美國貿易法規未必約束部分對手
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 稱貿易限制使其在部分市場競爭力受限，因部分對手不受同樣限制
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：Seeking Alpha：Advantest 與 Teradyne 雙寡占份額消長，稱 Advantest 2025 年取得顯著份額
  - 來源：Seeking Alpha, Advantest/Teradyne: Market Share Shifts In This Duopoly（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K：前五大直接客戶占營收 44%（2024 為 36%、2023 為 32%）；一家半導體測試客戶占 19%（含他人指定的營收）；失去或大幅減少大客戶需求可能造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025（經 WebSearch 摘要轉述，未逐字取得原文）（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前五大直接客戶占營收 44%（2024: 36%、2023: 32%）；兩家指定客戶驅動 12%、10%，另一家直接客戶占 19%（含他人指定）；失去重要客戶可能有重大不利影響，且幾乎無合約追索權。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2025/12/31 應收帳款中兩家客戶分別占約 22% 與 20%（2024 年底各 10%）；公司稱持續做客戶信用評估，必要時要求信用狀。
  - 來源：SEC EDGAR 10-K FY2025 Item 7A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：測試設備廠面臨 FPGA、CPU、GPU、驅動 IC 等關鍵零組件嚴重短缺，交期拉長（Digitimes 引 The Elec）；另 36Kr 引韓媒稱測試設備 FPGA 交期由 8–10 週拉至最長 52 週
  - 來源：Digitimes 2026-06-01 / 36Kr（as_of 2026-06-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#6`（supply_demand_durability｜方向 -｜狀態 ok）：有分析稱各主要廠商對同一需求訊號採相同多年期建廠時程，新增供給集中在 2027–2029 窗口，存在供過於求路徑風險（二手評論，未核原文）
  - 來源：Creative Strategies / stockwirex 評論（as_of 2026-08-01）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Q1 2026 10-Q 揭露美國出口管制合規已限制公司在部分地區的競爭能力，未來規則變動可能帶來重大成本
  - 來源：SEC EDGAR 10-Q（期末 2026-03-29）（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025：關稅與出口管制（含商務部對中國客戶限制）已限制公司在部分市場的競爭力；近期關稅變動至今未造成重大不利影響，但未來新增關稅可能有重大影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1/1A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：部分中國半導體公司被列入實體清單，對公司與這些客戶的業務已有且將持續有不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：供應商受關稅與出口限制規範，可能影響零組件供應或提高價格。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Teradyne 的 FY2025 10-K 指出供應商受美國及他國關稅與出口限制約束，可能影響零件供應或價格
  - 來源：Teradyne 10-K FY2025 (SEC)（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Teradyne 10-K（FY2014/2007 版）表示部分零件為單一來源，單一來源供應商延遲或停供會造成暫時衝擊
  - 來源：Teradyne 10-K FY2014 (SEC)（as_of 2015-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2018 10-K：產品及供應商零件越來越多在中國與馬來西亞生產
  - 來源：Teradyne 10-K FY2018 (SEC)（as_of 2019-02-28）｜affects：thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 10-K：新出口管制已影響對部分中國客戶的銷售
  - 來源：Teradyne 10-K FY2024 (SEC)（as_of 2025-02-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#5`（geo_supply_chain｜方向 -｜狀態 ok）：測試業務製造仰賴合約製造商，主要在馬來西亞
  - 來源：PolicyRisk（as_of 2026-01-01）｜affects：thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Advantest 在 SoC 測試機市占：2024 報導稱 2023 年 Advantest 約 50% 對 TER 約 30%；第三方電子報稱 CY25 Advantest SoC 市占由 56% 升至 66%（未經核實）；TER Q2 2026 call 稱 fast follower 階段市占預期從零增至約 30%。未找到 2026 明確定價/ASP 資料
  - 來源：Nasdaq/Zacks 與 datagravity、earningswhispers Q2 2026 transcript（搜尋摘要）（as_of 2026-07-29）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Teradyne 10-K 風險因子：電子、半導體與機器人產業的產品常被技術更先進的替代品取代，舊技術需求下降時售價下滑；若無法推出新技術，營收與財務狀況可能受不利影響。未點名具體替代技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":676.0,"bear_5y_price":170.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":34.7,"ev5y_pct":40.8,"irr_base_pct":6.1,"asym_ratio":3.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":9.44,"pe":29.06,"basis":"FY2026E 非 GAAP 共識 EPS 9.44（Koyfin 快照 2026-10-31）除判斷日股價 274.37；終端倍數同樣以終端年當年度的非 GAAP EPS 為分母"},"eps":{"bull":[12.6,17.2,19.5,22.5,26.0],"base":[11.6,14.5,13.5,15.0,16.8],"bear":[10.8,8.0,7.0,8.5,10.0]},"pe":{"bull":26,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.186,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TER_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Michelle Turner｜guidance：Q3 營收 12～13 億美元、非 GAAP EPS 1.85～2.15（營收數字在原文同句後半）（原話："$1.2 billion to $1.3 billion and non-GAAP EPS of $1.85"）
- 2026-07-29｜Michelle Turner｜guidance：上半年營收占全年比重更新為 50%～52%（原話："we are updating our first half weighted revenue to 50% to"）
- 2026-07-29｜Michelle Turner｜guidance：下半年展望轉強、區間較三個月前收窄（原話："The outlook for the second half has strengthened"）
- 2026-07-29｜Michelle Turner｜guidance：下半年對比上半年的分部成長與抵銷項目（原話："We expect this growth will be offset by softness"）
- 2026-07-29｜Michelle Turner｜guidance：預期 2027 年成長回升，來源為 ATE TAM 擴張與市占提升（原話："We anticipate a resurgence in growth in 2027"）
- 2026-07-29｜Gregory Smith｜guidance：CEO 預期 2027 為健康成長年（原話："We expect 2027 to be another year of healthy growth"）
- 2026-07-29｜Michelle Turner｜margin：Q3 毛利率指引 58%～59%，歸因產品組合與新產品（原話："Gross margins are expected to be in the"）
- 2026-07-29｜Michelle Turner｜margin：Q2 毛利率 59.8%，年增 250bp，季減 110bp（部分因 Q1 一次性利益）（原話："Gross margins for the quarter were 59.8%"）
- 2026-07-29｜Michelle Turner｜margin：Q3 營業費用占營收約 29%～30%（原話："approximately 29% to 30% of third quarter sales"）
- 2026-07-29｜Michelle Turner｜margin：Q3 非 GAAP 營業利益率指引 28%～30%（原話："operating profit rate is expected to be between 28% and 30%"）
- 2026-07-29｜Michelle Turner｜margin：Q2 非 GAAP 營業利益 4.48 億美元，營業利益率 33.7%（原話："non-GAAP operating income was $448 million,"）
- 2026-07-29｜Michelle Turner｜margin：CFO 說明毛利率季間波動幅度與全年區間的口徑（原話："you'll see about 400 basis point swing"）
- 2026-07-29｜Michelle Turner｜margin：CFO 稱上半年有不會重複的非營運有利因素（原話："some nonrecurring nonoperational"）
- 2026-07-29｜Michelle Turner｜margin：全年毛利率約 59%，略低於目標模型（原話："which is just shy of our target"）
- 2026-07-29｜Michelle Turner｜margin：CFO 稱記憶體產品對毛利率持續構成壓力，並延續至 2027（原話："memory is going to continue to be a strain from an overall"）
- 2026-07-29｜Michelle Turner｜margin：回答分析師：2027 毛利率不預期根本性變化，取決於產品組合（原話："any fundamental changes in gross margin."）
- 2026-07-29｜Michelle Turner｜margin：Q4 營業費用預期與 Q3 指引相當（原話："OpEx in Q4 to be comparable to Q3 guidance"）
- 2026-07-29｜Michelle Turner｜commitment：管理層表示有信心以更快速度達成目標獲利模型，並將於 Q4 法說更新（原話："We remain confident in achieving our target earnings model"）
- 2026-07-29｜Gregory Smith｜commitment：CEO 表示將在 Q4 法說分享更新後的目標獲利模型，更新方式與 WFE 連動（原話："which we will share in our Q4 earnings call"）
- 2026-07-29｜Gregory Smith｜commitment：CEO 稱正加碼投資，有機與併購皆在內（原話："We are leaning further into investments"）
- 2026-07-29｜Michelle Turner｜commitment：美國製造中心預計今年稍後啟用（原話："is on track for opening"）
- 2026-07-29｜Michelle Turner｜capital_allocation：資本配置首要為再投資於業務（原話："Our first priority for capital continues to be reinvesting"）
- 2026-07-29｜Michelle Turner｜capital_allocation：其次為維持營運現金並保留可做增值併購的火力（原話："keep dry powder available for accretive M&A"）
- 2026-07-29｜Michelle Turner｜capital_allocation：Q2 現金與投資 5.17 億美元，自由現金流 3.78 億美元（原話："We had free cash flow of $378 million in"）
- 2026-07-29｜Michelle Turner｜capital_allocation：Q2 股利 2,000 萬美元、買回 6,900 萬美元（原話："We paid $20 million in dividends in the"）
- 2026-07-29｜Michelle Turner｜capital_allocation：營運資金主要為存貨增加，資本支出較上季增加 2,600 萬美元（原話："predominantly inventory investment, increased in support"）
- 2026-07-29｜Gregory Smith｜customer：Q2 營收破 13 億美元，年增逾 100%；AI 營收占比逾 60%（原話："At more than 60%, AI-driven revenue is the key proof point"）
- 2026-07-29｜Michelle Turner｜customer：Semi Test 拆解：SOC 8.43 億、記憶體 2.12 億、IST 6,700 萬美元（原話："SOC of $843"）
- 2026-07-29｜Michelle Turner｜customer：運算占 SOC 產品營收 70%，年增近 600%（原話："compute remains the largest portion of our SOC product"）
- 2026-07-29｜Michelle Turner｜customer：運算訂單時點被記憶體與 IST 成長抵銷（原話："compute order timing was more"）
- 2026-07-29｜Michelle Turner｜customer：記憶體廠規劃更遠期擴產；Q2 記憶體 book-to-bill 超過 2（原話："planning capacity additions further out in time"）
- 2026-07-29｜Michelle Turner｜customer：手機相關 SOC 季增雙位數但仍低於歷史水準（原話："though it remains below historical"）
- 2026-07-29｜Michelle Turner｜customer：Product Test 營收 1.07 億，年增 26%、季增 33%；Robotics 1 億，年增 33%（原話："Revenue was $107 million, up 26% year-over-year"）
- 2026-07-29｜Gregory Smith｜customer：IST 營收季增 2.5 倍，來自 AI 帶動的 HDD（原話："Our IST business grew revenue 2.5x quarter-over-quarter"）
- 2026-07-29｜Gregory Smith｜customer：運算客戶下一波高峰預期在 2027 上半年（原話："The next surge for these customers is expected"）
- 2026-07-29｜Gregory Smith｜competition：第一筆 merchant GPU 客戶訂單 Q1 收到、Q2 出貨（原話："we received our first order from -- for a merchant GPU"）
- 2026-07-29｜Gregory Smith｜competition：管理層描述雙供應商資格認證流程，從啟動到量產 9～12 個月（原話："it takes 9 to 12 months from the start to the ramp"）
- 2026-07-29｜Gregory Smith｜competition：fast follower 階段市占預期由 0 增至約 30%（原話："market share to grow incrementally from 0 up to about 30%"）
- 2026-07-29｜Gregory Smith｜competition：三個運算客戶所處階段：成熟雙供應商 1、fast follower 1、量產前資格認證 1（原話："we have 1 compute customer in the mature dual vendor phase"）
- 2026-07-29｜Gregory Smith｜competition：CEO 同意競爭對手 Advantest 對記憶體市占下滑的說法，並預期 SOC 市占約持平、略增（原話："I have to say I agree with their commentary about memory."）
- 2026-07-29｜Gregory Smith｜competition：運算市占今年趨穩並開始上揚，市占變化 2027 起逐步顯現（原話："stabilizing and starting to inflect upward"）
- 2026-07-29｜Gregory Smith｜competition：伺服器 CPU 轉向 ARM 對 Teradyne 市占有利，同時也在 x86 爭取（原話："as the share mix of server CPU shifts towards ARM"）
- 2026-07-29｜Gregory Smith｜competition：客戶擅長逐階段挑選最佳方案，Teradyne 須逐項競爭（原話："we have to really compete for everything that we're getting"）
- 2026-07-29｜Gregory Smith｜competition：中國功率市場有在地競爭者，Teradyne 的中國功率占比與前高相近（原話："There is some local competition"）
- 2026-07-29｜Gregory Smith｜product：測試設備占半導體資本支出比重由 2023 年約 4% 升至 2026 前 5 個月 8%（原話："it's 8% of total semi CapEx has been on test equipment"）
- 2026-07-29｜Gregory Smith｜product：CEO 預期該比重落在 7%～9%，不會再持續上升（原話："it's going to settle somewhere in the 7% to 9% range"）
- 2026-07-29｜Gregory Smith｜product：WFE 增加代表需測電晶體與位元增加；管理層看到 ATE TAM 路徑達 200 億美元以上（原話："reach or exceed $20 billion"）
- 2026-07-29｜Gregory Smith｜product：2026 記憶體 TAM 預期較 2025 大逾 40%（原話："The 2026 memory TAM is likely to be more than 40% larger"）
- 2026-07-29｜Gregory Smith｜product：DDR 市場比 1 月預期更強；NAND 開始出現客戶拉貨（原話："the DDR market is stronger now than we thought it would be"）
- 2026-07-29｜Gregory Smith｜product：不預期 2027 記憶體出現特別的波動（原話："we are looking at particular lumpiness in memory"）
- 2026-07-29｜Gregory Smith｜product：預期 2028 年 CPO 市場規模 3 億～7 億美元（原話："We expect CPO alone will be a $300"）
- 2026-07-29｜Gregory Smith｜product：2027 年 CPO 偏向低端，約 2 億美元（原話："the low end would be in the $200 million range"）
- 2026-07-29｜Michelle Turner｜product：Omnyx 初期客戶動能強，管理層預期下半年持續成長（原話："continued growth expected in the second half"）
- 2026-07-29｜Gregory Smith｜product：預期 2027 年汽車與工業可能達到或超越前高（CEO 自稱憑直覺、尚未完整分析）（原話："'27 is going to be up to or exceeding prior peaks"）
- 2026-07-29｜Gregory Smith｜risk：CEO 稱 WFE 與 ATE 的關聯在單季層級不相關，且有約一年時間落差（原話："it's not at all correlated when you're down to a quarter"）
- 2026-07-29｜Gregory Smith｜risk：2027 年測試設備占半導體資本支出比重可能回落至約 7%（原話："It's possible that next year, that could revert down to 7%"）
- 2026-07-29｜Gregory Smith｜risk：良率或品質問題可能造成 ATE 超買，測試時間縮短也可能影響需求（原話："there's significant over buying in ATE"）
- 2026-07-29｜Michelle Turner｜risk：指引區間納入訂單時點可能使營收在季度或年度間位移（原話："timing of orders that could impact revenue"）
- 2026-07-29｜Gregory Smith｜risk：CEO 指出供應鏈中斷是此領域所有人關心的事項，並驅動雙供應商策略（原話："as strong as the weakest link in our whole supply chain"）

### 問答異常語氣（迴避／改口／保留）
- TER_Q2_2026_Earnings_Call_20260729.md｜問：Morgan Stanley 的 Shane Brett 追問記憶體測試成長 vs 位元成長（投影片第 6 頁）及記憶體測試成長 2 倍位元成長如何解讀｜答法：CEO 先說要離線再談，表示分析師過度解讀圖表、並非要預測記憶體 ATE TAM，之後才給一般性原則說明，未直接回答數字
- TER_Q2_2026_Earnings_Call_20260729.md｜問：UBS 的 Timothy Arcuri 追問長期市占目標（40%？42%？）及新認證何時反映市占｜答法：CEO 未給長期市占目標數字，僅稱 2027 起逐步顯現、逐 socket 進行
- TER_Q2_2026_Earnings_Call_20260729.md｜問：Bank of America 的 Vivek Arya 追問 2027 年 WFE 成長 30% 時 Teradyne 相對成長快慢的情境｜答法：CEO 未給 2027 成長率對照，僅稱 TAM 預期增加、測試占資本支出比重可能回落至 7% 但仍在釐清

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 6 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260626","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 測試強度結構提升 → SoC compute（custom ASIC + merchant GPU）持續為 SoC 測試主引擎","columns":{"2Y 驗證點":"FY27 SoC compute 維持 ≥ 50% of SoC 營收 + AI 佔總營收 ≥ 70%","5Y 驗證點":"FY30 ATE 市場達 mgmt 目標 $12-14B（vs $9B 2025）；TER 營收 ~$6B","10Y 驗證點":"FY36 AI/HPC 測試成為 SoC 測試主流（vs mobile）","Sourced Floor / 漂移觸發":"Floor：Q1'26 compute ~half of SoC、FY25 compute +90%（CEO Greg Smith 法說公開）。漂移：連 2 季 SoC compute 訂單環比下滑 = 循環鬆動"}},{"id":"H2","text":"突破 Advantest 在 merchant GPU 的主場：從 design-in → 量產（custom ASIC 已 ~50% 份額是既有強項，merchant GPU 才是新增量）","columns":{"2Y 驗證點":"FY27 merchant GPU 量產營收上量 + Rubin 認證落地","5Y 驗證點":"FY30 merchant GPU + custom ASIC 雙引擎","10Y 驗證點":"FY36 互連（MultiLane）/ 先進封裝（TEL）/ 矽光子 CPO（Photon 100）測試成獨立成長軸","Sourced Floor / 漂移觸發":"Floor：FY26 merchant GPU 指引僅 ~$50M（初期）、H1'26 認證、H2'26 初步營收；NVIDIA Blackwell 最終測試仍由 Advantest 近乎 sole-source，TER 為第二供應商候選（Rubin 預期最高 ~40% 份額，未落地）。漂移：H2'26 量產未實現或 Rubin 認證落空 = H2 thesis 受傷"}},{"id":"H3","text":"市場願維持 forward PE 在 28-40x（AI 測試溢價）而非回落至循環中樞 20-25x","columns":{"2Y 驗證點":"FY27 FPE 維持 ≥ 28x（不單季崩至 18-20x）","5Y 驗證點":"循環反轉後 normalized EPS $9-11、PE 擴張至 25-30x（mid-cycle）","10Y 驗證點":"長期合理 PE 趨向 22-28x","Sourced Floor / 漂移觸發":"Floor：5Y forward 中位 ~28-30x（macrotrends/finbox）。漂移：連續 4w FPE 50x（cycle peak 透支警戒，現值 49x 已逼近上緣）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Advantest 守住 merchant GPU 主場（Blackwell sole-source，Rubin 不讓 TER 進）+ 中國 ATE（長川/華峰）高端化蠶食","columns":{"對應假設":"H1, H2","時間尺度":"🔥 中（4-6 季）","監測指標":"Rubin 測試供應商選擇、Advantest 季度 GPU 份額、中國廠高端機台發佈","警戒閾值":"Rubin 認證 TER 出局 或 連 2 季 TER custom-ASIC 份額流失 5pp"}},{"id":"R2","text":"cycle peak 後 AI capex digestion → EPS/Rev 環比下滑（peak-EPS 回落）","columns":{"對應假設":"H1, H3","時間尺度":"⚡ 短（1-2 季）","監測指標":"季度營收/EPS 環比、book-to-bill、AI 佔比","警戒閾值":"連 2 季營收環比下滑（Q2'26 guide 已環比 -6%，需觀察 Q3 是否續弱）"}},{"id":"R3","text":"估值正常化（PE de-rating）：市場不再給 AI 測試溢價","columns":{"對應假設":"H3","時間尺度":"⚡ 短（1-2 季）","監測指標":"forward PE 分位、現價 vs 分析師均值","警戒閾值":"連續 4w FPE 15%（Q1'26 已現 -17% gap down）"}},{"id":"R4","text":"出口管制再收緊（中國 ~14% 營收）；Robotics 段（UR+MiR）持續低貢獻","columns":{"對應假設":"H1, —","時間尺度":"🐢 長（2+ 年）","監測指標":"美國 BIS 規則、UR+MiR 季度營收與 OM","警戒閾值":"新增測試機出口禁令；robotics 連 4 季虧損擴大"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":-3.0,"ev5y_pct":-13.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":null,"ev5y_pct":-13.0,"irr_base_pct":-3.0,"max_dd_pct":-60.0,"bull_5y_price":665.46,"bear_5y_price":169.91,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":471.96,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TER","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Teradyne, Inc."},"oneliner":"AI 測試需求把季營收推上 13 億美元平台，股價較 6 月底跌約四成，只剩 FY2027 共識 EPS 的 23 倍；運算放量延到 2027 下半年，2028 年後有產能消化風險，等 1 月展望或 230 美元以下再動。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TER_20261102/scenario.json","answers":{"q1_business":{"verdict":"TER 賺的是晶片廠與 AI 晶片設計者買測試機的錢。每顆高階晶片出廠前都要測，錢卡在測試機台加測試程式這一節。第三季 82% 營收來自半導體測試，毛利率 59.1%，非 GAAP 營業利益率 31.6%。","reasoning":"第三季營收 13.06 億美元，分三塊：半導體測試 10.72 億（82%，其中 SoC 6.76 億，記憶體 3.01 億創新高，硬碟測試 0.95 億創新高）；產品測試 1.38 億（11%，訂單出貨比 1.4）；機器人 0.96 億（7%，首度單季獲利）。GAAP 營業利益率 30.8%，非 GAAP 31.6%。第四季營收指引 12.5～13.5 億美元，中值與第三季持平。SoC 由第二季 8.43 億降到 6.76 億，季減約 20%，被記憶體與硬碟測試各約 42% 的季增抵銷；管理層說運算在第三季是年內低點。收錢方式是設備一次性銷售，能見度由過去 13 週拉長到約兩季。單點依賴：前五大直接客戶占 44%（2023 年為 32%），一家半導體測試客戶占 19%，兩家客戶分占應收 22% 與 20%。這是集中度風險，不是護城河證據。產業位置在擴張期，依據有三：SEMI 年中把 2026 測試設備上修到 153 億美元（年增 31%）；測試占半導體資本支出由 6.4% 升到 8.1%；零組件交期拉長。供需持久性屬週期性，2028 年後可能反轉：Wolfe 與 ASML 的持久證據只蓋到 2028，新增產能卻集中在 2027–2029。產業態勢是雙向拉鋸。競爭面，對手在運算強勢且在擴產；結構面，AI 推高測試強度；其他面，出口管制與 232 關稅持續壓縮中國業務。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi4_gaap","f_kpi8_q4_fy2026_1_300","f_earnings_recency"],"verdict_values":{"revenue_quality":"以設備一次性銷售為主，營收隨客戶建廠與產能時點起伏。半導體測試能見度約兩季（CFO 第三季法說）；機器人除最大客戶外，多為當季成交","unit_econ_note":"第三季毛利率 59.1%，年增 60bp、季減 70bp，變動來自產品組合。產品測試拉高毛利率，記憶體拉低。第四季因新品導入，毛利率指引 57.5%～58.5%","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 測試需求驅動的雙寡占測試設備商。營收隨半導體資本支出擺動（FY2023 年減 15%），毛利高、營運槓桿大"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性，2028 年後可能反轉。Wolfe 稱 2028 年前難以供過於求，ASML 稱 2027–28 設備供給不足；但二手評論指出新增產能集中在 2027–2029，CEO 在 Q2 法說也說測試占資本支出的比重 2027 年可能回到 7%","bargaining":{"up":"上游議價力上升。FPGA、CPU、GPU 等零件短缺，測試設備用 FPGA 交期最長拉到 52 週；部分零件單一來源，組裝依賴馬來西亞代工","down":"下游議價力強。前五大客戶占 44%，單一客戶占 19%；客戶刻意採雙供應商，一方面確保產能，一方面保有議價空間","geo":"出口管制與實體清單限制中國業務，232 條款對半導體設備課 25% 關稅，而部分外國對手不受同樣限制"},"profit_pool_dir":"利潤池往 AI 運算、HBM 與資料中心互連測試移動。TER 在 HBM 效能測試份額較高，在運算份額低但正在上升；手機段萎縮","tam_table":[{"item":"測試設備市場（SEMI）","value":"2025 年約 117 億美元（由 2026 年 153 億、年增 31% 回推）→ 2026 年 153 億 → 2028 年 208 億美元"},{"item":"管理層 ATE 市場路徑","value":"舊模型以 120～140 億美元編製，現稱可達或超過 200 億美元，1 月更新"},{"item":"測試占半導體資本支出","value":"2023 年約 4% → 2025 年 6.4% → 2026 前 8 月 8.1%；管理層預期長期落在 7%～9%"},{"item":"TER 半導體測試份額（粗估）","value":"2026 前三季 33.05 億美元，年化約 44 億，對 SEMI 的 153 億約 29%。SEMI 口徑含其他測試設備，只能看方向"},{"item":"運算 SoC 份額","value":"第三方稱 Advantest 的 SoC 份額 CY25 由 56% 升到 66%（未核實）；TER 在 fast follower 客戶的份額預期由 0 增到約 30%"},{"item":"CPO 測試設備","value":"2026 年約 1 億美元 → 2028 年 3～7 億美元（管理層），長期可達 10 億美元以上"},{"item":"營業利益池 5 年變化","value":"事實表未涵蓋產業營業利益池占比"}]}}},"q2_moat":{"verdict":"護城河持平。測試程式的轉換成本與雙寡占地位穩固，運算份額正在拿；但定價力沒有變強，利潤率仍落後 Advantest。","reasoning":"機制是裝機量加測試程式的轉換成本。客戶從啟動到量產要 9～12 個月認證（Q2 法說），換供應商就得重寫測試程式、重做 correlation。執行力給 8 分：UltraFLEXplus 產能 18 個月擴 4 倍，並認證第二家代工；推出三款新儀器，補上 2027 世代 AI 晶片的測試空缺；連續多季優於共識。定價力給 6 分：TTM 毛利率 59.4% 對 Advantest 65.7%，營業利益率 33.2% 對 45.9%，FCF 利潤率 21.6% 對 31.2%，三項都落後；第四季毛利率指引下滑，客戶用雙供應商保有議價力。對最強同業的利潤率差為負，但只有單一期間，看不出在擴大還是收窄。方向判持平：執行面擴大（merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中）；定價面縮減；運算市場成長太快，稀釋了整體份額（Q3 法說 CEO）。當期報酬方面，事實表沒有投入資本。外包代工、資本支出占營收低，推定為高利益率高周轉。但 FY2022→FY2025 營業利益由約 8.5 億降到 6.9 億美元，增量報酬明顯隨週期擺動。","fact_refs":["f_peer_ter_gross_margin_pct","f_peer_ter_operating_margin_pct","f_peer_ter_fcf_margin_pct","f_peer_6857_t_gross_margin_pct","f_peer_6857_t_operating_margin_pct","f_peer_6857_t_fcf_margin_pct","f_peer_form_gross_margin_pct","f_peer_form_operating_margin_pct","f_peer_cohu_operating_margin_pct","f_peer_keys_gross_margin_pct","f_peer_keys_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"裝機量加測試程式轉換成本（認證 9～12 個月），在運算靠客戶的雙供應商策略切入","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：第二家超大型雲端客戶通過認證、進入 fast follower；merchant GPU 多顆晶片開發中；第三家在認證；HBM 疊層降低，增加 TER 份額較高的效能測試需求。定價面縮減：第四季毛利率指引 57.5%～58.5%，低於第三季 59.1%；零件成本上升，客戶以雙供應商壓價。CEO 也承認運算市場擴大稀釋了整體份額。兩邊相抵，判持平","competitor_notes":[{"name":"6857.T","strategy_note":"運算 SoC 測試的領先者，利潤率全面高於 TER（營業利益率 45.9% 對 33.2%），並靠代工夥伴擴產守份額；TER 的份額成長要從它手上拿"},{"name":"FORM","strategy_note":"探針卡廠，剛與 TER 宣布光學測試合作，TER 第四季完成對它的投資；兩家偏互補，不是直接競爭"},{"name":"COHU","strategy_note":"年報點名的半導體測試對手，營業利益率 −6.2%，規模與獲利都威脅不到高階市場"},{"name":"KEYS","strategy_note":"量測儀器廠，毛利率 64.7%、營業利益率 20.3%，與 TER 產品測試的互連與高速測試部分重疊"}],"threats":[{"level":"🟡","text":"Advantest 在運算 SoC 測試的強勢份額與擴產。第三方稱它的 SoC 份額 CY25 由 56% 升到 66%（未核實），TER 只能逐個 socket 搶","p":"40%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"新興亞洲對手與客戶自製測試，且部分對手不受美國出口管制約束","p":"20%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","reg_tariff_export#0"]},{"level":"🟡","text":"韓國記憶體測試廠吃下晶圓測試段的擴產需求（Q3 法說 CEO），TER 在晶圓測試的份額較低","p":"30%","evidence_refs":[]},{"level":"🟡","text":"替代技術：系統級測試等相鄰測試層興起，舊世代機台售價下滑。TER 有 Titan 系統級測試與燒機產品，屬點對點競爭","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定，投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（晶片廠與封測廠）、決策者（晶片設計與測試工程）、付款者（晶片廠資本支出）三方都成立。測試是出貨前必經步驟，屬於「需要」；但購買時點跟著產能擴充走，可以延後。測試占資本支出 8.1%，已在管理層 7%～9% 區間的上半部，CEO 說 2027 年可能回到 7%，當前需求水位偏高"},{"item":"決策層級","level":"🟡","text":"替代性要在單一晶片 socket 層看。已導入的 socket 換供應商要 9～12 個月認證，轉換成本高；但新 socket 由客戶逐階段比較（CEO：每一個都要競爭）。雙供應商策略讓客戶刻意保留替代選項，轉換成本只保護既有裝機，保護不了新訂單的價格"},{"item":"價值鏈分配","level":"🟡","text":"測試只占半導體資本支出 6%～8%，金額小但攸關良率，給 TER 一定的定價空間。可是下游前五大占 44% 且逐年集中，上游 FPGA 等零件短缺把成本往 TER 推，兩頭擠壓。價值鏈的總利益在晶圓廠與 AI 晶片設計者手上，測試環節分多少由客戶決定"},{"item":"社會容忍度","level":"🟡","text":"企業對企業設備，沒有消費者漲價的社會壓力。天花板來自政策：出口管制與實體清單已限制中國銷售，232 條款課 25% 關稅，部分外國對手不受同樣限制。不靠監管授權，但地緣政策會壓縮可服務市場"}],"roiic":"35%（粗估，區間 30%～40%）","reinvest_rate":"35%（粗估，區間 30%～50%）","endo_ceiling":12,"formula_note":"單位為 %。內生成長上界＝增量報酬 35% × 再投資率 35% ≈ 12%。高點對高點：FY2022 營業利益約 8.5 億美元，2026 第三季年化約 16 億，增量為正且高；但 FY2022→FY2025 增量為負，所以取正常化值。再投資包含資本支出（第三季 0.86 億）、收購 1.667 億、存貨半年增約 2 億（一半是備料）；折舊與 NOPAT 事實表未涵蓋，兩項都是粗估，不承重"}}}},"q3_growth":{"verdict":"5 年後跑道中等。ATE 市場有望在 2030 年前到 200 億美元以上，TER 在運算份額也有空間；但第二曲線（CPO、實體 AI 機器人）規模小、時程在 2028 年後，成長大部分仍綁在半導體資本支出週期。","reasoning":"成長以量為主：AI 資本支出帶動測試台數，記憶體連四季超過 2 億美元，硬碟測試因近線儲存需求年增約 150%。價格面靠新世代儀器，ASP 資料事實表未涵蓋。併購（2026 年 1.667 億美元）與淨回購（年化約 0.6%）的貢獻都小。共識 FY2026→FY2028 EPS 由 9.44 到 15.92，兩年年化約 29.9%；FY2027 營收共識 65.2 億美元，年增約 24.6%（17 位分析師）。內生上界約 12%（增量報酬 35% × 再投資率 35%，皆粗估），共識高出約 18 個百分點。缺口來自產業資本支出上行帶來的量與營運槓桿，屬週期性外生成長，再投資解釋不了，長期信心上限為中。跑道：管理層說 ATE 市場可達或超過 200 億美元，TER 在運算 fast follower 客戶的份額預期到約 30%，這段約 5～9 年走完，之後成長回到跟著半導體資本支出走。衰退信號亮 2 個（核心份額被稀釋、EPS 成長遠快於營收），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct","f_kpi8_q4_fy2026_1_300"],"verdict_values":{"growth":{"driver_mix":"量為主（AI 資本支出帶動測試台數），價為輔（新世代儀器），併購與回購貢獻小","runway_years":"5～9","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的數字：增量報酬 35% × 再投資率 35% ≈ 12%（皆粗估，投入資本與折舊事實表未涵蓋）","segments":[{"item":"半導體測試","value":"第三季 10.72 億美元（82%），年增 77%。SoC 6.76 億（季減約 20%），記憶體 3.01 億（創新高），硬碟測試 0.95 億（創新高）"},{"item":"產品測試","value":"第三季 1.38 億美元（11%），年增 56%，訂單出貨比 1.4，拉高整體毛利率"},{"item":"機器人","value":"第三季 0.96 億美元（7%），年增 28%，首度單季獲利。最大客戶營收 2026 年是 2025 年的三倍；實體 AI 要到約 2028 年才會放量"}],"decay_signals":[{"item":"毛利率連2季年減","lit":false,"text":"第三季年增 60bp，第二季年增 250bp"},{"item":"核心市占近12個月縮減","lit":true,"text":"CEO 說運算市場擴大稀釋了整體份額；第三方稱 Advantest 的 SoC 份額上升（未核實）"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"事實表沒有提價與銷量資料"},{"item":"EPS成長顯著高於營收成長","lit":true,"text":"前 9 月非 GAAP EPS 年增 235%，營收年增 85%，屬週期性營運槓桿"},{"item":"FCF對淨利低於0.75連2年","lit":false,"text":"FY2023–2025 為 0.95、0.87、0.81，逐年下滑但還沒破線"},{"item":"SBC占營收超過5%且逐年上升","lit":false,"text":"約 1.7%"},{"item":"TAM萎縮或被替代","lit":false,"text":"SEMI 上修測試設備市場"},{"item":"產業估值倍數近3年系統性下移","lit":false,"text":"事實表未涵蓋產業倍數序列"},{"item":"維護性資本支出占FCF超過60%","lit":false,"text":"第三季資本支出 0.86 億對 FCF 2.27 億，總資本支出約占 38%"},{"item":"停止投資新產能且收入下滑","lit":false,"text":"正在擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等。本業再投資優先、帳上淨現金、股權稀釋很低；但回購在高本益比區間執行，收購成效也還沒驗證。","reasoning":"第三季 FCF 2.27 億美元（營業現金流 3.14 億減資本支出 0.86 億），前 9 月 8.06 億，年增近 250%。FCF 對淨利的比率 FY2023–2025 為 0.95、0.87、0.81，逐年下滑，部分是因為擴產期存貨堆高（第三季存貨季增 35%，CFO 說一半是備料、一半對應需求）。SBC 約為 GAAP 營業利益的 5.4%，約營收的 1.7%。現金去向：第一優先是本業，2026 年研發加資本支出近 10 億美元；收購 1.667 億美元（MLTP 合資與 TestInsight）；回購第二季 0.69 億、第三季 0.99 億（第一季事實表未涵蓋）；股利每季 0.20 億。資產負債方面，現金與投資 6.25 億美元，總債務 1.37 億，淨現金約 3.29 億，另有 10 億美元循環額度未動用。三項檢核：收購未滿一年，已實現報酬無法驗證。回購以現價 forward 本益比 29 倍計，盈餘殖利率約 3.4%；10 年期殖利率事實表未涵蓋，但只要高於 1.4%，門檻就會高於 3.4%，這項不過。SBC 淨稀釋為負（回購金額大於 SBC），這項過。","fact_refs":["f_kpi5_313_6_86_3_agent","f_kpi6_sbc_gaap","f_kpi7_non_gaap_eps","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"2026 年 4 月 MLTP 合資與 TestInsight 合計 1.667 億美元。產品測試第三季年增 56%、訂單出貨比 1.4，但收購未滿一年，已實現增量報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"第二季回購 0.69 億、第三季 0.99 億美元，回購均價事實表未涵蓋。以現價 forward 本益比 29.06 倍換算，盈餘殖利率約 3.4%；10 年期殖利率只要高於 1.4% 就不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 約為 GAAP 營業利益的 5.4%（第三季約 0.22 億美元，年化約市值 0.2%）。單季回購 0.99 億大於 SBC，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自本業 AI 測試需求，不是併購；2026 年收購合計 1.667 億美元，約市值 0.4%，不承重"}}}},"q5_valuation":{"verdict":"現價要求 2027–2028 年照共識成長、2029 年只小幅消化。我只信前半段：2027 有積壓訂單撐，2028 以後沒有。價格合理但不便宜，等 1 月展望或更低價格。","reasoning":"現價 274.37 美元，相當於 FY2026 共識 EPS 9.44 的 29.06 倍、FY2027 共識 11.9 的 23.1 倍、FY2028 共識 15.92 的 17.2 倍。兩年共識 EPS 年化約 29.9%，PEG 約 0.97。若終端給 22 倍、要每年賺 8%，FY2031 EPS 要到約 18.3 美元（5 年年化約 14%），等於穿越一次產能消化後仍維持兩位數成長；基本情境只給 16.8，年化約 7%。短期目標：FY2027 EPS 11.6 × 26 倍，約 302 美元（+10%）。中期目標：FY2028 EPS 14.5 × 24 倍，約 348 美元（+27%）。賣方目標價在 8 月時多落在 348～465 美元，資料偏舊；方向上支持上檔，但均值高於本判斷，差別在於有沒有把 2029 年的消化放進來。trailing 本益比 31.54 倍，在 4 個年度端點中位於 26.6% 分位；P/S 8.57 倍與 EV/S 8.5 倍位於約 67% 分位。事實表沒有五年高低點，不計算五年分位；也沒有同業本益比，終端倍數只能對照自身：22 倍低於現值 29 倍，高於 FY2028 共識隱含的 17 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E 非 GAAP 共識）","tier":"雙寡占測試設備","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比，改以自身 forward 本益比、年度端點分位與 PEG 定錨"},"fwd_pe":29.06,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"forward 本益比 29.06 倍，FY2027 為 23.1 倍。兩年共識 EPS 年化約 29.9%（基期只有 GAAP 數字，所以不用三年），PEG 約 0.97。trailing 本益比在 4 個年度端點的 26.6% 分位，P/S 在 67.3% 分位，兩者都不是五年分位。從成長看不貴，從週期高檔的獲利看不便宜，結論是合理、偏中性","upside_short_pct":10,"upside_mid_pct":27,"denominator_disputed":false,"denominator_note":"FY2026 EPS 處於週期高檔，但不是一次性獲利。上半年有不會重複的非營運利益（Q2 法說 CFO），金額事實表未涵蓋"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把 2026 年的 13 億美元高原當成新底部。運算放量已經延後一次，2027–2029 年新增產能集中；若 2027 年成長不到 10%，獲利與倍數會一起往下。","reasoning":"反證依據見反證紀錄的三條。陷阱評級中等：十項衰退信號亮 2 項（整體份額被運算成長稀釋、EPS 成長遠快於營收）。價格面：26 週落後大盤 20.5%，RSI 28.85 已超賣，股價低於 52 週均線 316 美元；但仍在 104 週均線 212 美元與 250 週均線 150 美元之上，250 週均線 13 週斜率 +1.83%，長期趨勢未破。共識面：FY2026 共識 EPS 近 3 個月上修 10.3%，但最近兩份快照之間 FY2026 持平、FY2027 只上修 0.25%，第三季優於預期並沒有再推高後面年度。資料缺口：歷史最大回撤、空方數字，以及法說上三題沒有正面回答（記憶體測試成長倍數、長期份額目標、2027 年相對 WFE 的成長），事實表都沒有落成數字。後兩題指向同一件事：管理層不願對運算份額與 2027 成長給出量化承諾。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高檔獲利與運算份額稀釋"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":9.44,"pe":29.06,"basis":"FY2026E 非 GAAP 共識 EPS 9.44（Koyfin 快照 2026-10-31）除判斷日股價 274.37；終端倍數同樣以終端年當年度的非 GAAP EPS 為分母"},"eps":{"bull":[12.6,17.2,19.5,22.5,26.0],"base":[11.6,14.5,13.5,15.0,16.8],"bear":[10.8,8.0,7.0,8.5,10.0]},"pe":{"bull":26,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.19,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-40,"basis":"熊市路徑谷底 EPS 7 美元，給 17～18 倍為 119～126 美元，對現價約 −54%～−57%；市場會提前反映復甦，深端取 −55%。淺端 −40% 對應 2028 年 EPS 10 美元、給 16～17 倍（160～170 美元）。現價已較 6 月底的 471.96 美元跌約 42%，這段已發生的回撤不計入；歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"2027 營收年增約 30%，第二、三家超大型雲端客戶與 merchant GPU 在 2027 下半年放量，運算份額往 30% 走。HBM、CPO 與實體 AI 機器人在 2028 年後接棒，產能消化只造成成長放緩。終端 26 倍對應仍有約 15% 的成長，低於現值 29 倍","base":"FY2027 EPS 11.6（略低於共識 11.9）；FY2028 為 14.5（低於共識 15.92，運算份額進度只算一半）；2029 年新增產能集中後進入消化，EPS 回落約 7%，之後回到正常成長。終端 22 倍是跨週期中段，低於現值 29 倍","bear":"機率 30%。2027 下半年起 AI 資本支出進入消化，測試占資本支出由 8.1% 回到 7% 以下，運算份額卡在認證階段。營收自高點回落約兩成，2029 年 EPS 跌到 7 美元，2031 年才回到 10 美元。終端 17 倍取成長熄火到 10% 的情境。供需持久證據只蓋到 2028 年，5 年內至少會遇到一次下行，所以熊市機率不低於 30%"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"二手評論指出新增產能集中在 2027–2029；CEO 在 Q2 法說說測試占資本支出 2027 年可能回到 7%；第三季 SoC 季減約 20%，運算是年內最低；CEO 在 Q3 法說承認對手在運算已建立很強的份額","assumption":"基本情境假設 2029 年只回落約 7%，2030 年就恢復成長","consequence":"若下行與份額停滯同時發生，2029 年 EPS 跌到 7 美元，給 17 倍約 120 美元，5 年後虧損約一半","ruling":"採納，放進熊市情境（機率 30%）。這條與 Single Thing 部分重疊：1 月展望若成長不到 10%，等於提前驗證這條路徑","watch":"半導體測試營收季增減、SEMI 測試設備年增率、第二家超大型雲端客戶的採購時點","evidence_refs":["supply_demand_durability#6","competitive_share_entrants#4"],"fact_refs":["f_kpi0_gaap","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"第四季毛利率指引 57.5%～58.5%，低於第三季 59.1%；CFO 提到成本與通膨壓力，以及 2027 下半年的產能擴充費用；記憶體拉低毛利（Q2 法說 CFO）；2026 年研發加資本支出近 10 億美元，存貨半年增約 2 億美元；FPGA 等零件交期拉長","assumption":"份額提升與營收成長會等比例落到每股盈餘","consequence":"營收照劇本成長，但客戶用雙供應商壓價、零件成本上升、產能與存貨占用資金，營業利益率回到 25% 以下，FCF 轉換率下滑，每股價值的成長落後營收","ruling":"部分採納。第三季營業利益率 31.6%、前 9 月 FCF 8.06 億美元仍強，這條還沒發生；以非 GAAP 營業利益率連 2 季低於 26% 作為減碼門檻","watch":"非 GAAP 毛利率與營業利益率、存貨天數（目前 189 天，CFO 說正常約 200 天）、季度 FCF","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi2_non_gaap","f_kpi5_313_6_86_3_agent"]},{"view":"價格已反映太多","evidence":"forward 本益比 29.06 倍，P/S 8.57 倍位於年度端點 67% 分位；SIG 分析師在 Q3 法說指出共識已高於公司自己的目標模型；週期股在獲利高檔給近 30 倍並不便宜","assumption":"市場會維持 FY2027 23 倍以上的倍數，並相信 FY2028 共識 15.92","consequence":"若市場改用跨週期 EPS 定價，倍數壓到 18～20 倍，即使 FY2027 達標，股價也只在 215～240 美元","ruling":"部分反駁。舊目標模型以 130 億美元的 ATE 市場編製，已經過時（CEO 說明），而且股價已較 6 月底跌 42%，FY2027 只剩 23 倍。但基本情境 5 年年化約 7%，價格不算便宜，所以選擇等價格或等證據","watch":"1 月新版目標模型、FY2027 共識是否下修","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 471.96 → 本次 274.37（-41.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=471.96","side_b":"本次 price_at_dd=274.37","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 471.96 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 471.96 美元：Bull 價 665.46、Bear 價 169.91，五年期望值 −13.0%，基準年化 −3.0%，前份未列不對稱比","side_b":"本次情境、股價仍用 471.96 美元：Bull 價 676、Bear 價 170，五年期望值 −18.1%，基準年化 −4.8%，不對稱比 0.56","ruling":"先換情境、股價不動：五年期望值少 5.1 個百分點，基準年化少 1.8 個百分點。前份未列不對稱比，本次為 0.56。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 471.96 美元：五年期望值 −18.1%，基準年化 −4.8%，不對稱比 0.56","side_b":"本次情境、股價 274.37 美元：五年期望值 +40.8%，基準年化 6.1%，不對稱比 3.21","ruling":"再換股價、情境不動：起點價下跌 41.9%，五年期望值多 58.9 個百分點，基準年化多 10.9 個百分點，不對稱比由 0.56 升到 3.21。合計五年期望值比前份多 53.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"運算份額：TER 說在拿份額，對手說沒有掉","cause":null,"prior_field":null,"side_a":"TER（Q3 法說 CEO）：merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中，2026 年在運算份額有顯著進展","side_b":"對手在財報中持續否認掉份額，並增加代工產能；第三方稱 Advantest 的 SoC 份額 CY25 由 56% 升到 66%（未核實）；CEO 也承認運算市場成長稀釋了 TER 的整體份額","ruling":"可調和，屬程度差異。TER 在運算的 socket 數從低基期往上，但運算市場擴大得更快，整體份額可能持平或下滑，2026 年兩邊說法可以同時成立。決勝點在 2027 年 SoC 運算營收增速是否高於市場","evidence_level":"管理層說法加未核實的第三方資料","settle_metric":"2027 年 SoC 運算營收年增率對照 SEMI 測試設備年增率","if_then":["若 2027 年 SoC 運算營收年增比測試設備市場高 10 個百分點以上 → 份額論點成立，牛市機率回到 30%","若低於市場增速 → 份額論點受損，牛市機率降到 20%，停止加碼"],"evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#3","end_markets#3"]},{"axis":"運算放量時點：Q2 說上半年，Q3 改說年中到下半年","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說（Gregory Smith）：運算客戶的下一波高峰預期在 2027 上半年","side_b":"2026-10-28 Q3 法說（Gregory Smith）：第一家超大型雲端客戶下一次大量產在 2027 年中，第二家的產能採購在下半年，ASIC 專案偏下半年；CFO 同時說 2027 每季都會成長，第一季高於第四季","ruling":"可調和。放量往後移一到兩季，但記憶體、汽車工業與產品測試撐住上半年，屬時點風險，論點沒有破。管理層已經延過一次，再延一次就算論點漂移","evidence_level":"兩季法說逐字稿","settle_metric":"2027 第一季營收指引與 SoC 運算季增","if_then":["若 Q4 法說的第一季指引高於第四季實際 → 接受新時程","若第一季指引低於第四季，或第一家量產再延到下半年 → 視同 Single Thing 發生，放棄建倉"],"evidence_refs":[]},{"axis":"測試占半導體資本支出：會回落還是會續擴","cause":null,"prior_field":null,"side_a":"2026-07-29 Q2 法說（Gregory Smith）：比重會落在 7%～9%，2027 年可能回到 7%","side_b":"2026-10-28 Q3 法說（Gregory Smith）：比重由 2025 年 6.4% 升到 2026 前 8 月的 8.1%，條件成熟，ATE 市場會長期擴張","ruling":"可調和。比重由 8.1% 回到 7%，等於少 13.6%，只要半導體資本支出年增約 16% 以上，測試支出就不會縮。SEMI 預測設備銷售 2026→2028 由 1,659 億到 2,295 億美元，年化約 17.6%，剛好在打平線附近。SEMI 的 2027 測試年增 18.1% 數字來源有疑義，不採用。結論是 2027 年測試市場大致持平到小增，不是管理層口中的強勁擴張","evidence_level":"SEMI 預測加兩季法說","settle_metric":"SEMI 年底預測的 2027 測試設備年增率、1 月管理層更新的測試占比","if_then":["若 SEMI 年底預測 2027 測試設備年增 10% 以上 → 維持基本情境","若轉為負成長 → 熊市機率升到 35%，持股減碼一半"],"evidence_refs":["supply_demand_durability#0","end_markets#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價較 6 月底跌 42%，RSI 28.85，26 週落後 20.5%；同期 FY2026 共識 EPS 上修 10.3%，且連續多季優於共識。FY2027 只有 23 倍，FY2028 共識只有 17 倍。能見度由 13 週拉長到兩季，管理層說積壓訂單走強、2027 每季成長。賣方目標價多在 348～465 美元","side_b":"基本情境（2029 年有一次消化）5 年年化只有約 7%；運算放量已延後一次；第四季毛利率指引下滑；共識已高於公司的舊模型","ruling":"選擇觀望、等條件。證據顯示 2027 上半年大概率不差，但便宜的論證建立在 FY2028 共識 15.92 上，這個數字還沒有公司模型背書。1 月 Q4 法說就是決勝點，等兩個月的代價小於追錯週期的代價","evidence_level":"共識快照加法說","settle_metric":"1 月 Q4 法說的 2027 展望與新版目標模型","if_then":["若 1 月展望年增 15% 以上且第一季指引高於第四季 → 建 1/3 首倉，第二季確認後補到 2/3","若 1 月前股價跌到 230 美元以下而共識沒有下修 → 先建 1/3","反向條件：若展望年增低於 10% → 放棄建倉，一季內不再評估"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#1"]},{"axis":"估值、熊市機率、最大回撤與裁決隨價格重算","cause":"價格變動","prior_field":["val","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-06-26，股價 471.96 美元，forward 本益比約 49 倍）：估值偏貴，熊市機率 30%，最大回撤 −60%，觀望","side_b":"本次（股價 274.37 美元，forward 本益比 29.06 倍，FY2027 共識 23 倍）：估值回到合理區，熊市機率維持 30%，最大回撤 −40%～−55%","ruling":"股價跌約 42%，同期 FY2026 共識 EPS 上修 10.3%，估值改善全部來自價格。熊市機率不動，因為週期風險沒有變小；最大回撤區間收窄，是因為有一段已經跌完；裁決與角色由新輸入重算","evidence_level":"公司財報與共識快照","settle_metric":"forward 本益比與 FY2027 共識 EPS","if_then":["若股價回到 230 美元以下且 FY2027 共識沒有下修 → 建 1/3 首倉","若 1 月展望公布前股價反彈到 330 美元以上 → 不追"],"evidence_refs":[]},{"axis":"陷阱風險與牛市機率","cause":"新證據","prior_field":["trap","p_bull_pct"],"side_a":"前份：價值陷阱風險低，牛市機率 30%","side_b":"本次：陷阱風險中等，牛市機率 25%","ruling":"陷阱風險上調有兩個新證據：一是前 9 月非 GAAP EPS 年增 235%、營收年增 85%，EPS 成長遠快於營收，屬營運槓桿的週期性放大；二是 CEO 在 Q3 法說說運算市場長太快，稀釋了 TER 的整體份額。牛市機率下調，是因為運算客戶放量時點後移：Q2 法說說下一波在 2027 上半年，Q3 法說改說第一家年中、第二家下半年，ASIC 專案偏下半年","evidence_level":"法說逐字稿與季報","settle_metric":"2027 上半年 SoC 運算營收季增","if_then":["若 2027 第一季 SoC 運算營收季增 20% 以上 → 牛市機率回到 30%","若第二家超大型雲端客戶的採購延到 2028 → 牛市機率降到 20%，熊市升到 35%"],"evidence_refs":["competitive_share_entrants#4"]},{"axis":"品質、護城河方向與長期跑道（結論不變）","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5"],"side_a":"前份：品質中上，護城河持平，5 年後跑道中等","side_b":"本次：三項結論與前份相同","ruling":"正反兩面的新證據相抵。正面：merchant GPU 進入 fast follower，第二家超大型雲端客戶通過認證，第三家認證中，HBM 疊層變低對 TER 有利。負面：對手在運算的強勢份額，第四季毛利率指引下滑，整體份額被稀釋。第二曲線（CPO、實體 AI 機器人）有管理層說法，但規模小、時程在 2028 年後，跑道不升級","evidence_level":"法說逐字稿與同業利潤率","settle_metric":"2027 年 SoC 運算營收增幅對照 Advantest；CPO 測試市場 2028 年是否落在 3～7 億美元","if_then":["若 2027 年 SoC 運算營收年增 30% 以上且毛利率守住 57% → 護城河方向改為擴大","若最大客戶公開導入第三方替代方案 → 護城河方向改為縮減，停止建倉"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#4"]},{"axis":"公司類型與循環位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：未分類（null）","side_b":"本次：循環型設備股，循環位置在中段","ruling":"前份的框架沒有要求分類。本次歸為循環型，因為 FY2023 營收年減 15%，EPS 隨週期大幅擺動；AI 改變的是週期的振幅與時點，沒有消除週期。循環位置判在中段：營收連三季站在 13 億美元平台，管理層預期 2027 每季成長；但測試占資本支出 8.1%，已在管理層 7%～9% 區間的上半部","evidence_level":"年度財報與法說","settle_metric":"2027 上半年營收逐季變化、測試占資本支出比重","if_then":["若 2027 上半年營收逐季成長，且 SEMI 年底預測維持 2027 測試設備兩位數成長 → 維持中段","若測試占比跌回 7% 且半導體測試連 2 季季減 → 改判晚段，熊市機率調到 35%"],"evidence_refs":[]},{"axis":"重啟建倉條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：未設重啟條件（null）","side_b":"本次：股價 230 美元以下且 FY2027 共識下修不超過 5%，或 1 月 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際 → 首倉建倉 1/3","ruling":"前份判觀望，但沒寫出卡住的條件。本次觀望的約束是價格相對週期風險不夠便宜（基本情境 5 年年化約 7%），重啟條件就是推翻這個約束：要嘛價格便宜到基本情境年化約 10%，要嘛用證據把熊市機率壓下去","evidence_level":"情境樹與法說","settle_metric":"股價與 1 月 Q4 法說展望","if_then":["若兩個條件之一成立 → 首倉建倉 1/3","若股價先到 230 美元，但 1 月展望年增低於 10% → 不建倉，已持有則清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份：未設減碼與清倉門檻（null）","side_b":"本次：半導體測試營收連 2 季季減且下一季指引中值再低 → 減碼一半；2027 營收指引年增低於 10% 或第一季指引低於第四季 → 清倉；非 GAAP 營業利益率連 2 季低於 26% → 減碼一半","ruling":"前份只有監測指標，沒有動作。本次把週期與份額兩條主風險綁到具體動作，門檻取第三季實際值的合理偏離幅度","evidence_level":"季報與法說","settle_metric":"各季財報","if_then":["若任一減碼門檻觸發 → 減碼一半","若清倉門檻觸發 → 清倉，並移出觀察名單一季"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"本次 Single Thing：2027 年 1 月底 Q4 法說給出 2027 營收年增低於 10%，或第一季營收指引中值低於 2026 年第四季實際","ruling":"選 2027 年成長展望，不選單一客戶或出口管制，因為它是 EPS 路徑上數學敏感度最大的一項。發生就清倉，或放棄建倉","evidence_level":"情境樹敏感度","settle_metric":"1 月 Q4 法說","if_then":["若發生 → 清倉，或放棄建倉","若展望年增 15% 以上 → 這個風險解除，改看第二家超大型雲端客戶的時程"],"evidence_refs":[]},{"axis":"營收季減門檻改寫","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份：連 2 季營收環比下滑即警戒；Rubin 認證 TER 出局，或連 2 季 custom-ASIC 份額流失 5pp","side_b":"本次：半導體測試營收連 2 季季減且下一季指引中值再低 → 減碼；第二家超大型雲端客戶的採購延到 2028，或 SoC 運算 2027 年增低於 15% → 份額論點受損","ruling":"第三季總營收 13.06 億美元，較第二季約 13.29 億美元（半導體測試 11.22 億、產品測試 1.07 億、機器人 1.00 億）季減 1.7%；第四季指引中值 13 億美元，再低 0.5%。營收停在高原時，舊門檻會被這種小幅波動觸發，失去區分力，因此改用半導體測試（第三季季減 4.5%）加下一季指引的雙條件。舊門檻提到的具體產品名，在本包證據中無法驗證，改用法說可以追蹤的客戶階段","evidence_level":"季報與法說","settle_metric":"半導體測試季營收與下一季指引","if_then":["若新門檻觸發 → 減碼一半","若第四季實際營收高於 13.06 億美元 → 舊門檻的疑慮解除"],"evidence_refs":["supply_demand_durability#6"]}],"triggers":[{"n":1,"text":"Q4 法說確認 2027 年成長","type":"假設驗證","maps_to":"H1","metric":"2027 營收成長指引、第一季營收指引中值","threshold":"年增 15% 以上，且第一季高於第四季實際","action":"達標則重啟條件成立，建 1/3 首倉","source_freq":"季報（1 月底）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"第二家超大型雲端客戶下產能單","type":"假設驗證","maps_to":"H2","metric":"法說客戶階段說明、SoC 運算營收季增","threshold":"2027 第三季財報前出現產能採購","action":"出現則加碼到 2/3；延到 2028 則牛市機率降到 20%","source_freq":"季報","date":"2027-10","evidence_refs":["competitive_share_entrants#4"]},{"n":3,"text":"產品組合撐住獲利率","type":"假設驗證","maps_to":"H3","metric":"非 GAAP 毛利率、非 GAAP 營業利益率","threshold":"毛利率 57% 以上，營業利益率 28% 以上","action":"守住則維持；跌破見減碼列","source_freq":"季報","date":null,"evidence_refs":[]},{"n":4,"text":"半導體測試連續季減","type":"風險","maps_to":"R2","metric":"半導體測試季營收","threshold":"連 2 季季減，且下一季指引中值再低","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#6"]},{"n":5,"text":"客戶集中度惡化","type":"風險","maps_to":"R3","metric":"前五大客戶營收占比、單一客戶應收占比","threshold":"前五大超過 50%，或單一客戶應收超過 25%","action":"倉位上限降一級，停止加碼","source_freq":"年報","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0"]},{"n":6,"text":"出口管制與零組件成本吃掉毛利","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率與公司歸因、美國出口規則","threshold":"毛利率跌破 57% 且歸因零件或關稅，或新禁令涵蓋測試機","action":"停止加碼，重估熊市機率","source_freq":"季報與法規公告","date":null,"evidence_refs":["reg_tariff_export#1","supply_demand_durability#3","regulatory_antitrust#1"]},{"n":7,"text":"Single Thing：2027 展望不及","type":"Single Thing","maps_to":"Single Thing","metric":"2027 營收成長指引、第一季指引","threshold":"年增低於 10%，或第一季指引中值低於第四季實際","action":"已持有則清倉，未持有則放棄建倉","source_freq":"Q4 法說","date":"2027-01","evidence_refs":[]},{"n":8,"text":"價格回到重啟區","type":"估值rearm","maps_to":"H1","metric":"股價、FY2027 共識 EPS","threshold":"230 美元以下，且 FY2027 共識下修不超過 5%","action":"建 1/3 首倉","source_freq":"每日","date":null,"evidence_refs":[]},{"n":9,"text":"首倉後加碼","type":"加碼","maps_to":"H2","metric":"2027 第一季營收季增、非 GAAP 毛利率","threshold":"第一季營收季增，且毛利率 57% 以上","action":"加碼到 2/3","source_freq":"季報","date":"2027-04","evidence_refs":[]},{"n":10,"text":"獲利率失守","type":"減碼","maps_to":"H3","metric":"非 GAAP 營業利益率","threshold":"連 2 季低於 26%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":[]},{"n":11,"text":"週期反轉","type":"清倉","maps_to":"R2","metric":"半導體測試營收年增率、第二家超大型雲端客戶時程","threshold":"半導體測試連 2 季年減 20% 以上，或第二家超大型雲端客戶退回認證階段","action":"清倉","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#6"]},{"n":12,"text":"Q4 法說後全份重評","type":"複審日期","maps_to":null,"metric":"整份判斷重跑","threshold":"Q4 法說與新版目標模型公布後","action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"半導體測試季營收連續季減","bear_threshold":"連 2 季季減且下一季指引中值再低 → 減碼一半","window":"2027 年每季財報","source":"公司季報新聞稿 Exhibit 99.1","last_status":"warning"},{"metric":"2027 年營收成長指引與第一季指引","bear_threshold":"年增低於 10% 或第一季指引中值低於 2026 第四季實際 → 清倉或放棄建倉","window":"2027 年 1 月底 Q4 法說","source":"Q4 2026 法說與新版目標模型","last_status":"unknown"},{"metric":"非 GAAP 營業利益率","bear_threshold":"連 2 季低於 26% → 減碼一半","window":"2027 全年各季","source":"季報非 GAAP 對帳表","last_status":"ok"},{"metric":"前五大客戶營收占比、單一客戶應收占比","bear_threshold":"前五大超過 50% 或單一客戶應收超過 25% → 停止加碼","window":"FY2026 年報（2027-02）","source":"10-K Item 1A 與 7A","last_status":"warning"},{"metric":"第二家超大型雲端客戶產能採購","bear_threshold":"2027 第三季財報前仍未出現，或延到 2028 → 牛市機率降到 20%","window":"至 2027-10","source":"季度法說的客戶階段說明","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這條出自 FY2018 年報的舊敘述（產品與零件越來越多在中國生產），已被之後把半導體製造遷出蘇州的事實取代，現行製造以馬來西亞代工為主。它描述的是七年前的供應鏈結構，不代表目前曝險；目前的供應鏈曝險已由馬來西亞代工與單一來源零件兩條證據承接，列在第四條風險"}],"action_conditions":{"rearm_trigger":"股價≤230美元且FY2027共識下修不超過5%，或1月Q4法說確認2027營收年增≥15%且第一季指引高於第四季實際","exec_line":"條件成立先建 1/3 首倉；2027 第一季營收季增且毛利率在 57% 以上，再補到 2/3；第二家超大型雲端客戶下產能單才建滿。半導體測試連 2 季季減，則停止加碼並減碼一半"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把第三季 SoC 季減約 20% 與第四季毛利率指引下滑當成見頂訊號，股價較 6 月底跌 42%。但同期 FY2026 共識 EPS 上修 10.3%，管理層也說積壓訂單走強、2027 每季成長、第一季高於第四季。若 2027 上半年兌現，現價只有 FY2027 EPS 的 23 倍，是過度折價；兌現之前只算部分理由","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 1 月底 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際；或股價回到 230 美元以下（約 FY2027 共識的 19 倍），且共識下修不超過 5%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把第三季 SoC 季減約 20% 與第四季毛利率指引下滑當成見頂訊號，股價較 6 月底跌 42%。但同期 FY2026 共識 EPS 上修 10.3%，管理層也說積壓訂單走強、2027 每季成長、第一季高於第四季。若 2027 上半年兌現，現價只有 FY2027 EPS 的 23 倍，是過度折價；兌現之前只算部分理由"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-20.51, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年 1 月底 Q4 法說確認 2027 營收年增 15% 以上且第一季指引高於第四季實際；或股價回到 230 美元以下（約 FY2027 共識的 19 倍），且共識下修不超過 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 帶動的測試需求讓 2027 年營收繼續成長，季營收脫離 13 億美元平台","2y":"FY2027 營收 60 億美元以上（較 2026 年約 52 億成長至少 15%），且 2027 每季營收不低於前一季（CFO 第三季法說的說法）","5y":"2030 年前 ATE 市場達 200 億美元以上（管理層說法），TER 營收 75 億美元以上","10y":null,"threshold":"FY2027 營收年增至少 15%，第一季營收高於第四季","source":"公司季報新聞稿、Q4 2026 法說的 2027 展望與新版目標模型、SEMI 設備預測","drift_rule":"以 TTM 營收對照 2 年路徑：連 2 季落後 5% 以上視為削弱，連 3 季落後 10% 以上視為反轉"},{"id":"H2","text":"運算 SoC 份額靠客戶的雙供應商策略往上走：merchant GPU 與第二家超大型雲端客戶在 2027 下半年轉成產能採購","2y":"2027 年內第二家超大型雲端客戶下產能單，merchant GPU 營收高於 2026，第三家完成認證；SoC 運算營收 2027 年增至少 30%","5y":"在運算 fast follower 客戶拿到約 30% 份額（Q2 法說管理層描述的上限）","10y":null,"threshold":"2027 第三季財報前出現第二家超大型雲端客戶的產能採購","source":"季度法說的客戶階段說明、SoC 運算營收增幅揭露","drift_rule":"2 年期：客戶時程連 2 季延後視為削弱；連 3 季延後，或客戶退回認證階段，視為反轉"},{"id":"H3","text":"產品組合夠廣，撐得住獲利率，運算訂單時點的波動不至於壓垮獲利","2y":"2027 年每季非 GAAP 毛利率 57% 以上，非 GAAP 營業利益率 28% 以上","5y":"跨週期（含一個下行年）GAAP 營業利益率平均 22% 以上（FY2022–2025 介於 19.5%～26.9%）","10y":null,"threshold":"非 GAAP 營業利益率連 2 季低於 26%，即視為論點受損","source":"季報新聞稿的非 GAAP 對帳表","drift_rule":"2 年期：連 2 季低於門檻 5% 以上視為削弱，連 3 季低於 10% 以上視為反轉；5 年期看 TTM 連 4 季偏離"}],"R":[{"id":"R1","text":"Advantest 守住運算主場，TER 的雙供應商進度卡在認證或小量出貨","h_ref":"H2","clock":"🔥","threshold":"第二家超大型雲端客戶的產能採購延到 2028，或 SoC 運算營收 2027 年增低於 15%","evidence_refs":["competitive_share_entrants#4"]},{"id":"R2","text":"2027–2029 新增產能集中後，AI 資本支出進入消化，測試占半導體資本支出由 8.1% 回落","h_ref":"H1","clock":"⚡","threshold":"半導體測試營收連 2 季季減（第三季已季減 4.5%），且下一季指引中值再低","evidence_refs":["supply_demand_durability#6"]},{"id":"R3","text":"客戶集中：前五大占 44%（2023 年 32%），單一客戶占 19%，兩家客戶分占應收 22% 與 20%，幾乎沒有合約保障","h_ref":"H1","clock":"🔥","threshold":"前五大占比超過 50%，或最大客戶下修、延後訂單","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"出口管制、232 關稅與供應鏈（馬來西亞代工、單一來源零件、FPGA 交期拉到 52 週）推高成本或卡住出貨","h_ref":"H3","clock":"🔥","threshold":"非 GAAP 毛利率跌破 57% 且公司歸因零件或關稅，或新出口禁令涵蓋測試機","evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3","geo_supply_chain#5","supply_demand_durability#3"]},{"id":"R5","text":"替代技術與新進者：系統級測試等相鄰測試層、新興亞洲廠、客戶自製","h_ref":"H2","clock":"🐢","threshold":"大客戶公開導入自製測試，或亞洲廠拿到高階 SoC 量產機台訂單","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]}],"single_thing":{"description":"2027 年 1 月底的 Q4 法說，2027 年展望給出營收年增低於 10%，或第一季營收指引中值低於 2026 年第四季實際","why_fatal":"2027 年成長是 EPS 路徑上最大的單一敏感項。FY2027 EPS 若由 11.6 降到約 9.5（持平），倍數會同步從 23 倍壓到 18～20 倍，股價落在 170～190 美元，比現價低三成以上，也代表 2026 年就是週期高點","if_happens":"放棄建倉；已持有則清倉，改列循環交易觀察，等半導體測試營收連 2 季季增再重評","how_monitor":"Q4 法說的營收展望、第一季指引與新版目標模型；事前看 UBS 會議與 SEMI 年底預測的口徑","probability":"25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.06,"peg_fy2":0.68,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":3.47,"FY2026E":9.44,"FY2027E":11.9,"FY2028E":15.92},"fy_end_month":12,"eps_basis":"共識為非 GAAP 稀釋 EPS（Koyfin 快照 2026-10-31）。基期 FY2025A 的 3.47 是 GAAP 稀釋 EPS，因為事實表沒有 FY2025 全年非 GAAP 值；用這個基期算三年 CAGR 會高估，判斷改用 FY2026E→FY2028E 的兩年 CAGR，約 29.9%"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報、新版目標獲利模型（以更大的 ATE 市場重編）與 2027 年展望","impact":"高","watch":"2027 營收成長指引、第一季指引是否高於第四季、新模型的營收與營業利益率目標"},{"date":"2026-12","date_precision":"month","type":"other","event":"UBS 科技投資人會議（管理層出席）","impact":"低","watch":"運算客戶時程與產能計畫的口徑有沒有改變"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"完成對 FormFactor 的投資（待主管機關核准）","impact":"中","watch":"投資金額，以及光學測試合作的實際產品"},{"date":"2026-12","date_precision":"month","type":"macro","event":"SEMI 年底設備預測（2027 年測試設備年增率）","impact":"中","watch":"2027 年測試設備是否維持兩位數成長"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 年報揭露前五大客戶占比與應收集中度","impact":"中","watch":"前五大是否超過 50%、單一客戶應收是否超過 25%"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"第二家超大型雲端客戶的產能採購；第一家年中的下一波量產","impact":"高","watch":"SoC 運算營收季增，以及管理層的客戶階段說明"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
