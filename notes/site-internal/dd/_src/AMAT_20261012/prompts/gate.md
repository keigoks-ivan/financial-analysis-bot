你是 DD 管線 v20 的判斷層閘（gate），標的 AMAT（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、裁決、角色）。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝9115 USD M｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release（經 mfn.se 轉載全文取數）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：未查得共識營收，省略
- `f_kpi1_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝34.0 %｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；Non-GAAP 營業利益 $3,096M（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：未查得共識，省略
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝33.7 %｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；GAAP 營業利益 $3,075M（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：n/a
- `f_kpi3_non_gaap_free_cash_flow`（q1_business）｜Non-GAAP free cash flow＝2330 USD M｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；營運現金流 $3,037M、資本支出 $707M；FCF 占營收約 25.6%（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：n/a
- `f_kpi5_guidance_q4_fy2026_reven`（q1_business）｜Guidance: Q4 FY2026 revenue＝10,250 ± 500 USD M｜期間與口徑：Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026）
  - 註記：未查得共識，省略
- `f_kpi6_guidance_q4_fy2026_non_g`（q1_business）｜Guidance: Q4 FY2026 non-GAAP diluted EPS＝4.02 ± 0.20 USD｜期間與口徑：Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；含 $0.01 SBC 正常化稅務利益與 $0.05 集團內無形資產移轉淨稅務利益（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026 新聞稿（公告於 2026-08-13），指引對象 Q4 FY2026）
  - 註記：未查得共識，省略
- `f_kpi7_contract_liabilities_bac`（q1_business）｜Contract liabilities (backlog 替代指標)＝3271 USD M｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；新聞稿未揭露 backlog、book-to-bill、產能利用率，此為最接近的指標（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：n/a
- `f_peer_amat_gross_margin_pct`（q2_moat）｜AMAT 毛利率＝49.4 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amat_operating_margin_pct`（q2_moat）｜AMAT 營業利益率＝31.09 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amat_fcf_margin_pct`（q2_moat）｜AMAT FCF 利潤率＝18.23 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_asml_gross_margin_pct`（q2_moat）｜ASML 毛利率＝52.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_asml_operating_margin_pct`（q2_moat）｜ASML 營業利益率＝35.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_asml_fcf_margin_pct`（q2_moat）｜ASML FCF 利潤率＝24.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2330_tw_operating_margin_pct`（q2_moat）｜2330.TW 營業利益率＝56.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝12.79 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝18.47 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝23.6 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.32 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 12.26 → 12.79（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_kpi4_share_based_compensation`（q1_business）｜Share-based compensation＝169 USD M｜期間與口徑：Q3 FY2026（季末 2026-07-26，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.appliedmaterials.com Q3 FY26 press release；占營收約 1.85%、占 GAAP 營業利益約 5.5%（自算）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-07-26，公告於 2026-08-13））
  - 註記：n/a
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.391 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝39.64 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 12.79，分子＝快照價 507.03｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝507.03 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝43.75 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.05 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.99 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（12.79 → 12.79）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.11 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（18.45 → 18.47）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（23.6 → 23.6）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝27.21 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.57｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（17 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Castellano 通訊稿標題主張 AMAT 於 2025 年在多個關鍵設備區段失去份額（全文付費牆，僅見摘要；Lam、KLA、ASML 在各自 SAM 擴大）
  - 來源：Dr. Robert Castellano's Semiconductor Deep Dive Newsletter - Applied Materials lost share across（as_of 2026-05-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Mizuho 2025 年 9 月降評至 Neutral：中國本土 OEM（Naura、AMEC）在 PVD、成熟 28nm 蝕刻與電漿 CVD 持續拿份額
  - 來源：Finviz news - Applied Materials (AMAT) stock downgraded to neutral as competition rises in China; Barron's 同一報告（as_of 2025-09-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Reuters 經 247WallSt 轉述：中國要求晶圓廠新增產能至少 50% 使用國產設備，有利 Naura、AMEC
  - 來源：247wallst - Applied Materials' China Problem Is Getting Worse（as_of 2026-08-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：AMAT FY2025 10-K 風險揭露：中國本土設備商因地方政府誘因與出口管制，競爭可能加劇
  - 來源：SEC EDGAR AMAT FY2025 10-K（as_of 2025-12-01）｜affects：thesis.R、moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：中國晶圓廠使用國產設備占比 2025 年達 35%（2024 年 25%），蝕刻與薄膜沉積等關鍵製程替代率據報逾 40%；屬客戶端導入國產第二來源的產業層證據，未點名 AMAT 客戶。
  - 來源：TrendForce News 2026-01-12 China's domestic chip equipment adoption beats 2025 target at 35%（as_of 2026-01-12）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：AMEC 5nm 蝕刻機據報已進入 TSMC 先進製程產線驗證；中國監管據報要求新增產能設備至少 50% 採國產。
  - 來源：TrendForce News 2026（搜尋摘要，未取得原文）（as_of 2026-01-12）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：兩家客戶分別占淨營收約 19% 與 15%（FY2024 為約 12% 與 11%）；客戶未具名。
  - 來源：Applied Materials Form 10-K FY2025 (SEC)（as_of 2025-12-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：2026年2月，AMAT 與美國商務部 BIS 就 2020年11月至2022年7月對中國客戶出貨未遵守出口管制規定達成和解，支付 2.525 億美元；此為出口管制事項，非反壟斷。
  - 來源：Applied Materials press release: Applied Materials Reaches Resolution with the U.S. Department of Commerce（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：2025年10月美國商務部將出口黑名單擴及列管公司的多數持股子公司；AMAT 預告此規則將使 FY2026 營收減少約 6 億美元，其中 FY Q4 約 1.1 億美元。
  - 來源：Yahoo Finance／Reuters: Applied Materials flags $600 million revenue hit in 2026 on broader chip export curbs（as_of 2025-10-01）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：2026年2月報導 AMAT 就向中芯國際（SMIC）違規出口晶片設備達成約 2.52 億美元和解／罰款；設備經南韓子公司轉運，SMIC 於 2020年12月被列入實體清單之後出貨開始。
  - 來源：TrendForce News: US reportedly hits Applied Materials with $252M penalty for illegally sending chip equipment to SMIC（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：中國占 AMAT 營收比重：聚合站稱 FY Q3 中國營收 25.1 億美元、占 28%（去年同期 35%）；CFO 稱限制影響相當於 FY2024 中國市場約 10%、FY2025 逾兩倍（次級聚合來源，未核對公司申報）。
  - 來源：Yahoo Finance／Reuters 摘要: Applied Materials sees weaker China spending in 2026 on tighter US curbs（as_of 2025-11-13）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：公司稱美國出口管制預計使 FY2026 營收減少約 6 億美元（Q4 減 1.1 億）；另有報導引述 7.1 億美元口徑
  - 來源：Reuters 經 Yahoo Finance：Applied Materials sees weaker China spending in 2026 on tighter US curbs（as_of 2025-11-13）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：中國營收占比由近 40% 降至 20% 中段；CEO 指非美系設備商不受同等限制，受限客戶可轉向對手（日期為推定，原文發布日未於摘要中確認）
  - 來源：Reuters 經 Korea JoongAng Daily：Applied Materials sees weaker China spending in 2026 on tighter US curbs（as_of 2025-11-13）｜affects：moat_trend、decision_inputs.bear
