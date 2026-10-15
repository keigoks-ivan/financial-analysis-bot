你是 DD 管線 v20 的判斷層閘（gate），標的 MRVL（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝2739.3 USD M｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：新聞稿稱高於自家指引中點 $39.0M；分析師共識未取得
- `f_kpi1`（q1_business）｜資料中心營收＝2171.5 USD M｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：未取得
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝36.6 %（營業利益 1,003.2M）｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：未取得
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益／利益率＝16.8 %（營業利益 459.7M）｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：未取得
- `f_kpi6_gaap_non_gaap`（q1_business）｜GAAP／Non-GAAP 毛利率＝58.9 % Non-GAAP（GAAP 53.1%）｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：未取得
- `f_kpi7_q3_fy2027_2026_10_31`（q1_business）｜管理層指引：Q3 FY2027（季末 2026-10-31）＝營收 3.150B ±5%（約 2.99–3.31B）；Non-GAAP 毛利率 57.5–58.5%；Non-GAAP 營業費用約 655M；Non-GAAP EPS 1.10±0.05；GAAP EPS 0.53±0.05 指引｜期間與口徑：Q2 FY2027（公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2027（公告於 2026-08-27））
  - 註記：未取得
- `f_peer_mrvl_gross_margin_pct`（q2_moat）｜MRVL 毛利率＝52.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_operating_margin_pct`（q2_moat）｜MRVL 營業利益率＝16.81 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_fcf_margin_pct`（q2_moat）｜MRVL FCF 利潤率＝18.23 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_gross_margin_pct`（q2_moat）｜AVGO 毛利率＝68.77 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_fcf_margin_pct`（q2_moat）｜AVGO FCF 利潤率＝44.22 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amd_gross_margin_pct`（q2_moat）｜AMD 毛利率＝53.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amd_operating_margin_pct`（q2_moat）｜AMD 營業利益率＝15.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3661_tw_gross_margin_pct`（q2_moat）｜3661.TW 毛利率＝37.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3661.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3661_tw_fcf_margin_pct`（q2_moat）｜3661.TW FCF 利潤率＝-10.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3661.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.22 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.25 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝12.18 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝17.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（10.41 → 12.18）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝7.25 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（6.76 → 7.25）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占營收／占 GAAP 營業利益＝11.9 % 占營收（SBC 326.2M；占 GAAP 營業利益約 71%）｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.marvell.com Q2 FY27 press release；比率自算（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：不適用
- `f_kpi4_605_5m_capex_126_7m`（q4_capital）｜自由現金流（營業現金流 605.5M − capex 126.7M，自算，公司未列示）＝478.8 USD M｜期間與口徑：Q2 FY2027（季末 2026-08-01，公告於 2026-08-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表 investor.marvell.com Q2 FY27 press release；FCF 為自算（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2027（季末 2026-08-01，公告於 2026-08-27））
  - 註記：未取得
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.087 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝65.23 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 4.22，分子＝快照價 275.28｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝275.28 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝90.55 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝26.18 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝26.32 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.2 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 4.05 → 4.22（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝114.34 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝61.52｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（28 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Futurum 估計 Marvell 仍為 XPU 第二大業者，但 Alchip、GUC 與 Broadcom 的既有優勢是主要逆風
  - 來源：Futurum Group, Marvell Q2 FY 2026 Earnings: Data Center Growth Healthy but Overshadowed by Rising Competition（as_of 2025-08-29）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Marvell 的 XPU 專案面臨台灣設計服務業者（Alchip、GUC）競爭而有毛利壓力；有未證實的二手報導稱 Trainium 3/4 轉向 Alchip
  - 來源：Dolphin Research 筆記（經搜尋摘要轉述，Marvell FY26 Q2 後）（as_of 2025-09-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：Digitimes 2026-01-30 標題顯示 MediaTek、Alchip、Marvell 爭奪 ASIC 第二名；內文未取得
  - 來源：Digitimes, MediaTek, Alchip, Marvell clash for ASIC runner-up spot（as_of 2026-01-30）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：光 DSP：Marvell 與 Broadcom 合計近 90% 份額；2025 年 5 月研究稱 Broadcom 與 MaxLinear 開始送 800G DSP 認證，報價 Marvell $90–100 對 $50–60
  - 來源：Dolphin Research (2025-01)；Global Technology Research Substack (2025-05)（as_of 2025-05-01）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#6`（competitive_share_entrants｜方向 -｜狀態 ok）：Cignal AI：相干 DSP 400G 由 Acacia 與 Marvell 主導，800G 可插拔份額之爭將更競爭
  - 來源：Cignal AI, Tracking the coherent DSP supply chain 2026（as_of 2026-04-01）｜affects：moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-Q 風險揭露：AWS 為 Marvell 最大客戶且差距顯著；Trainium 放緩或轉向其他設計夥伴將對營收造成重大影響。
  - 來源：Marvell 10-Q FY2026 (quarter ended 2026-05-02), via search summary（as_of 2026-05-02）｜affects：decision_inputs.bear、thesis.R
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：Marvell 風險揭露警告部分大客戶可能自行開發並製造半導體方案，導致 Marvell 失去業務。
  - 來源：Marvell 10-Q FY2026 (quarter ended 2026-05-02), via search summary（as_of 2026-05-02）｜affects：moat_trend、thesis.R
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：Benchmark 降評稱 Marvell 將 Trainium 3 與 4 設計輸給台灣 Alchip；未經公司證實。
  - 來源：AOL/Barron's-type coverage: Will Customer Defections Crumble Marvell Technology's AI Empire?（as_of 2026-03-08）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：The Information 報導 Microsoft 正評估 Broadcom 作為晶片設計夥伴（Maia）。
  - 來源：AOL: Will Customer Defections Crumble Marvell Technology's AI Empire?（as_of 2026-03-08）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 10-K：兩家客戶占營收 10% 以上（一家經銷商、一家直接客戶）；前十大客戶（含經銷商與直接客戶）占 FY2026 淨營收 82%。
  - 來源：Marvell Form 10-K FY2026 (mrvl-20260131)（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：第三方彙整稱 FY2026 經銷商 A 占淨營收 37%、一家直接客戶 14%（未對照 10-K 原文確認）；經銷商 A 占比 FY2024 24%→FY2025 34%，FY2025 直接客戶 13%。
  - 來源：autobound.ai / policyrisk.com 彙整；FY2025 10-K（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：超大型雲端業者資本支出與舉債升高：S&P 預估 2026 年五大業者 capex 約 7,500 億美元；Q1 美國超大型業者直接發債 1,150 億美元（2025 全年 700 億）；PIMCO 預估 capex 吃掉 94% 營運現金流。搜尋結果未見 Amazon／Microsoft／Google 的評等調降事件。
  - 來源：FactSet Insight 2026-07-23 及 fi-desk 等彙整（as_of 2026-07-23）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：S&P：聯發科瞄準 2027 年客製 AI 加速器可服務市場最高 20%，首顆 ASIC Q4 2026 量產（客製 ASIC 競爭者增加）
  - 來源：S&P Global Market Intelligence: MediaTek's AI ASICs growth to offset smartphone weakness（as_of 2026-08-26）｜affects：decision_inputs.bear、moat_trend
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：Bank of America 預估超大型雲端業者合計自由現金流 2026 約 -640 億美元、2027 約 -1,440 億、2028 約 -1,860 億；Goldman 預期債務涵蓋 2027 年 AI capex 約三分之一；市場共識傾向 2027 年 capex 見頂後持平
  - 來源：TFTC: AI capex cash flow negative 2027 peak hyperscalers（as_of 2026-09-01）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2026 10-K 揭露：部分對中國客戶銷售需出口許可，過去部分許可曾被延遲或拒絕，未來核准無保證；10-Q（2026-05）重複此語。
  - 來源：Marvell Technology, Inc. Form 10-K FY2026 / Form 10-Q (quarter ended 2026-05-02)（as_of 2026-01-31）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2026 年報（ARS）討論美國商務部對半導體進口的 Section 232 國安調查，可能導致額外關稅與貿易限制（貿易事項，非反壟斷）。
  - 來源：Marvell Technology, Inc. Form ARS FY2026 (SEC)（as_of 2026-01-31）｜affects：thesis.R、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K 稱出口限制已降低且未來可能降低對中國銷售，部分對中國銷售需美國出口許可，過去曾有許可被延遲或拒發，現有許可可能因政策變動被撤銷；Entity List 新增曾壓抑需求。
  - 來源：Marvell Form 10-K FY2026 (fiscal year ended 2026-01-31), SEC（as_of 2026-01-31）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：Marvell 財報稱 Section 232 半導體調查（BIS 2025 年 4 月啟動）可能導致額外關稅與貿易限制；FY2026 年報仍列為開放風險，未量化影響。
  - 來源：Marvell Form ARS FY2026 / 10-Q filings, SEC（as_of 2026-01-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Marvell FY2026 10-K（會計年度止 2026-01-31）：多數合格晶圓代工廠位於台灣同一區域；台灣政治、軍事或天災中斷會損及業務（搜尋摘要轉述10-K，未讀全文頁面）。
  - 來源：Marvell Technology, Inc. Form 10-K FY2026 (SEC EDGAR)（as_of 2026-01-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：封裝與測試分包商集中於泛太平洋地區（中國、馬來西亞、新加坡、台灣、加拿大）；FY2026 10-K 並列地緣緊張與衝突為中斷風險（搜尋摘要轉述）。
  - 來源：Marvell Technology, Inc. Form 10-K FY2026 (SEC EDGAR)（as_of 2026-01-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：歷史 10-K（FY2013）揭露多數產品同一時間不在超過一家晶圓廠生產，轉換晶圓廠困難；FY2020 10-K 稱替代晶圓廠有限、導入需時。為舊年度文件，現行單源程度未於本軸確認。
  - 來源：Marvell Technology Group 10-K FY2013 / FY2020 (SEC EDGAR)（as_of 2013-03-01）｜affects：decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：2026年產業分析：自研晶片（Google TPU、Amazon Trainium）仍與其他客戶競爭同一批先進製程與先進封裝產能（TSMC）；CoWoS 與 HBM 為產業瓶頸，非 TSMC 的 CoWoS 產能很小。屬產業層次二手分析，非針對 MRVL。
  - 來源：enkiai.com / softwareseni.com 等產業分析（搜尋摘要）（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Counterpoint 預估 Marvell 在客製 AI ASIC 的份額 2027 年降至約 8%（出貨量 2024–2027 約倍增）；JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 約 10–12%；Motley Fool 引 Broadcom 約 70%
  - 來源：Counterpoint Research / JPMorgan via KuCoin / Motley Fool（as_of 2026-06-30）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：HSBC 以 Hold、目標價 $85 啟動 MRVL 評等，認為其 ASIC 業務至 2027 年可能落後同業，並稱 Broadcom ASIC 路線圖能見度較高。
  - 來源：Yahoo Finance: Marvell started at Hold as weak ASIC outlook offsets strength in AI optical（as_of 2026-06-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Digitimes 2026 年 1 月標題：MediaTek、Alchip、Marvell 爭奪 ASIC 第二名；另有分析稱台系 IP 廠 Alchip、GUC 對 Marvell XPU 專案造成毛利壓力。
  - 來源：Digitimes: MediaTek, Alchip, Marvell clash for ASIC runner-up spot（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Marvell FY2026 10-K 將 LPO 晶片組（TIA、雷射驅動）與 CPO 列為產品線，並列有 AEC DSP；LPO 為無 DSP 模組，是對模組 DSP 需求的潛在替代路徑，採用面仍有訊號完整性與互通性挑戰（OFC workshop）。
  - 來源：Marvell 10-K FY2026; OFC workshop: Will LPO have a future（as_of 2026-01-31）｜affects：moat_trend、thesis.R
- `substitute_technology#4`（substitute_technology｜方向 -｜狀態 ok）：Semtech OFC 2026 摘要：scale-up 目前以銅為最實用，光學與銅並行進入而非取代；Broadcom Taurus BCM83640（3nm、400G/lane 光 DSP）為 1.6T/3.2T 模組關鍵件，競爭 Marvell DSP。
  - 來源：Semtech blog OFC 2026; Digitimes 2026-04-21（as_of 2026-04-21）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：財報後盤後股價約下跌 2%，市場關注 Q2 小幅優於預期與 Q3 毛利率指引走低，儘管多年展望上調。
  - 來源：StockTwits: MRVL Stock Slips After-Hours Despite Raised Multi-Year Outlook（as_of 2026-08-27）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":816.0,"bear_5y_price":115.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":67.8,"ev5y_pct":62.2,"irr_base_pct":10.9,"asym_ratio":2.8,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":4.22,"pe":65.23,"basis":"FY2027E（2027 年 1 月止）非 GAAP 共識 EPS 4.22 美元、判斷日股價 275.28 美元；終端倍數同為當年度前瞻一年非 GAAP EPS 口徑"},"eps":{"bull":[7.9,13.5,20.0,28.0,34.0],"base":[7.4,12.0,15.0,18.0,21.0],"bear":[6.4,7.6,5.6,5.9,6.8]},"pe":{"bull":24,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.087,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MRVL_Q1_2027_Earnings_Call_20260527.md
