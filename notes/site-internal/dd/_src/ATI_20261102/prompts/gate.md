你是 DD 管線 v20 的判斷層閘（gate），標的 ATI（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
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
- `f_kpi7_guidance_fy2026`（q1_business）｜Guidance：FY2026（上修）＝Adj EBITDA 1,135–1,185M；Adj EPS 4.90–5.18；Adj FCF 550–600M USD｜期間與口徑：Q2 2026 新聞稿（2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026 新聞稿（2026-08-06））
  - 註記：本站 FY1 EPS 共識 5.12（2026-10-08 快照，位於指引區間內）
- `f_peer_ati_gross_margin_pct`（q2_moat）｜ATI 毛利率＝24.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ati_operating_margin_pct`（q2_moat）｜ATI 營業利益率＝16.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_crs_operating_margin_pct`（q2_moat）｜CRS 營業利益率＝23.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hwm_operating_margin_pct`（q2_moat）｜HWM 營業利益率＝28.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ati_fcf_margin_pct`（q2_moat）｜ATI FCF 利潤率＝8.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_crs_fcf_margin_pct`（q2_moat）｜CRS FCF 利潤率＝10.69 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hwm_fcf_margin_pct`（q2_moat）｜HWM FCF 利潤率＝19.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cstm_operating_margin_pct`（q2_moat）｜CSTM 營業利益率＝8.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CSTM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mtrn_operating_margin_pct`（q2_moat）｜MTRN 營業利益率＝6.35 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTRN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.21 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.43 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝7.52 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝16.82 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 4.46 → 5.21（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5296.83 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（4 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5763.39 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_adjusted_free_cash_flow`（q1_business）｜Adjusted free cash flow＝68.6 USD M｜期間與口徑：Q2 2026（季末 2026-06-28，公告 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；營業現金流 131.8M，capex 68.6M（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-28，公告 2026-08-06））
  - 註記：未取得
- `f_kpi4_sbc_0_6`（q4_capital）｜SBC（上半年累計，占上半年營收約 0.6%）＝14.1 USD M｜期間與口徑：2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 2026 新聞稿（8-K EX 99.1）；占比 = 14.1 ÷ (1,261.1+1,151.5)（numbers.latest_quarter_kpis.items[4]，as_of 2026 上半年（至 2026-06-28，公告 2026-08-06）；新聞稿未單列 Q2）
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1415.2 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 1857.5、現金 442.3（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝135.82 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝165.59 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝31.78 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.21，分子＝快照價 165.59｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝41.4 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝98.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝98.4 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.49 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.77 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝6.65 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝38.52｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 165.59 / W52 160.1 / W104 114.41 / W250 71.17 / W250 13週斜率 3.67%」

### findings_digest 中方向為負或來源衝突的條目（16 條）
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
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露 2024-08 起的退休金年金合約（Athene）集體訴訟；2025-08 聽證後 magistrate judge 建議以無訴訟資格駁回，待主審法官裁定；公司無法估計損失範圍。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：decision_inputs.bear
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：同業 Carpenter Technology 的 Athens 棕地擴建（約 9,000 噸、含新 VIM 爐）預計於 FY2028 開始前完成，進度與預算符合預期
  - 來源：Nasdaq/Zacks 與 MarketBeat Carpenter Q2 call highlights（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Argus 報導：ATI 在 Monroe NC 第五座 VIM 爐約增 9,000 噸/年，2027 下半年啟用；另提 Doncasters 5,000 萬美元超合金廠及 SMP 增爐增壓機；合金業者預期新產能 2027 末至 2030 逐步爬坡
  - 來源：Argus Media, Jet engines driving nickel, PQ titanium demand（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#3`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Argus：空巴波音去庫存拖累 ATI 2Q 鈦銷售（2025 Q2，預期2026年復甦）
  - 來源：Argus Media（as_of 2025-08-01）｜affects：thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2020疫情下行期：Q3 2020 HPMC航太國防銷售年減55%（商用航太-64%），Q3 ATI調整後EBITDA僅16.6百萬美元、占銷售2.8%。
  - 來源：ATI Q3 2020 results / 10-Q (SEC)（as_of 2020-10-30）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2020全年銷售29.8億美元，調整後EBITDA 196.3百萬美元（6.6%）；Q4 HPMC商用航太銷售-68%，HPMC段EBITDA率3.4%（前年同期18.7%）；管理層稱Q4營收季增10%為最差已過的跡象。
  - 來源：ATI Q4/FY2020 results (metal-am.com)（as_of 2021-01-28）｜affects：thesis.R、decision_inputs.bear、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：退休金年金合約集體訴訟（W.D. Pa.），已提駁回動議，magistrate 建議駁回，待主審法官裁定。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-20）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":302.4,"bear_5y_price":75.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":14.3,"ev5y_pct":10.7,"irr_base_pct":2.7,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.21,"pe":31.78,"basis":"FY1（FY2026E）調整後 EPS 共識5.21（2026-10-31 快照），現價165.59；終端倍數同樣套在當年度調整後 EPS"},"eps":{"bull":[6.7,8.0,9.1,10.0,10.8],"base":[6.35,7.2,7.85,8.3,8.6],"bear":[5.8,5.2,4.5,4.3,4.7]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ATI_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：CFO 公布上調後全年調整後 EBITDA 區間（原話："range of $1.135 billion to $1.185 billion."）
- 2026-08-06｜CFO｜guidance：CFO 給 Q3 調整後 EBITDA 區間 305–315 百萬美元與 EPS 區間（原話："$315 million, translating to adjusted EPS of $1.31 to $1.37."）
- 2026-08-06｜CFO｜guidance：CFO 說明財測中點隱含 Q4 EBITDA 約 3.35 億美元（原話："approximately $335 million of EBITDA in Q4."）
- 2026-08-06｜CFO｜guidance：CFO 稱 Q4 為 2026 年銷售與獲利最強的一季（原話："as our strongest quarter of 2026 for sales and profit"）
- 2026-08-06｜CFO｜guidance：CFO 表示不提供 2027 財測（原話："While we are not providing 2027 guidance today"）
- 2026-08-06｜CFO｜guidance：CFO 給全年調整後自由現金流區間（中點調升 8,000 萬）（原話："range between $550 million and $600 million."）
- 2026-08-06｜CFO｜guidance：CFO 給全年總資本支出區間不變（原話："prior guidance at $280 million to $300 million."）
- 2026-08-06｜CEO｜guidance：CEO 維持噴射引擎全年營收高十位數成長（原話："high teens jet engine revenue growth for the full year."）
- 2026-08-06｜CEO｜guidance：CEO 維持機身全年中至高個位數成長、下半年加重（原話："mid- to high single-digit full year airframe revenue growth"）
- 2026-08-06｜CEO｜guidance：CEO 將國防全年成長預期上調至高十位數（原話："expectation for full year defense growth to the high teens"）
- 2026-08-06｜CEO｜guidance：CEO 維持特殊能源全年中十位數成長（原話："mid-teens Specialty Energy revenue growth for the full year."）
- 2026-08-06｜CFO｜margin：CFO 給全年合併 EBITDA 利潤率落在 20% 出頭（原話："adjusted EBITDA margins now projected in the low 20% range."）
- 2026-08-06｜CFO｜margin：CFO 將全年合併增量利潤率預期由 40% 提高到 50%（原話："in the range of 50%. This is an improvement over the 40%"）
- 2026-08-06｜CFO｜margin：CFO 將 AA&S 全年利潤率由上季的高十幾%上調至 20% 出頭（原話："an improvement over the upper teens level we"）
- 2026-08-06｜CFO｜margin：CFO 稱 HPMC 全年 EBITDA 利潤率維持 20% 中段（原話："for HPMC in the mid-20% range, consistent with our outlook"）
- 2026-08-06｜CFO｜margin：CFO 於備稿中稱 AA&S EBITDA 利潤率前瞻為持續高於 20%（原話："we see AA&S EBITDA margins consistently above 20%"）
- 2026-08-06｜CEO｜margin：CEO 於問答中稱 AA&S 往後可達 20% 中段（原話："we can see AA&S in the mid-20% range going forward."）
- 2026-08-06｜CEO｜margin：CEO 說明剔除資產出售利益後 AA&S 的底層利潤率口徑（原話："an underlying EBITDA margin of approximately 22%"）
- 2026-08-06｜CEO｜margin：管理層拆解 Q2 EBITDA 超標數字時扣除 AA&S 資產出售利益（原話："Excluding a $10 million asset sale gain"）
- 2026-08-06｜CFO｜margin：CFO 報告 AA&S Q2 利潤率年增 930 bp（原話："Segment margin expanded 930 basis points to an all-"）
- 2026-08-06｜CFO｜margin：CFO 報告 HPMC Q2 利潤率 24.1%（原話："basis points from the same period last year to 24.1%."）
- 2026-08-06｜CEO｜margin：CEO 量化 HPMC 由上半年遞延到下半年的營收規模（原話："around $30 million to $40 million of revenue that moved"）
- 2026-08-06｜CFO｜margin：CFO 說明海軍核能新合約拆分為 2/3 價格組合、1/3 數量（原話："2/3 price mix, 1/3 volume in that contract."）
- 2026-08-06｜CFO｜margin：CFO 稱新合約的量價較預期早入帳於 AA&S（原話："financials a bit earlier than we were anticipating."）
- 2026-08-06｜CFO｜commitment：CFO 稱 HPMC 展望建立在已簽約訂單上（原話："contracts in place. This is not speculative."）
- 2026-08-06｜CFO｜commitment：CFO 重申自由現金流轉換率目標在 90% 以上（原話："free cash flow conversion at 90% or greater"）
- 2026-08-06｜CEO｜commitment：CEO 承諾各項新增產能投資須達內部 30% 報酬門檻（原話："have to meet our 30% return thresholds internally"）
- 2026-08-06｜CEO｜commitment：CEO 稱先榨取既有資產再投資新產能（原話："before we invest in new capacity"）
- 2026-08-06｜CEO｜commitment：CEO 預告今年稍後召開投資人日（原話："We look forward to sharing more at our Investor Day"）
- 2026-08-06｜CEO｜commitment：CEO 說明鎳熔煉擴產新 VIM 爐時程（原話："new VIM furnace coming online by the end of 2027"）
- 2026-08-06｜CEO｜commitment：CEO 稱鎳投資將於 2028 前帶來約 3.5 億美元增量年營收（原話："we will deliver approximately $350 million of"）
- 2026-08-06｜CFO｜capital_allocation：CFO 稱庫藏股是增量自由現金流的優先用途（原話："We view them as the most efficient way to return capital to"）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告庫藏股剩餘授權額度（原話："we have $495 million remaining"）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告 Q2 資本支出中客戶直接出資的部分（原話："including $23 million funded directly by customers."）
- 2026-08-06｜CFO｜capital_allocation：CFO 報告 Q2 管理營運資金占營收比（原話："percentage of sales at the end of Q2 was 34%"）
- 2026-08-06｜CFO｜capital_allocation：CFO 提到推動鍛造原料客戶寄售以改善營運資金（原話："customer consignment strategy for forging input material"）
- 2026-08-06｜CEO｜risk：CEO 說明 HPMC 因墨西哥新廠與 EB2 認證時程使部分出貨遞延（原話："qualification timing at"）
- 2026-08-06｜CFO｜risk：CFO 解釋 EBITDA 上調幅度大於自由現金流上調的兩個原因之一為應收帳款時點（原話："it's the timing of conversion through accounts receivable."）
- 2026-08-06｜CFO｜risk：CFO 表示為 2027 年初備貨而增加庫存（原話："we do plan on a little bit more inventory as we prepare"）
- 2026-08-06｜CEO｜customer：CEO 報告記錄訂單餘額與年增、季增（原話："another record $4.4 billion. That's up 18% year-over-year"）
- 2026-08-06｜CEO｜customer：CEO 稱約 70% 在手訂單預期於未來 12 個月轉為營收（原話："About 70% of that backlog we expect to convert"）
- 2026-08-06｜CEO｜customer：CEO 給鎳合金交期（原話："about 12 months on nickel alloys"）
- 2026-08-06｜CEO｜customer：CEO 給優質鈦交期（原話："20 months on the premium quality titanium"）
- 2026-08-06｜CEO｜customer：CEO 給等溫鍛件交期（原話："above 24 months on isothermal forgings"）
- 2026-08-06｜CFO｜customer：CFO 說明海軍核能新合約規模與期限（原話："essentially a $1 billion revenue contract over 5 years."）
- 2026-08-06｜CEO｜customer：CEO 稱海軍核能續約延至 2030 並改善價格與組合（原話："through 2030 with improved pricing and product mix."）
- 2026-08-06｜CEO｜customer：CEO 稱已開始收到戰斧飛彈計畫訂單（原話："receiving orders in support of the Tomahawk program."）
- 2026-08-06｜CEO｜customer：CEO 稱飛彈相關營收季成長 4 倍（原話："That revenue is up 4x in the quarter."）
- 2026-08-06｜CEO｜customer：CEO 稱機身訂單簿已延伸到 2027（原話："we've got order books now extending into 2027"）
- 2026-08-06｜CEO｜competition：CEO 稱 ATI 是西方僅三家合格高純度鉿鋯生產商之一（原話："1 of 3 qualified producers in the Western"）
- 2026-08-06｜CEO｜competition：CEO 提到中國限制出口與 ATI 能力價值的關聯（原話："With China limiting exports to these markets"）
- 2026-08-06｜CEO｜competition：CEO 稱 ATI 生產 7 種最先進鎳基超合金中的 6 種（原話："produce 6 of the 7 most advanced nickel-based super alloys"）
- 2026-08-06｜CEO｜product：CEO 稱新世代引擎上的 ATI 含量為舊平台兩倍以上（原話："than double that of legacy platforms"）
- 2026-08-06｜CEO｜product：CEO 報告 Elevation 帶來的產能提升（原話："throughput by 30% in ultrasonic inspection, 15% in"）
- 2026-08-06｜CEO｜product：CEO 稱 AA&S 的 A&D 占比往後維持並可能上升（原話："mix of A&D continues to stay at that level and it will"）

### ATI_Shareholder_Analyst_Call_ATI_Inc_20260514.md
- 2026-05-14｜Robert S. Wetherbee｜risk：執行董事長 Wetherbee 表示這是他擔任董事長的最後一次正式行動（領導層交接）。（原話："This is my last official act as the Executive Chairman"）
- 2026-05-14｜Robert S. Wetherbee｜risk：Kim Fields 自即日起兼任董事會主席，並仍為總裁暨 CEO。（原話："Fields as President, CEO, and, as of now, Board Chair."）
- 2026-05-14｜Robert S. Wetherbee｜competition：Wetherbee 稱團隊已轉型並成為有差異化的市場領導者（無數字佐證）。（原話："differentiated itself as a market leader."）
- 2026-05-14｜Robert S. Wetherbee｜product：Wetherbee 以航空應用說明 ATI 產品的重要性（無細節）。（原話："And you can't fly without ATI either."）

### 問答異常語氣（迴避／改口／保留）
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：David Strauss 問 2027 是否可沿用 50% 增量利潤率、Q4 運行率是否有一次性因素｜答法：CFO 未給 2027 數字，稱「directionally makes sense」並說 40–50% 增量區間合理，但明說不給 2027 細部指引
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：Richard Safran 追問 AA&S 利潤率潛力是否願給更具體數字｜答法：備稿中 CFO 稱「consistently above 20%」，問答中 CEO 改稱「mid-20% range going forward」，同一場說法由 20% 以上變為 20% 中段
- ATI_Q2_2026_Earnings_Call_20260806.md｜問：Seth Seifman 問是否會在 Slide 6 之外增加產能投資及決策方式｜答法：CEO 談 Elevation 與 30% 報酬門檻，未點名 Slide 6 以外的新增產能項目或金額

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 7 | 4 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 2 | 3 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 2 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","irr_base_pct":3.5,"ev5y_pct":12.4,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.2,"ev5y_pct":12.4,"irr_base_pct":3.5,"max_dd_pct":-65,"bull_5y_price":348.0,"bear_5y_price":79.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","price_at_dd":187.98,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ATI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ATI Inc."},"oneliner":"Q3 第三次上修、引擎合金定價權擴大，但倍數仍在自身區間頂部，業界新產能2027下半年起投產；不追，等股價≤154美元且2027指引 EBITDA 中點≥13億美元","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺航太引擎與機身 OEM、國防與核能客戶的錢；錢卡在經過認證的熔煉與鍛造產能，ATI 靠熱段合金獨家或雙源供應拿到定價權，產業處擴張期","reasoning":"賺誰的錢：引擎與機身 OEM、國防與核能客戶。Q3（10-Q 與2026-10-29 法說）營收14.2億美元、年增26%，航太國防近七成；噴射引擎年增39%、約占全公司四成，新機與維修各半，且同件同價同利。分部：HPMC 7.21億美元（年增20%，利益率23.2%），AA&S 7.02億美元（年增34%，利益率25.8%）。TTM 毛利率24.5%、營益率16.5%；Q2 單季 GAAP 營業利益2.2億美元。錢卡在經過認證的熔煉與鍛造產能：優質鈦交期20個月、等溫鍛件逾24個月，管理層稱本季增幅約三分之二來自價格與組合。產業時鐘判擴張期：OEM 產量仍低於目標（A320 月產75架延至2027年）、交期拉長、新產能2027下半年才投產，尚未見供給過剩。供需持久性：需求端偏結構（新世代引擎含量為舊引擎兩倍以上），供給緊俏屬週期性、可逆性中高。單點依賴：HPMC 約92%營收來自航太國防，客戶為少數引擎與機身 OEM，但無單一客戶超過10%。產業態勢雙向拉鋸：競爭面 Carpenter、Doncasters、SMP 與 ATI 自身新產能陸續投產，結構面有長約、客戶出資擴產與 AA&S 組合轉向，其他變數為中國出口管制推升鉿鋯價格。","fact_refs":["f_kpi0_sales_gaap","f_kpi1_adjusted_ebitda_non_gaap","f_kpi2_operating_income_gaap","f_kpi5_backlog","f_kpi7_guidance_fy2026","f_peer_ati_gross_margin_pct","f_peer_ati_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"長約為主，價格與組合貢獻約三分之二增幅；航太國防近七成，HPMC 航太國防占93%；2026 年連三次上修，在手訂單43億美元、年增20%（Q2 為44億），約七成可在12個月內轉營收","unit_econ_note":"同一鍛件用於新機或維修同價同利；新世代引擎單機含量為舊引擎兩倍以上；全年合併增量利潤率約50%，新合金爬坡使 HPMC 本季利益率少約200基點","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"航太材料認證門檻加交期驅動的定價循環：2020 年 HPMC 航太國防銷售年減55%，2026 年價格與組合貢獻約三分之二增幅"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏結構：需求端有新世代引擎含量翻倍、維修與新機各半、Airbus 2025 年底積壓8,754架支撐；供給緊俏屬週期，ATI、Carpenter、Doncasters、SMP 新產能2027下半年至2030投產，可逆性中高","bargaining":{"up":"上游鎳、海綿鈦、鈷、鉻鐵多家供應，但來源含哈薩克、中國、沙烏地等地，中國出口管制可能延誤取得；ATI 已能回收一項難以取得的關鍵原料、支應多數需求","down":"下游為 GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran 與 Boeing、Airbus 等少數大客戶，無單一客戶逾10%；交期20–24個月讓客戶以較高價格與出資擴產換取產能","geo":"生產基地以美國為主，部分原料須進口；2025 年關稅年化曝險約5,000萬美元，經轉嫁與退稅影響極小（2026 年數字事實表未涵蓋）"},"profit_pool_dir":"短期往材料端移動（交期拉長、客戶出資擴產、鉿鋯漲價）；2027末至2030新產能爬坡後可能回流 OEM 與零件端","tam_table":{"expanded":false,"reason":"事實表未收 TAM、滲透率與利潤池歷史；成長以 OEM 產量、單機含量與交期判斷，不靠滲透率承重"}}}},"q2_moat":{"verdict":"護城河向上、等級 B：認證門檻與稀缺產能讓定價權擴大，但利益率仍低於 Carpenter 與 HWM，部分定價屬週期性緊俏","reasoning":"機制是認證門檻加稀缺產能：熱段六種非自製先進鎳基超合金 ATI 全部能產，其中五種獨家供應，今年新合金9個月完成認證並成為全球兩家之一（Q3 法說）；鉿鋯為西方三家合格廠之一（Q2 法說）。同業報酬率差無法取得，改用定價軸：交期拉長、長約重新定價、客戶出資擴產，定價力擴大；執行力持平，墨西哥廠與 Richland 爐認證延宕、新合金爬坡拖累 HPMC 約200基點。TTM 營益率 ATI 16.5%，低於 Carpenter 23.4%、HWM 28.0%，利益率差為負，評分封頂在 B。威脅都屬點對點：Carpenter 擴產、業界2027–2030新產能、積層製造。持續期四檢查點三綠一黃，弱點在價值鏈分配；增量報酬無法計算，管理層宣稱的30%報酬門檻未經驗證。","fact_refs":["f_peer_ati_operating_margin_pct","f_peer_crs_operating_margin_pct","f_peer_hwm_operating_margin_pct","f_peer_ati_gross_margin_pct","f_peer_ati_fcf_margin_pct","f_peer_crs_fcf_margin_pct","f_peer_hwm_fcf_margin_pct","f_peer_cstm_operating_margin_pct","f_peer_mtrn_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"認證門檻加稀缺產能：熱段六種非自製先進鎳基超合金全部能產、五種獨家，優質鈦與等溫鍛件交期逾20個月，客戶要排隊或出資才拿得到產能","execution":7,"pricing":8,"grade":"B","trend":"↑","trend_evidence":"定價力擴大：管理層稱本季增幅約三分之二來自價格與組合，優質鈦交期20個月、等溫鍛件逾24個月，客戶出資擴產，海軍核能合約以較佳價格續約至2030；執行力持平：新合金9個月完成認證並擴大市占，但墨西哥廠與 Richland 爐認證延宕、新合金爬坡拖累 HPMC 約200基點。對 Carpenter 營益率低6.8個百分點，差距近年是否收窄事實表未涵蓋；定價力有一部分屬供給緊俏的週期成分","competitor_notes":[{"name":"HWM","strategy_note":"下游鍛鑄件龍頭，TTM 營益率28.0%、FCF 利潤率19.8%，比 ATI 高約11.5個百分點，顯示價值鏈下游零件端拿走較多利潤；同時是鈦合金的直接對手"},{"name":"CRS","strategy_note":"鎳基與特殊鋼最直接的對手，TTM 營益率23.4%、高 ATI 6.8個百分點；2026 資本支出2.2–2.4億美元投向引擎合金，Athens 擴建 FY2028 前完工，是2028年後價格壓力的主要來源"},{"name":"CSTM","strategy_note":"鋁材加工，營益率8.7%，屬不同材料層級，不構成熱段合金替代，只作利益率下緣參照"},{"name":"MTRN","strategy_note":"特用合金與先進材料，營益率6.4%，與 ATI 核心引擎合金重疊有限"},{"name":"Precision Castparts","strategy_note":"隸屬 Berkshire 的垂直整合鍛鑄廠，10-K 列為競爭者，財務未公開、事實表無數據"}],"threats":[{"level":"🟡","text":"Carpenter 2026 資本支出2.2–2.4億美元投向引擎合金，Athens 擴建約9,000噸與新 VIM 爐 FY2028 前完工，直接增加鎳基合金供給","p":"35%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1"]},{"level":"🟡","text":"業界新產能（ATI Monroe 第五座 VIM 爐約9,000噸/年、Doncasters 5,000萬美元超合金廠、SMP 增爐）2027末至2030爬坡，交期縮短將削弱議價","p":"40%","evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"積層製造（GKN 與美國空軍 TITAN-AM 專案，840萬美元）與替代材料，目前針對大型鈦機身結構而非熱段旋轉件","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"peer_na_reason":"同業報酬率比較無法計算：事實表只有利益率，未收投入資本；以營益率差代替","roic_durability":{"quadrant":"中利益率×低周轉（TTM 營益率16.5%；管理營運資金占營收32.9%，重資產熔煉鍛造）；投入資本事實表未涵蓋，ROIC 無法精算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（航空公司）、決策者（引擎與機身 OEM）、付款者三者皆成立；材料是飛安關鍵件，新機與維修各半，新世代引擎含量為舊引擎兩倍。2020 年航太國防銷售曾年減55%，顯示需求可延後但不會消失"},{"item":"決策層級","level":"🟢","text":"替代要在單一合金、單一零件的認證層級衡量：熱段六種非自製先進合金 ATI 全部能產、其中五種獨家，新合金認證快也要9個月，引擎服役數十年；Boeing 鈦協議非排他是例外"},{"item":"價值鏈分配","level":"🟡","text":"目前交期拉長讓材料端分到較多利潤，客戶甚至出資擴產；但下游 HWM 營益率28.0% 高於 ATI 16.5%，且2027下半年至2030業界新產能投產後，議價可能回到 OEM 端"},{"item":"社會容忍度","level":"🟢","text":"民航與國防材料不受價格管制，漲價由 OEM 與航空公司吸收，政治敏感度低；海軍核能長約屬政府採購，有成本稽核但已以較佳價格續約至2030"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷未收）；管理層稱新增產能須達內部30%報酬門檻（2026-08-06 法說 CEO），未經驗證","reinvest_rate":"事實表未涵蓋：2026 總資本支出2.8–3.0億美元、客戶出資0.55–0.65億美元，折舊未收，無法求淨再投資","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率，兩項輸入皆缺；以共識 FY2027 EPS +23.4% 遠高於共識營收 +8.8% 判定共識已超出量能驅動的內生上界，差額靠利益率擴張與回購"}}}},"q3_growth":{"verdict":"跑道中等：兩年內靠新世代引擎含量翻倍與長約重新定價，五年後取決於2027–2030業界新產能投產後價格能否守住","reasoning":"成長是價格加量，無併購、回購貢獻小。共識 FY2026E 5.21、FY2027E 6.43、FY2028E 7.52，兩年年複合約20.1%，FY1 共識近三個月上修16.8%；同期營收共識 FY1→FY2 僅成長8.8%，EPS 與營收差14.6個百分點，缺口歸因利益率擴張（全年增量利潤率約50%）與小幅回購，可歸因但依賴定價延續。內生上界因投入資本與折舊未收無法計算，判定共識已超出量能驅動的上界。跑道：新世代引擎維修週期長達數十年、鎳擴產2028年中約3.5億美元增量營收、飛彈與核能為第二腿，但滲透率事實表未涵蓋；業界新產能2027下半年至2030投產後成長將轉向以量為主，五年後判中等。衰退信號亮一項。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_backlog"],"verdict_values":{"growth":{"driver_mix":"價格與組合約三分之二、量約三分之一（Q3 管理層拆解）；噴射引擎年增39%、特殊能源49%、機身11%、國防6%；回購年初至今7,000萬美元，貢獻小；無併購","runway_years":"5–9年（新世代引擎維修週期長達數十年，但滲透率事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與折舊事實表未涵蓋，無法算增量報酬×再投資率；共識 FY2026E→FY2028E EPS 年複合約20.1%，同期營收共識 FY1→FY2 僅 +8.8%，差額歸因利益率擴張與小幅回購，可歸因但依賴定價延續","segments":[{"item":"HPMC","value":"Q3 營收7.21億美元，年增20%，利益率23.2%（新合金爬坡拖累約200基點，管理層稱 Q4 回到20%中段）"},{"item":"AA&S","value":"Q3 營收7.02億美元，年增34%，利益率25.8%（年增850基點），航太國防占比45%（2021 年18%）"}],"decay_signals":["EPS 成長高於營收成長逾5個百分點：共識 FY2027 EPS +23.4%、營收 +8.8%，差14.6個百分點（亮）","FCF 對淨利：FY2024 0.46、FY2025 0.83，未連2年低於0.75（未亮）","SBC 約占營收0.6%（未亮）","毛利率 FY2022–2025 由18.6%升至22.0%、TTM 24.5%（未亮）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：獲利轉現金仍在追趕、回購規模小且買在高倍數，SBC 稀釋輕微、無併購","reasoning":"自由現金流轉換在改善但仍落後：FY2023 FCF 為負、FY2024 FCF 對淨利0.46、FY2025 0.83；2026 年初至 Q3 調整後 FCF 2.23億美元，全年指引5.5–6.0億要靠 Q4 約3.3–3.8億。TTM FCF 利潤率8.4%，低於 Carpenter 10.7%、HWM 19.8%。現金去向：資本支出全年2.8–3.0億（客戶出資0.55–0.65億）、回購年初至今0.7億（剩餘授權4.25億）、無股息、無併購；2026-06 發行4.5億美元5.875%、2033年到期無擔保債。淨負債14.15億美元，約為2026年 EBITDA 指引中點的1.2倍。SBC 約占營收0.6%。債務到期結構與加權利率事實表未涵蓋。","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_kpi4_sbc_0_6","f_kpi7_guidance_fy2026","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_peer_ati_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近12個月8-K 未見併購完成，只有小型閒置廠房處分；無可評估的併購"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"年初至 Q3 回購7,000萬美元，剩餘授權4.25億；回購均價事實表未涵蓋，以現價前瞻盈餘殖利率約3.1%（1÷31.78倍）衡量，門檻為十年期殖利率加2%，只有十年期低於1.1%才過，判為未過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 1,410萬美元，約占營收0.6%；年化約2,800萬、占市值約0.1%，同期回購金額大於 SBC，淨稀釋率遠低於1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能與定價，非併購；資本回報僅回購（年初至今7,000萬美元）、無股息，規模不承重"}}}},"q5_valuation":{"verdict":"偏貴：現價要五年 EPS 年複合約16%並守住22倍才有8%年報酬，等同多方情境；我們信未來兩年獲利，不信2028年後定價與倍數同時守住","reasoning":"現價165.59美元對 FY2026E 前瞻本益比31.8倍、FY2027E 25.8倍、FY2028E 22.0倍；追蹤本益比41.4倍、P/S 4.49倍、EV/S 4.77倍，分別位於自身四個年度端點的98.4、100、100分位（非五年分位）。反推：要拿到年化8%，2031年需 EPS 約11.1美元配22倍，五年年複合約16%，等同多方情境。PEG 以兩年共識年複合20.1%計約1.58，屬合理。賣方目標價多在175–265美元（Investing.com 9位全數買進，均值約200），Benzinga 來源全距逾3倍但含過時目標；本次結論比賣方保守，分歧在框架：賣方把交期驅動的定價延伸到2028年後並沿用目前倍數。動能：26週報酬6.7%、RSI 38.5，未過熱；週線均線多頭排列。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比：FY2026E 調整後 EPS 共識5.21對現價165.59","peers":{"expanded":false,"reason":"事實表只收同業利益率，未收同業前瞻本益比或 EV 倍數；終端倍數改以 ATI 自身倍數區間與 FY2027E 25.8倍為錨，屬資料缺口"},"fwd_pe":31.78,"peg":1.58,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比31.8倍、FY2027E 25.8倍；追蹤本益比、P/S、EV/S 位於自身四個年度端點98.4–100分位（連續五年序列事實表未涵蓋）；PEG 1.58 屬合理；12個月：FY2028E 基本情境 EPS 7.20×23倍約165.6美元，與現價持平；五年：基本情境8.60×22倍約189美元，+14.3%、年化約3%，低於8%。偏貴但未到極端","upside_short_pct":0.0,"upside_mid_pct":14.3,"denominator_disputed":false,"denominator_note":"分母為調整後 EPS，Q3 含新合金爬坡成本（約1,500–2,000萬美元 EBITDA）屬暫時性壓低；週期高點疑慮由空方情境30%承接，不判分母爭議"}}},"q6_how_wrong":{"verdict":"陷阱風險中等：最怕的不是需求消失，而是新產能投產後定價回吐，讓高倍數失去支撐","reasoning":"最可能看錯的三條路寫在反證紀錄：OEM 去庫存疊加新產能讓定價回吐（論點失敗）、獲利成長但現金轉換與回購價位拖累股東報酬、倍數已反映長期定價。衰退信號亮一項，價值陷阱風險中等；最大回撤區間−40%至−65%，論點未見破損，不因波動砍倉，但要有深回撤心理準備。","fact_refs":["f_pe_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點定價風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.21,"pe":31.78,"basis":"FY1（FY2026E）調整後 EPS 共識5.21（2026-10-31 快照），現價165.59；終端倍數同樣套在當年度調整後 EPS"},"eps":{"bull":[6.7,8.0,9.1,10.0,10.8],"base":[6.35,7.2,7.85,8.3,8.6],"bear":[5.8,5.2,4.5,4.3,4.7]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-65,"hi":-40,"basis":"依2020先例與現價倍數：2020 年 HPMC 航太國防銷售年減55%、Q3 2020 調整後 EBITDA 利益率2.8%；目前追蹤本益比41.4倍位於自身四個年度端點98.4分位。淺端：去庫存使 FY2027 EPS 降至5.8、倍數回到17倍，約99美元（−40%）；深端：谷底 EPS 4.3配15倍約65美元（−61%），加情緒超跌取−65%。空方終點跌幅約−55%，落在區間內","trigger_time":null},"basis":{"bull":"引擎新機與維修雙引擎、長約續約維持漲價、鎳擴產2028年帶來約3.5億美元營收，EPS 五年年複合約16%，市場給品質溢價28倍","base":"FY2027–2028 略低於共識（6.35、7.20），2029年後業界新產能投產、定價趨緩，EPS 年複合約10.5%；倍數由31.8倍回到22倍（同業倍數事實表未涵蓋，以自身區間為錨）；淨回購殖利率0.4%","bear":"2027下半年起 OEM 去庫存疊加業界新產能，定價回吐，谷底 EPS 4.3（約 FY2027 共識的三分之二），終端16倍；參照2020年航太國防銷售年減55%，但長約與國防核能分散使跌幅較淺"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2020 年 HPMC 航太國防銷售年減55%、Q3 2020 調整後 EBITDA 利益率僅2.8%；Q3 2026 法說分析師點出 Boeing 重設與 Airbus 爬坡放慢；Argus 稱引擎瓶頸正在緩解；HPMC 約92%營收集中航太國防；2025 年機身端去庫存曾拖累鈦銷售","assumption":"飛機產量一路爬升到2028年，長約保護量與價","consequence":"OEM 去庫存疊加2027下半年起新產能，FY2029 EPS 回落到4.3–4.5美元、倍數降至15–16倍，股價約65–75美元，五年虧損逾五成","ruling":"部分採納：長約、國防與核能第二腿、維修過半使2020式崩跌機率低，但週期形狀保留在空方情境30%機率；與唯一致命點部分重疊（需求轉弱會削弱續約議價），已回補到續約監測","watch":"機身營收年增率、在手訂單是否跌破40億美元、HPMC 航太國防銷售年增率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","customer_concentration_credit#0","supply_demand_durability#6","cyclical_inventory_price_position#3"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年初至 Q3 調整後 FCF 僅2.23億美元，全年指引要 Q4 補3.3–3.8億；管理營運資金占營收32.9%、存貨因新產能暫時偏高；TTM FCF 利潤率8.4%，低於 Carpenter 10.7%、HWM 19.8%；回購在前瞻31.8倍執行，盈餘殖利率約3.1%","assumption":"獲利成長能以90%以上轉為自由現金流（2026-08-06 法說 CFO 承諾）","consequence":"EPS 照共識成長，但擴產資本支出與營運資金吃掉現金，回購買在高價，每股自由現金流成長落後 EPS 數年","ruling":"採納為監測項：Q4 FCF 是第一個裁決點；若未達5.5億，基本情境回購假設歸零","watch":"FY2026 調整後 FCF（2027-02 Q4 財報）、管理營運資金占營收比","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_peer_ati_fcf_margin_pct","f_peer_crs_fcf_margin_pct","f_peer_hwm_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"前瞻本益比31.8倍，追蹤本益比、P/S、EV/S 皆在自身四個年度端點頂部（98.4–100分位）；FY1 共識三個月上修16.8%；賣方幾乎全數買進","assumption":"市場把交期驅動的定價延伸到2028年後，並願意長期給25倍以上","consequence":"即使 FY2027 EPS 6.43 如期達成，倍數回到22倍只值約141美元，較現價低約15%","ruling":"採納，為觀望的主要約束；股價跌到154以下且2027指引確認時重跑","watch":"股價對154美元、FY2027 共識變動、投資人日中期目標","fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 187.98 → 本次 165.59（-11.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=187.98","side_b":"本次 price_at_dd=165.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 187.98 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 187.98 美元：Bull 價 348、Bear 價 79.5，五年期望值 +12.4%，基準年化 3.5%，不對稱比 1.2","side_b":"本次情境、股價仍用 187.98 美元：Bull 價 302.4、Bear 價 75.2，五年期望值 −2.5%，基準年化 0.1%，不對稱比 0.85","ruling":"先換情境、股價不動：五年期望值少 14.9 個百分點，基準年化少 3.4 個百分點。不對稱比由 1.2 變為 0.85。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 187.98 美元：五年期望值 −2.5%，基準年化 0.1%，不對稱比 0.85","side_b":"本次情境、股價 165.59 美元：五年期望值 +10.7%，基準年化 2.7%，不對稱比 1.26","ruling":"再換股價、情境不動：起點價下跌 11.9%，五年期望值多 13.2 個百分點，基準年化多 2.6 個百分點，不對稱比由 0.85 升到 1.26。合計五年期望值比前份少 1.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求訊號：管理層與 OEM 減速訊號","cause":null,"prior_field":null,"side_a":"Q3 法說（2026-10-29）CEO：看不到去庫存，訂單延伸到2027，引擎 OEM 稱產量加倍也全收；機身營收季增14%","side_b":"同場分析師點出 Boeing 重設、Airbus 爬坡放慢；Argus 稱引擎瓶頸緩解；HPMC 3,000–4,000萬美元遞延出貨 Q3 只出約四分之一；在手訂單由44億降至43億","ruling":"可調和，屬程度差異：ATI 材料提前下單、訂單與 OEM 排程對齊，短期營收有在手訂單支撐；但管理層訊號是自述，利空不到一季且未進賣方模型（FY2027 共識10月仍上修0.63%），凍結加碼到 Q4 財報確認","evidence_level":"中（管理層自述加第三方產業報導，無 OEM 一手數據）","settle_metric":"機身營收年增率、在手訂單","if_then":["若 Q4 2026 或 Q1 2027 機身營收轉年減、或在手訂單跌破40億美元 → 不追，基本情境 FY2027 EPS 下修至6.0以下、空方機率提高到35%","反向：若在手訂單回到44億美元以上且2027指引 EBITDA 中點≥13億美元 → 維持基本情境，股價到154以下時分批反買"],"evidence_refs":["supply_demand_durability#6","cyclical_inventory_price_position#3"]},{"axis":"利益率屬結構還是週期","cause":null,"prior_field":null,"side_a":"Q3 法說 CFO：AA&S 已結構轉型，航太國防占比由2021年18%升至45%，利益率可在20%中段維持到可見未來；長約與海軍核能合約（5年約10億美元）提供底","side_b":"增幅約三分之二來自價格與組合，靠的是優質鈦20個月、等溫鍛件逾24個月的交期；Carpenter Athens 約9,000噸與新 VIM 爐 FY2028 前完工，ATI Monroe 約9,000噸/年、Doncasters、SMP 新產能2027下半年至2030投產；Q2 法說同一場內 CFO 說持續高於20%、CEO 說20%中段，口徑不一","ruling":"可調和，結構與週期成分並存：組合轉向與退出商品不鏽鋼屬結構，AA&S 約20–22%為可守底線（依據：Q2 剔除資產出售利得後底層利益率約22%）；超過的部分視為週期性定價，2028年續約前無法裁決。基本情境假設2029年後利益率回落約2個百分點","evidence_level":"中","settle_metric":"AA&S 分部利益率、優質鈦交期、2027–2028 續約價格","if_then":["若 AA&S 利益率連兩季低於20% → 結構論點失敗，若持有則清倉，未持有則撤銷估值重啟條件","反向：若2028年續約後 AA&S 仍≥22%且優質鈦交期≥12個月 → 結構論點成立，終端倍數由22倍上調至24倍重跑情境"],"evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"axis":"前季承諾與本季兌現","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-08-06）CFO：Q3 EBITDA 3.05–3.15億、Q4 約3.35億、自由現金流轉換率≥90%；CEO：3,000–4,000萬美元 HPMC 出貨移到下半年、引擎全年高十位數成長","side_b":"Q3 實績 EBITDA 3.28億（超過上緣）、Q4 指引上調至3.45–3.55億、引擎成長上調至低至中段20%；但年初至今 FCF 2.23億，全年中點5.75億對應調整後淨利約7.06億（EPS 5.20×1.358億股，未計可轉債稀釋），轉換率約81%；遞延出貨 Q3 只出約四分之一，Richland 高階引擎合金認證延到2027年中","ruling":"可調和，屬時點差異：獲利承諾兌現且超標，現金轉換與產能爬坡落後；以 Q4 FCF 裁決","evidence_level":"高（兩場法說原話與實績）","settle_metric":"FY2026 調整後 FCF","if_then":["若 FY2026 調整後 FCF 低於5.5億美元 → 停止加碼，現金轉換風險視為成立","反向：若≥5.75億美元 → 保留基本情境的回購假設"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"第三次上修、FY2026 EBITDA 年增39%，Q4 EPS 指引年化約6.2美元；股價自前份187.98跌至165.59（−11.9%）而基本面無損，RSI 38.5；FY2027 只要25.8倍；熱段合金五種獨家，引擎 OEM 稱產量加倍也全收","side_b":"跌後倍數仍在自身區間頂部；反推年化8%需要五年 EPS 年複合約16%，等同多方情境；業界新產能2027下半年起投產，循環位置屬中段，持有不加","ruling":"不追。約束是估值：基本情境五年年化約3%，低於8%門檻；跌但基本面無損屬分批反買情境，但價位未到。股價≤154且2027指引 EBITDA 中點≥13億美元時重跑研究","evidence_level":"中","settle_metric":"股價、2027 指引","if_then":["若股價續漲但2027指引尚未公布 → 不追","若股價跌破154而在手訂單與分部利益率無損 → 重跑研究後分批反買，首倉小倉位"]},{"axis":"價格變動後的估值、品質與機率","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-10-13，股價187.98美元）：觀望、追蹤、估值偏貴、品質 B、多方25%、空方30%、最大回撤−65%","side_b":"本次（股價165.59美元，−11.9%）：前瞻本益比31.8倍仍在自身區間頂部，估值偏貴、品質 B 維持；多方25%、空方30%不變；最大回撤區間−40%至−65%","ruling":"跌幅來自價格而非基本面，倍數仍高，估值與品質結論不變；Q3 上修已由基本情境 FY2027 EPS 6.35承接，機率不動","evidence_level":"高（價格與共識皆為事實表數據）","settle_metric":"股價對154美元、FY2027 共識","if_then":["若股價跌至154美元以下且2027指引 EBITDA 中點≥13億美元 → 重跑研究後分批反買","若股價回升至187.98以上而指引未出 → 不追"]},{"axis":"新證據檢視：陷阱、護城河方向、跑道、類型、循環位置","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱中等、護城河向上、跑道中等、循環/商品、中循環","side_b":"Q3 新證據：定價力續強（三分之二增幅來自價格與組合、新合金市占擴大）、AA&S 創紀錄25.8%；同時 OEM 減速訊號浮現、業界新產能時程確認；各欄結論維持","ruling":"新證據同時強化定價力與確認2027–2030供給回補，兩者相抵，各欄不變；循環位置仍判中段，未到晚期，因 OEM 產量仍低於目標、交期仍在拉長","evidence_level":"中","settle_metric":"交期、分部利益率、在手訂單","if_then":["若優質鈦交期縮短到12個月以下且分部利益率回落 → 循環位置改判晚期，不追","若2027指引確認 EBITDA 成長且交期維持 → 維持中段判斷"]},{"axis":"估值重啟門檻變動（進場首倉條件）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","side_b":"股價 ≤ 154 美元（FY2027 共識 6.43 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","ruling":"方法不變（FY2027 共識24倍），共識由6.37上修至6.43使價位由153調至154；EBITDA 條件不變","evidence_level":"高","settle_metric":"股價、2027 指引","if_then":["兩條件同時成立 → 重跑研究，通過後分批反買"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點欄為空（摘要未保存）","side_b":"任一主要引擎 OEM（GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran）在2027–2028長約續約時，把熱段鎳基超合金或等溫鍛件改為雙源，或議定降價","ruling":"前份未存唯一致命點，本次依數學敏感度最大項新設：價格與組合貢獻約三分之二增幅，續約降價或雙源是單一最大衝擊，發生即清倉","evidence_level":"中","settle_metric":"續約揭露、交期","if_then":["若任一主要引擎客戶公開雙源化或續約降價 → 清倉（若持有），未持有則撤銷估值重啟條件"]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics","triggers"],"side_a":"前份清倉與減碼門檻、觸發器皆為空（摘要未保存）","side_b":"AA&S 利益率連兩季<20%；在手訂單<40億美元；FY2026 調整後 FCF<5.5億美元；HPMC 利益率 Q4 2026 與 Q1 2027 皆<24%；優質鈦交期<12個月","ruling":"前份摘要未保存門檻，本次依論點與風險逐條新設，各自對應減碼或清倉動作","evidence_level":"中","settle_metric":"每季分部資料與法說","if_then":["AA&S 利益率連兩季<20% → 清倉（若持有）","在手訂單<40億美元或優質鈦交期<12個月 → 減碼（若持有）"]}],"triggers":[{"n":1,"text":"估值重啟：股價回到 FY2027 共識24倍以下，且2027指引確認 EBITDA 成長","type":"估值rearm","maps_to":"H1","metric":"股價；2027 年指引調整後 EBITDA 中點","threshold":"股價≤154美元且 EBITDA 中點≥13億美元同時成立","action":"重跑研究，通過後分批反買、首倉小倉位","source_freq":"每日股價；2027-02 Q4 財報","date":"2027-02-01"},{"n":2,"text":"投資人日公布3–5年展望，驗證引擎成長與利益率目標","type":"假設驗證","maps_to":"H1","metric":"引擎營收成長目標、合併 EBITDA 利益率目標","threshold":"引擎營收年成長目標≥15%且利益率目標≥20%中段","action":"未達則基本情境 FY2028 EPS 下修至7.0以下並不追","source_freq":"一次性","date":"2026-11-12"},{"n":3,"text":"OEM 減產或去庫存傳導到訂單","type":"風險","maps_to":"R1","metric":"機身營收年增率、在手訂單","threshold":"機身營收轉年減，或在手訂單<40億美元","action":"不追；若持有則減碼","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#6","customer_concentration_credit#0","cyclical_inventory_price_position#3"]},{"n":4,"text":"業界新產能投產後定價回吐","type":"風險","maps_to":"R2","metric":"優質鈦交期、AA&S 分部利益率","threshold":"優質鈦交期<12個月，或 AA&S 利益率連兩季<20%","action":"若持有則減碼，利益率條件成立則清倉","source_freq":"每季法說與財報","date":null,"evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"n":5,"text":"擴產期獲利轉現金落後","type":"風險","maps_to":"R3","metric":"FY2026 調整後 FCF","threshold":"<5.5億美元","action":"停止加碼","source_freq":"Q4 2026 財報","date":"2027-02-01"},{"n":6,"text":"新合金爬坡成本是否如管理層所說為一次性（未證、監測）","type":"假設驗證","maps_to":"H2","metric":"HPMC 分部利益率","threshold":"Q4 2026 與 Q1 2027 皆<24%，則一次性歸因不成立","action":"不追，基本情境利益率下修","source_freq":"每季財報","date":"2027-05-01"},{"n":7,"text":"原料地緣供應中斷或中國出口管制吃掉利潤","type":"風險","maps_to":"R4","metric":"出貨遞延金額、分部利益率","threshold":"單季出貨遞延≥3,000萬美元，或分部利益率受損≥100基點","action":"若持有則減碼","source_freq":"每季法說、10-K 風險因子","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"n":8,"text":"積層製造進入引擎旋轉件量產","type":"風險","maps_to":"R5","metric":"OEM 量產公告","threshold":"任一引擎 OEM 公開以積層製造取代旋轉件鍛件並量產","action":"若持有則減碼","source_freq":"產業新聞、OEM 公告","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":9,"text":"退休金年金集體訴訟：民事集體案，公司無法估計損失；magistrate 法官已建議以無訴訟資格駁回，待主審法官裁定","type":"風險","maps_to":null,"metric":"主審法官裁定、集體認證","threshold":"駁回建議遭推翻且集體認證成立","action":"停止加碼；不利和解金額超過年度 FCF 一成則減碼","source_freq":"10-Q 與10-K 法律程序","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"Single Thing：主要引擎 OEM 續約改雙源或議定降價","type":"Single Thing","maps_to":"Single Thing","metric":"續約揭露、熱段合金供應地位","threshold":"任一主要引擎客戶公開雙源化或續約降價","action":"清倉（若持有），未持有則撤銷估值重啟條件","source_freq":"每季法說、10-K","date":null},{"n":11,"text":"Q4 2026 財報複審","type":"複審日期","maps_to":null,"metric":"2027 指引、FY2026 FCF、在手訂單","threshold":"依前列各門檻","action":"重跑情境","source_freq":"一次性","date":"2027-02-01"}],"kill_metrics":[{"metric":"AA&S 分部 EBITDA 利益率","bear_threshold":"連兩季<20%","window":"2027–2028 每季","source":"公司季報新聞稿分部資料","last_status":"ok"},{"metric":"在手訂單","bear_threshold":"<40億美元或轉為年減","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2026 調整後自由現金流","bear_threshold":"<5.5億美元","window":"2027-02 Q4 財報","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"HPMC 分部利益率","bear_threshold":"Q4 2026 與 Q1 2027 皆<24%","window":"2027-02 至 2027-05","source":"公司季報分部資料","last_status":"warning"},{"metric":"優質鈦交期","bear_threshold":"<12個月","window":"每季法說","source":"法說會管理層口述","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"來源是投資人社群自撰敘事，非公司揭露也非分析師研究，未附替代比例、平台或時程等可驗證數據；替代風險改由10-K 風險因子與 GKN TITAN-AM 專案兩條一手證據承接"}],"action_conditions":{"rearm_trigger":"股價 ≤ 154 美元（FY2027 共識 6.43 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","exec_line":"不追；兩條件同時成立才重跑研究，通過後首倉小倉位、分兩批；續漲而2027指引未出則不追","holding_cap":"≤3%（最大回撤可能逾五成的循環股）"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價≤154美元（FY2027 共識6.43的24倍）且2027年指引調整後 EBITDA 中點≥13億美元，兩者同時成立後重跑研究","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=6.65, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"引擎、國防與特殊能源需求加上長約重新定價，使 FY2027 調整後 EPS 達6.0美元以上（共識6.43）","2y":"FY2027 調整後 EPS≥6.0美元、EBITDA≥13億美元","5y":null,"10y":null,"threshold":"2027 年調整後 EBITDA≥13億美元（2026 指引中點11.95億）；噴射引擎營收年增≥15%","source":"季報新聞稿、2026-11-12 投資人日、2027-02 Q4 法說指引","drift_rule":"TTM 調整後 EBITDA 較此路徑連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"AA&S 組合轉向（航太國防占比由2021年18%升至45%）與長約，讓兩分部 EBITDA 利益率在2027下半年至2030業界新產能投產後仍守住20%以上","2y":null,"5y":"2031 年合併調整後 EBITDA 利益率≥20%","10y":null,"threshold":"AA&S 與 HPMC 分部利益率皆≥20%；合併調整後 EBITDA 利益率≥20%","source":"每季分部資料、續約揭露、交期口述","drift_rule":"利益率較門檻低5%（約1個百分點）連4季為削弱、低10%（約2個百分點）連6季為反轉"},{"id":"H3","text":"新世代引擎單機含量為舊引擎兩倍以上，熱段合金多為獨家或雙源，新機與維修各半，使引擎業務成長延續到2030年代","2y":null,"5y":null,"10y":"2036 年引擎營收占全公司仍≥40%，熱段合金無客戶雙源化","threshold":"無主要引擎客戶導入第二供應商；噴射引擎營收占全公司≥40%","source":"10-K 客戶與競爭揭露、法說會終端市場拆分","drift_rule":"引擎營收占比跨2個年度下降為削弱、跨3個年度為反轉"}],"R":[{"id":"R1","text":"飛機 OEM 減產或去庫存（Boeing 重設、Airbus 爬坡放慢）傳導到 ATI 訂單，HPMC 高度集中航太國防放大衝擊","h_ref":"H1","clock":"⚡","threshold":"機身營收轉為年減，或在手訂單低於40億美元","evidence_refs":["supply_demand_durability#6","customer_concentration_credit#0","cyclical_inventory_price_position#3"]},{"id":"R2","text":"Carpenter、Doncasters、SMP 與 ATI 自身新產能2027下半年至2030投產，交期縮短後續約價格回吐","h_ref":"H2","clock":"🔥","threshold":"優質鈦交期低於12個月，或 AA&S 利益率連兩季低於20%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"擴產期存貨與應收墊高，獲利轉現金落後，全年 FCF 指引落空","h_ref":"H1","clock":"⚡","threshold":"FY2026 調整後 FCF 低於5.5億美元"},{"id":"R4","text":"鎳、海綿鈦、鈷等原料多來自地緣不穩國家，中國出口管制與中國合資持股帶來供應與政策風險","h_ref":"H3","clock":"🐢","threshold":"公司揭露原料中斷致單季出貨遞延≥3,000萬美元，或分部利益率受損≥100基點","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"id":"R5","text":"積層製造與複合材料長期替代部分鈦與合金鍛件","h_ref":"H3","clock":"🐢","threshold":"任一引擎 OEM 公開以積層製造取代旋轉件鍛件並進入量產","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"single_thing":{"description":"任一主要引擎 OEM（GE Aerospace、Rolls-Royce、Pratt & Whitney、Safran）在2027–2028長約續約時，把熱段鎳基超合金或等溫鍛件改為雙源，或議定降價","why_fatal":"管理層稱本季增幅約三分之二來自價格與組合，引擎約占全公司營收四成、增量利潤率約50%；價格回吐對 EPS 的衝擊是營收的兩倍以上，共識 FY2027–2028 每年17–23%的 EPS 成長主要靠利益率擴張","if_happens":"基本情境改走空方路徑（FY2028 EPS 由7.2降至5以下），終端倍數下修至16倍；持有則清倉，未持有則撤銷估值重啟條件","how_monitor":"每季法說的續約揭露（Q3 法說稱數份合約即將續約）、優質鈦與等溫鍛件交期、HPMC 利益率、10-K 客戶與競爭揭露","probability":"12–24個月約15%：五種合金獨家供應、認證週期長，但 Carpenter 等新產能2027下半年起投產，提高客戶雙源選項"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.75,"peg_fy2":1.28,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":2.85,"FY2026E":5.21,"FY2027E":6.43,"FY2028E":7.52},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 調整後 EPS 共識（2026-10-31 快照，家數事實表未涵蓋）；FY2025A 2.85 為年度 GAAP 稀釋 EPS，調整後口徑事實表未涵蓋，基期與共識口徑不同"},"catalysts":[{"date":"2026-11-12","type":"guidance","event":"投資人日：公布3–5年展望（引擎成長、資本支出與利益率目標）","impact":"高","watch":"引擎營收成長目標是否≥15%、利益率目標是否在20%中段以上"},{"date":"2027-02-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與2027年指引","impact":"高","watch":"2027 調整後 EBITDA 中點是否≥13億美元；FY2026 FCF 是否≥5.5億美元"},{"date":"2027-06-30","date_precision":"quarter","type":"capacity","event":"Richland EB2 爐高階引擎鈦合金完成認證","impact":"中","watch":"認證是否如期於2027年中完成"},{"date":"2027-12-31","date_precision":"quarter","type":"capacity","event":"Monroe 新 VIM 爐上線（2028年中約3.5億美元鎳增量營收）；同期 Carpenter Athens 擴建完工","impact":"中","watch":"交期與續約價格是否鬆動"}]}
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