- `end_markets#6`（end_markets｜方向 -｜狀態 ok）：中國：AMAT 中國占系統與服務營收比重 FY2025 降至 28%，預期 2026 中國 WFE 支出下降且限制無實質放寬；FQ2 FY26 中國約占營收 24%；Mizuho 預期持續流失份額，UBS 認為中國需求被低估。
  - 來源：Nasdaq/Zacks；Hudson Labs AMAT Earnings Preview Memo（as_of 2026-08-10）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：TIKR 報導：AMAT 股價 2026-07-20 最大回撤 27%，儘管指引上調。
  - 來源：TIKR（as_of 2026-07-20）｜affects：decision_inputs.bear、valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-02-11 AMAT 與美國商務部 BIS 和解，支付 2.525 億美元；DOJ 與 SEC 通知已無行動結案相關調查（原為對中國/SMIC 出貨之出口管制調查）
  - 來源：Applied Materials press release: Applied Materials reaches resolution with U.S. Department of Commerce（as_of 2026-02-11）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：原告律所發佈 AMAT 投資人調查公告（2023-11 至 2024-08），2024-10-15 股價單日跌 10.69% 至 191.02 美元；搜尋結果僅見律所招攬，未見確認已提起的集體訴訟（超出近 12 個月，僅供背景）
  - 來源：Pomerantz via SDxCentral: Pomerantz investigates claims from Applied Materials investors（as_of 2024-10-16）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1040.0,"bear_5y_price":272.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":17.2,"ev5y_pct":20.1,"irr_base_pct":3.2,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":12.79,"pe":39.64,"basis":"FY1＝FY2026E（10 月底結束）Koyfin 共識 EPS；終端倍數同樣以終端財年 EPS 為分母，同為當年度口徑"},"eps":{"bull":[20.5,27.0,31.5,36.0,40.0],"base":[18.3,22.0,22.0,24.5,27.0],"bear":[16.5,13.5,12.0,14.0,16.0]},"pe":{"bull":26,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.391,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMAT_Q2_2026_Earnings_Call_20260514.md
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 營收指引 8.95 億美元（原文單位 billion）±5 億，年增近 23%（原話："company revenue of $8.95 billion plus or minus $500"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 non-GAAP EPS 指引 3.36 美元 ±0.20（原話："We expect non-GAAP EPS of $3.36 plus or minus"）
- 2026-05-14｜Brice Hill (CFO)｜margin：FQ3 non-GAAP 毛利率指引約 50.1%，小幅上升（原話："to increase modestly to approximately 50.1%"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：FQ3 non-GAAP 營業費用指引約 14.85 億美元（原話："we expect non-GAAP operating expenses of around $1.485"）
- 2026-05-14｜Gary Dickerson (CEO)｜guidance：半導體設備事業 2026 曆年成長 30% 以上（相較上季上調，因客戶找到更多無塵室空間）（原話："we'll grow 30% or more in the year"）
- 2026-05-14｜Gary Dickerson (CEO)｜guidance：先進封裝營收 2026 曆年成長逾 50%（原話："grow our packaging revenues more than 50% in calendar 2026"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：AGS 成長預期由先前的低雙位數上調為中十位數（mid-teens），今年更高（原話："we are going to raise our expectations for AGS to mid-teens"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：中國與全球 ICAPS 業務曆年預期持平至小幅成長（原話："our ICAPS business worldwide, to be flat to slightly"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：管理層預期 2027 年為產業另一個創紀錄年（原話："we expect 2027 will be another strong,"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：被問 FQ3 後走勢，CFO 稱可假設從 FQ3 指引到 FQ1 以美元計線性成長，不提供逐季明細（原話："it grows linearly from our Q3 guide through Q1"）
- 2026-05-14｜Brice Hill (CFO)｜guidance：回答 2028 是否仍為 WFE 成長年：CFO 表示現在判斷並不嫌早（原話："We don't think it's too early, Krish."）
- 2026-05-14｜Brice Hill (CFO)｜margin：本季營收與營業利益率數字：營業利益率 32.1%（原話："32.1%, up 140 basis points year-over-year"）
- 2026-05-14｜Brice Hill (CFO)｜margin：管理層把毛利率提升歸因於高差異化產品的價值定價（原話："driven by value-based pricing from our most differentiated"）
- 2026-05-14｜Brice Hill (CFO)｜margin：開始分部門揭露毛利率；半導體系統 Q2 為 54.8%（原話："Semi Systems gross margin is 54.8% in Q2"）
- 2026-05-14｜Brice Hill (CFO)｜margin：定價機制：以專案為基礎的長約，變動較慢（原話："our pricing generally works as long-term contracts with"）
- 2026-05-14｜Brice Hill (CFO)｜margin：AGS 毛利率改善驅動因素：備品／交易型業務占比提高（原話："the mix to more transactional and more"）
- 2026-05-14｜Brice Hill (CFO)｜margin：AGS 費用下降部分來自重組（原話："we did some restructuring that helped us with expenses"）
- 2026-05-14｜Gary Dickerson (CEO)｜commitment：CEO 表示對毛利率進展延續高度有信心（原話："I have high confidence that the margin progress that"）
- 2026-05-14｜Brice Hill (CFO)｜commitment：費用成長慢於營收、營業利潤持續增加（原話："we also expect to increase spending more slowly than"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：本季股東回饋 7.65 億美元（原文 million），含股利與買回（原話："We distributed $765 million to shareholders"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：季股利調升 15%（原話："15% increase to the quarterly cash dividend"）
- 2026-05-14｜Brice Hill (CFO)｜capital_allocation：製造產能已近乎倍增（美、歐擴建及新加坡新製造中心）（原話："We've nearly doubled our manufacturing capacity to support"）
- 2026-05-14｜Brice Hill (CFO)｜customer：最大客戶提供滾動 8 季預測（原話："giving us the clearest and longest visibility we've ever had"）
- 2026-05-14｜Brice Hill (CFO)｜customer：追蹤中的晶圓廠專案逾 100 個（原話："tracking over 100 factory projects globally"）
- 2026-05-14｜Gary Dickerson (CEO)｜customer：EPIC 共同開發夥伴新增 TSMC（原話："we announced our EPIC co-development engagement"）
- 2026-05-14｜Brice Hill (CFO)｜customer：NAND 位元成長預測上調，預期仍以升級滿足（原話："we did raise our bit growth forecast for"）
- 2026-05-14｜Brice Hill (CFO)｜customer：ICAPS 面臨既有產能消化期（原話："there'll be some digestion with all the capacity that's been"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：敘事變化：新增 agentic AI 為晶圓廠設備的額外需求來源（原話："they provide an additional tailwind for wafer fab"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：敘事變化：上季稱無塵室空間是投資步調的關鍵因素，本季客戶正找到新空間（原話："the availability of cleanroom space was a key factor pacing"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：3 個領域預期占 2026 年 WFE 成長 80% 以上，2027 類似（原話："account for more than 80% of the year-on-year growth"）
- 2026-05-14｜Gary Dickerson (CEO)｜product：Sym3 為公司史上最快放量產品（原話："Sym3 is the fastest ramping product in Applied's history."）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：宣稱導體蝕刻在先進邏輯 GAA 與 DRAM 均為第一（原話："Sym3 is the fastest ramping product in Applied's history"）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：DRAM 市占過去十餘年增加 10 個百分點（原話："we gained 10 points of overall share in WFE and DRAM"）
- 2026-05-14｜Gary Dickerson (CEO)｜competition：被質疑製程控制市占下滑，CEO 表示不同意該看法（原話："I don't share your view on the perspective on the business."）
- 2026-05-14｜Gary Dickerson (CEO)｜risk：CEO 指出供應鏈是限制，產能擴張受供應鏈回應速度牽制（原話："And it's really supply chain."）
- 2026-05-14｜Gary Dickerson (CEO)｜risk：被問出口管制（華為相關）風險擴大，CEO 拒絕評論，稱已納入指引（原話："I don't really want to comment on that."）

### AMAT_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜Brice Hill (CFO)｜guidance：CFO 稱明年預期為強勁成長年，驅動力為 AI 投資循環，看不到改變（原話："we expect next year to be a strong growth year"）
- 2026-09-08｜Brice Hill (CFO)｜customer：最大客戶提供的滾動 8 季預測全年持續上升，歸因於 AI 系統需求（原話："rolling 8-quarter forecast we get from our largest"）
- 2026-09-08｜Brice Hill (CFO)｜customer：雲端業者資本支出預測全年上修，美系逾 7,000 億美元、全球近 1 兆（原話："over $700 billion this year for the U.S. companies"）
- 2026-09-08｜Brice Hill (CFO)｜customer：8 季預測因按工廠進單而非線性，呈跳升式成長；管理層看不到見頂點（原話："we don't see a place where it peaks"）
- 2026-09-08｜Brice Hill (CFO)｜customer：追蹤的新廠專案超過 100 座，最近兩季每季新增逾 10 座，作為領先指標（原話："well over 100 factories that we're tracking"）
- 2026-09-08｜Brice Hill (CFO)｜risk：中期受限因素為無塵室，需求大於供給（原話："in the medium term, it's gated by clean room"）
- 2026-09-08｜Brice Hill (CFO)｜product：先進封裝去年營收 14 億美元，今年成長逾 70%，預期與先進邏輯及 DRAM 同步成長（原話："We've said this year, it's growing more than 70%."）
- 2026-09-08｜Brice Hill (CFO)｜guidance：ICAPS 今年預期溫和成長，明年為較正常的成長年（敘事相對過去兩年疲弱有變）（原話："We actually expect some moderate growth in ICAPS this year"）
- 2026-09-08｜Brice Hill (CFO)｜margin：ICAPS 正常成長的口徑：終端元件年增中高個位數，設備最終跟隨（原話："the devices themselves grow at mid- to high single digits"）
- 2026-09-08｜Brice Hill (CFO)｜competition：NAND 位元需求高但層數堆疊使所需晶圓減少，屬升級循環，設備市場較小且預期至少持續數年（原話："it makes that market smaller"）
- 2026-09-08｜Brice Hill (CFO)｜product：面板級封裝目前仍在開發階段，已有設備營收但無量產；近期收購 NEXX（原話："I don't think there's any volume production at this point."）
- 2026-09-08｜Brice Hill (CFO)｜risk：對 HBM 堆疊層數降低（de-speccing）的看法：設備端中性，未見需求減少（原話："we would view that overall as neutral"）
- 2026-09-08｜Brice Hill (CFO)｜competition：管理層否認公司只是跟隨整體設備市場，定位為最具賦能性的整合製程設備組合（原話："We certainly don't view it that way."）
- 2026-09-08｜Brice Hill (CFO)｜capital_allocation：近期收購 X 光檢測公司與 NEXX，用於微凸塊檢測與面板細線互連（原話："We did the NEXX acquisition that I mentioned"）
- 2026-09-08｜Brice Hill (CFO)｜commitment：公司已投資並持續投資，使每季產能達目前系統產量的兩倍；強調為產能陳述而非營收預測（原話："It's not necessarily a revenue forecast"）
- 2026-09-08｜Brice Hill (CFO)｜commitment：將依元件類型彙整客戶 8 季預測並提供給 2,000 多家供應商，提前 8 季預告（原話："so that they're getting 8-quarter advance notice"）
- 2026-09-08｜Brice Hill (CFO)｜margin：近三年毛利率約擴張 300bp，其中相當部分來自定價，但管理層定位為價值反映而非漲價（原話："A lot of that has been on pricing, but it's not -- I don't"）
- 2026-09-08｜Brice Hill (CFO)｜margin：鋁、鋼、晶片、人力成本上升，因此需要往後調整價格（原話："So we do have to adjust prices going forward"）
- 2026-09-08｜Brice Hill (CFO)｜margin：價值定價適用所有產品，新舊不分，每期都須調整（原話："we have to make an adjustment each period"）
- 2026-09-08｜Brice Hill (CFO)｜guidance：服務業務長期成長預期由低雙位數上調至中十位數，因安裝基數成長快於預期（原話："from low double digits to mid-teens"）
- 2026-09-08｜Brice Hill (CFO)｜guidance：服務今年成長逾 20%，因產能利用率近滿載帶動備品採購；明年回到長期成長率（原話："We can't go to 110% next year."）
- 2026-09-08｜Brice Hill (CFO)｜margin：服務成長拆解：安裝基數每年 5–7% 加上每台平均營收提升（含 AI 調校類新服務）（原話："installed base growing every single year. 5%, 6%, 7%"）
- 2026-09-08｜Brice Hill (CFO)｜customer：DRAM 單一年產能由約 160 萬片/月，今年新增 40 萬片，未來數年每年增 30–40 萬片，且為新廠（原話："300,000 to 400,000 additional wafer starts a month"）
- 2026-09-08｜Brice Hill (CFO)｜margin：DRAM 數字口徑：升級廠設備投資約為新建廠的 25%；新建廠約 100 億美元對應 10 萬片/月（原話："about 25% of the equipment investment"）
- 2026-09-08｜Brice Hill (CFO)｜product：製程診斷與控制：電子束檢測需求顯著上升，驅動因素為 3D DRAM、4F²、GAA 到 CFET（原話："So the demand for e-beam is going up significantly"）

### AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 表示 2026 營收成長預測由 2 月 >20%、5 月 >30% 一路上調，目前接近 40%（原話："Now we're approaching 40% revenue growth"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱 2026 年 WFE 成長的 80% 來自先進邏輯代工、DRAM（含 HBM）與先進封裝，2027 年起同樣結構（原話："80% of wafer fab equipment growth this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 說明客戶提供滾動八季預測與較長期承諾（原話："rolling 8-quarter forecast and longer-term commitments"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱與客戶的討論已延伸到 2030 年（原話："discussions with customers all the way through 2030"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 指 Agentic AI 推高長期 WFE 預測，尤其是 CPU 與 DRAM（原話："driving increase in our longer-term WFE forecast"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 以先進製程晶圓起量比例說明資料中心需求：未來兩年資料中心對智慧手機達 2:1（原話："it will be 2:1 data center versus smartphone"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 回應是否有循環頂部警訊時，強調需求的廣度（原話："I've never seen a driver that's as broad and pervasive"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 表示不花時間擔心短期總體因素（原話："I don't really spend time worrying about macro effects"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：CEO 承認可能出現成長放緩的階段，但稱多年趨勢明確（原話："are there going to be periods of time where it's not growing"）
- 2026-09-09｜Gary Dickerson (CEO)｜risk：被問及客戶的客戶靠資本市場融資支撐資本支出時，CEO 表示不太擔心（原話："I don't worry so much about what you just talked about"）
- 2026-09-09｜Gary Dickerson (CEO)｜margin：CEO 稱服務業務年增逾 20%，服務毛利率提升 180 個基點（原話："Margins are up 180 basis points"）
- 2026-09-09｜Gary Dickerson (CEO)｜margin：CEO 給出半導體系統毛利率口徑：約五十幾％中段，一年增加約 190 個基點（原話："our semi systems gross margin is in the mid-50s"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 對毛利率持續上升表達高度信心（未給數字）（原話："I have very high confidence we're going to continue"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱改採不同服務合約時，每台設備營收可超過加倍（原話："we can more than double revenue per tool"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱現場已有逾 3.7 萬個腔體連接至 AI 伺服器（原話："over 37,000 chambers in the field today"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 稱 AI 內部運用主要在營收成長；會增加人力，營收成長快很多倍（原話："we will add headcount, but we're going to grow revenue"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：CEO 稱客戶遷往新地區是服務業務的順風（原話："the regionalization is a tailwind for us in our service business"）
- 2026-09-09｜Gary Dickerson (CEO)｜customer：被問 Terrafab 時，CEO 表示不談任何特定客戶（原話："I'm not going to talk about any specific customer"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱中國與整體 ICAPS 今年成長，並在可競爭領域小幅取得份額（原話："we're seeing growth this year in China and overall ICAPS"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 給 ICAPS 長期成長口徑為中至高個位數（原話："ICAPS grows at kind of mid- to high single digits"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 稱明年 ICAPS 成長會比今年略快，但仍慢於資料中心相關（原話："Next year, we see that business also growing a little bit faster"）
- 2026-09-09｜Gary Dickerson (CEO)｜guidance：CEO 對 2027 給定性說法，不給具體數字（原話："'27 is going to be a great year for Applied"）
- 2026-09-09｜Gary Dickerson (CEO)｜commitment：CEO 稱 2027 之後成長將非常強勁（原話："beyond '27, growth is going to be very strong"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱先進封裝業務今年預計成長逾 70%，規模約 20～30 億美元中點（原話："is forecasted to grow over 70% this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱檢測量測業務本曆年成長逾 50%（原話："our inspection measurement business is growing over 50% this calendar year"）
- 2026-09-09｜Gary Dickerson (CEO)｜competition：CEO 稱在電子束技術上領先業界幅度大（原話："Applied is the leader in the industry by a large amount"）
- 2026-09-09｜Gary Dickerson (CEO)｜competition：CEO 稱在晶片與封裝的材料創新上規模遠大於最近的競爭對手（原話："Applied is much larger than our nearest competitor"）
- 2026-09-09｜Gary Dickerson (CEO)｜product：CEO 稱過程控制中 e-beam 與光學兩類技術今年皆成長逾 50%（原話："growing at a very fast pace, over 50% this year"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 表示將把 80%～100% 現金回饋股東（原話："We'll return 80% to 100% of cash to shareholders"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 稱地緣政治環境下大型併購不可能（原話："it's just not possible to do large M&A"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及近期小型併購：面板級電鍍公司（原話："We just acquired a company in panel-level plating"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及另一筆 X 光技術小型併購（原話："We acquired another company with X-ray technology"）
- 2026-09-09｜Gary Dickerson (CEO)｜capital_allocation：CEO 提及混合鍵合的策略性投資，結合夥伴技術與應用材料五項技術（原話："combining a partner technology with 5 technologies"）

### 問答異常語氣（迴避／改口／保留）
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Tim Arcuri：設備成長「至少 30%」隱含下半年幾乎不再成長，為何不是 40% 以上？是保守還是有限制？｜答法：CFO 未回答保守與否，只重申 30% 年增並說不給逐季線性度，僅建議假設 FQ3 到 FQ1 以美元計線性；CEO 另指供應鏈是限制
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Tim Arcuri：華為相關限制若擴大到混合廠區，是否擴大影響？｜答法：CEO 拒絕評論限制（'I don't really want to comment on that'），僅稱已納入指引，隨即轉談 AI 運算帶動的混合
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Vivek Arya：未來 1–3 年半導體產業成長來自數量還是價格？｜答法：CEO 兩次表示不推測價格／數量（'I'm not going to speculate on pricing'），改談運算需求與市場地位
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Atif Malik：Terafab 是否在新增專案管線中？｜答法：CFO 更正自己說的是「超過 10 個」並表示無法具體點名任何專案，未回答 Terafab
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Atif Malik：大面板封裝的採用時程？｜答法：CEO 表示不願評論具體時程，改談封裝領導地位與 2026 年逾 50% 成長
- AMAT_Q2_2026_Earnings_Call_20260514.md｜問：Shane Brett：製程控制市占持續下滑，策略重要性為何？｜答法：CEO 直接反駁分析師前提，未提供市占數字，改談成長與 eBeam 領導地位
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：2027 年成長是否優於 2026 年（定性評估）｜答法：只說 2027 會 strong、不給具體數字，且未直接比較 2027 與 2026 的成長快慢
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：是否看到成長延續到 2028 年｜答法：未直接回答 2028，改談算力需求與 Agentic／實體 AI 的整體論述
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：記憶體是否持續領先成長，或何時由先進邏輯代工接手｜答法：拒絕排序（I don't know I want to handicap one versus the other），也不給數字
- AMAT_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：與 Terrafab 的技術與商業合作程度及市場地位｜答法：不談特定客戶，改答對所有客戶的合作與產品組合

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | found | 3 | 3 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 2 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 7 | 3 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260626","verdict":"觀望","role":"條件式核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI WFE 超級週期兌現（多年·非單年 melt-up）","columns":{"2Y 驗證點":"CY26 WFE +30%·先進封裝 +50%·Q3 $8.95B","5Y 驗證點":"WFE 2027 $156B·延續「similar profile」","10Y 驗證點":"AI 算力 capex 結構需求","數字門檻":"CY26 semicap +30%·8 季客戶 forecast","來源":"AMAT Q2 FY26 法說 + SEMI + Micron $100B 合約","漂移觸發":"連 2 季 capex 下修 → 削弱"}},{"id":"H2","text":"AMAT 廣度龍頭份額 holding（邊緣流失可控）","columns":{"2Y 驗證點":"核心沉積/蝕刻份額穩·先進封裝對 LRCX 不大失","5Y 驗證點":"廣度平台地位鞏固","10Y 驗證點":"材料工程廣度無被複製","數字門檻":"製程控制份額不再大降·ICAPS China 流失可控","來源":"市佔報告（MaximizeMarketResearch/Castellano）","漂移觸發":"核心沉積/蝕刻份額流失 → 削弱"}},{"id":"H3","text":"估值極端 de-rate（de-rating ＝ 進場條件）","columns":{"2Y 驗證點":"fwd PE FY27 回測 ≤ 30x（~$490）/ BB 中軌 $423","5Y 驗證點":"倍數正常化至 10 年均上緣 25-28x","10Y 驗證點":"—","數字門檻":"fwd PE FY27 ≤ 30x","來源":"§11.1（trailing 55x vs 10 年 max 31.9x）","漂移觸發":"fwd PE 維持 &gt;45x → 進場延後"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"China 結構性 mandate + 出口管制：China 24% 營收(~$6-7B)·本土 mandate 50%→2027 70%→100%·NAURA 在 SMIC 28nm 氧化爐 &gt;60%·ICAPS($3B+/yr)結構侵蝕 + MATCH Act 擬禁 DUV 對中","columns":{"對應假設":"H1·H2","時間尺度":"🔥 中期（4-6 季）·結構慢變數","監測指標":"China 本土滲透率、MATCH Act 進度、ICAPS 中國收入 YoY","警戒閾值":"mandate 達 70% 或 MATCH Act 院會通過 或 ICAPS China 收入連 4 季降"}},{"id":"R2","text":"AI WFE 週期見頂：企業 AI 落地 &lt;40% 規模化·2027 消化·hyperscaler capex 可逆·6/25 +13.4% 為單一同業財報驅動（過度解讀風險）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"hyperscaler/記憶體 capex 指引、WFE 修訂","警戒閾值":"連 2 季 capex 下修 或 mgmt 下修 CY26 WFE"}},{"id":"R3","text":"估值極端壓縮：fwd PE 54x（10 年均 19x·+138%）·現價超共識均值 $532 約 25%·melt-up 動能過飽和","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"fwd PE 分位、動能、分析師目標 vs 現價","警戒閾值":"fwd PE 跌破 30x = 進場窗口重開（非賣出）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":2.5,"ev5y_pct":5.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式核心持倉","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":null,"ev5y_pct":5.0,"irr_base_pct":2.5,"max_dd_pct":-65.0,"bull_5y_price":955.24,"bear_5y_price":307.28,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":668.0,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"AMAT","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Applied Materials"},"oneliner":"AMAT 正吃到 AI 擴產帶來的量價齊揚，毛利率連 13 季年增；但現價已按 FY2027 共識 27 倍定價，若 2028 年設備支出轉為高原，五年基準報酬只有約 4%，等 440 美元附近再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMAT_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺晶片廠擴產與換製程的設備錢：錢卡在先進邏輯、DRAM、先進封裝的材料工程步驟，服務是第二條較穩的收入","reasoning":"錢從哪來：FQ3 營收 91.15 億美元，其中半導體系統約 70.4 億（年增 27%，Non-GAAP 毛利率 55.4%、營益率 37.7%），服務 AGS 約 17.8 億（年增 22%，營益率 30.1%），其他（顯示器為主）2.94 億；公司 Non-GAAP 營益率 34.0%、GAAP 33.7%，FCF 23.3 億。FQ4 指引營收 102.5 億 ±5 億、Non-GAAP EPS 4.02 ±0.20。錢卡在哪：客戶每換一次製程（GAA、背面供電、HBM 堆疊、混合鍵合）都要多做沉積、蝕刻、CMP、磊晶與電子束檢測步驟，AMAT 在這些步驟的組合最廣；議價力來自趕產能、趕上市的時間價值，客戶給 8 季滾動預測與長交期訂單，並接受取消費與急單費。集中度：FY2025 兩大客戶各占約 19% 與 15%（前一年 12% 與 11%），合計未過四成但快速上升，是集中度風險而非護城河證據。產業時鐘在擴張期：依據是先進邏輯與 DRAM 工廠滿載、本季客戶新增逾 10 座新廠專案、合約負債 32.71 億美元（訂單代理指標）。供需判斷：週期性將反轉、時點未定，短中期瓶頸是無塵室而非需求，但需求源頭的雲端資本支出可逆。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_margi","f_kpi2_gaap_operating_margin","f_kpi3_non_gaap_free_cash_flow","f_kpi5_guidance_q4_fy2026_reven","f_kpi6_guidance_q4_fy2026_non_g","f_kpi7_contract_liabilities_bac"],"verdict_values":{"revenue_quality":"設備約 77%（循環性高）、服務約 20%（訂閱服務＋零件，隨裝機基數年增 5%–7% 與單機營收上升）、其他約 3%；未揭露 backlog 與訂單出貨比，合約負債 32.71 億美元為最接近的代理","unit_econ_note":"逐台價值定價：每台設備依為客戶創造的價值重新定價，新舊產品皆適用，用以抵銷鋁、鋼、晶片與人力成本上升（CFO 2026-09-08）；三年公司毛利率約 +300bp","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨設備支出擺動：FY2022–FY2025 年增僅 2%–4%，CY2026 接近 40%；毛利率結構性上升與服務占兩成提供部分底部"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉、時點未定：短中期瓶頸是無塵室與供應鏈而非需求（CFO 2026-09-08），但需求源頭的雲端資本支出可逆；SEMI（2026-04）預測 2027–2029 呈高原而非持續加速","bargaining":{"up":"上游逾 2,000 家供應商，CEO 稱擴產速度受供應鏈牽制；公司把 8 季預測轉給供應商以鎖定產能，上游議價力中等","down":"前兩大客戶 19% 與 15%（FY2025，前一年 12% 與 11%），買方集中上升；但目前客戶搶交期、接受取消費與急單費，賣方暫占上風","geo":"約 89% 營收來自美國以外；中國占系統＋服務營收 26%（FQ3 FY2026）"},"profit_pool_dir":"利潤池集中在晶片設計與代工端（NVIDIA 營益率 65.21%、台積電 56.1%），設備端靠價值定價小幅回收；五年利潤池占比變化事實表未涵蓋","tam_table":[{"item":"全球半導體設備銷售（SEMI，2025-12）","value":"2026 年 1,450 億、2027 年 1,560 億美元，成長主要來自 AI"},{"item":"300mm 晶圓廠設備（SEMI，2026-01 與 2026-04）","value":"2026 年 1,330 億（+18%）、2027 年 1,510 億（+14%）；2027–2029 記憶體累計 1,750 億、邏輯與微元件 2,280 億"},{"item":"WFE（Morgan Stanley，2026-07）","value":"2027 年 2,020 億（原 1,910 億）、2028 年 2,270 億（原 2,150 億）；各家口徑不同，不可直接相比"},{"item":"成長來源結構（公司，2026-08-13）","value":"先進邏輯與代工、DRAM、先進封裝約占 2026–2027 年 WFE 增量 80%"},{"item":"AMAT 先進封裝","value":"去年約 14 億美元，CY2026 成長逾 70%（CFO 2026-09-08）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋產業營業利益池歷史，無法判斷是否淨流出 5 個百分點以上"}]}}},"q2_moat":{"verdict":"護城河方向持平：AI 三大區段的份額與定價在擴大，被中國本土化的流失抵銷","reasoning":"機制：材料工程步驟的組合廣度（沉積、蝕刻、CMP、磊晶、熱處理、電子束檢測），加上早期共同開發（EPIC 已有 11 個合作，含台積電、博通）與裝機基數服務（逾 3.7 萬個腔體連上 AIx）。方向證據：投入資本事實表未涵蓋，ROIC 價差算不出；改以利潤率對最接近的設備同業 ASML：毛利率 49.4% 對 52.73%、營益率 31.09% 對 35.42%、FCF 利潤率 18.23% 對 24.27%，三項皆落後；FQ3 法說分析師也指另一家美系同業毛利率近期高約 150bp。定價權給 7 分（三年毛利率約 +300bp、13 季年增，但絕對水準仍低於同業）；執行給 8 分（營收年增 25%、全年成長預期由 >20% 一路上調到接近 40%、擴充產能到可支撐現有季產量兩倍）；合併落在 B。方向判持平：AI 三大區段在擴大，中國在縮減；第三方報告稱 2025 年多區段失份額、管理層稱今年拿份額，前者為付費牆摘要無數字可核，暫不改方向，裁決見反證紀錄。持續期：需求基礎與決策層級強，價值鏈分配與政策容忍度偏弱；增量報酬缺投入資本數據。","fact_refs":["f_peer_amat_gross_margin_pct","f_peer_amat_operating_margin_pct","f_peer_amat_fcf_margin_pct","f_peer_asml_gross_margin_pct","f_peer_asml_operating_margin_pct","f_peer_asml_fcf_margin_pct","f_peer_2330_tw_operating_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_avgo_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"最廣的材料工程製程組合（沉積、蝕刻、CMP、磊晶、熱處理、電子束檢測）＋架構定案前的共同開發（EPIC）＋裝機基數服務與 AI 調校","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（先進封裝 +70%、製程控制 +50%、DRAM 營收年增 52%）；定價面穩定偏擴大（三年毛利率約 +300bp、13 季年增，但仍低於 ASML）；中國面縮減（本土設備占比 25%→35%，新增產能據報須 50% 以上國產）。三向合計判持平","competitor_notes":[{"name":"ASML","strategy_note":"最接近的設備同業，毛利率、營益率與 FCF 利潤率皆高於 AMAT，顯示 AMAT 的定價權仍低一截；兩者分工在曝光與材料工程，直接重疊有限"},{"name":"2330.TW","strategy_note":"是客戶不是同業；營益率 56.1% 對 AMAT 31.09%，說明價值鏈利潤多留在代工端，也是 EPIC 共同開發夥伴"},{"name":"NVDA","strategy_note":"下游 AI 晶片設計端，營益率 65.21%，是需求來源而非競爭者"},{"name":"AVGO","strategy_note":"下游客製晶片端，已加入 EPIC 共同開發先進封裝，是需求與合作方而非競爭者"},{"name":"Lam Research","strategy_note":"導體蝕刻與記憶體主要對手；分析師在 FQ3 法說指其毛利率近期高 AMAT 約 150bp，數字事實表未收"},{"name":"北方華創、中微","strategy_note":"中國本土對手，在 PVD、成熟製程蝕刻與 CVD 拿份額；中微 5nm 蝕刻據報在台積電驗證"}],"spread_notes":null,"peer_na_reason":"事實表同業只有利潤率、沒有投入資本，ROIC 價差無法計算；台積電、NVIDIA、博通是客戶或下游，不是同級設備同業，只有 ASML 可比，Lam 與 KLA 事實表未涵蓋","threats":[{"level":"🟡","text":"中國本土設備商在 PVD、成熟製程蝕刻與 CVD 拿份額，政策據報要求新增產能 50% 以上用國產；限於中國成熟製程，屬點對點競爭","p":70,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","geo_supply_chain#1"]},{"level":"🟡","text":"Lam、KLA、ASML 在各自強項擴大可服務市場份額，第三方稱 AMAT 2025 年多個關鍵區段失份額","p":35,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"中微 5nm 蝕刻據報進入台積電先進製程驗證，若通過代表中國廠商首度打進中國以外的先進客戶","p":30,"evidence_refs":["customer_second_source#1"]}],"roic_durability":{"quadrant":"高利益率（TTM 營益率 31.09%）×周轉率未知（事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是晶圓廠製程工程師、決策者是晶片廠管理層、付款者是晶片廠，背後是雲端與記憶體需求；每代製程多出的材料步驟是需要不是想要，延後採購的代價是錯過 AI 晶片上市時程。急迫性不等於持久性，付款鏈最上游的雲端資本支出可逆，屬週期風險另計"},{"item":"決策層級","level":"🟢","text":"替代要在製程步驟層級衡量：每一步都要重新認證，配方與良率和設備綁定；客戶給 8 季滾動預測與長交期訂單、接受取消費，EPIC 讓 AMAT 在架構定案前就被設計進去。例外是中國受限客戶，CEO 自己承認他們可以改買非美系設備"},{"item":"價值鏈分配","level":"🟡","text":"下游拿走大部分利潤：台積電營益率 56.1%、NVIDIA 65.21%、博通 48.52%，AMAT 31.09%；AMAT 靠逐台價值定價三年回收約 300bp 毛利率，但前兩大客戶占比由 23% 升到 34%，買方集中上升，長期需求存在不等於設備端能一直多拿"},{"item":"社會容忍度","level":"🟡","text":"設備價格不受輿論約束，真正的上限是政策：美國出口管制（2026-02 與 BIS 和解付 2.525 億美元、affiliates 規則曾預告 FY2026 營收少約 6 億美元）與中國新增產能國產比例要求，共同限制中國市場（占系統＋服務 26%）可取得的份額"}],"roiic":"事實表未涵蓋投入資本；以 FY2022→FY2025 淨利增量約 4.7 億美元除以同期累計（淨利−FCF）約 2.5 億美元得到的比值約 190%，分母過小失真，不採用","reinvest_rate":"代理值約 8%：FY2022–FY2025 的 1−FCF／淨利分別為 29%、−11%、−4%、19%；FY2026 擴產期回升，TTM FCF 利潤率 18.23% 低於 FY2023 的 28.64%","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；增量 ROIC 缺數據，不給數字上限。不論增量報酬多高，約 8% 的再投資率都解釋不了 30% 以上的共識成長，成長主要來自週期量能與毛利率擴張"}}}},"q3_growth":{"verdict":"五年後的跑道仍寬：技術轉換持續增加製程步驟；但未來三年的共識成長多半是週期量能，不是再投資複利","reasoning":"成長是量為主、價為輔：CY2026 營收成長接近 40%（CEO 2026-09-09），來自客戶擴產與份額；價值定價三年貢獻約 300bp 毛利率；回購每季約 4.4 億美元，對 EPS 貢獻小；併購可忽略。共識 EPS：FY2026E 12.79、FY2027E 18.47、FY2028E 23.6，兩年 CAGR 35.8%；若以 FY2025 GAAP 8.66 為基期，三年 CAGR 39.7%，但基期口徑不同會高估；共識家數事實表未涵蓋。FY1 共識近 3 個月上修 4.32%。缺口歸因：一部分是營益率擴張（FQ3 Non-GAAP 營益率 34% 創高），其餘是既有產能利用率與客戶擴產的週期量能，屬無法歸因於再投資的部分，依規加註依賴 re-rate，長期信心上限為中。五年後跑道：設備不適用滲透率口徑；跑道來自技術轉換（GAA→CFET、4F² 與 3D DRAM、混合鍵合、面板級封裝）持續增加步驟數，且已有在收錢的第二曲線（先進封裝去年約 14 億美元、今年 +70%；製程控制 +50%），判寬。衰退信號十項亮 2 項。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi1_non_gaap_operating_margi","f_kpi5_guidance_q4_fy2026_reven"],"verdict_values":{"growth":{"driver_mix":"量（客戶擴產＋份額）為主、價（逐台價值定價）為輔；回購貢獻小、併購可忽略","runway_years":"不適用滲透率口徑；以製程技術轉換的節奏估計 10 年以上","runway_post_y5":"🟢","endo_ceiling_basis":"增量 ROIC 缺投入資本數據；再投資率代理約 8%（FY2022–FY2025 平均 1−FCF／淨利）。共識成長遠高於此可解釋範圍，判定超出內生上限","segments":[{"item":"半導體系統","value":"FQ3 約 70.4 億美元，年增 27%，Non-GAAP 毛利率 55.4%、營益率 37.7%；DRAM（含 HBM 封裝）年增 52%；FQ4 指引約 79 億（年增 62%）"},{"item":"AGS 服務","value":"FQ3 約 17.8 億，年增 22%，毛利率 35.6%、營益率 30.1%；CY2026 預期成長逾 20%，長期中雙位數；CFO 稱利用率已近滿載，明年回到長期成長率"},{"item":"其他（主要為顯示器）","value":"FQ3 2.94 億；FQ4 指引約 5.1 億，2027 年平均每季約 4 億；毛利率較低，成長時拉低公司毛利率"},{"item":"地區","value":"中國占系統＋AGS 營收 26%（FQ3），公司預期 CY2026 中國營收成長，由 28nm 代工邏輯帶動"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Non-GAAP 毛利率連 13 季年增"},{"item":"核心市占近 12 個月縮減","lit":true,"note":"中國本土設備占比 25%→35%；第三方稱 2025 年多區段失份額，AI 區段管理層稱拿份額"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"提價同時營收年增 25%"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"FQ4 指引 EPS 年增 85% 對營收 51%，屬上升段營運槓桿，反轉時同樣放大"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY2024 為 1.04、FY2025 為 0.81；TTM FCF 利潤率 18.23% 偏低，需追蹤"},{"item":"SBC／營收逾 5% 且上升","lit":false,"note":"1.85%"},{"item":"TAM 萎縮或被替代","lit":false,"note":"NAND 晶圓投片下降屬局部；未見取代現行設備的替代技術"},{"item":"產業倍數近 3 年系統性下移","lit":false,"note":"倍數在年度端點高位"},{"item":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"事實表未涵蓋拆分；資本支出主要為擴產"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"正在擴產"}]}}},"q4_capital":{"verdict":"資本配置中規中矩：股利與回購穩定、稀釋可忽略，但回購以高倍數執行，近兩季回饋率遠低於 80%–100% 的說法","reasoning":"FCF／淨利 FY2022–FY2025 為 0.71、1.11、1.04、0.81，TTM FCF 利潤率 18.23% 低於 FY2023 的 28.64%，擴產與營運資金正在吃現金。SBC 占營收 1.85%，稀釋可忽略。FQ3 現金去向（營運現金流 30.37 億美元）：資本支出 7.07 億（23%）、股利 4.2 億（14%）、回購 4.4 億（14%）、併購趨近零、其餘約 14.7 億留在帳上（48%）。股東回饋 8.6 億只占 FCF 23.3 億的約 37%，遠低於 CFO 重申的 80%–100%；回購以約 40 倍 FY1 本益比執行，買到的盈餘收益率只有 2.5%–3.6%。BIS 罰款 2.525 億美元已於 FY2026 第二季付清；剩餘回購授權 128 億美元。淨回購殖利率以 FQ3 回購年化約 17.6 億、扣除 SBC 發股後取約 0.4%。","fact_refs":["f_kpi3_non_gaap_free_cash_flow","f_kpi4_share_based_compensation","f_peer_amat_fcf_margin_pct","f_dividend_yield_ttm","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近期併購僅 NEXX（約 1.2 億美元）與一家 X 光檢測公司，規模遠低於市值 1%，已實現報酬無法量測；CEO 稱地緣政治下大型併購不可行"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"現價回購的盈餘收益率＝1÷本益比：FY1 約 2.5%、FY2 約 3.6%；通過需高於 10 年期殖利率＋2%，即殖利率須低於 0.5%–1.6%；10 年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"FQ3 SBC 1.69 億美元（營收 1.85%），年化約 6.8 億，約當市值 0.2%（市值以 FY2025 稀釋股數約 8.08 億股×507.03 推算約 4,100 億美元），遠低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近期收購只有 NEXX 約 1.2 億美元與一家 X 光檢測公司，CEO 稱大型併購不可行；回饋政策為 FCF 的 80%–100%，實際落差已寫入理由與反證紀錄"}}}},"q5_valuation":{"verdict":"現價要求 FY2027–FY2028 共識 EPS（18.47→23.6）如期兌現，且 2028 年後不明顯消化，才有中個位數年報酬；我只信前半段","reasoning":"現價 507.03，FY1 本益比 39.64 倍、FY2027 27.45 倍、FY2028 21.5 倍。要讓這個價格五年賺到 8% 以上，需要 FY2031 EPS 約 32 以上並維持 22 倍，等於 FY2028 共識之後每年再成長約 10%、且不經歷消化年。我信 FY2027 接近共識（客戶 8 季預測、FQ4 指引營收年增 51%），不信 FY2028 的 23.6 能不打折：SEMI 預測 2027–2029 呈高原，Base 取 22.0。歷史位置：trailing P/E 43.75、P/S 13.05、EV/S 12.99 都在四個年度端點最高（分位 100），但這不是五年連續分位，五年分位事實表未涵蓋。PEG 1.11 看似合理，但分母是週期上升段的成長，對循環股會低估風險。賣方目標均值 619–649 美元，現價低約 18%–22%，全距 358–900 約 2.5 倍，分歧大。結論是偏貴、不是最貴；分母（FY2027–FY2028 是否為高峰盈餘）就是爭點，所以倍數已降到 30 倍以下的便宜論證不成立。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY1＝FY2026E 共識 12.79）並列 FY2027 本益比 27.45 倍；循環股另看 FY2028 隱含 21.5 倍","tier":"大型半導體設備","peers":{"expanded":false,"reason":"事實表同業只收利潤率、未收估值倍數（Lam、KLA、ASML 本益比皆未涵蓋），無法建立同級對照；終端倍數改以本公司 FY2028 隱含 21.5 倍與前份記載的 10 年平均約 19 倍校準，此為資料缺口"},"fwd_pe":39.64,"peg":1.11,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 本益比 39.64 倍、FY2027 27.45 倍、FY2028 21.5 倍；trailing P/E、P/S、EV/S 皆在四個年度端點最高（分位 100，非五年連續分位）；PEG 1.11（FY1 本益比÷FY2026–FY2028 共識 CAGR 35.8%）。成長調整後不算最貴，但分母可能是週期高點，判偏貴；較前份降一檔，因股價跌 24% 且 FY2027 共識上修","upside_short_pct":4.1,"upside_mid_pct":17.2,"denominator_disputed":true,"denominator_note":"爭點在分母：FY2027–FY2028 共識 EPS（18.47、23.6）是否為週期高峰盈餘。若是，FY2027 本益比 27.45 倍並不便宜，倍數已降到 30 倍以下的論證無效；Base 改用低於共識的 FY2028 22.0 定價。短期上檔以 FY2028 Base 22.0×24 倍＝528 美元計，中期以 FY2031 Base 27.0×22 倍＝594 美元計"}}},"q6_how_wrong":{"verdict":"最可能看錯在把 2026–2027 的擴產高峰當成新常態；陷阱風險中等","reasoning":"依據見反證紀錄四條：論點失敗（2028 年消化）、股東經濟變差（擴產固定成本與客戶集中）、價格已反映（FY2027 本益比 27 倍）、出口管制再收緊。衰退信號十項亮 2 項：中國份額縮減、預期 EPS 成長遠快於營收（FQ4 指引 EPS 年增 85% 對營收 51%）。毛利率仍連 13 季年增、FCF／淨利未連兩年低於 0.75、SBC 低，所以不是價值陷阱，但有高峰盈餘被當常態的風險，判中等。26 週漲 27.21%、RSI 54.57，動能不過熱。","fact_refs":["f_week26_return_pct","f_rsi14","f_price_at_dd","f_consensus_rev_3m_fy1_pct","f_peer_amat_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰盈餘被當常態"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":12.79,"pe":39.64,"basis":"FY1＝FY2026E（10 月底結束）Koyfin 共識 EPS；終端倍數同樣以終端財年 EPS 為分母，同為當年度口徑"},"eps":{"bull":[20.5,27.0,31.5,36.0,40.0],"base":[18.3,22.0,22.0,24.5,27.0],"bear":[16.5,13.5,12.0,14.0,16.0]},"pe":{"bull":26,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.39,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-40,"basis":"兩段推估：只發生一次消化時，FY2027 EPS 16.5×19 倍約 313 美元（−38%）；Bear 路徑 FY2028 EPS 13.5×18 倍約 243 美元（−52%）；股價通常在 EPS 見底前先反映，再往外加寬。實例參照：2026-07 在指引上調下仍回撤 27%、6 月至今由 668 跌到 507（−24%）、前份歷史週期參考 −65%。取 −40% 至 −60%","trigger_time":null},"basis":{"bull":"AI 擴產延續到 2030（管理層稱客戶對話已延伸到 2030）：FY2028 超越共識、2029 年無消化，份額與毛利率雙升","base":"FY2027 接近共識，FY2028 低於共識（SEMI 預測 2027–2029 呈高原），FY2029 持平後恢復中高個位數成長","bear":"2027 下半年起消化：FY2028–FY2029 EPS 較高點下滑約 35%，中國本土化與出口管制同時壓縮，回升緩慢"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"SEMI（2026-04）預測 2027–2029 記憶體設備累計 1,750 億、邏輯 2,280 億美元，對應 2027 年後是高原而非加速；CEO（2026-09-09）承認會有不成長的時期，被問客戶的客戶靠資本市場融資時答不太擔心；NAND 晶圓投片持續下降","assumption":"雲端業者資本支出（美系逾 7,000 億美元）與記憶體擴產延續到 2028 年後","consequence":"設備支出單年下滑逾 20%，EPS 由 FY2027 約 18 降到 12–14，倍數壓到 17–18 倍，低點約 200–250 美元，虧損近半","ruling":"部分採納：列為 Bear 情境 30%；不全額採納，因客戶 8 季預測仍在上修、FY1 共識 3 個月上修 4.32%","watch":"8 季滾動預測用語、FY2027 與 FY2028 共識、主要客戶年度資本支出指引","evidence_refs":["supply_demand_durability#1","end_markets#3"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"公司把系統產能擴到可支撐現有季產量兩倍（目標 2028），本季新增逾 1,500 名製造與服務人員；TTM FCF 利潤率 18.23%，低於 FY2023 的 28.64%；前兩大客戶占比由 12% 與 11% 升到 19% 與 15%；FQ1 FY2027 為 14 週季、費用前置；2027 年稅率由約 11% 升到約 13%","assumption":"營收成長足以吸收擴產與人力的固定成本，且大客戶集中不轉成議價壓力","consequence":"即使 AI 需求成立，若成長在 2028 年後放緩，新增產能與人力變成負槓桿，毛利率回吐、FCF 轉換率續低，高倍數回購降低每股價值","ruling":"採納為監測項，不進 Base 數字：CFO（2026-09-08）強調是產能而非營收預測，擴產可分段；已納入毛利率與客戶集中的風險門檻","watch":"Non-GAAP 毛利率年增減、FCF／淨利、前兩大客戶占比（年報）","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_peer_amat_fcf_margin_pct","f_kpi3_non_gaap_free_cash_flow"]},{"view":"價格已反映太多","evidence":"FY2027 本益比 27.45 倍；trailing P/E 43.75、P/S 13.05、EV/S 12.99 都在四個年度端點最高；2026-07 在指引上調下仍回撤 27%；6 月至今股價由 668 跌到 507","assumption":"市場在可能的高峰盈餘上仍給接近 30 倍","consequence":"Base 五年價格報酬約 17%（年化約 3%），加股息與回購約 4%；需要 Bull 才有雙位數","ruling":"採納，為本輪主要約束；但不認為已反映全部，因股價低於賣方均值約 18%–22%、FY2027 共識仍在上修","watch":"股價對 440 美元重啟價、FY2027 共識方向","evidence_refs":["capital_markets_pricing#5"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current"]},{"view":"論點失敗","evidence":"affiliates 規則曾預告使 FY2026 營收少約 6 億美元（FQ4 約 1.1 億），美中會談後暫停；2026-02 因經南韓子公司對中芯出貨違規與 BIS 和解付 2.525 億美元；CEO 承認受限客戶可改買非美系設備","assumption":"暫停持續，限制不擴大到更多中國客戶或成熟製程","consequence":"單一規則約 6 億美元營收（FY2025 營收約 2%），粗估 EPS 影響約 2%；若擴大到更多客戶或成熟製程影響可到數倍，且份額被日歐與本土廠接手後不回流，與週期轉弱同時發生時會放大 Bear","ruling":"部分採納：列為風險 R2，不設為唯一致命點，因單一規則的衝擊小於設備支出週期的 EPS 槓桿","watch":"公司 8-K 與法說揭露的營收影響金額、affiliates 規則狀態","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","reg_tariff_export#2"],"fact_refs":["f_kpi0_revenue_gaap"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 668.0 → 本次 507.03（-24.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=668.0","side_b":"本次 price_at_dd=507.03","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式核心持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式核心持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"份額方向","cause":null,"prior_field":null,"side_a":"第三方研究（Castellano，2026-05）稱 AMAT 2025 年在多個關鍵設備區段失份額，Lam、KLA、ASML 在各自可服務市場擴大；FQ2 法說（2026-05-14）分析師也質疑製程控制份額下滑","side_b":"CFO（2026-08-13）稱今年預期拿份額、成長快於市場；CEO 稱 GAA 與配線可服務市場份額逾 50%、DRAM 份額十餘年增約 10 個百分點；製程控制今年成長逾 50%","ruling":"不可調和（方向相反），裁採管理層一側但只限 AI 三大區段：CY2026 營收成長接近 40%（CEO 2026-09-09），與分析師在法說引述的同業 WFE 年增約 38% 大致相當，快於市場尚未被數字證實，只能說沒有落後；第三方報告為付費牆摘要，無數字可核，中國成熟製程則採第三方一側","evidence_level":"A 側為付費牆摘要（二手），B 側為公司法說（一手但自利）","settle_metric":"CY2026 AMAT 半導體系統成長率對 WFE 成長率（2027 年初第三方統計）","if_then":["若 AMAT 成長低於 WFE：H2 削弱，Bull 機率降到 20%，不追、停止加碼","若 AMAT 成長高於 WFE 3 個百分點以上：H2 確認，護城河執行分維持並考慮上調","反向條件：若 FQ1 FY2027 法說不再提拿份額，即使 WFE 數據未出也視同削弱"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#4"]},{"axis":"中國營收方向","cause":null,"prior_field":null,"side_a":"財報前預覽（Hudson Labs，2026-08-10）稱公司預期 2026 年中國 WFE 下降、限制無實質放寬，Mizuho 預期持續失份額；中國本土設備占比 2025 年達 35%","side_b":"CFO（2026-08-13）稱中國占系統＋AGS 營收 26%，預期中國營收今年成長，由 28nm 代工邏輯帶動；CEO（2026-09-09）稱在可競爭領域小幅拿份額","ruling":"可調和（程度差）：短期採公司口徑（最新且有占比數字），長期採本土化方向（新增產能國產比例要求）；中國營收短期成長不改變份額長期下滑的結構","evidence_level":"公司法說為一手；本土化比例為產業媒體二手","settle_metric":"FY2026 年報中國營收占比（FY2025 為 28%）與金額年增減","if_then":["若 FY2026 中國金額年增且占比不低於 24%：R1 維持觀察","若 FY2026 中國金額年減逾 15%：R1 升為主要風險，Bear 機率加 5 個百分點"],"evidence_refs":["end_markets#6","reg_tariff_export#4","customer_second_source#0"]},{"axis":"股東回饋承諾對實際","cause":null,"prior_field":null,"side_a":"CFO（2026-08-13）稱持續預期把 80%–100% FCF 回饋股東，CEO（2026-09-09）重申","side_b":"FQ3 FCF 23.3 億美元，股利 4.2 億＋回購 4.4 億＝8.6 億，回饋率約 37%；FQ2 回饋 7.65 億","ruling":"可調和：擴產與營運資金占用現金，承諾以全年或多年計；但若全年回饋率仍低於 60%，代表現金被擴產鎖住","evidence_level":"皆為公司一手揭露","settle_metric":"FY2026 全年股東回饋÷FCF","if_then":["若全年低於 60%：資本配置結論下修一級，Base 終端倍數下修 1 倍","若全年達 80% 以上：承諾兌現，維持"],"evidence_refs":[]},{"axis":"毛利率擴張節奏","cause":null,"prior_field":null,"side_a":"FQ4 指引 Non-GAAP 毛利率約 50.4%，在營收季增約 12% 下仍持平；CFO（2026-08-13）稱後續改善屬緩慢","side_b":"CEO（2026-08-13、2026-09-09）稱對毛利率持續上升有高度信心；三年約 +300bp、13 季年增","ruling":"可調和：本季新增逾 1,000 名服務工程師等擴產前置成本壓住短期；H3 只要求不連 2 季年減，不假設加速擴張","evidence_level":"皆為公司一手","settle_metric":"FQ1 FY2027（14 週季）Non-GAAP 毛利率年增減","if_then":["若 FQ1 FY2027 毛利率年減：H3 進入觀察，再一季即削弱","若達 51% 以上：H3 確認，Base 終端倍數可上調 1 倍"],"evidence_refs":[]},{"axis":"賣方共識對本判斷","cause":null,"prior_field":null,"side_a":"賣方均值偏多：Investing.com 均值約 639（36 位，33 位買進）、Benzinga 649、StockAnalysis 623、TIKR 619；UBS 695、Citi 710","side_b":"近期下調與保守：Mizuho 8/25 降至 590，Morgan Stanley 9/28 持有、目標 563；全距 358–900","ruling":"可調和：現價 507 低於各來源均值約 18%–22%，賣方均值方向上支持偏多，但本判斷不跟隨，因均值隱含 2028 年後不消化，與 SEMI 2027–2029 高原預測不一致；全距 900÷358 約 2.5 倍，已達分歧上限，下調自身 Bull 信心並限制起始倉位","evidence_level":"二手彙整，各來源基準日不一","settle_metric":"投資人早餐會後賣方目標價與 FY2028 共識方向","if_then":["若早餐會後 FY2028 共識上修至 26 以上：重算 Base，重啟價可上調","若 FY2028 共識下修：維持觀望，重啟價下修"],"evidence_refs":[]},{"axis":"估值與情境結果漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-06-26，股價 668）：估值結論為最貴一檔，Base IRR 2.5%、五年期望值 5.0%，Bull 價 955.24、Bear 價 307.28，裁決觀望","side_b":"本輪股價 507.03（較前份 −24%）；FY2027 共識由前份隱含約 16.3（30 倍約 490 美元）上修到 18.47，FY2027 本益比由約 41 倍降到 27.45 倍；估值結論降一檔為偏貴；IRR、期望值、Bull 與 Bear 價位的變動拆成「情境重建」與「股價下跌」兩條","ruling":"漂移主因是價格下跌，次因是共識上修，兩者同向壓縮倍數；但不改變分母可能是週期高點的爭點","evidence_level":"價格與共識皆為事實表數字","settle_metric":"股價與 FY2027 共識","if_then":["若股價反彈到 600 以上而共識未再上修：估值結論回到最貴一檔"],"evidence_refs":[]},{"axis":"期望報酬拆解：情境重建（股價固定在前份 668 美元重算）","cause":"方法變動","prior_field":["bull_5y_price","bear_5y_price","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份情境、股價 668 美元：Bull 價 955.24、Bear 價 307.28，五年期望值 5.0%，基準年化 2.5%，前份未列不對稱比","side_b":"本次情境、股價仍用 668 美元：Bull 價 1,040、Bear 價 272，五年期望值 −8.8%，基準年化 −2.3%，不對稱比 0.78","ruling":"先換情境、股價不動：Base 的 FY2028 取 22.0 美元、低於共識，五年期望值少 13.8 個百分點，基準年化少 4.8 個百分點。Bull、Bear 價位與股價無關，變動全部來自情境重建。","evidence_level":"程式計算","settle_metric":"股價與 FY2027 共識","if_then":[],"evidence_refs":[]},{"axis":"期望報酬拆解：股價下跌（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 668 美元：五年期望值 −8.8%，基準年化 −2.3%，不對稱比 0.78","side_b":"本次情境、股價 507.03 美元：五年期望值 +20.1%，基準年化 3.2%，不對稱比 1.9","ruling":"再換股價、情境不動：起點價跌 24%，五年期望值多 28.9 個百分點，基準年化多 5.5 個百分點。期望報酬比前份好，全部來自股價下跌，情境本身比前份差。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"股價與 FY2027 共識","if_then":[],"evidence_refs":[]},{"axis":"評級、護城河方向與跑道維持","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5"],"side_a":"前份：綜合評級 B、護城河方向持平、五年後跑道寬","side_b":"本輪三者維持不變","ruling":"新證據正負相抵：正面為 FQ3 毛利率 13 連季年增、先進封裝成長逾 70%、製程控制逾 50%、DRAM 營收年增 52%；負面為中國新增產能國產比例要求、本土設備占比 35%、第三方份額流失報告與 2026-08 中國問題惡化報導","evidence_level":"公司一手與產業媒體二手並存","settle_metric":"CY2026 半導體系統成長對 WFE、中國營收占比","if_then":["若中國占比連 4 季低於 20%：護城河方向改為縮減並重跑判斷"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"陷阱、類型、循環位置與機率","cause":"方法變動","prior_field":["trap","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：價值陷阱判低、公司類型與循環位置未填、最大回撤單點 −65%、Bull 30% 與 Bear 25%","side_b":"本輪：逐條核對十項衰退信號亮 2 項，陷阱風險改為中等；類型定為循環股（次為品質複利）、位置中循環；最大回撤改為 −40% 至 −60% 範圍；Bull 25% 與 Bear 30%","ruling":"方法變動：本輪先檢查內生成長上限，共識成長明顯超出再投資可解釋的範圍，Bear 機率下限 30%；最大回撤改範圍，以反映倍數壓縮與 EPS 下修兩段來源","evidence_level":"推導依據為事實表年報與共識數字","settle_metric":"FY2027 共識方向、8 季預測用語","if_then":["若 FY2028 共識上修至 26 以上且 8 季預測續升：Bear 機率可回到 25%"],"evidence_refs":[]},{"axis":"重啟進場門檻變動","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份重啟條件未設（null）；前份進場條件為 H3 的 FY2027 本益比 30 倍以下（約 490 美元），與 R3 的 Fwd P/E 跌破 30 倍即進場窗口重開","side_b":"本輪重啟進場（首倉）條件：股價 440 美元以下（約 FY2027 共識 24 倍）且 FY2027 共識 EPS 未自 18.47 下修逾 5%","ruling":"前份進場條件已在價格下跌與共識上修下達成（27.45 倍），本輪不據此進場：一，舊條件只看單一年度倍數，沒處理 2028 年後的高原；二，本輪 Base 以 FY2028 22.0（低於共識 23.6）計，現價五年年化約 4%，440 美元時約 7%。門檻提高來自方法改用週期調整後的 Base 報酬，不是因價格到了才改，舊門檻退休理由記於此。現在就買的最強論證：舊條件已達、FY1 共識 3 個月上修 4.32%、股價低於賣方均值約 20%、管理層全年成長預期由 >20% 一路上調到接近 40%；若早餐會長期模型把 FY2028 共識推到 26 以上，按新方法也接近進場","evidence_level":"價格與共識為事實表數字，高原判斷來自 SEMI 預測","settle_metric":"股價、FY2027 與 FY2028 共識","if_then":["若股價 440 以下且 FY2027 共識未下修逾 5%：重跑判斷後小額首倉","若 FY2028 共識達 26 以上而股價在 520 以下：重算，可能提前進場","若 FY2027 共識下修逾 10%：價格錨作廢，改等 8 季預測恢復上修"],"evidence_refs":[]},{"axis":"減碼與清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標（null）","side_b":"本輪五項：FY2027 共識下修逾 10%、Non-GAAP 毛利率連 2 季年減、中國占比連 4 季低於 20%、8 季預測首次下修、出口管制新規影響 5 億美元以上","ruling":"新設為減碼與清倉的依據：前兩項任一觸發且持有時減碼至半倉；8 季預測下修與共識下修同時觸發時清倉","evidence_level":"指標皆為公司或共識每季可得","settle_metric":"各指標每季讀數","if_then":["任一指標觸發：重跑判斷，持有時依上列動作執行"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"主要晶圓廠客戶的 8 季滾動預測轉為下修（管理層法說首次承認較前季下修）","ruling":"新設：以數學上最大的單一敏感度為準，EPS 對設備支出的槓桿約 1.7 倍（FQ4 指引營收年增 51%、EPS 年增 85%），大於中國或出口管制的單一衝擊","evidence_level":"公司指引為一手","settle_metric":"每季法說 8 季預測用語","if_then":["若發生：不追，重啟價作廢，改等預測恢復上修；持有時清倉一半"],"evidence_refs":[]},{"axis":"風險門檻變動","cause":"方法變動","prior_field":["thesis.R"],"side_a":"前份 R1：本土設備規定達 70% 或 MATCH Act 院會通過或 ICAPS 中國營收連 4 季降；R2：連 2 季資本支出下修或管理層下修 CY26 WFE；R3：Fwd P/E 跌破 30 倍即進場窗口重開","side_b":"本輪 R1 保留 70% 規定與 ICAPS 中國連 4 季降，新增中國占比連 4 季低於 20%；MATCH Act 本包無進度資料，標資料缺口保留；前份 R2 併入本輪 R3（8 季預測首次下修或 FY2027 共識下修逾 10%）；前份 R3 退休","ruling":"前份 R3 退休理由：條件已達成（FY2027 本益比 27.45 倍），角色由新的重啟價取代；其餘門檻保留，或改用公司每季揭露、可追蹤的指標；觸發時的減碼動作見 kill 指標","evidence_level":"門檻來源為公司揭露與政策事件","settle_metric":"中國占比、8 季預測用語、FY2027 共識","if_then":["若 MATCH Act 取得進度資料且院會通過：R1 視同觸發"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到 440 美元以下（約 FY2027 共識 24 倍）且 FY2027 共識 EPS 未較 18.47 下修逾 5%","type":"估值rearm","maps_to":"H1","metric":"收盤價＋FY2027 共識 EPS","threshold":"440 美元以下且共識不低於 17.55","action":"重跑判斷，通過後小額首倉","source_freq":"每日股價；共識每月快照","date":null},{"n":2,"text":"投資人早餐會公布長期模型：若隱含 FY2028 EPS 明顯高於共識 23.6 且賣方跟進上修到 26 以上，重算情境","type":"複審日期","maps_to":"H1","metric":"FY2028 共識 EPS","threshold":"26.0 以上","action":"重跑情境與重啟價","source_freq":"一次性事件＋月度共識","date":"2026-10-13"},{"n":3,"text":"FQ4 FY2026 營收低於指引下緣 97.5 億美元，或 Non-GAAP EPS 低於 3.82","type":"假設驗證","maps_to":"H1","metric":"FQ4 營收與 Non-GAAP EPS","threshold":"低於 97.5 億美元或低於 3.82","action":"H1 標削弱，重啟價下修並暫停進場","source_freq":"季報","date":"2026-11"},{"n":4,"text":"管理層首次表示客戶 8 季滾動預測較前季下修","type":"Single Thing","maps_to":"R3","metric":"8 季滾動預測方向（法說用語）","threshold":"首次下修","action":"不追；重啟價作廢，改等預測恢復上修","source_freq":"每季法說與投資人活動","date":null},{"n":5,"text":"美國出口管制新規（或 affiliates 規則恢復）使次財年營收受影響 5 億美元以上","type":"風險","maps_to":"R2","metric":"公司揭露的營收影響金額","threshold":"5 億美元以上","action":"Bear 機率上調到 35% 並重算重啟價","source_freq":"公司 8-K 與法說，事件驅動","date":null},{"n":6,"text":"中國占系統＋AGS 營收比重連 4 季低於 20%，或本土設備規定提高到 70%","type":"風險","maps_to":"R1","metric":"中國營收占比；本土設備比例規定","threshold":"連 4 季低於 20%，或規定達 70%","action":"H2 標削弱，護城河執行分下修 1 分","source_freq":"季報；政策事件","date":null},{"n":7,"text":"Non-GAAP 毛利率連 2 季年減","type":"假設驗證","maps_to":"H3","metric":"Non-GAAP 毛利率年增減","threshold":"連 2 季為負","action":"H3 標削弱，Base 終端倍數下修 2 倍重算","source_freq":"季報","date":null},{"n":8,"text":"CY2026 半導體系統成長率低於同期 WFE 成長率","type":"假設驗證","maps_to":"H2","metric":"AMAT 半導體系統曆年成長對 WFE 成長","threshold":"差距為負","action":"H2 標削弱，Bull 機率下修到 20%","source_freq":"年度（2027 年初第三方統計）","date":"2027-03"}],"kill_metrics":[{"metric":"FY2027 共識 EPS","bear_threshold":"較 18.47 下修逾 10%（低於 16.6）","window":"2026-10 至 2027-04","source":"Koyfin 月度共識快照","last_status":"ok"},{"metric":"Non-GAAP 毛利率年增減","bear_threshold":"連 2 季為負","window":"滾動 2 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"中國占半導體系統＋AGS 營收比重","bear_threshold":"連 4 季低於 20%（FQ3 FY2026 為 26%）","window":"滾動 4 季","source":"公司法說與季報","last_status":"ok"},{"metric":"客戶 8 季滾動預測方向（管理層用語）","bear_threshold":"首次表示較前季下修","window":"每季法說","source":"公司法說與投資人活動逐字稿","last_status":"ok"},{"metric":"出口管制新規對次財年營收影響","bear_threshold":"5 億美元以上","window":"公告後 1 季內","source":"公司 8-K、新聞稿與法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"lawsuit_class_action#0","reason":"只有律所招攬調查的公告，搜尋未見已提起的集體訴訟，沒有求償金額、受影響期間營收或程序里程碑可追蹤；事件期間 2023-11 至 2024-08 已超出近 12 個月"}],"action_conditions":{"rearm_trigger":"股價≤440 美元（約 FY2027 共識 24 倍）且 FY2027 共識 EPS 未自 18.47 下修逾 5%；觸發後重跑判斷再定首倉","exec_line":"觀望不追；觸及重啟條件後重跑判斷，通過才以小額起始倉進場；FY2027 共識下修逾 10% 則價格錨作廢，改等 8 季預測恢復上修"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 440 美元以下且 FY2027 共識 EPS 未較 18.47 下修逾 5%；或投資人早餐會後 FY2028 共識上修到 26 以上時重算","qc48_result":"pass","qc48_note":"AMAT 的 Bull 情境有逐年 EPS 數字，但沒有分部的量價推導，成長跑道的證據主要來自管理層說法，且我查不到可比案例的 5 年報酬；這三項都不足以判成立，也沒有足以直接否定的反證，因此只能算部分站得住。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=27.21, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='AMAT 的 Bull 情境有逐年 EPS 數字，但沒有分部的量價推導，成長跑道的證據主要來自管理層說法，且我查不到可比案例的 5 年報酬；這三項都不足以判成立，也沒有足以直接否定的反證，因此只能算部分站得住。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 440 美元以下且 FY2027 共識 EPS 未較 18.47 下修逾 5%；或投資人早餐會後 FY2028 共識上修到 26 以上時重算'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 驅動的晶圓廠設備支出延續多年成長：2027 年續創新高，2028 年不轉為年減","2y":"CY2026 營收成長接近 40%（CEO 2026-09-09）；FQ4 營收落在 97.5–107.5 億美元指引內；FY2027 共識 EPS 維持在 18.47 附近","5y":"2027–2029 設備支出呈高原或成長、無單年逾 20% 下滑（SEMI 2026-04：2027 年 300mm 設備首破 1,500 億美元）","10y":null,"threshold":"FY2027 共識 EPS 不低於 16.6（較 18.47 下修不超過 10%），且管理層未表示 8 季滾動預測下修","source":"公司季報與法說、SEMI 與賣方設備支出預測、Koyfin 共識快照","drift_rule":"共識或實際營收連 2 季低於前次基準 5% 以上視為削弱；連 3 季低於 10% 以上視為反轉"},{"id":"H2","text":"AMAT 在先進邏輯（GAA、背面供電）、DRAM、先進封裝三個成長最快區段擴大份額，足以抵銷中國成熟製程的流失","2y":"CY2026 先進封裝成長逾 70%、製程診斷與控制逾 50%，半導體系統成長不低於整體設備支出","5y":"GAA 與配線可服務市場份額維持過半（公司 2026-02 法說），DRAM 份額不回吐","10y":null,"threshold":"CY2026 半導體系統成長率不低於同期 WFE 成長率（第三方統計）","source":"公司法說、第三方份額研究（TechInsights、Castellano 等）、賣方 WFE 統計","drift_rule":"連 4 季成長落後 WFE 5 個百分點以上視為削弱；連 6 季落後 10 個百分點以上視為反轉"},{"id":"H3","text":"價值定價、服務與製程控制的組合推動毛利率續升","2y":"Non-GAAP 毛利率維持 50% 以上（FQ4 指引 50.4%），半導體系統 55% 以上","5y":"公司 Non-GAAP 毛利率 52% 以上，服務維持中雙位數年成長","10y":null,"threshold":"Non-GAAP 毛利率年增減不得連 2 季為負","source":"公司季報新聞稿與法說的分部毛利率","drift_rule":"連 2 季年減視為削弱；連 3 季年減且累計逾 100bp 視為反轉"}],"R":[{"id":"R1","text":"中國本土化：本土設備占比 2025 年達 35%，新增產能據報須 50% 以上國產；北方華創、中微在 PVD、成熟製程蝕刻與 CVD 拿份額；中國占系統＋AGS 營收 26%","h_ref":"H2","clock":"🔥","threshold":"中國占比連 4 季低於 20%；或本土設備規定提高到 70%；或 ICAPS 中國營收連 4 季年減；或 MATCH Act 院會通過（本包無進度資料，資料缺口）","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","customer_second_source#0","reg_tariff_export#4","geo_supply_chain#1","end_markets#6"]},{"id":"R2","text":"美國出口管制再收緊：affiliates 規則曾預告使 FY2026 營收少約 6 億美元，暫停後可能恢復；2026-02 因 2020–2022 年對中出貨違規與 BIS 和解付 2.525 億美元，後續須內部稽核","h_ref":"H1","clock":"⚡","threshold":"公司揭露新規使次財年營收受影響 5 億美元以上，或再出現出口管制違規調查","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","regulatory_antitrust#0","geo_supply_chain#0","major_events#0"]},{"id":"R3","text":"設備支出週期在 2027–2028 年轉弱：雲端資本支出可逆，NAND 晶圓投片持續下降，SEMI 預測 2027 年後呈高原","h_ref":"H1","clock":"🔥","threshold":"管理層首次表示 8 季滾動預測下修；或 FY2027 共識 EPS 自 18.47 下修逾 10%；或主要客戶連 2 季下修資本支出","evidence_refs":["supply_demand_durability#1"]},{"id":"R4","text":"客戶集中上升：前兩大客戶由 FY2024 的 12% 與 11% 升到 FY2025 的 19% 與 15%，議價力向買方移動","h_ref":"H3","clock":"🐢","threshold":"單一客戶占比逾 25%，且同期毛利率年減","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"主要晶圓廠客戶的 8 季滾動預測轉為下修（管理層法說首次承認較前季下修），代表 2028 年設備支出由成長轉為年減","why_fatal":"營收與 EPS 對設備支出高度槓桿：FQ4 指引營收年增 51%、EPS 年增 85%，槓桿約 1.7 倍；反向時 FY2028 共識 23.6 會被砍向 13–16，倍數同時壓縮，兩段疊加","if_happens":"不追；重啟價作廢，改用事件錨（預測恢復上修）；若當時持有，清倉一半","how_monitor":"每季法說的 8 季預測用語、主要晶圓廠與雲端業者資本支出指引、FY2027 與 FY2028 共識月度快照","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":27.45,"peg_fy2":0.99,"stress":{"pass":8,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":8.66,"FY2026E":12.79,"FY2027E":18.47,"FY2028E":23.6},"fy_end_month":10,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識，推定為 Non-GAAP（FQ3 Non-GAAP 3.50＋FQ4 指引 4.02 已占 7.52，與 12.79 量級相符）；FY2025A 用年報 GAAP 稀釋 EPS 8.66（事實表未收 Non-GAAP 年度值），基期口徑不同會高估三年 CAGR"},"catalysts":[{"date":"2026-10-12","date_precision":null,"type":"product","event":"EPIC Center 揭幕（矽谷共同研發中心）","impact":"低","watch":"首批客戶進駐與正式啟用時程"},{"date":"2026-10-13","date_precision":null,"type":"guidance","event":"SEMICON West 投資人早餐會，公布長期成長與利潤率展望","impact":"高","watch":"長期模型隱含的 FY2028 EPS 是否高於共識 23.6；WFE 1,500–1,750 億美元情境下的營收與營益率"},{"date":"2026-11","date_precision":"month","type":"guidance","event":"FQ4 FY2026 財報與 FQ1 FY2027（14 週季）展望","impact":"高","watch":"營收對 97.5–107.5 億美元區間、毛利率 50.4%、8 季預測用語"},{"date":"2027-01","date_precision":"quarter","type":"macro","event":"主要晶圓廠與記憶體客戶公布年度資本支出計畫","impact":"高","watch":"2027 年資本支出是否續增、2028 年有無消化跡象"},{"date":null,"date_precision":null,"type":"regulatory","event":"出口管制 affiliates 規則暫停狀態","impact":"中","watch":"是否恢復；恢復即回到約 6 億美元年營收影響"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