- 2026-05-27｜CEO｜guidance：CEO 說明 Q3、Q4 營收各季對季成長至少 10%。（原話："to also grow by at least 10% sequentially."）
- 2026-05-27｜CEO｜guidance：CEO 回顧上一季說法：自 Q2 起各季對季成長為高個位數。（原話："trend in the high single-digit range sequentially"）
- 2026-05-27｜CEO｜guidance：CEO 表示本次再度上調展望（FY27 營收預測增加逾 5 億美元，FY28 增加約 15 億美元）。（原話："we are again raising our outlook"）
- 2026-05-27｜CEO｜guidance：CEO 給 FY27 全公司營收約年增 40%、近 115 億美元。（原話："year to nearly $11.5 billion."）
- 2026-05-27｜CEO｜guidance：CEO 給 FY28 營收約 165 億美元，並稱較上季展望高約 15 億美元。（原話："fiscal 2028 revenue to reach approximately $16.5 billion"）
- 2026-05-27｜CEO｜guidance：CEO 預期 FY28 資料中心營收約年增 55%，快於 FY27 預期成長率。（原話："revenue in fiscal 2028 to grow approximately 55%"）
- 2026-05-27｜CEO｜guidance：CEO 說明 FY28 規劃假設雲端 CapEx 成長率放緩至 30% 以上區間。（原話："planning for the rate of cloud CapEx growth to moderate"）
- 2026-05-27｜CEO｜guidance：CEO 給 Q2 資料中心營收對季成長預期（中高十位數百分比）。（原話："data center revenue growth to accelerate into the mid-"）
- 2026-05-27｜CEO｜guidance：CEO 給 Q2 通訊及其他市場營收對季下滑中個位數。（原話："expect revenue to decline in the mid-single-digit range"）
- 2026-05-27｜CFO｜guidance：CFO 給 Q2 營收區間：27 億美元正負 5%。（原話："$2.7 billion, plus or minus 5%"）
- 2026-05-27｜CFO｜guidance：CFO 給 Q2 non-GAAP EPS 區間 0.88–0.98 美元。（原話："in the range of $0.88 to $0.98"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 165 億美元之下，互連業務仍有向上偏誤。（原話："there's upward bias for sure"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 互連業務年增逾 70%。（原話："our interconnect business to grow more than 70%"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 客製化業務預期年增超過一倍，高於先前展望。（原話："our custom business to more than double year-over-year"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 客製化業務維持年增逾 20%。（原話："Custom revenue remains on track to grow more than 20%"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 1.6T 營收將再顯著墊高。（原話："We expect 1.6T revenue to take another substantial step up"）
- 2026-05-27｜CEO｜guidance：CEO 稱 TIA 與驅動器季營收數季內將超過年化 10 億美元。（原話："exceed a $1 billion annualized run rate"）
- 2026-05-27｜CEO｜guidance：CEO 稱 DCI 模組業務對 FY28 年化營收 10 億美元有可見度。（原話："line of sight to a $1 billion annualized revenue"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY27 scale-out 交換器營收將超過 6 億美元。（原話："scale-out switch revenue in fiscal 2027 to exceed $600"）
- 2026-05-27｜CEO｜guidance：CEO 稱交換器業務在 FY28 年化營收追蹤超過 10 億美元。（原話："see the business tracking to more than $1 billion"）
- 2026-05-27｜CEO｜guidance：CEO 稱 AEC 與 retimer 合併營收 FY27 將成長逾一倍。（原話："combined revenue to more than double year-over-year"）
- 2026-05-27｜CEO｜guidance：CEO 稱 scale-up 光學業務 FY28 營收將大幅躍升，較先前僅含 Celestial AI 的約 1.5 億美元展望增逾一倍。（原話："we expect our scale-up optics business to ramp significantly"）
- 2026-05-27｜CEO｜guidance：Q&A 中 CEO 稱 scale-up 光學目前估計約 3 億美元。（原話："effectively calling at this point to be about $300 million"）
- 2026-05-27｜CEO｜guidance：CEO 稱 scale-up 網路與交換器幾乎未計入 165 億美元（逐字稿原文如此）。（原話："that's not very little or nothing in the $16.5 billion"）
- 2026-05-27｜CEO｜guidance：CEO 稱 FY28 客製化成長三大來源比例與上季相近。（原話："it's roughly the same ratio"）
- 2026-05-27｜CFO｜margin：CFO 報 Q1 non-GAAP 毛利率。（原話："non-GAAP gross margin was 58.9%"）
- 2026-05-27｜CFO｜margin：CFO 給 Q2 non-GAAP 毛利率區間。（原話："non-GAAP gross margin to be between 58.25% and 59.25%"）
- 2026-05-27｜CFO｜margin：CFO 說明毛利率取決於營收水準與產品組合。（原話："revenue and product mix will remain key determinants"）
- 2026-05-27｜CFO｜margin：CFO 解釋 Q1 GAAP EPS 低於財測，來自 Celestial AI 與 XConn 購併會計及 earn-out。（原話："$0.04 lower than our guidance"）
- 2026-05-27｜CFO｜margin：CFO 稱 FY28 non-GAAP 營業費用成長遠低於營收成長。（原話："we expect non-GAAP operating expense to grow year-over-year"）
- 2026-05-27｜CFO｜margin：CFO 給 FY27 non-GAAP 營業費用約 24.5 億美元，含兩項購併（逐字稿誤植為 earnings expense）。（原話："expense of approximately $2.45 billion"）
- 2026-05-27｜CFO｜commitment：CFO 承諾 FY28 營業利益率達目標模型上緣。（原話："operating margin model of 38% to 40%"）
- 2026-05-27｜CEO｜commitment：CEO 重申對客製化業務 FY29 逾 100 億美元的目標有信心。（原話："deliver on over $10 billion in revenue in fiscal 2029"）
- 2026-05-27｜CEO｜commitment：CEO 稱新 Tier 1 XPU 專案已有涵蓋下一整個財年的明確需求。（原話："we already have firm requirements in place for all of next"）
- 2026-05-27｜CEO｜commitment：CEO 稱新斬獲設計的典型開發週期約兩年才貢獻增量營收。（原話："typical development cycle of approximately 2 years"）
- 2026-05-27｜CFO｜capital_allocation：CFO 預計本財年約 10 億美元供應商預付款，自 Q2 起。（原話："approximately $1 billion in prepayments"）
- 2026-05-27｜CFO｜capital_allocation：CFO 報 Q1 買回 2 億美元股票。（原話："we repurchased $200 million of our stock"）
- 2026-05-27｜CFO｜capital_allocation：CFO 說明後續持續買回股票以管理稀釋。（原話："we plan to continue to repurchase shares to manage"）
- 2026-05-27｜CEO｜capital_allocation：CEO 宣布收購 Polariton（電漿子矽光子元件）。（原話："the acquisition of Polariton, a developer of high-speed"）
- 2026-05-27｜COO｜risk：COO 說明 AI 相關供應自 2020–2021 起持續受限。（原話："I don't think we've been in an unconstrained environment"）
- 2026-05-27｜COO｜risk：COO 說明確保產能的做法：向少數關鍵供應商提供五年預測。（原話："giving them a 5-year forecast of what we need"）
- 2026-05-27｜CEO｜customer：CEO 稱 DCI 方案已出貨給全部五大美國超大規模業者。（原話："we shipped DCI solutions to all 5"）
- 2026-05-27｜CEO｜customer：CEO 稱 Celestial AI 方案已被一家 Tier 1 超大規模業者選用於下一代 XPU scale-up。（原話："The solution has already been selected by a Tier 1"）
- 2026-05-27｜CEO｜customer：CEO 稱 AEC 已取得三家 Tier 1 美國超大規模業者設計案。（原話："design wins with 3 Tier 1 U.S. hyperscalers"）
- 2026-05-27｜CEO｜customer：CEO 稱新 Tier 1 XPU 專案約占明年客製化總成長的三分之一。（原話："probably still about 1/3 of the total growth"）
- 2026-05-27｜CEO｜customer：CEO 稱近期新設計案不是既有預測所需，視為保險。（原話："Think of that as like an insurance policy."）
- 2026-05-27｜CEO｜customer：CEO 稱客製化預測不需要任何增量。（原話："it's not requiring anything incremental"）
- 2026-05-27｜CEO｜product：CEO 說明與 NVIDIA 的 NVLink Fusion 整合內容。（原話："This allows Marvell to build custom chips and networking"）
- 2026-05-27｜CFO｜product：（逐字稿標示為 Willem Meintjes 回答）稱 XPU（原文為 XPO）attach 單一項目數年內營收將逾 10 億美元。（原話："attach alone over $1 billion in revenue"）
- 2026-05-27｜CFO｜competition：（同上段發言者）稱記憶體週期的疑慮正推動 CXL 設計採用。（原話："driving additional adoption of CXL-based design"）

### MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CEO｜guidance：CEO 說明營收口徑已從一年前的兩年 $20B 拉到本財年 $12B、下財年 $18B（原話："we can do $12 billion this year and $18 billion next year"）
- 2026-09-09｜CEO｜guidance：CEO 稱資料中心營收從 2023 曆年約 $2.2B 到明年約 $15–16B（原話："next year, we're looking at $15 billion, $16 billion"）
- 2026-09-09｜CEO｜guidance：CEO 稱連接業務今年成長 70% 以上，明年維持高成長但未給具體數字（原話："that business this year is growing like 70% plus"）
- 2026-09-09｜CEO｜guidance：CEO 提到供應鏈一年內彈性上調約 50%（原話："our supply chain has been able to flex up 50%"）
- 2026-09-09｜CEO｜guidance：CEO 回溯上一季對 NPO/CPO 明年營收的說法為 0 至 $300M（原話："we said it was going to be 0 to $300 million"）
- 2026-09-09｜CEO｜guidance：CEO 稱上一季已說該數字會高得多（原話："This past quarter, I said that was going to be much higher"）
- 2026-09-09｜CFO｜guidance：CFO 給營業利益率路徑：本年底進入長期目標區間（原話："exit this year entering the long-term target model"）
- 2026-09-09｜CFO｜guidance：CFO 稱明年底觸及該區間上緣（原話："We will exit next year touching the top end of that range."）
- 2026-09-09｜CFO｜margin：CFO 稱 Q3、Q4 營業利益率連續季增（原話："increase in operating margin in Q3 and again in Q4"）
- 2026-09-09｜CFO｜margin：CFO 稱客製化占比上升時毛利率會逐步下降（原話："you will see incremental step down"）
- 2026-09-09｜CEO｜margin：CEO 說明客製化 NRE 以 contra R&D 入帳（原話："an offset or contra R&D"）
- 2026-09-09｜CEO｜margin：CEO 稱明年毛利率可在客製化翻倍下大致持平並伴隨營業利益率擴張（原話："gross margin flattish with OM expansion"）
- 2026-09-09｜CEO｜margin：CEO 拆解 $13.5B 到 $18B 的上調來源，多數來自互連、交換器與儲存（原話："most of that raise has come from interconnect and switching"）
- 2026-09-09｜CFO｜margin：CFO 稱營運費用成長約為營收成長的一半（原話："your OpEx will grow roughly half the rate of revenue"）
- 2026-09-09｜CFO｜commitment：CFO 承諾分析師日重設長期營業利益率目標（原話："we'll reset what we think the new long-term target is"）
- 2026-09-09｜CEO｜commitment：CEO 稱客製化 FY29 目標軌道正常，並預告分析師日將給區間（原話："we probably need to give a range for the future"）
- 2026-09-09｜CEO｜commitment：CEO 預告 10/6 投資人日（原話："We got an Investor Day coming up on October 6."）
- 2026-09-09｜CEO｜commitment：CEO 稱到目前為止拿到足夠供給以兌現承諾（原話："we're getting what we need, I think, to deliver"）
- 2026-09-09｜CEO｜product：CEO 稱 Teralynx 交換器業務預計達 $1B 以上（原話："on track to do $1 billion plus"）
- 2026-09-09｜CEO｜product：CEO 稱 scale-up 目前尚屬綠地市場（原話："sort of greenfield at the moment"）
- 2026-09-09｜CEO｜product：CEO 稱 NPO 與 CPO 並存而非二選一（原話："this is not an or. This is going to be an and"）
- 2026-09-09｜CEO｜product：CEO 稱 1.6T 的 2nm DSP 率先宣布（原話："We were first to market on announcing our 2-nanometer DSPs"）
- 2026-09-09｜CEO｜product：CEO 稱 scale across 可能使 DCI 市場放大數倍（原話："that could 2, 3, 4, 5x the size of the DCI market"）
- 2026-09-09｜CEO｜product：CEO 稱現有業務仍以每年 50% 以上成長（原話："the existing businesses growing at 50% a year plus"）
- 2026-09-09｜CEO｜product：CEO 稱交換器加光學為下一個大型成長引擎（原話："switching plus optics is going to be very big"）
- 2026-09-09｜CEO｜competition：CEO 稱 1.6T 地位與以往同樣強（原話："we're as well positioned as we've ever been at 1.6T"）
- 2026-09-09｜CEO｜competition：CEO 預期多家公司將推出 XPU attach 策略（原話："a whole bunch of companies are going to come out"）
- 2026-09-09｜CEO｜competition：CEO 稱競爭對手多只有一塊拼圖（原話："A lot of our competitors don't have that."）
- 2026-09-09｜CEO｜customer：CEO 稱涵蓋四大美系雲端業者的設計案已逾 20 件（原話："20-plus design wins across all the 4 U.S. hyperscalers"）
- 2026-09-09｜CEO｜customer：CEO 說明 Google 的 8-K 認股權屬 XPU attach 關係（原話："that is really an XPU attach relationship"）
- 2026-09-09｜CEO｜customer：CEO 稱客製化業務將多元而非單一插槽（原話："there's no one trick pony in there"）
- 2026-09-09｜CEO｜customer：CEO 稱與 NVIDIA 的關係是反向於緊張（原話："I would say it's the opposite of tension."）
- 2026-09-09｜CEO｜risk：CEO 稱供給自疫情以來持續吃緊（原話："It's been constrained since the pandemic."）
- 2026-09-09｜CEO｜risk：CEO 稱部分領域目前特別吃緊（原話："It's very acute right now in some areas."）
- 2026-09-09｜CEO｜risk：CEO 提到社會對資料中心的反彈（原話："societal pushback"）
- 2026-09-09｜CEO｜risk：CEO 稱若供給無限則產業總會過度擴張（原話："the industry always overdoes it"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱資本配置第一支柱為讓公司成長（原話："pillar 1 of capital allocation is grow the company"）
- 2026-09-09｜CFO｜capital_allocation：CFO 稱保留彈性以供應鏈下單（原話："preserve the flexibility to put order in the supply chain"）
- 2026-09-09｜CEO｜capital_allocation：CEO 稱已提高 CapEx 與預付款規模（原話："We've upped the CapEx and the prepays"）

### MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md
- 2026-10-06｜CEO Matt Murphy｜guidance：FY28 總營收展望由八月的約 180 億美元再上調至約 200 億美元。（原話："approximately $20 billion in total company revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY28 資料中心營收預期成長約 80%。（原話："we expect data center revenue to grow approximately 80%"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY29 客製化（custom）營收目標由逾 100 億上調為 FY28 的三倍以上、逾 120 億美元。（原話："custom revenue in FY '29 to more than triple from FY '28"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 長期營收目標區間為 700 億至 900 億美元，中點 800 億。（原話："a range of $70 billion to $90 billion in revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 資料中心營收對應 55%–70% 成長區間，約 675 億至 875 億美元。（原話："approximately $67.5 billion to $87.5 billion"）
- 2026-10-06｜CEO Matt Murphy｜guidance：CEO 稱自下而上的路徑是資料中心營收 FY28 後年增約 70% 至 FY31，CapEx 假設趨緩。（原話："growing our data center revenue at roughly 70% annually"）
- 2026-10-06｜SVP Xi Wang｜guidance：FY31 互連（interconnect）中點目標約 375 億美元。（原話："approximately $37.5 billion in FY '31 at the midpoint"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 交換器與儲存中點約 100 億美元。（原話："approximately $10 billion in switching and storage revenue"）
- 2026-10-06｜CEO Matt Murphy｜guidance：FY31 客製化中點約 300 億美元。（原話："approximately $30 billion at the midpoint in FY '31"）
- 2026-10-06｜CEO Matt Murphy｜guidance：通訊及其他業務假設僅維持位置、成長極小。（原話："maintain our position with very modest growth"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 稱 FY31 資料中心 CAGR 中點為 65%，與 CEO 口述的約 70%／55–70% 區間口徑並陳。（原話："a 65% CAGR at the midpoint of our long-term model"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給三條產品線中點 CAGR：客製化約 80%。（原話："We see a revenue CAGR of approximately 80% at the midpoint"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給互連中點 CAGR 約 65%。（原話："we forecast a revenue CAGR of about 65% at the midpoint"）
- 2026-10-06｜CFO Dan Durn｜guidance：CFO 給長期模型 FY31 non-GAAP EPS 中點大於 30 美元（「$30 in '30」）。（原話："non-GAAP EPS of greater than $30 a share in FY '31"）
- 2026-10-06｜SVP Russ Esmacher｜guidance：Russ 稱其相干（coherent）業務由 FY26 約 5 億美元成長至 FY28 逾 10 億美元。（原話："$500 million in fiscal '26 to safely over $1 billion"）
- 2026-10-06｜EVP David Lazovsky｜guidance：Teralynx 交換器業務（51T 放量）明年預期超過 10 億美元。（原話："exceed north of $1 billion and significantly so"）
- 2026-10-06｜CFO Dan Durn｜margin：FY31 毛利率目標 56%–59%，依產品組合而定。（原話："We expect a gross margin of 56% to 59%"）
- 2026-10-06｜CFO Dan Durn｜margin：CFO 說明客製化毛利率相對較低，但因客戶出資 NRE 與規模，營業利益率仍具吸引力。（原話："Custom silicon carrying a relatively lower gross margin"）
- 2026-10-06｜CFO Dan Durn｜margin：CFO 說毛利率區間低端需要客製化營收大幅優於基本預測，連接業務超預期則趨向高端。（原話："it likely requires a significant upside to the base case"）
- 2026-10-06｜CFO Dan Durn｜margin：FY31 營業利益率目標 44%–46%。（原話："We expect an operating margin of 44% to 46%"）
- 2026-10-06｜CFO Dan Durn｜margin：營業費用成長速度約為營收成長的一半，是營業槓桿假設的來源。（原話："grow operating expenses at roughly half the rate of revenue"）
- 2026-10-06｜CFO Dan Durn｜margin：稅率 15%、自由現金流利潤率長期大於 36%。（原話："a free cash flow margin of greater than 36% over time"）
- 2026-10-06｜CEO Matt Murphy｜margin：CEO 重申去年說法：XPU attach 毛利率高於 XPU，原因含 IP 差異化與量。（原話："you should expect that the XPU attach side is more margin"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 表示達成目標不需要新的大型設計案或新 socket。（原話："We don't need any new home run design wins"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 對交付預測作出明確承諾。（原話："my team and I are going to deliver that forecast"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 稱明年 200 億美元所需的供給已備妥。（原話："the supply I need to hit the $20 billion next year"）
- 2026-10-06｜President/COO Chris Koopmans｜commitment：COO 稱靠前四大美國超大規模客戶即可達成 Murphy 所述目標的絕大部分。（原話："we can hit the vast majority of the goals that Matt laid out"）
- 2026-10-06｜EVP Will Chu｜commitment：客製化負責人表示不需新增勝案即可達成客製化目標。（原話："we don't need new wins to achieve our target."）
- 2026-10-06｜CFO Dan Durn｜commitment：CFO 稱長期目標不依賴單一大型 socket。（原話："no mega socket is needed to deliver on our long-term targets"）
- 2026-10-06｜CEO Matt Murphy｜commitment：Murphy 表示在互連的 scale-out 與 scale-across 不打算流失市占。（原話："We don't intend to lose any market share there"）
- 2026-10-06｜CFO Dan Durn｜commitment：CFO 承諾平均長期返還超過 50% 自由現金流。（原話："returning greater than 50% of our free cash flow on average"）
- 2026-10-06｜CFO Dan Durn｜capital_allocation：CFO 回顧 FY21–FY26：有機研發約 80 億美元，併購約 110 億美元。（原話："$11 billion of inorganic investments"）
- 2026-10-06｜CFO Dan Durn｜capital_allocation：同期以股利與買回返還股東約 40 億美元。（原話："returning about $4 billion to shareholders via dividends"）
- 2026-10-06｜President/COO Chris Koopmans｜capital_allocation：COO 稱公司已投入資本預付產能以鎖定供應鏈，並給供應商五年預測。（原話："we are investing ahead of our growth to reserve the capacity"）
- 2026-10-06｜President/COO Chris Koopmans｜capital_allocation：COO 說明 FY24 研發投入占資料中心營收超過一半。（原話："investing well north of 50% of our revenue back into R&D"）
- 2026-10-06｜CEO Matt Murphy｜customer：客製化矽已出貨給全部四家美國超大規模雲端業者。（原話："we're shipping custom silicon to all 4 U.S. hyperscalers"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：COO 揭露與 Google 的協議：6.5 年 1,200 億美元的 TPU 生態系客製化機會。（原話："$120 billion opportunity over 6.5 years for custom products"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：COO 列出與 NVIDIA 的策略協議（光學、NVLink Fusion 等）。（原話："we announced a strategic agreement with NVIDIA"）
- 2026-10-06｜President/COO Chris Koopmans｜customer：前四大美國超大規模客戶占去年資料中心 CapEx 過半。（原話："the top 4 U.S. hyperscalers alone were more than half"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱預測成長高度集中於四大客戶，但產品面分散。（原話："highly leveraged to the Big 4, but very diversified"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱客製化專案皆為 Marvell 獨家（sole source）。（原話："are all proprietary sole source"）
- 2026-10-06｜CEO Matt Murphy｜customer：Murphy 稱 AI 實驗室屬於模型之外的潛在上行選項，未納入目標。（原話："I think it's a real call option"）
- 2026-10-06｜SVP Xi Wang｜competition：Xi Wang 稱沒有其他公司涵蓋整條連接堆疊。（原話："No other companies cover this entire stack."）
- 2026-10-06｜SVP Xi Wang｜competition：Xi Wang 稱 1.6T DSP 領先競爭對手約兩年。（原話："leading our competitors by 2 years and continuing"）
- 2026-10-06｜EVP David Lazovsky｜competition：Lazovsky 稱 T100 交換器延遲與功耗優於任一領先競爭對手。（原話："on the order of 20% or more lower latency"）
- 2026-10-06｜President/COO Chris Koopmans｜competition：COO 劃清定位：不是單純 ASIC 供應商。（原話："We're not an ASIC vendor."）
- 2026-10-06｜CEO Matt Murphy｜competition：Murphy 以客製化 TAM 的演變說明市場超出當年辯論的預期（2024 年為 400 億美元 XPU 客製化 TAM）。（原話："we called out a $40 billion XPU custom TAM"）
- 2026-10-06｜CEO Matt Murphy｜competition：Murphy 以 300 億美元對 2,350 億美元客製化 TAM 推算約 13% 占比，稱並非不合理。（原話："You get 13% share, okay?"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 總量：2030 曆年約 4,000 億美元可定址市場。（原話："approximately $400 billion total addressable market"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 與前次相比放大約四倍。（原話："So this is a 4x increase to our TAM opportunity"）
- 2026-10-06｜CEO Matt Murphy｜product：TAM 的 CapEx 前提：2030 年資料中心 CapEx 約 3 兆美元。（原話："total data center CapEx to reach roughly $3 trillion"）
- 2026-10-06｜CEO Matt Murphy｜product：XPU attach 的可定址市場一年前約 150 億美元，現在已放大數倍。（原話："We said it was about $15 billion a year ago."）
- 2026-10-06｜CEO Matt Murphy｜product：FY28 資料中心 180 億美元目標比原訂 FY29 提早近一年達成。（原話："the $18 billion data center target we set for FY '29"）
- 2026-10-06｜CEO Matt Murphy｜product：scale-up 光學目前幾乎沒有營收，明年開始放量。（原話："multi-hundred million starting next year"）
- 2026-10-06｜CEO Matt Murphy｜product：scale-out 業務近年大致每年翻倍，模型假設成長率會趨緩。（原話："that business has been roughly doubling each year"）
- 2026-10-06｜EVP David Lazovsky｜product：Teralynx T100 為單晶 102.4T 交換器，主打 scale-out 與 scale-up 雙用。（原話："the first and only monolithic full reticle-limited die"）
- 2026-10-06｜EVP David Lazovsky｜product：預期 100T 交換器本身可新增數十億美元年營收。（原話："multiple billions of dollars of annual revenue"）
- 2026-10-06｜EVP David Lazovsky｜product：UALink U115 交換器預計明年推出，已有一家超大規模客戶部署。（原話："we'll be releasing next year, a UALink U115 switch"）
- 2026-10-06｜EVP David Lazovsky｜product：每顆 XPU 的 scale-up 光學內容約為數千美元。（原話："thousands of dollars of scale-up optics per XPU"）
- 2026-10-06｜EVP David Lazovsky｜product：Photonic Fabric 記憶體模組已完成 tape-out，明年向多家客戶送樣。（原話："we'll be sampling with multiple customers"）
- 2026-10-06｜SVP Xi Wang｜product：3.2T 路線轉向 coherent-lite：管理層稱 PAM4 在 400G/lane 有物理極限。（原話："3-nanometer alone wasn't the optimal answer"）
- 2026-10-06｜SVP Xi Wang｜product：類比（TIA／driver）業務年營收正朝 10 億美元以上邁進。（原話："rapidly headed towards $1 billion plus annually"）
- 2026-10-06｜SVP Xi Wang｜product：scale-in（光學進封裝）被稱為可能再成就數十億美元事業。（原話："yet another multibillion-dollar business for Marvell"）
- 2026-10-06｜CEO Matt Murphy｜product：Murphy 稱 scale-in 在 FY31 數字中並不重大，視為選擇權。（原話："not really material at that point in FY '31"）
- 2026-10-06｜CEO Matt Murphy｜product：Murphy 稱 scale-in 可能在目標期內起步，但屬未來投資人日的主題。（原話："which could start in the period"）
- 2026-10-06｜SVP Russ Esmacher｜product：相干可插拔模組的資料中心間需求預估到 FY31 超過 300 萬顆。（原話："grows to over 3 million units"）
- 2026-10-06｜EVP Will Chu｜product：XPU attach 新增兩個先前未談過的類別之一：AI 基礎設施管理矽。（原話："Today, we're introducing an entirely new XPU attach category"）
- 2026-10-06｜EVP Will Chu｜product：Chu 給 XPU attach 單價與機會量級：每類可達 10 億美元，部分達數十億。（原話："with some reaching several billions"）
- 2026-10-06｜EVP Will Chu｜product：Chu 以每 XPU 一至兩個 attach socket、ASP 約 1,000 美元作示範算式。（原話："sockets attaching to each XPU with ASPs around $1,000"）
- 2026-10-06｜EVP Will Chu｜product：Chu 稱 XPU attach 的 socket 黏性高、可跨多代 XPU。（原話："these sockets are very sticky"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 承認外部衝擊下公司同樣暴露。（原話："We're all exposed if the world turns upside down"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 稱此預測實質上是三年而非五年的押注。（原話："it is a 3-year kind of a pick, not a 5-year"）
- 2026-10-06｜CEO Matt Murphy｜risk：CapEx 假設：模型假設 CapEx 成長由目前的高速放緩，尾端約 20%。（原話："it's probably growing more like 20%"）
- 2026-10-06｜CEO Matt Murphy｜risk：對分析師詢問的供電與廠房（powered shell）限制，Murphy 稱客戶討論中未見此限制。（原話："we don't see that as any kind of constraint"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 稱 Google 大型策略協議在 FY31 中只計入部分 warrant 價值。（原話："that comprehends not the full value of the warrant"）
- 2026-10-06｜CEO Matt Murphy｜risk：Murphy 說明其預測哲學：取最可能結果，不偏保守也不偏積極。（原話："I'm not conservative, and I'm not aggressive. I'm pragmatic."）

### 問答異常語氣（迴避／改口／保留）
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Arya：新 Tier 1 XPU 客戶何時揭露、是否獨家。｜答法：CEO 確認 10 億美元目標，但未回答客戶名稱與是否獨家，僅稱進度符合預期、隨年度推進信心增加。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Arcuri：是否進入運算 TAM、是否含於預測。｜答法：CEO 未直接回答是否進入運算 TAM，改述既有設計案，稱預測不需任何增量。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Wells Fargo：新增客製化插槽的 XPU 類型細節。｜答法：CEO 明確表示目前不提供額外細節，稱適當時機再做回顧。
- MRVL_Q1_2027_Earnings_Call_20260527.md｜問：Seymore：互連成長率 30%→50%→70% 逐步上調，為何 FY28 回落至略高於 CapEx，是否保守。｜答法：CEO 以「這是我們目前所在位置」帶過，未解釋減速原因，只稱有向上偏誤與選擇權。
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：Google 認股權協議的營收何時開始貢獻｜答法：CEO 先談歷史與 XPU attach 範疇，未給時點或金額，改指分析師日再說明
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：對同業與金融夥伴合資建資料中心的風險看法｜答法：CFO 表示不評論其他公司，回到技術領先與客戶成功；CEO 補充 Marvell 不參與
- MRVL_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：客戶對土地、電力、廠房（LPS）的疑慮｜答法：CEO 稱沒有太多新資訊，轉談限制反而健康
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Vivek Arya 問客製化多重來源程度，以及 300 億美元目標與八月大型策略協議（warrant）規模的關係。｜答法：Murphy 回答 sole source 並說 FY31 模型只計入「部分」warrant 價值，未給出被納入的具體金額或比例。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Tom O'Malley 要求拆解 2030 年互連 TAM（DSP 占比、量、NPO／CPO）。｜答法：Murphy 只給定性分桶（scale-out、scale-across、scale-up、scale-in），並說「we're not going to give a lot more precision than that」，未給數字拆解。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Mark Lipacis 問客戶超額下單（double ordering）風險與本輪與過往超級週期的差異。｜答法：Murphy 未直接回應超額下單機制，改以「看得到明年 200 億」「實質是三年的押注」框架回答；CFO Durn 被點名後表示無補充。
- MRVL_Analyst_Investor_Day_Marvell_Technology_Inc_20261006.md｜問：Chris Rolland 問 scale-in 市場規模、客戶接觸現況與時程（傳聞最早曆年 2029）。｜答法：Murphy 表示有多家客戶接洽、正在投入研發，但稱「today is not the day」，未給規模或時程。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 8 | 4 |
| customer_second_source | found | 5 | 2 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 5 | 4 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 4 | 6 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：Marvell distribution channel OR go-to-market change 2026；Marvell business model transition custom silicon platform XPU attach 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260831","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"客製運算業務藉多客戶分散化抵銷單一旗艦社羣的執行風險——Google／Microsoft／新一線雲端商上線速度快於 AWS 旗艦社羣份額流失速度"},{"id":"H2","text":"互連端首發技術優勢持續轉化為超越資本支出的成長（1.6T PAM4、規模化光學 NPO/CPO、DCI）"},{"id":"H3","text":"AI 資料中心資本支出多年結構性不反轉，且 Marvell 毛利率結構在客製組合上升後仍能靠營運槓桿撐住 EPS"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"AWS／Microsoft 旗艦 custom 社羣世代交接持續失利，且 Google/新客戶放量不如預期補位"},{"id":"R2","text":"非 GAAP 毛利率結構性跌破 57.5-58.5% 目標區間——除客製組合佔比上升外，記憶體（DRAM/HBM）成本通膨是本次新增查證的成本側變數：DRAM 價格 2025→2027 累計漲幅估計 ~275-300%，TrendForce（2026-06-02）預期 HBM 合約價 2027 年倍數級上漲且短缺延續至 2027 年後，Goldman 估 custom ASIC 用 HBM 需求 +82%；Google 協議本身涵蓋 memory interface controllers/near-memory compute，成本與客戶系統預算兩條路徑都通向毛利率"},{"id":"R3","text":"CPO（共同封裝光學）在規模化網路加速取代可插拔 DSP 模組，侵蝕互連端長期經濟性（Broadcom Tomahawk 6 已具第三代 CPO、NVIDIA 承諾於未來 Spectrum-X 導入）"},{"id":"R4","text":"AI 資本支出消化／融資結構風險（前份報告原有、本次恢復）：主流預估 hyperscaler capex 增速由 2026 年 +51% 降至 2027 年 +13%、2028 年約 +5%；增量負債占 capex 比重由 FY24 的 9% 升至 2026 年中 LTM 32%，五大雲端商自 2024 年底起舉債逾 $137.5B；另有折舊年限（會計 5-6 年 vs 估計經濟壽命 2-3 年）爭議，估計 2026-28 少認列約 $1,760 億，FASB 新揭露要求要到 FY2027 才上路——資訊最不透明期與折舊壓力最集中期重疊"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"三旗艦socket任一正面確認＋GM守57.5-58.5%","irr_base_pct":10.9,"ev5y_pct":64.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.3,"ev5y_pct":64.6,"irr_base_pct":10.9,"max_dd_pct":-48.0,"bull_5y_price":570.3,"bear_5y_price":134.1,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"三旗艦socket任一正面確認＋GM守57.5-58.5%","price_at_dd":216.62,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MRVL","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Marvell Technology, Inc."},"oneliner":"互連與客製晶片雙引擎，投資人日把 FY28 營收拉到約 200 億美元；但股價六週漲 27%、基準五年年化約 11%，唯一致命點是雲端客戶資本支出轉為年減。不追，等股價回到 FY28 共識 EPS 32 倍以下","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRVL_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺四大美國雲端業者 AI 建置的錢：資料中心占營收 79%，獲利卡在互連（光 DSP 與 TIA／驅動）與客製加速器及 attach 晶片兩個節點，上游產能與下游大客戶兩端的議價力都比 Marvell 強","reasoning":"Q2 FY27 營收 27.39 億美元，資料中心 21.72 億美元（占 79%、年增 46%），通訊及其他 5.68 億美元（年增 10%，法說會）。非 GAAP 毛利率 58.9%、營益率 36.6%；GAAP 為 53.1%、16.8%，差距主要是 SBC 與併購攤銷。Q3 指引營收 31.5 億美元±5%、非 GAAP 毛利率 57.5–58.5%，下滑來自客製放量的組合效應。錢卡在兩個節點：互連（光 DSP、TIA／驅動、DCI，800G 換 1.6T）與客製加速器及 attach 晶片（設計案綁定、單一來源）。議價權：上游台積電先進製程、CoWoS 與 HBM 稀缺，Marvell 以五年預測加約 10 億美元預付鎖產能；下游前十大客戶占 FY26 營收 82%、一家經銷商約 37%（第三方彙整），AWS 為差距顯著的最大客戶，這是集中度風險而非護城河證據。產業時鐘判為過熱期：客戶資本支出 2026 年約 7,850 億美元、2027 年逼近 1 兆美元，但雲端業者自由現金流轉負、Q1 直接發債 1,150 億美元已超過 2025 全年，屬擴張後段靠舉債延續的特徵；供給仍吃緊，尚未進入收縮。供需持久性：需求屬結構性，但增速預計 2027 年見頂後持平，判為週期性將反轉（反轉的是增速而非總量），這是空頭機率 30% 的來源。產業態勢裁決為雙向拉鋸：競爭面惡化（Broadcom 份額估 55–85%、聯發科瞄準 20% 可服務市場、台系設計服務壓價、800G 光 DSP 對手低價送樣），結構面轉好（光互連被點名為新瓶頸，Moody's 估新增約 7,000 億美元 RPO 支撐多年軌跡）。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi6_gaap_non_gaap","f_kpi7_q3_fy2027_2026_10_31"],"verdict_values":{"revenue_quality":"Q2 FY27 資料中心 21.72 億美元、占營收 79%，由設計案綁定的客製晶片與標準互連、交換器產品組成；前十大客戶占 FY26 營收 82%（10-K），一家經銷商約 37%（第三方彙整、未核對原文），集中度高","unit_econ_note":"非 GAAP 毛利率 58.9%、營益率 36.6%；GAAP 53.1%、16.8%，差距來自 SBC（占營收 11.9%）與併購無形資產攤銷。客製產品毛利率較低，但客戶出資的 NRE 沖減研發，營益率可隨規模擴張（CFO：營業費用增速約為營收一半）","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"fabless 設計案黏著（單一來源、跨代沿用）疊加 AI 資本支出循環；FY24–FY25 營收低谷期 GAAP 營業虧損、毛利率約 41%"},"industry":{"clock_phase":"III","sd_verdict_source":"BofA 雲端業者自由現金流預估與 2027 年見頂共識（TFTC 2026-09）、Moody's 資本支出預估（DatacenterDynamics 2026-09）、FactSet 發債統計（2026-07）","bargaining":{"up":"台積電先進製程、CoWoS 與 HBM 為瓶頸，Marvell 以五年預測與約 10 億美元預付鎖產能，上游強勢","down":"前十大客戶占 82%，四大雲端占成長絕大部分，Google 長約附認股權屬讓利，下游強勢","geo":"多數晶圓在台灣同一區域代工，封測分布於中國、馬來西亞、新加坡、台灣、加拿大"},"profit_pool_dir":"AI 資料中心利潤池往加速器與 HBM 集中；連接與客製設計的池子在擴大，但 Marvell 分到的毛利率低於 Broadcom 與 Nvidia","tam_table":[{"item":"2030 曆年可定址市場（公司估）","value":"約 4,000 億美元，較前次放大約 4 倍；前提為 2030 年資料中心資本支出約 3 兆美元（投資人日 2026-10-06）"},{"item":"客製市場與目標份額（公司估）","value":"客製 TAM 約 2,350 億美元，FY31 客製中點約 300 億美元、約 13% 份額；2024 年公司估 XPU 客製 TAM 為 400 億美元"},{"item":"互連（公司估）","value":"FY31 中點約 375 億美元、中點年複合約 65%；FY27 年增逾 70%"},{"item":"交換器與儲存（公司估）","value":"FY31 中點約 100 億美元；Teralynx 明年逾 10 億美元"},{"item":"XPU attach（公司估）","value":"一年前估約 150 億美元，現稱已放大數倍；每顆 XPU 一到兩個 socket、單價約 1,000 美元"},{"item":"第三方份額對照","value":"JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 10–12%；Counterpoint 估 Marvell 2027 年約 8%"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：執行面擴大（全連接堆疊、客製出貨四大美國雲端、Google 長約），定價面縮減（客製組合拉低毛利率、800G 光 DSP 對手約低四成報價），兩者相抵；最大客戶次世代有流失報導未證實，證實前不給上升","reasoning":"機制是設計案轉換成本加上高速 SerDes 與光電 IP 的廣度：客製專案流片後為單一來源，attach socket 可跨多代 XPU，互連端靠 1.6T DSP 首發（公司稱領先約兩年）與 TIA／驅動份額。執行力評 8：五個月內三度上調展望、客製出貨四大美國雲端、Google 6.5 年 1,200 億美元機會與 NVIDIA 20 億美元入股，Teralynx 交換器已證明能量產大晶片。定價權評 6：Q3 毛利率指引因客製組合較 Q2 下滑，800G 光 DSP 對手以約低四成報價送樣，世芯以 37.2% 毛利率搶單；對最強同業 Broadcom 的利潤率差距大（TTM GAAP 營益率 16.8% 對 48.5%、FCF 利潤率 18.2% 對 44.2%），投入資本事實表未涵蓋、無法算 ROIC spread，以利潤率差替代，未見收窄證據。方向判持平。威脅中 Broadcom 屬生態型攻擊，其餘為點對點。報酬持續期：以非 GAAP 營益率看屬高利益率，投入資本含約 110 億美元併購商譽、周轉率低；四檢查點皆黃，持續期取決於客戶資本支出能否延續、以及每次換代能否守住設計案；增量報酬與再投資率因投入資本、折舊攤銷序列缺而不給數字。","fact_refs":["f_peer_mrvl_gross_margin_pct","f_peer_mrvl_operating_margin_pct","f_peer_mrvl_fcf_margin_pct","f_peer_avgo_gross_margin_pct","f_peer_avgo_operating_margin_pct","f_peer_avgo_fcf_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_amd_gross_margin_pct","f_peer_amd_operating_margin_pct","f_peer_3661_tw_gross_margin_pct","f_peer_3661_tw_fcf_margin_pct","f_kpi2_non_gaap"],"verdict_values":{"moat":{"mechanism":"設計案轉換成本＋高速 SerDes／光電 IP 廣度：客製晶片流片後為單一來源、attach socket 跨代沿用；互連端靠 1.6T DSP 首發與 TIA／驅動份額","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"對最強同業 Broadcom：TTM GAAP 營益率 16.81% 對 48.52%、FCF 利潤率 18.23% 對 44.22%，投入資本事實表未涵蓋、以利潤率差代替 ROIC spread，差距約 32pp 且無收窄證據（同業僅 TTM 單點）；客戶側 AWS 為差距顯著的最大客戶，次世代 Trainium 傳轉 Alchip（未證實），JPMorgan 則稱現世代與次世代無份額流失","competitor_notes":[{"name":"Broadcom（AVGO）","strategy_note":"客製加速器份額估 55–85%，另有 Tomahawk 交換器與 Taurus 光 DSP，是唯一在客製、交換、光 DSP 三線同時正面競爭的對手，48.5% 營益率顯示規模與定價優勢"},{"name":"NVIDIA（NVDA）","strategy_note":"既有自家 NVLink 與網路產品，也是投資人與合作方（20 億美元入股、NVLink Fusion），短期互補大於替代"},{"name":"AMD","strategy_note":"利潤率結構與 Marvell 相近（毛利率 53.2%、營益率 15.7%），屬 GPU 供應方而非客製設計對手，影響在雲端客戶 GPU 與自研晶片的預算分配"},{"name":"世芯（3661.TW）","strategy_note":"以 37.2% 低毛利設計服務搶 XPU 專案，FCF 利潤率 −10.5% 顯示以資本換份額，是 Trainium 次世代傳聞的接手方"},{"name":"聯發科","strategy_note":"首顆 ASIC 2026 年第四季量產，瞄準 2027 年客製 AI 加速器可服務市場最高 20%，爭奪 ASIC 第二名"}],"threats":[{"level":"🔴","text":"Broadcom 生態型攻擊：客製加速器份額估 55–85%、路線圖能見度較高（HSBC），同時以 Tomahawk 交換器與 3 奈米 Taurus 光 DSP 正面競爭，Microsoft 傳評估改用其設計","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#3","substitute_technology#0","customer_second_source#3"]},{"level":"🟡","text":"台系設計服務與聯發科以低毛利搶 XPU 專案：Alchip、GUC 造成毛利壓力，聯發科瞄準 2027 年 20% 可服務市場，Trainium 3／4 傳轉 Alchip（未證實）；屬破壞性價格競爭","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","substitute_technology#1","supply_demand_durability#1","customer_second_source#2"]},{"level":"🟡","text":"雲端客戶自研晶片：10-Q 警告大客戶可能自行開發並製造半導體方案，導致業務流失","p":"25%","evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"光互連路線與價格競爭：LPO 去模組 DSP、800G 可插拔與相干 DSP 份額之爭轉激烈、Broadcom 與 MaxLinear 以約低四成報價送樣；Marvell 自身也賣 LPO／NPO／CPO 元件，屬點對點而非架構全面替代","p":"30%","evidence_refs":["competitive_share_entrants#5","competitive_share_entrants#6","substitute_technology#3","substitute_technology#4"]}],"roic_durability":{"quadrant":"高利益率×低周轉（非 GAAP 營益率 36.6% 屬高利益率；投入資本含約 110 億美元併購商譽、周轉率低；精確投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型開發與推論服務）、決策者（雲端架構團隊）、付款者（雲端資本支出）三角都成立，光互連被點名為新瓶頸、屬需要而非想要；但付款端自由現金流轉負、靠舉債支撐，急迫性高不等於持久性高"},{"item":"決策層級","level":"🟡","text":"替代性要在單一晶片世代的設計案層級看：流片後為單一來源、開發週期約兩年（Q1 FY27 法說），世代內幾乎不可替換；但每次換代重新競標，AWS 次世代傳聞正落在這個節點"},{"item":"價值鏈分配","level":"🟡","text":"稀缺環節在台積電先進製程、CoWoS（2026 年 Nvidia 約占六成）與 HBM，Marvell 需預付約 10 億美元鎖產能；下游四大客戶議價力強，Google 長約附認股權即是讓利；Marvell TTM 毛利率 52.2% 遠低於 Broadcom 68.8%，夾在兩端"},{"item":"社會容忍度","level":"🟡","text":"非民生必需品，沒有漲價的政治天花板；但資料中心用電的社會反彈（CEO 於 Citi 會議提及）、Section 232 半導體關稅與對中國出口許可屬政策風險，從客戶需求與成本兩端間接設限"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷序列缺）。方向判讀：fabless 有機成長所需實體資本低（Q2 資本支出 1.27 億美元對營業現金流 6.06 億美元），但近五年約 110 億美元併購與 FY27 約 10 億美元產能預付拉高增量投入，GAAP 口徑的增量報酬尚未證明高於資金成本","reinvest_rate":"事實表未涵蓋（折舊攤銷、營運資金變動、併購淨額未收錄）","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；本輪兩項輸入皆缺，天花板不給數字，共識缺口歸因寫在成長段"}}}},"q3_growth":{"verdict":"Y5 後跑道寬：管理層點名的 scale-up 光學、scale-up 交換器、跨資料中心 DCI、XPU attach 都還在起步，以公司估的市場規模計 FY31 中點只占約兩成；但成長是量驅動、押在四大雲端資本支出，FY29 之後落在管理層自稱的三年能見度之外","reasoning":"成長以量為主：資料中心 FY27 預期年增約 60%、投資人日把 FY28 上調為約 80%，來自出貨量與每顆 XPU 的連接、attach 內容增加；1.6T 換代帶來單價升級，但客製產品毛利較低；併購（Celestial AI、XConn、Polariton）只貢獻 scale-up 光學起步；回購只抵銷稀釋。共識 EPS FY27 4.22、FY28 7.25、FY29 12.18 美元，兩年年複合約 70%；FY26 非 GAAP 基期事實表未涵蓋，以 GAAP 3.07 美元算三年年複合約 58%，但 GAAP 基期含出售利益、口徑不一。FY29 共識一季上修 17%，家數事實表未涵蓋。內生天花板無數字，缺口歸因：營益率由 36.6% 擴到 40% 只解釋一小段，其餘是客戶資本支出驅動的量增，無法歸因於公司自身再投資報酬，屬依賴產業順風而非估值重評；長期信心上限中。跑道：以公司估 2030 年 4,000 億美元市場計，FY31 中點 800 億美元約占兩成，若市場不再擴大約 FY33 觸及三成，約 6–8 年、給中等折扣。衰退訊號亮 2 項（第三方份額下滑估計、SBC 占營收過高），價值陷阱風險與長期成長性皆為中。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_consensus_rev_fy2_pct","f_kpi1","f_kpi7_q3_fy2027_2026_10_31","f_kpi5_sbc_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（AI 資料中心出貨量與每顆 XPU 連接、attach 內容增加），價為次（1.6T 對 800G 升級，客製毛利較低）；併購貢獻小；回購只抵銷稀釋","runway_years":"6–8（公司 FY31 營收中點約占其估 2030 年可服務市場 20%，若市場不再擴大約 FY33 觸及 30%；市場規模與份額皆為公司估計）","runway_post_y5":"🟢","endo_ceiling_basis":"內生天花板無法以事實表算出（投入資本、折舊攤銷缺）；共識 FY27→FY29 EPS 兩年年複合約 70%，遠超 fabless 增量報酬×再投資率可支撐的區間，保守視為超出；缺口主要來自客戶資本支出驅動的量增與營業槓桿，依賴產業順風","segments":[{"item":"資料中心（Q2 FY27）","value":"21.72 億美元、占 79%、年增 46%、季增 18%；Q3 指引季增逾 20%、年增約 75%（法說會）"},{"item":"通訊及其他（Q2 FY27）","value":"5.68 億美元、年增 10%；Q3 預期季減與年減十幾個百分點，Q4 回升（法說會）"},{"item":"客製（XPU＋attach）","value":"FY27 下半年顯著放量、FY28 年增逾一倍、FY29 為 FY28 三倍以上逾 120 億美元、FY31 中點約 300 億美元（投資人日）"},{"item":"互連（光 DSP、TIA／驅動、DCI、AEC）","value":"FY27 年增逾 70%、FY31 中點約 375 億美元；TIA／驅動與 DCI 各朝年化 10 億美元（法說會、投資人日）"},{"item":"交換器與儲存","value":"scale-out 交換器 FY27 逾 6 億美元、Teralynx FY28 逾 10 億美元、FY31 中點約 100 億美元（Q1 法說、投資人日）"},{"item":"scale-up 光學（NPO／CPO）","value":"目前幾乎無營收，FY28 數億美元起步（上季口徑約 3 億美元，本季稱大幅高於此）"},{"item":"組合對毛利率","value":"客製占比上升使毛利率逐步下降，FY31 目標 56–59%；連接超預期則趨向高端"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"非 GAAP 毛利率 Q1、Q2 FY27 皆 58.9%，Q3 指引 57.5–58.5% 季減；去年同期值事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"Counterpoint 估客製 AI ASIC 份額 2027 年降至約 8%、JPMorgan 估 10–12%（屬預估非實現）"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"無證據"},{"signal":"EPS 年複合高於營收年複合逾 5pp","lit":false,"note":"FY28 共識 EPS 年增約 72%、管理層營收約年增 67%，差約 5pp 邊緣，屬營業槓桿擴張且口徑混用，不計入"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY26 為 0.52 但淨利含出售車用乙太網路事業利益；FY24、FY25 淨利為負不適用"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":true,"note":"Q2 FY27 為 11.9%、約占 GAAP 營業利益 71%；逐年走勢事實表未涵蓋，以水準過高計入"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"LPO／CPO 對模組 DSP 有替代壓力，但未見市場萎縮證據"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"倍數在可得區間頂部"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"Q2 總資本支出 1.27 億美元對 FCF 4.79 億美元約 26%"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"相反，正預付產能"}],"trap_rating":"價值陷阱風險🟡（亮 2 項）／長期成長性🟡"}}},"q4_capital":{"verdict":"資本配置屬中段：回購只抵銷稀釋且買在 65 倍前瞻本益比，過去約 110 億美元併購到 FY26 才轉為 GAAP 營業獲利，SBC 占營收 11.9%；正面是淨負債／EBITDA 僅 0.27 倍，投資人日承諾長期返還逾五成自由現金流","reasoning":"現金轉換：Q2 營業現金流 6.06 億美元、資本支出 1.27 億美元，自由現金流 4.79 億美元；營業現金流季減主因產能預付，FY27 預付約 10 億美元。FY26 自由現金流 13.92 億美元對淨利 26.70 億美元約 0.52，但淨利含出售車用乙太網路事業利益；FY24、FY25 淨利為負而自由現金流 10.2、13.9 億美元，轉換率靠 SBC 加回撐起。SBC 3.26 億美元占營收 11.9%、約為 GAAP 營業利益 71%。Q2 現金去向：回購 2 億美元、股利 0.54 億美元、資本支出 1.27 億美元、產能預付；近三年四分結構事實表未涵蓋。三項計分：併購已實現增量報酬未證明高於資金成本，不過；回購盈餘殖利率約 1.5%，不過；稀釋股數與上季持平，過，但 Google 認股權與 NVIDIA 入股屬另一條稀釋來源、規模本包未揭露。負債 49.6 億美元、淨負債／EBITDA 0.27 倍，資產負債表安全。CFO 於 6 月更替（Willem Meintjes 離任、前董事 Dan Durn 接任），屬重大事件，但交接有序、指引口徑未變，不涉核心假設。","fact_refs":["f_kpi4_605_5m_capex_126_7m","f_kpi5_sbc_gaap","f_peer_mrvl_fcf_margin_pct","f_dividend_yield_ttm","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"FY21–FY26 併購約 110 億美元（投資人日 CFO）；同期 GAAP 營益率 FY23 6.07%、FY24 −7.93%、FY25 −6.35%、FY26 16.33%，到 FY26 才轉為營業獲利，併購資產的已實現增量報酬未證明高於資金成本"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q2 回購 2 億美元；回購均價事實表未涵蓋，以判斷日前瞻本益比 65.23 倍換算盈餘殖利率約 1.5%，低於 10 年期公債殖利率加 2%（公債殖利率事實表未涵蓋，但任何正值加 2% 皆高於 1.5%）"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 指引稀釋加權股數約 9.21 億、與 Q2 大致持平（CFO），每季 3.26 億美元 SBC 由約 2 億美元回購抵銷；Google 認股權與 NVIDIA 入股為另一稀釋來源，規模本包未揭露，年度淨稀釋率事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機的互連與客製放量，近期併購（Celestial AI、XConn、Polariton）只貢獻 scale-up 光學起步而非成長主力；回購僅抵銷稀釋"}}}},"q5_valuation":{"verdict":"現價要求 FY32 非 GAAP EPS 約 21 美元（FY27 共識的五倍）並維持 22 倍，才換得約 11% 年化，等於管理層 FY31 目標兌現約六到七成；我信基準可達，但價格已把它算進去，不追","reasoning":"判斷日股價 275.28 美元：對 FY27 共識 EPS 4.22 為 65.23 倍、FY28 7.25 為 38.0 倍、FY29 12.18 為 22.6 倍；trailing 本益比 90.55 倍（GAAP、含出售利益），P/S 26.18 倍、EV/S 26.32 倍皆在可得 4 個年度端點的最高。PEG 以 FY27→FY29 兩年 EPS 年複合約 70% 計為 0.93，但成長集中在資本支出最熱的兩年，PEG 偏低不代表便宜。反推：以 22 倍終端倍數換約 11% 年化，FY32 EPS 需約 21 美元。短期上檔：一年後以 FY28 基準 EPS 7.4 美元×42 倍約 311 美元（+13%）；中期：三年後以 FY30 基準 15 美元×28 倍約 420 美元（+53%）。賣方 7–8 月平均目標價 245–261 美元低於現價，但屬投資人日前資料；目標價全距 105–400 美元約 3.8 倍，賣方分歧大，對自身上下檔比的信心相應下調。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（非 GAAP 共識 EPS），以市場現給 FY29 共識的 22.6 倍作終端倍數的內部對照","tier":"AI 半導體高成長","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋（同業對照只有利潤率），無法建同層級倍數對照"},"fwd_pe":65.23,"peg":0.93,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"前瞻本益比 65.23 倍、P/S 26.18 倍位於可得 4 個年度端點最高（分位 100，非五年連續序列）；基準五年年化約 11%（中）、上下檔比約 2.8；股價高於投資人日前賣方平均目標價；FY28 共識倍數由前份約 32 倍升至 38 倍，結論由合理偏貴轉為偏貴","upside_short_pct":13,"upside_mid_pct":53,"denominator_disputed":false,"denominator_note":"trailing GAAP 分母含出售車用乙太網路事業一次性利益與併購攤銷，改用前瞻非 GAAP 共識；SBC 占營收 11.9% 未從非 GAAP EPS 扣除，已以淨回購 0 與空頭倍數處理，分母本身不是本檔爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在客戶資本支出 2027 年見頂後轉向消化：客製放量遞延、光 DSP 價格戰與 65 倍本益比同步收縮，股價可回到 115 美元上下","reasoning":"最可能看錯的三處：一是客戶資本支出時點，BofA 估雲端業者自由現金流 2027 年 −1,440 億美元、共識預期 2027 年見頂後持平，與管理層 FY31 模型假設的約 20% 增速衝突；二是 AWS 次世代設計歸屬，傳聞指向的放量窗在 FY28–FY29，現有證據蓋不到；三是管理層問答迴避處：超額下單風險未正面回答、Google 認股權在 FY31 只計入部分價值卻不給比例、互連 TAM 拒絕拆數字。路徑風險：空頭終點約 −58%，FY30 谷底若倍數同步壓縮可到約 −65%，屬深回撤；論點本身完整（護城河持平、跑道寬、非估值依賴），持有後不因波動砍倉，進場前先做好深回撤心理準備。壓力檢核四項過二：淨負債／EBITDA 0.27 倍、FY24–FY25 營收低谷期自由現金流仍為正；同期毛利率跌到約 41%、GAAP 營業虧損，兩項不過。陷阱判為中：高估值成長股而非價值陷阱。","fact_refs":["f_week26_return_pct","f_rsi14","f_ps_percentile","f_kpi5_sbc_gaap","f_fwd_pe_latest"],"verdict_values":{"trap":{"verdict":"🟡","label":"高估值成長股、非價值陷阱；亮燈在第三方份額下滑估計與 SBC 占營收 11.9%"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":4.22,"pe":65.23,"basis":"FY2027E（2027 年 1 月止）非 GAAP 共識 EPS 4.22 美元、判斷日股價 275.28 美元；終端倍數同為當年度前瞻一年非 GAAP EPS 口徑"},"eps":{"bull":[7.9,13.5,20.0,28.0,34.0],"base":[7.4,12.0,15.0,18.0,21.0],"bear":[6.4,7.6,5.6,5.9,6.8]},"pe":{"bull":24,"base":22,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.087,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-65,"hi":-50,"basis":"下緣：空頭路徑 FY30 EPS 谷底 5.6 美元若倍數同步壓到 17 倍，價格約 95 美元（約 −65%），涵蓋空頭終點 −58%；上緣：FY28 共識 7.25 美元不變、本益比壓到 19 倍即達約 138 美元（−50%），對應 26 週已漲 114% 的動能反轉。歷史最大回撤序列事實表未涵蓋，未拿歷史值校準","trigger_time":null},"basis":{"bull":"管理層 FY31 目標（營收 700–900 億美元、非 GAAP EPS 逾 30 美元）約九成兌現：Google TPU 生態系長約與新一線 XPU 專案如期放量，scale-up 光學與交換器成為第二曲線；終端 24 倍對應 FY32 後仍有約 15% 成長","base":"FY28 達管理層約 200 億美元營收、FY29 貼近共識 12.18 美元，之後客戶資本支出增速放緩至約 20%，Marvell 每年成長 25%→20%→17%，FY32 EPS 21 美元約為管理層 FY31 目標的六到七成；終端 22 倍，同業前瞻倍數事實表未涵蓋，以市場現給 FY29 共識的 22.6 倍作對照","bear":"客戶資本支出 2027 年見頂後轉向消化（BofA 估雲端業者自由現金流 2027 年 −1,440 億美元、融資受限），AWS 次世代設計外流與光 DSP 價格戰同時發生，EPS 由 FY29 7.6 美元回落至 FY30 谷底 5.6 美元；終端 17 倍對應成長熄火至約 10%。機率 30%：RPO 約 7,000 億美元與已鎖定的 FY28 供給撐住近兩年，故不高於 30%；融資結構與份額報導讓它不低於 30%"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"BofA 估雲端業者合計自由現金流 2027 年 −1,440 億、2028 年 −1,860 億美元，市場共識傾向 2027 年資本支出見頂後持平；Q1 美國超大型業者直接發債 1,150 億美元，已超過 2025 全年 700 億","assumption":"管理層 FY31 模型假設客戶資本支出增速尾端仍約 20%、不轉負","consequence":"FY29 之後客製放量遞延、互連訂單消化，EPS 由約 7.6 美元回落到 5.6 美元谷底，倍數由 65 倍壓到 17 倍，五年後股價約 116 美元（−58%）","ruling":"部分採納：放進空頭情境、機率 30%，與唯一致命點是同一件事，兩處一致；不再往上加，因 Moody's 估新增約 7,000 億美元 RPO 撐住多年需求、公司稱 FY28 所需供給已到位","watch":"四大雲端每季資本支出指引；Marvell 下季營收指引是否季減","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"],"fact_refs":["f_consensus_eps_fy3","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"前十大客戶占 FY26 營收 82%，一家經銷商約 37%（第三方彙整），10-Q 稱 AWS 是差距顯著的最大客戶；Benchmark 稱 Trainium 3／4 設計輸給 Alchip，Microsoft 評估 Broadcom；10-Q 亦警告大客戶可能自製晶片","assumption":"四大客戶各自多世代留在 Marvell","consequence":"單一客戶換代即可吃掉客製成長的一大段","ruling":"採納為中期風險，但不升為唯一致命點：管理層稱 FY31 目標不需新勝案、產品面分散，單一客戶流失的衝擊小於資本支出整體反轉","watch":"10-Q 客戶集中度揭露、AWS 次世代 Trainium 設計夥伴","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0","customer_second_source#1","customer_second_source#2","customer_second_source#3"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 11.9%、約為 GAAP 營業利益 71%；Q3 指引 GAAP EPS 0.53 美元對非 GAAP 1.10 美元；Google 長約附認股權、NVIDIA 20 億美元入股，客戶以股權分享成長；FY27 約 10 億美元產能預付；TTM 自由現金流利潤率 18.2%，遠低於管理層長期逾 36% 目標","assumption":"非 GAAP EPS 代表股東實得盈餘、回購足以抵銷稀釋","consequence":"營收照目標成長，但每股可得現金被 SBC、客戶認股權與預付款分走一截，以非 GAAP 本益比估值會高估股東報酬","ruling":"採納：情境樹淨回購殖利率設 0、不給回購加分；SBC 淨稀釋目前被回購抵銷，但認股權規模本包未揭露，列監測","watch":"稀釋股數逐季、SBC 占營收、Google 認股權行使條件與股數","evidence_refs":[],"fact_refs":["f_kpi5_sbc_gaap","f_kpi4_605_5m_capex_126_7m","f_peer_mrvl_fcf_margin_pct","f_kpi3_gaap","f_kpi2_non_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"客製占比提高拉低毛利率（Q3 指引 57.5–58.5% 低於 Q2 58.9%）；世芯以 37.2% 毛利率、−10.5% FCF 利潤率搶專案；先進封裝產能 2026 年由 Nvidia 約占六成，自研晶片與其他客戶搶同一批台積電產能","assumption":"營收成長能同比例轉成利潤","consequence":"價值鏈兩端（晶圓與封裝產能、雲端客戶）多拿，Marvell 營收倍增但毛利率往 56% 下緣走","ruling":"部分採納：基準 EPS 已低於管理層 FY31 目標，吸收部分壓力；毛利率連 2 季跌破 57.0% 時改判為價格戰","watch":"非 GAAP 毛利率逐季","evidence_refs":["geo_supply_chain#3","competitive_share_entrants#1"],"fact_refs":["f_kpi6_gaap_non_gaap","f_kpi7_q3_fy2027_2026_10_31","f_peer_3661_tw_gross_margin_pct","f_peer_3661_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"26 週漲 114.34%；前瞻本益比 65.23 倍、P/S 26.18 倍在可得年度端點最高；股價高於 7–8 月賣方平均目標價 245–261 美元（投資人日前資料）；前份判斷以來六週漲 27%","assumption":"市場給 FY29 共識 22.6 倍代表已充分折現長期目標","consequence":"基準情境年化約 11%，多數上檔已在價格內；若 Q3 只是符合指引，倍數可回到 FY28 共識 32 倍（約 232 美元）","ruling":"採納：不追，進場條件綁 FY28 共識 32 倍","watch":"股價對 FY28 共識 EPS 倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_ps_percentile","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 216.62 → 本次 275.28（+27.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=216.62","side_b":"本次 price_at_dd=275.28","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟡→🟠、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AWS 次世代 Trainium 設計歸屬","cause":null,"prior_field":null,"side_a":"Benchmark 降評稱 Trainium 3／4 設計輸給 Alchip，Dolphin Research 亦有轉向傳聞；10-Q 自承 AWS 是差距顯著的最大客戶，轉換設計夥伴會重大影響營收","side_b":"管理層 2026 年 3 月稱 FY26 看不到 Amazon 營收中斷、否認失去 Amazon 或 Microsoft；投資人日稱客製專案皆為單一來源、目標不需新勝案；Q2 FY27 資料中心季增 18%、Q3 指引季增逾 20%","ruling":"不可調和（一邊是失去下一代、一邊是沒有中斷），但兩邊的時間窗不同：管理層證據蓋到 FY27，傳聞指向的 Trainium 3／4 放量落在 FY28–FY29。現有證據不蓋風險窗，裁定不可裁決至 2027 年中；在此之前不稱風險已解，基準情境不扣 AWS，空頭情境吃進此風險","evidence_level":"二手報導（未經公司證實）對公司口頭說法","settle_metric":"FY28 上半年客製營收年增率是否 ≥100%；10-Q 最大客戶占比與客戶揭露","if_then":["若 10-Q 或法說會確認 AWS 次世代主力 XPU 改由他家設計，且 FY28 客製倍增目標下修→持有部位減碼一半，未持有則撤回進場價位並重跑判斷","反向：若 FY28 上半年客製營收年增 ≥100% 且 AWS 仍列最大客戶→移除此風險，進場價位上調至 FY28 共識 EPS 的 35 倍"],"evidence_refs":["customer_second_source#0","customer_second_source#2","competitive_share_entrants#1","customer_concentration_credit#1"]},{"axis":"管理層長期模型對客戶資本支出路徑","cause":null,"prior_field":null,"side_a":"管理層 FY31 模型：資料中心營收中點年複合約 65%、營收 700–900 億美元、EPS 逾 30 美元，假設資本支出增速尾端約 20%；CEO 自稱這是三年押注而非五年","side_b":"市場共識傾向 2027 年資本支出見頂後持平，BofA 估雲端業者合計自由現金流 2026–2028 年由 −640 億擴大到 −1,860 億美元，Goldman 估 2027 年 AI 資本支出約三分之一靠舉債","ruling":"不可調和，選資本支出共識側作基準：Marvell 年增 65% 而客戶支出年增 20%，代表份額或單位內容每年要擴大約 1.4 倍、連續五年，超過現有證據；管理層目標只放進多頭情境（25%），基準取其六到七成","evidence_level":"公司長期模型對第三方資本支出與現金流預估","settle_metric":"四大雲端 2027–2028 年資本支出指引年增率；Marvell FY29 客製營收是否 ≥120 億美元","if_then":["若 FY29 客製營收 ≥120 億美元且四大雲端 2028 年資本支出指引仍年增 ≥15%→基準 EPS 上調到管理層目標八成並重跑，首倉後可加碼至 4%","反向：若任一年度四大雲端合計資本支出指引年減→改用空頭路徑，持有部位減碼至半倉"],"evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3","supply_demand_durability#3"]},{"axis":"毛利率走向","cause":null,"prior_field":null,"side_a":"CFO：FY28 毛利率與 FY27 下半年同區間（57.5–58.5%），FY31 目標 56–59%；客製有客戶出資 NRE 沖減研發，營益率仍可擴張","side_b":"客製占比上升時毛利率逐步下降（CFO 於 Citi 會議），Q3 指引較 Q2 的 58.9% 下滑；800G 光 DSP 有 Broadcom、MaxLinear 以約 50–60 美元對 Marvell 90–100 美元送樣認證；財報後盤後下跌約 2% 即反映毛利率走低","ruling":"可調和（程度差異）：毛利率走低是組合使然、公司已提前揭露，營益率由營業費用增速約為營收一半撐住；真正的分界是跌破指引下緣，那代表價格戰而非組合","evidence_level":"公司指引對第三方報價資料（2025 年 5 月）","settle_metric":"Q3–Q4 FY27 非 GAAP 毛利率實際值","if_then":["若非 GAAP 毛利率連 2 季低於 57.0%→持有部位減碼至半倉","反向：若 Q4 FY27 毛利率 ≥58% 且營益率 ≥38%→組合衝擊已吸收，可依進場條件建倉"],"evidence_refs":["competitive_share_entrants#5","capital_markets_pricing#3"]},{"axis":"客製加速器份額","cause":null,"prior_field":null,"side_a":"Counterpoint 估 Marvell 客製 AI ASIC 份額 2027 年降至約 8%，JPMorgan 估 Broadcom 占高階 ASIC 80–85%、Marvell 10–12%；聯發科瞄準 2027 年 20% 可服務市場","side_b":"管理層稱客製出貨四大美國雲端、20 件以上設計案，FY31 客製 300 億美元約占其估 2,350 億美元客製市場 13%；JPMorgan 另稱 Microsoft、AWS 現世代與次世代無份額流失","ruling":"可調和：第三方多以加速器出貨顆數算份額，管理層算的是含 XPU attach 的營收，而 Marvell 的成長愈來愈靠 attach 與連接；份額下滑估計計為一個衰退訊號，但不改護城河方向","evidence_level":"第三方預估對公司營收口徑","settle_metric":"FY28 客製營收（含 attach）與第三方下一版份額估計","if_then":["若 FY28 客製營收未達倍增且第三方份額估計續降→護城河方向改為縮減並重跑判斷","反向：若 FY28 客製倍增達成→維持方向持平"],"evidence_refs":["end_markets#3","competitive_share_entrants#0","competitive_share_entrants#4","supply_demand_durability#1","substitute_technology#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"五個月內 FY28 營收展望三度上調（165→180→200 億美元），FY29 共識 EPS 一季上修 17%；以 FY29 共識計本益比只有 22.6 倍、兩年 EPS 年複合約 70%，若 FY31 達 30 美元則現價約 9 倍","side_b":"上修集中在客戶資本支出最熱的一年，FY31 目標連管理層都稱超出三年能見度；26 週已漲 114%、P/S 在可得區間頂部，基準五年年化約 11% 只算中等；空頭 30% 機率下跌約 58%","ruling":"不追：買進論證成立的前提是 FY29 之後的成長，那段沒有可驗證證據；等價格給出更好的上下檔比","evidence_level":"公司指引與共識對情境推算","settle_metric":"股價對 FY28 共識 EPS 倍數","if_then":["若股價回落至 FY28 共識 EPS 32 倍以下（約 232 美元）且毛利率守 57.5%→重跑判斷後以 2% 首倉進場","反向：若股價續漲而 Q3 財報前證據未更新→不追"],"evidence_refs":[]},{"axis":"估值與上下檔比（股價 216.62→275.28 美元，+27%）","cause":"價格變動","prior_field":["signal","val","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct"],"side_a":"前份：估值合理偏貴、綜合評級 A、上下檔比 4.3、基準年化 10.9%、五年期望 +64.6%、最大回撤 −48%、裁決觀望","side_b":"本次：股價六週漲 27%，FY28 共識 EPS 只上修約 7%，FY28 倍數由約 32 倍升至 38 倍，估值轉偏貴、綜合評級降為 B；基準年化約 11%（遠年 EPS 上修抵銷）、上下檔比約 2.8、最大回撤範圍 −50%～−65%；裁決與倉位角色隨新輸入重算","ruling":"估值結論與綜合評級下調的主因是價格先走、近年 EPS 跟得慢；基準報酬沒降是遠年上修抵銷，屬不同年期互抵，不視為變便宜；上下檔比下降另含多頭機率由 30% 降至 25%","evidence_level":"事實表股價與共識快照","settle_metric":"股價對 FY28 共識 EPS 倍數","if_then":["若股價回落至 FY28 共識 EPS 32 倍以下→估值結論回到合理偏貴並重跑進場","反向：若 FY28 共識再上修 10% 以上而股價不動→同樣達到價位條件"],"evidence_refs":[]},{"axis":"投資人日與 Google 長約後的長期假設","cause":"新證據","prior_field":["bull_5y_price","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：多頭五年價 570.3 美元、護城河持平、Y5 後跑道寬、品質複利成長型、未給循環位置","side_b":"本次：投資人日把 FY28 營收上調至約 200 億美元、FY31 給 700–900 億美元與 EPS 逾 30 美元，揭露 Google 6.5 年 1,200 億美元客製機會；多頭五年價升至約 816 美元；護城河方向、跑道、類型與循環位置不變","ruling":"新證據抬高多頭天花板，不改方向判斷：執行面擴大被定價面縮減抵銷，Trainium 傳聞未解，仍標持平；跑道寬由管理層點名的第二曲線支撐，但市場規模屬公司估計；類型維持品質複利成長，循環屬性以次要類型與空頭情境處理，不另給循環位置","evidence_level":"公司投資人日與 8-K","settle_metric":"FY28 客製營收、Q4 FY27 營益率","if_then":["若 FY28 客製倍增且 Q4 FY27 營益率 ≥38%→重審護城河執行面是否轉為擴大","反向：若 AWS 次世代確認外流→護城河改縮減並重跑判斷"],"evidence_refs":["end_markets#1","customer_second_source#2"]},{"axis":"情境定義與陷阱計數","cause":"方法變動","prior_field":["trap","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份：陷阱風險低、空頭五年價 134.1 美元、多頭與空頭機率各 30%","side_b":"本次：陷阱風險中（亮 2 項：第三方份額下滑估計、SBC 占營收 11.9%）、空頭五年價約 116 美元（終端 17 倍、EPS 不高於 FY28 共識）、多頭機率 25%、空頭 30% 不變","ruling":"兩項亮燈證據前份已存在，變的是計數口徑：本次把 SBC 水準與第三方份額預估計入；多頭改定義為管理層 FY31 目標約九成兌現，門檻比前份高，機率相應下調；空頭終端倍數改用成長熄火至約 10% 的 17 倍","evidence_level":"口徑調整","settle_metric":"SBC 占營收逐季走勢、第三方份額估計","if_then":["若 SBC 占營收降至 8% 以下且份額估計止跌→陷阱風險回到低","反向：若 SBC 占營收逐季上升→陷阱風險升為高並減碼至半倉"],"evidence_refs":["end_markets#3"]},{"axis":"首倉進場條件（估值重啟）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"三旗艦socket任一正面確認＋GM守57.5-58.5%","side_b":"股價回落至FY2028E共識EPS的32倍以下（以7.25美元計約232美元）且最近一季非GAAP毛利率≥57.5%","ruling":"前份條件未發火：投資人日只說客製出貨四大雲端，沒有客戶端對特定旗艦世代的確認，Q3 毛利率實際值未出。股價六週漲 27% 後，卡住首倉進場的是倍數而非證據，故首倉進場與後續加碼條件改綁 FY28 共識本益比；毛利率守 57.5% 保留為論點完好的前提","evidence_level":"價格與共識快照","settle_metric":"股價÷FY28 共識 EPS；最近一季非 GAAP 毛利率","if_then":["若條件達成→重跑判斷後首倉進場 2%","反向：若 Q3 毛利率跌破 57.5%→進場條件作廢，改看減碼條件"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"四大美國雲端業者合計年度資本支出指引首次轉為年減","ruling":"前份把客戶資本支出放在風險清單而未指定唯一致命點；本次以數學敏感度選定：資本支出年減同時打到客製、互連、交換器三條線並觸發倍數壓縮，對 Y5 EPS 的衝擊大於任一單一客戶事件；發生即減碼至半倉","evidence_level":"第三方資本支出與現金流預估","settle_metric":"四大雲端年度資本支出指引年增率","if_then":["若合計指引首次年減→持有部位減碼至半倉，未持有則撤回進場條件","反向：若 2027 年指引年增 ≥15%→維持基準"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"出場門檻（減碼與清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"毛利率連 2 季低於 57.0%→減碼至半倉；FY28 營收展望低於 180 億美元且 FY29 客製目標下修→清倉；AWS 次世代外流確認→減碼一半；四大雲端資本支出年減→減碼至半倉","ruling":"前份只有進場條件、沒有減碼與清倉門檻，本次補齊；之後降位也保留指標、門檻與資料來源","evidence_level":"口徑補齊","settle_metric":"各門檻對應的季報與指引","if_then":["若任一減碼門檻觸發→依門檻動作並重跑判斷","反向：若四項皆維持正常至 FY28 年報→門檻依新共識上調"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回落至 FY28 共識 EPS 32 倍以下且毛利率守 57.5%：重跑判斷後首倉 2%","type":"估值rearm","maps_to":"H3","metric":"股價÷FY2028E 共識 EPS","threshold":"≤32 倍（以 7.25 美元計約 232 美元）且最近一季非 GAAP 毛利率 ≥57.5%","action":"重跑判斷後首倉 2%","source_freq":"每日股價／每月共識快照","date":null,"evidence_refs":[]},{"n":2,"text":"Q3 FY27 財報驗證資料中心加速與毛利率指引","type":"假設驗證","maps_to":"H1","metric":"資料中心季增率、總營收、非 GAAP 毛利率","threshold":"資料中心季增 ≥20%、營收在 29.9–33.1 億美元、毛利率 57.5–58.5%、Q4 指引續季增","action":"達標：依新共識重算進場價；未達：凍結進場至 Q4 財報","source_freq":"每季財報","date":"2026-12","evidence_refs":[]},{"n":3,"text":"Q4 FY27 營益率進入長期目標區間且 FY28 約 200 億美元重申：已持有首倉則加碼","type":"加碼","maps_to":"H3","metric":"非 GAAP 營益率；FY28 營收展望","threshold":"Q4 FY27 營益率 ≥38% 且 FY28 展望 ≥200 億美元","action":"加碼至 4%","source_freq":"每季財報","date":"2027-03","evidence_refs":[]},{"n":4,"text":"四大美國雲端業者合計年度資本支出指引首次轉為年減","type":"Single Thing","maps_to":"R3","metric":"四大雲端合計年度資本支出指引年增率","threshold":"首次轉為年減","action":"持有部位減碼至半倉；未持有則撤回進場條件、重跑判斷","source_freq":"每季（各公司季報）","date":"2027-02","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"]},{"n":5,"text":"AWS 次世代 Trainium 確認改由他家主導設計","type":"風險","maps_to":"R1","metric":"AWS 次世代 Trainium 設計夥伴","threshold":"公司或 AWS 確認改由他家主導","action":"減碼一半並重跑判斷","source_freq":"每季 10-Q／法說會","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#2"]},{"n":6,"text":"非 GAAP 毛利率連 2 季跌破 57.0%，判為價格戰","type":"減碼","maps_to":"R2","metric":"非 GAAP 毛利率","threshold":"連 2 季 <57.0%","action":"減碼至半倉","source_freq":"每季財報","date":null,"evidence_refs":["competitive_share_entrants#5"]},{"n":7,"text":"FY28 營收展望與 FY29 客製目標同時下修","type":"清倉","maps_to":"H1","metric":"FY28 營收展望；FY29 客製營收目標","threshold":"FY28 展望低於 180 億美元且 FY29 客製目標下修至 FY28 兩倍以下","action":"清倉","source_freq":"每季法說會／投資人日","date":null,"evidence_refs":[]},{"n":8,"text":"股價先於 EPS 衝高：持有部位分批獲利了結","type":"減碼","maps_to":"H3","metric":"股價÷FY2028E 共識 EPS","threshold":"≥55 倍（以 7.25 美元計約 400 美元）且 FY29 共識未同步上修","action":"持有部位減碼三分之一","source_freq":"每日股價／每月共識快照","date":null,"evidence_refs":[]},{"n":9,"text":"Section 232 半導體關稅第二階段涵蓋 Marvell 主要產品並傷及毛利率","type":"風險","maps_to":"R4","metric":"Section 232 涵蓋範圍與公司毛利率指引","threshold":"涵蓋主要產品且毛利率指引因此下修 ≥100bp","action":"減碼至半倉","source_freq":"政策公告／每季財報","date":null,"evidence_refs":["reg_tariff_export#1","regulatory_antitrust#2"]},{"n":10,"text":"Q3 FY27 財報後複審","type":"複審日期","maps_to":"H1","metric":"全部論點與門檻","threshold":"財報公布","action":"重跑判斷","source_freq":"每季","date":"2026-12","evidence_refs":[]}],"kill_metrics":[{"metric":"非 GAAP 毛利率（季）","bear_threshold":"連 2 季 <57.0%（低於指引下緣 57.5%）","window":"Q3–Q4 FY27 財報（2026-12、2027-03）","source":"公司季報新聞稿","last_status":"ok"},{"metric":"資料中心營收對當季指引","bear_threshold":"單季實際低於指引區間下緣，或下季指引季減","window":"每季財報","source":"公司季報新聞稿與法說會","last_status":"ok"},{"metric":"FY2028 營收展望（管理層）","bear_threshold":"由約 200 億美元下修至 180 億美元以下","window":"至 2027-03 年度財報","source":"法說會／投資人日","last_status":"ok"},{"metric":"四大美國雲端業者合計年度資本支出指引","bear_threshold":"任一年度指引合計年減","window":"12–24 個月，每季更新","source":"各公司季報","last_status":"ok"},{"metric":"AWS 次世代 Trainium 設計夥伴","bear_threshold":"公司或 AWS 確認改由他家主導設計","window":"12–24 個月","source":"10-Q 客戶揭露、法說會","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至FY2028E共識EPS的32倍以下（以7.25美元計約232美元）且最近一季非GAAP毛利率≥57.5%","exec_line":"條件達成先重跑判斷，再以 2% 首倉進場；Q4 FY27 營益率 ≥38% 且 FY28 約 200 億美元重申後加碼至 4%；路徑風險高但論點完整，持有後不因 −50% 以內波動砍倉，只依減碼與清倉條件動作"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價回落至 FY2028E 共識 EPS 的 32 倍以下（以 7.25 美元計約 232 美元）且非 GAAP 毛利率守 57.5%；或 Q3 FY27 財報確認資料中心季增 ≥20%、毛利率在指引內後，依新共識重算價位","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"衛星"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=114.34, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"客製業務（XPU＋XPU attach）靠四大雲端分散與 Google TPU 生態系長約放量，FY28 年增逾一倍、FY29 達 FY28 三倍以上，抵銷 AWS 世代交接風險","2y":"FY29 客製營收 ≥100 億美元（管理層目標逾 120 億美元）","5y":null,"10y":null,"threshold":"FY28 客製年增 ≥100%；FY29 客製 ≥100 億美元","source":"公司季報、法說會與投資人日的客製營收口頭揭露；10-Q 客戶集中度","drift_rule":"資料中心營收連 2 季低於當季指引中點 5% 以上＝削弱；連 3 季低於 10% 以上或下修 FY29 客製目標＝反轉"},{"id":"H2","text":"互連（光 DSP、TIA／驅動、DCI）與交換器成長持續快於客戶資本支出，scale-up 光學與交換器成為第二曲線","2y":null,"5y":"FY31 互連營收達管理層中點 375 億美元的六成以上（≥225 億美元）","10y":null,"threshold":"互連 FY27 年增 ≥70%；FY28 互連年增率高於四大雲端資本支出增速 10pp 以上；交換器 FY28 年化 ≥10 億美元","source":"法說會分項口頭數字、投資人日、Cignal AI 與 Dell'Oro 份額報告","drift_rule":"互連成長率連 4 季低於門檻 5pp 以上＝削弱；連 6 季低於 10pp 以上＝反轉"},{"id":"H3","text":"毛利率在客製占比上升下守住 57.5%，營業費用增速約為營收一半，非 GAAP 營益率 FY28 內觸及 40%，EPS 成長快於營收；客戶資本支出 2027 年後放緩但不轉負","2y":"FY28 非 GAAP EPS ≥7.0 美元（共識 7.25）","5y":null,"10y":null,"threshold":"非 GAAP 毛利率 ≥57.5%；Q4 FY27 營益率 ≥38%、FY28 觸及 40%","source":"季報新聞稿非 GAAP 損益；四大雲端季報資本支出指引","drift_rule":"毛利率或營益率連 2 季低於門檻 5% 以上（相對值）＝削弱；連 3 季低於 10% 以上＝反轉"}],"R":[{"id":"R1","text":"最大客戶 AWS 次世代 Trainium 設計外流（傳 Trainium 3／4 轉 Alchip）或 Microsoft 改用 Broadcom，Google 與新一線客戶放量來不及補位","h_ref":"H1","clock":"🔥","threshold":"公司或客戶確認任一旗艦世代改由他家設計，或 FY28 客製營收未達倍增","evidence_refs":["customer_second_source#0","customer_second_source#2","customer_second_source#3","customer_concentration_credit#0","customer_concentration_credit#1","competitive_share_entrants#1"]},{"id":"R2","text":"毛利率由組合下滑轉為價格戰：800G 光 DSP 對手報價約低四成、相干 800G 競爭加劇、客製占比升高，Q3 指引已較 Q2 走低","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率連 2 季 <57.0%","evidence_refs":["competitive_share_entrants#5","competitive_share_entrants#6","capital_markets_pricing#3"]},{"id":"R3","text":"客戶資本支出 2027 年見頂後轉向消化，雲端業者自由現金流轉負、舉債比重升高，訂單遞延","h_ref":"H3","clock":"🔥","threshold":"四大雲端合計年度資本支出指引年減，或 Marvell 下季營收指引季減","evidence_refs":["supply_demand_durability#4","customer_concentration_credit#3"]},{"id":"R4","text":"台灣晶圓與泛太平洋封測集中（歷年 10-K 皆揭露替代晶圓廠有限）、Section 232 半導體關稅第二階段、對中國出口許可延遲或拒發","h_ref":"H3","clock":"🐢","threshold":"關稅或出口管制使公司毛利率指引下修 ≥100bp，或台海供應中斷","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R5","text":"光互連架構替代：LPO 去掉模組 DSP、Broadcom 3 奈米 400G／lane Taurus DSP 競爭 1.6T／3.2T，scale-up 走 CPO 時 Marvell 光 DSP 經濟性被侵蝕","h_ref":"H2","clock":"🐢","threshold":"Cignal AI 或 Dell'Oro 的可插拔光 DSP 份額連 2 年下滑，或互連年增率低於四大雲端資本支出增速","evidence_refs":["substitute_technology#3","substitute_technology#4","competitive_share_entrants#6"]}],"single_thing":{"description":"四大美國雲端業者合計年度資本支出指引首次轉為年減","why_fatal":"資料中心占營收 79%、前十大客戶占 82%，FY31 模型假設資本支出增速只放緩到約 20%；一旦轉負，客製、互連、交換器三條線同時遞延，65 倍前瞻本益比向 17 倍收斂，EPS 與倍數雙殺，對五年價值的衝擊大於任何單一客戶事件","if_happens":"持有部位減碼至半倉；未持有則撤回進場條件，待下一季營收指引確認後重跑判斷","how_monitor":"四大雲端每季財報的年度資本支出指引（每年 1–2 月給次年度、每季更新），搭配 Marvell 下季營收指引是否季減","probability":"約 15%（12–24 個月）：BofA 估自由現金流轉負、共識預期 2027 年見頂持平，但 Moody's 估 2027 年仍逼近 1 兆美元、RPO 約 7,000 億美元撐住近兩年"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":37.97,"peg_fy2":0.54,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2026A":3.07,"FY2027E":4.22,"FY2028E":7.25,"FY2029E":12.18},"fy_end_month":1,"eps_basis":"基期 FY2026A 為 GAAP 稀釋 EPS 3.07 美元（含出售車用乙太網路事業一次性利益，事實表未提供非 GAAP 基期）；FY2027E–FY2029E 為 Koyfin 共識（2026-10-08 快照，口徑判斷為非 GAAP），兩者口徑不同，三年年複合僅作參考；財年止於 1 月"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q3 FY27 財報與 Q4 指引","impact":"高","watch":"資料中心季增是否 ≥20%、非 GAAP 毛利率是否落在 57.5–58.5%"},{"date":"2027-02","date_precision":"month","type":"macro","event":"四大雲端 2027 年度資本支出指引（各家第四季財報）","impact":"高","watch":"合計年增率是否仍為正、是否 ≥15%"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q4 FY27 財報與 FY28 全年展望","impact":"高","watch":"非 GAAP 營益率是否進入 38–40%、FY28 約 200 億美元是否重申"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"Photonic Fabric 記憶體模組送樣、UALink U115 交換器推出（管理層稱明年）","impact":"中","watch":"scale-up 光學與交換器是否如期貢獻數億美元營收"},{"date":null,"date_precision":null,"type":"regulatory","event":"Section 232 半導體關稅第二階段範圍","impact":"中","watch":"是否涵蓋 Marvell 主要產品、毛利率指引是否因此下修"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
