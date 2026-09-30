你是 DD 管線 v20 的判斷層閘（gate），標的 NTAP（20260930）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

④ priced-in——共識與賣方目標價 vs 現價，裁決是否只是把市場已知的事再說一次。看 `decision_inputs.market_wrong_reason_given` 是否有具體內容（非空泛套話），對照 facts.json 的 `latest_quarter_kpis[].vs_consensus` 與 `valuation_current`。[gate_contract §④]

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝2025 USD million｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.netapp.com Q1 FY27 press release；YoY/QoQ 見 prepared remarks (s21.q4cdn.com)（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
  - 註記：查無可靠共識數字；公司稱超越所有指引區間高端
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝31.9 %｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.netapp.com Q1 FY27 press release（營業利益 $645M）（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
  - 註記：超越指引高端（共識數字查無）
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝23.9 %｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.netapp.com Q1 FY27 press release（GAAP 營業利益 $484M）（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi7_remaining_performance_ob`（q1_business）｜Remaining Performance Obligations (RPO)＝5650 USD million｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 prepared remarks (s21.q4cdn.com Q1 FY27)；遞延收入 $4.85B（+7% YoY）（numbers.latest_quarter_kpis.items[7]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi8_billings`（q1_business）｜Billings＝2057 USD million｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27 press release（numbers.latest_quarter_kpis.items[8]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi9_product_revenue_all_flas`（q1_business）｜Product revenue / All-flash array revenue＝987 USD million（AFA $1,309M，+47% YoY）｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 prepared remarks 與新聞稿 Q1 FY27（numbers.latest_quarter_kpis.items[9]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi10_product_gross_margin_non`（q1_business）｜Product gross margin (non-GAAP)＝54.6 %｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 prepared remarks Q1 FY27（整體 non-GAAP 毛利率 70.6%）（numbers.latest_quarter_kpis.items[10]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi5_guidance_q2_fy27`（q1_business）｜Guidance: Q2 FY27＝營收 $2.025–2.175B；non-GAAP EPS $2.54–2.64；non-GAAP 營業利益率 30.9–31.9%；non-GAAP 毛利率 67.0–68.0% range｜期間與口徑：Q1 FY2027（公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Q1 FY27 press release（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（公告於 2026-09-02））
- `f_kpi6_guidance_fy27`（q1_business）｜Guidance: FY27 全年＝營收 $7.975–8.225B；non-GAAP EPS $9.73–10.03（本次上調） range｜期間與口徑：Q1 FY2027（公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Q1 FY27 press release；上調表述見 prepared remarks（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027（公告於 2026-09-02））
- `f_peer_ntap_gross_margin_pct`（q2_moat）｜NTAP 毛利率＝70.63 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NTAP.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_ntap_operating_margin_pct`（q2_moat）｜NTAP 營業利益率＝26.03 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NTAP.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_ntap_fcf_margin_pct`（q2_moat）｜NTAP FCF 利潤率＝22.32 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NTAP.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_sndk_operating_margin_pct`（q2_moat）｜SNDK 營業利益率＝61.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_000660_ks_operating_margin_pct`（q2_moat）｜000660.KS 營業利益率＝68.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_operating_margin_pct`（q2_moat）｜005930.KS 營業利益率＝36.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.01 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-26）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝11.12 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-26）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝12.36 USD/share｜期間與口徑：2026-09-26／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-26）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝12.47 %｜期間與口徑：2026-06-23 → 2026-09-26／FY1 共識 EPS 8.9 → 10.01（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260926.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-26）
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝401 USD million｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.netapp.com Q1 FY27 press release（營運現金流 $503M，capex $102M）（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占營收 / 占 GAAP 營業利益＝4.8 % of revenue（SBC $98M；約占 GAAP 營業利益 20.2%）｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q1 FY27 press release（SBC $98M）；比率由本 agent 換算（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_kpi11_inventory_turns`（q1_business）｜Inventory turns＝6 x｜期間與口徑：Q1 FY2027（季末 2026-07-31，公告於 2026-09-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 prepared remarks Q1 FY27（numbers.latest_quarter_kpis.items[11]，as_of Q1 FY2027（季末 2026-07-31，公告於 2026-09-02））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.994 %｜期間與口徑：2026-09-30／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-09-30）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝209.18 USD｜期間與口徑：2026-09-29（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-29（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.9 x｜期間與口徑：2026-09-26／分母＝FY1 EPS 10.01，分子＝快照價 209.18｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-26）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝28.89 x｜期間與口徑：2026-09-29（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-29（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-09-29（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-29（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.56 x｜期間與口徑：2026-09-29（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-29（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-29（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-29（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.42 x｜期間與口徑：2026-09-29（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-29（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-29（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-29（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝105.97 %｜期間與口徑：2026-09-29（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-29（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-09-30／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-30）
  - 原文：「price 209.18 / W52 134.02 / W104 120.45 / W250 95.87 / W250 13週斜率 2.08%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝134.02 USD｜期間與口徑：2026-09-30／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-30）
- `f_ma_w104`（q5_valuation）｜104 週均線＝120.45 USD｜期間與口徑：2026-09-30／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-30）
- `f_ma_w250`（q5_valuation）｜250 週均線＝95.87 USD｜期間與口徑：2026-09-30／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-30）

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：NetApp 財報風險揭露：對手含既有公開公司、專注快閃的新公開公司，以及鎖定 AI 商機的新進入者
  - 來源：NetApp Form ARS FY2026 / 8-K (SEC)（as_of 2026-07-15）｜affects：decision_inputs.bear、thesis.R
- `competitive_share_entrants#5`（competitive_share_entrants｜方向 -｜狀態 ok）：搜尋摘要稱：受供給限制的超大規模雲業者更願意認證新供應商，可能替新進入者打開取代缺口（摘要為搜尋工具轉述，未讀原頁）
  - 來源：search summary on NetApp Q3 FY2026 (Futurum / Forbes results)（as_of 2026-02-28）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：NetApp FY2026 10-K：兩家經銷商客戶合計約占營收 43%（搜尋摘要未指名、未拆個別比重；明細在 10-K Note 14）
  - 來源：NetApp, Inc. Form 10-K FY2026 (SEC EDGAR)（as_of 2026-04-24）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：StorageSwiss (2026-05-06) 標題主張記憶體與快閃價格到 2027 都不會回落；搜尋摘要稱這是結構性重新配置，而非暫時性缺貨。
  - 來源：StorageSwiss: Memory and Flash Prices Are Not Coming Down (Through 2027)（as_of 2026-05-06）｜affects：thesis.R、decision_inputs.bear、valuation
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Micron 新加坡 NAND 廠預計 2028 下半年才開始出貨；搜尋摘要稱有意義的新產能要到 2027 或 2028 才會出現，2026 年吃緊不受影響。
  - 來源：搜尋結果彙整 (NAND supply discipline new capacity timeline 2026)；相關來源含 NAND Research、Kioxia via IBS Electronics（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：NetApp FY2026 10-K 風險揭露：自進口來源國採購／製造的產品，若貿易限制、關稅或稅負變動，可能對業務與財務結果造成重大不利影響；美國關稅政策仍在變動，另有中美緊張與台海風險可能影響關鍵零組件取得。
  - 來源：NetApp, Inc. Form 10-K FY2026 (period ended 2026-04-24), SEC EDGAR（as_of 2026-04-24）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：產業層：IEEPA 關稅遭最高法院否決後，10% 全球關稅於 2026-07-24 到期，改為對 80 國課 10–12.5% 的 Section 301 關稅；IT 硬體成本 2026 年上升 15–30%。此為一般產業資料，非 NetApp 專屬。
  - 來源：WebSearch 摘要（growrk.com 等）：data storage hardware tariff exposure supply chain 2026（as_of 2026-07-24）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：NetApp 10-K 揭露：不直接控制製造環節，製造夥伴與供應商地理分散，地緣衝突等可能中斷供應鏈
  - 來源：NetApp Form 10-K FY2026 (SEC)（as_of 2026-04-24）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：NetApp 10-K 揭露：中台緊張升級可能影響其或代工廠取得關鍵供應鏈零組件的能力
  - 來源：NetApp Form 10-K FY2026 (SEC)（as_of 2026-04-24）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：NAND/DRAM 生產集中於三家廠商，產能轉向 HBM/企業級，下游議價空間有限；企業級 SSD 2026 合約價預估大漲，短缺可能延續至 2027–2028
  - 來源：NAND Research: Memory & Flash Crisis March 2026 Update / Avnet / Microchip USA（搜尋彙整）（as_of 2026-03-01）｜affects：decision_inputs.bear、valuation
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Dell 在 2025 年第二季重奪 AFA 市佔第一（NetApp 曾於 2025 年第一季居首）。
  - 來源：Blocks and Files: Dell reclaims top spot in all-flash array market（as_of 2025-09-21）｜affects：moat_trend、decision_inputs.bear
- `end_markets#7`（end_markets｜方向 -｜狀態 ok）：AWS 於 2026 年 4 月為 S3 加入檔案存取，Blocks and Files 稱其對標 NetApp 與 Qumulo。
  - 來源：Blocks and Files: AWS adds file access to S3, taking on NetApp and Qumulo（as_of 2026-04-07）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：NetApp FY2026 10-K risk factors: competes with established public companies, newer flash-focused public companies and new entrants targeting the AI opportunity; markets have rapidly changing technology; AI technologies evolving with significant competition.
  - 來源：NetApp Form 10-K FY2026 (period ended 2026-04-24), SEC（as_of 2026-04-24）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：NetApp risk factor: business may be harmed if it cannot keep pace with rapid technological change or manage the transition from older products to new ones (10-K language surfaced in search; the exact filing year of the surfaced text is not confirmed).
  - 來源：SEC NetApp filings via search (10-K/10-Q)（as_of 2026-04-24）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 12 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":358.6,"bear_5y_price":122.2,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":9.7,"ev5y_pct":6.7,"irr_base_pct":1.9,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.01,"pe":20.9,"basis":"FY1（FY2027E，2027-04 年度結束）共識 non-GAAP 稀釋 EPS；終端倍數套在 FY2031E 同口徑 EPS"},"eps":{"bull":[10.3,11.6,13.0,14.6,16.3],"base":[10.0,10.8,11.7,12.6,13.5],"bear":[9.7,8.6,8.8,9.1,9.4]},"pe":{"bull":22,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.994,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NTAP_Q4_2026_Earnings_Call_20260528.md
- 2026-05-28｜CFO｜guidance：FY27 毛利率財測區間 68.5%–69.5%（FY27 營收財測 $7.325B–$7.575B、中點 $7.45B）（原話："expect gross margin to be in the range of 68.5% to 69.5%"）
- 2026-05-28｜CFO｜guidance：FY27 營收中點對應年增 8%，前一年為 5%（原話："this implies 8% year-over-year growth"）
- 2026-05-28｜CFO｜guidance：FY27 營業利益率財測 29.1%–30.1%（原話："operating margin to be in the range of 29.1% to 30.1%"）
- 2026-05-28｜CFO｜guidance：FY27 EPS 財測 $8.70–$9（原話："We expect EPS to be in the range of $8.70 to $9."）
- 2026-05-28｜CFO｜guidance：Q1 營收財測 $1.75B–$1.9B（含額外一週）（原話："We expect revenue to be in the range of $1.75 billion"）
- 2026-05-28｜CFO｜guidance：Q1 含額外一週，約貢獻 $65M 營收（原話："Q1 includes an extra week, which is expected to contribute"）
- 2026-05-28｜CFO｜guidance：FY27 指引納入可能出現加速採購的需求（原話："we recognize the potential for pockets of"）
- 2026-05-28｜CFO｜guidance：上下半年季節性：扣除 Q1 額外一週後類似（原話："roughly similar type of seasonality first half, second half"）
- 2026-05-28｜CFO｜guidance：Q2–Q4 相較 FY26 同期為中個位數成長（原話："it gets you still in the sort of mid-single-digit"）
- 2026-05-28｜CFO｜commitment：FY27 打算把最高 100% 自由現金流還給股東（原話："intend to return up to 100% of free cash flow"）
- 2026-05-28｜CFO｜commitment：FY27 股數預計年減低個位數百分比（原話："expect to reduce share count by low-single-digit percentage"）
- 2026-05-28｜CFO｜capital_allocation：宣布回購額度增加 $10 億（原話："announcing an increase in that authorization by $1 billion"）
- 2026-05-28｜CEO｜capital_allocation：M&A：持續評估，不排除也不排除不做（原話："we won't rule anything in"）
- 2026-05-28｜CFO｜margin：產品毛利率 7 月季為底部，之後逐步改善（原話："For us, July quarter is more or less the trough."）
- 2026-05-28｜CFO｜margin：靠調價回應零組件成本上升，效果逐步顯現（原話："price adjustments as we see component costs increase"）
- 2026-05-28｜CFO｜margin：產品毛利率長期目標未調整（mid-50s 到 high-50s）（原話："we're not really moving from our long-term goal or target"）
- 2026-05-28｜CFO｜margin：Public Cloud 毛利率長期目標區間 80–85%，近兩季高於區間上緣（原話："operated within the 80% to 85% long-term target range"）
- 2026-05-28｜CFO｜margin：Public Cloud 成長較快被描述為毛利率順風（原話："it does give us a bit of a nice tailwind to the margin line"）
- 2026-05-28｜CFO｜margin：NAND 價格主要反映在產品毛利率（原話："NAND prices would manifest themselves in"）
- 2026-05-28｜CFO｜margin：Q4 產品毛利率 56.1%，季增 80bp（原話："Product gross margin was 56.1%, up 80 basis points"）
- 2026-05-28｜CFO｜margin：Google 協議抵銷較高零組件成本（原話："offsetting higher component costs."）
- 2026-05-28｜CFO｜margin：管理層也以毛利額年增作為目標（原話："we look at gross profit growth year-over-year as well"）
- 2026-05-28｜CEO｜margin：FY26 營業利益率達 30% 目標（原話："Achieving our full year target of a 30% operating margin"）
- 2026-05-28｜CEO｜risk：坦承可能有部分拉貨（原話："there are probably some amounts of pull forward"）
- 2026-05-28｜CEO｜risk：稱 Q4 損益表上拉貨影響極小，另有看到決策加速（原話："We have seen some accelerated decision-making"）
- 2026-05-28｜CEO｜risk：稱財測已納入拉貨風險（原話："the risks of pull-ins and the dynamics it creates"）
- 2026-05-28｜CEO｜risk：稱可取得足夠供給達成全年展望（原話："can source adequate supply to meet our outlook for the year"）
- 2026-05-28｜CEO｜risk：記憶體與零組件成本上升，以調價平衡成長與毛利（原話："We're managing rising memory and component costs"）
- 2026-05-28｜CEO｜risk：客戶以美元編預算、價格彈性小（原話："customers budget in dollars"）
- 2026-05-28｜CFO｜risk：存貨增加、週轉降至 12（原話："Inventories expanded both year-over-year and quarter-over"）
- 2026-05-28｜CFO｜risk：Q4 支援營收年增部分來自一次性項目（原話："partly driven by a onetime item"）
- 2026-05-28｜CFO｜customer：Q4 大型交易兌現，先前已預告（原話："we mentioned the potential for large deals to materialize"）
- 2026-05-28｜CEO｜customer：Q4 約 500 筆 AI 與資料準備訂單（原話："We had approximately 500 AI and data preparation wins"）
- 2026-05-28｜CEO｜customer：500 筆 AI 訂單全為地端（原話："All of the 500 AI wins are on-prem wins"）
- 2026-05-28｜CEO｜customer：AI 用例分布約 50/25/25（原話："So it's roughly 50%, 25%, 25%, roughly speaking."）
- 2026-05-28｜CEO｜customer：Google Distributed Cloud 協議，NetApp 為資料基礎設施大宗（原話："NetApp was chosen by Google to be a"）
- 2026-05-28｜CEO｜customer：大型 neo cloud 客戶為美國前五（原話："meaning top 5, U.S. neo cloud"）
- 2026-05-28｜CFO｜customer：Unbilled RPO 年增 88%（原話："$807 million, up 88% year-over-year"）
- 2026-05-28｜CEO｜product：Keystone 營收較 FY25 成長約 65%（原話："grew approximately 65% from FY '25"）
- 2026-05-28｜CEO｜product：第一方與 marketplace 雲端服務 FY26 成長 30%（原話："which increased 30% in FY '26"）
- 2026-05-28｜CEO｜product：AFX 為新架構，需要時間（原話："It's a new architecture"）
- 2026-05-28｜CEO｜product：AIDE 可單獨以軟體訂閱變現（原話："monetize that as either stand-alone software"）
- 2026-05-28｜CEO｜product：全快閃占裝機基礎升至 48%（原話："it picked up another 1% to 48% of the installed"）
- 2026-05-28｜CEO｜competition：歐洲航太客戶綠地案取代競爭對手（原話："chose NetApp displacing competitors in a greenfield win"）
- 2026-05-28｜CEO｜competition：調價尚未明顯反映在交易，預期未來一到兩季傳導（原話："We raised prices during the quarter"）
- 2026-05-28｜CEO｜competition：已收緊客戶合約，調價傳導預期一到兩季（原話："We have tightened up our agreements with customers"）
- 2026-05-28｜CEO｜customer：部分客戶可能因通膨環境選擇 Keystone（原話："customers who bought Keystone because they felt that it"）
- 2026-05-28｜CEO｜guidance：預期雲端明年成長快於今年（原話："which should cause cloud to grow faster next"）
- 2026-05-28｜CEO｜commitment：增加銷售資源以支撐展望，如去年（原話："some additional sales resources just like we did last year"）

### NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜CFO｜guidance：CFO 說 FY27 全年財測已上調（原話："we basically increased the guidance for fiscal year '27"）
- 2026-09-08｜CFO｜guidance：CFO 說下半年財測也比 90 天前高（原話："the guidance for the second half also is higher"）
- 2026-09-08｜CFO｜guidance：CFO 拆解上下半年營收中點約五五對分（Q1 含多一週）（原話："roughly the revenue is split almost 50-50"）
- 2026-09-08｜CFO｜guidance：被問財測高低端風險，CFO 表示等本季結束再更新（原話："we'll wait until the end of this quarter"）
- 2026-09-08｜CFO｜guidance：CFO 說營運利益率財測中點上調約 120 個基點（原話："increased the operating margin guidance at the midpoint"）
- 2026-09-08｜CFO｜risk：CFO 說分銷通路沒有塞貨的動態（原話："there is no stocking the channel for this type of dynamics"）
- 2026-09-08｜CFO｜customer：CFO 說 Q1 需求跨區域、客戶類型與產業皆成長（原話："we experienced broad-based demand"）
- 2026-09-08｜CFO｜risk：被問供給，CFO 表示對交付財測的供給有把握（部分 LTA、部分承諾）（原話："we feel comfortable about the supply we have"）
- 2026-09-08｜CFO｜margin：CFO 說漲價因素屬通膨環境下正常現象，並把成長歸因於 AI 與基礎設施現代化（原話："pretty normal and understandable and inflationary environment"）
- 2026-09-08｜CFO｜margin：CFO 說 Q2–Q4 產品毛利率預期比 90 天前略好（原話："slightly better product gross margin than we had expected"）
- 2026-09-08｜CFO｜margin：CFO 說全年毛利率財測略低，原因是產品營收占比較高（原話："that's solely driven by the richer product revenue mix"）
- 2026-09-08｜CFO｜margin：被問零組件通膨何時緩和，CFO 說現在下判斷太早（原話："too early to sort of make a call on the component pricing"）
- 2026-09-08｜CFO｜margin：CFO 說零組件成本漲價已轉嫁數季（原話："pass through the component cost inflation"）
- 2026-09-08｜CFO｜margin：CFO 說全快閃與混合快閃的毛利差異不大（原話："we don't have much of a differential on the margin side"）
- 2026-09-08｜VP IR｜margin：IR 提醒不要假設歷來各產品類別的相對毛利在現況下仍成立（原話："I wouldn't necessarily assume that the historical"）
- 2026-09-08｜CFO｜product：CFO 說 AI 案件平均規模變大，從概念驗證走向量產部署（原話："the average size of the deal is now bigger than before"）
- 2026-09-08｜CFO｜product：CFO 說 Q1 全快閃陣列營收年增 47%（原話："the all-flash array business grew by 47%"）
- 2026-09-08｜CFO｜product：CFO 說混合快閃營收連兩季小幅年增，前面是多季下滑（原話："a small uptick in the hybrid flash revenue year-on-year"）
- 2026-09-08｜CFO｜product：CFO 說 CPU 伺服器部署後需要儲存，但規模現在難判斷（原話："It's a bit too early to tell the magnitude"）
- 2026-09-08｜CFO｜product：被問 AI 占營收比重，CFO 說未來 AI 與非 AI 界線會模糊（原話："the line between AI and non-AI could become blurry"）
- 2026-09-08｜CFO｜product：被問儲存 TAM 未來兩三年規模，CFO 說現在判斷太早（原話："it is too early for us to tell where this could be"）
- 2026-09-08｜CFO｜competition：被問 AFX 與 Vast／WEKA 等的差異，CFO 說有客戶處於 AFX 認證階段（原話："some customers that are in certification phase on AFX"）
- 2026-09-08｜CFO｜competition：CFO 稱統一平台是差異化關鍵（原話："which is really the key differentiator for us"）
- 2026-09-08｜CFO｜product：CFO 說公有雲 Q1 剔除多出一週後約成長 19%（原話："for the extra week that we had in Q1, it was around 19%"）
- 2026-09-08｜CFO｜commitment：CFO 說公有雲高個位數以上（high-teens）成長率可持續（原話："the high teens growth rates are sustainable"）
- 2026-09-08｜CFO｜customer：CFO 說對公有雲內 AI 工作負載的能見度有限，因為是客戶的客戶（原話："the visibility isn't as great"）
- 2026-09-08｜CFO｜margin：CFO 說公有雲長期毛利率區間為 80–85%（原話："The long-term range for us is 80% to 85%"）
- 2026-09-08｜CFO｜commitment：CFO 說公有雲毛利率區間暫不調整，但承認有上行偏向（原話："We think there's potentially some upward bias"）
- 2026-09-08｜CFO｜margin：CFO 說 Keystone 對整體毛利與營業利益率有正貢獻（原話："It's accretive to our overall gross margin"）
- 2026-09-08｜CFO｜commitment：CFO 說費用成長不超過營收成長的一半，並稱 FY27 財測仍在此框架內（原話："not to have OpEx grow faster than half of the growth rate"）
- 2026-09-08｜CFO｜capital_allocation：CFO 說資本配置不變，最高將 100% 自由現金流還給股東（原話："return up to 100% of our free cash flow to our shareholders"）
- 2026-09-08｜CFO｜capital_allocation：CFO 說 DataPelago 與 JetStream 是小型技術補強併購（原話："both of these are small tuck-ins"）
- 2026-09-08｜CFO｜customer：被問客戶如何調整預算，CFO 說客戶依業務優先順序編預算（原話："customers budget based on their business priorities"）

### NTAP_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜George Kurian｜guidance：CEO 描述新財年開局強勁，並稱各產品線、地區皆優於計畫（原話："It was a super strong start to the quarter, to the year."）
- 2026-09-08｜George Kurian｜product：全快閃陣列營收創紀錄、年增 47%（原話："All-flash array revenue was a record, up 47% year-on-year."）
- 2026-09-08｜George Kurian｜guidance：全年產品毛利率展望每季都比年初給的數字逐步上修（原話："product gross margins, it's incrementally up every quarter"）
- 2026-09-08｜George Kurian｜margin：產品毛利率靠提價轉嫁成本，管理層承認無法一對一完全轉嫁（原話："we can't match them always one for one"）
- 2026-09-08｜George Kurian｜margin：公司整體毛利率受產品與服務組合影響，產品成長遠快於服務（原話："product is growing much faster than service"）
- 2026-09-08｜George Kurian｜margin：產品毛利率比 90 天前的預期更好（原話："better than we thought 90 days ago"）
- 2026-09-08｜George Kurian｜margin：AI 專屬配置與一般企業業務的毛利率結構無實質差異（原話："the margin profile, there's no material difference"）
- 2026-09-08｜George Kurian｜risk：被問到 NAND／硬碟供給與定價，管理層表示存貨增加是為了備足供給，並提到現貨與長約並用（原話："inventory was up because we want to make sure"）
- 2026-09-08｜George Kurian｜risk：向供應商採購方式包含公開市場與長期合約（原話："buying in the open market as well as through long-term"）
- 2026-09-08｜George Kurian｜product：快閃成本升高下，磁碟式系統已開始出現成長（原話："our disk-based systems have started to show growth"）
- 2026-09-08｜George Kurian｜risk：管理層給出快閃與磁碟的成本倍數（原話："as the cost of flash becomes 15 to 20x the cost of disk"）
- 2026-09-08｜George Kurian｜product：Keystone（儲存即服務）Q1 表現高於內部目標（原話："were above our internal targets"）
- 2026-09-08｜George Kurian｜commitment：預告在 INSIGHT 大會發布針對高階 neocloud 訓練場景的新進展（原話："We are going to be announcing even more advancements"）
- 2026-09-08｜George Kurian｜customer：AFX 平台客戶需經認證流程（原話："They go through a certification process"）
- 2026-09-08｜George Kurian｜competition：對 neocloud 的銷售模式是夥伴多於供應商（原話："we are more partner than vendor"）
- 2026-09-08｜George Kurian｜customer：主權雲端：法國前八大雲端業者中六家以 NetApp 為基礎設施（原話："6 of the 8 largest cloud providers in France have NetApp"）
- 2026-09-08｜George Kurian｜competition：面對全堆疊綑綁廠商，管理層稱與六個月前相比無根本改變（原話："No fundamental changes from 6 months ago."）
- 2026-09-08｜George Kurian｜competition：管理層點名 NetApp、Pure、Dell 為持平或增加份額的專注型廠商（原話："it's probably us, Pure and Dell"）
- 2026-09-08｜George Kurian｜customer：美國公部門採購干擾已緩解（原話："the disruption from a procurement side has mitigated"）
- 2026-09-08｜George Kurian｜competition：公部門市場管理層稱是與 Dell 的兩強競爭（原話："it's a 2-horse race between us and Dell"）
- 2026-09-08｜George Kurian｜product：公有雲長期以來維持高十位數到低二十位數成長（原話："public cloud has grown in the high teens, low 20s"）
- 2026-09-08｜George Kurian｜commitment：CEO 表示正在向銷售團隊施壓要求雲端更快成長（原話："I'm pushing for faster growth."）
- 2026-09-08｜George Kurian｜customer：舉例：剛把一家大型競爭對手客戶的 AI 資料湖搬上公有雲（原話："moved a large competitive customer to the public cloud"）
- 2026-09-08｜George Kurian｜customer：銷售模式：不直接賣給超大型雲端業者，而是透過它們賣給企業（原話："We sell through them to the enterprise."）
- 2026-09-08｜George Kurian｜product：對儲存而言推論的重要性遠大於訓練（原話："inference is the much bigger part of the overall business"）
- 2026-09-08｜George Kurian｜risk：面對元件漲價，基礎設施升級需求高於正常型態（原話："We are seeing infrastructure upgrades way above normal"）
- 2026-09-08｜George Kurian｜customer：新use case 需求同樣高於正常型態（原話："We are seeing new use cases also way above normal pattern"）
- 2026-09-08｜George Kurian｜capital_allocation：內部 AI 專案由約 400 件收斂，其中 13 件已在損益表貢獻正報酬（原話："that are contributing to positive returns in the P&L"）

### 問答異常語氣（迴避／改口／保留）
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Fox：NAND 漲價推升的營收占比｜答法：CFO 表示 too early，不願量化；CEO 稱這是特殊領域，難以精確告知
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Sankar／Chokshi：AI 相關占產品營收或訂單比重｜答法：CFO 兩次表示不拆分，只給筆數；被問每筆金額是否上升，回答範圍很廣、不願推測
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Mohan：為何 Q4 沒看到拉貨、後續調價節奏｜答法：重申 Q4 損益表拉貨影響極小，未回答調價節奏；後段又承認可能有部分拉貨
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Woodring：FY27 財測有多少來自已取得的 AI 訂單｜答法：未給占比，改談廣泛動能、裝機基礎與銷售投資
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Sankar：neo cloud 大單是否為唯一供應商｜答法：CEO 表示不評論對方環境，只說對方為美國前五 neo cloud
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Wilhelm：AFX 何時成為較大營收來源｜答法：只說需要時間，未給時程或數字
- NTAP_Q4_2026_Earnings_Call_20260528.md｜問：Singh：AIDE 定價與 ASP 提升幅度｜答法：回答取決於資料量與服務，未給百分比
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：漲價（P×Q）在財測中占多少、持續漲價是否為財測上行空間｜答法：未給任何數字，改談 AI 採用與基礎設施現代化是成長的底層驅動
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：除供給外還有哪些上行因素，以及財測低端的風險｜答法：未回答上行因素或低端風險，只說財測已納入當時所有資訊、等本季結束再更新
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：快閃占比上升對產品毛利率的影響｜答法：確認 Q1 快閃占比較高，但前瞻不拆分；IR 補充不要假設歷來各產品毛利關係仍成立
- NTAP_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：AI 案件未來兩三年可占營收多少｜答法：不給比例，改說 AI 與非 AI 界線會變模糊
- NTAP_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md｜問：FY27 財測有多少 NAND／硬碟已由長約鎖定、多少要以浮動價採購，以及財測內含的元件價格假設｜答法：未給長約占比或價格假設，改談需求可見度、供應商合作與存貨增加

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | found | 1 | 4 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 3 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 4 | 4 |
| end_markets | found | 8 | 4 |
| substitute_technology | found | 4 | 5 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：NetApp antitrust OR monopoly investigation 2026；NetApp regulation OR regulatory scrutiny data storage 2026；NetApp DOJ OR FTC OR EU competition 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"B 觀望偏進場·thesis 完整等估值或時機修復（Q4 5/28 法說催化）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Keystone STaaS 成為主要成長引擎，從目前約 5% 占比擴大至 15%+ 並進入穩定 ~30% YoY 成長","columns":{"2Y 驗證點（2026-28）":"Q4 FY26 ~ Q4 FY28：YoY 從 +65% 收斂至 +35%（穩態前奏）；占營收 ≥ 10%","5Y 驗證點（2028-31）":"FY29-31：穩態 ~30% YoY；占營收 ≥ 18%；ARR sourced floor $1.5B","10Y 驗證點（2031-36）":"FY31-36：穩態 +20% YoY；占營收 ≥ 30%；成熟期","驗證指標":"Keystone billings YoY%，unbilled RPO 季度增長","資料來源":"2Y: §6 / 5Y: §8 A / 10Y: §8 A + §9 趨勢"}},{"id":"H2","text":"All-Flash + AI 引擎建立第二曲線，AFF + AFX 取代傳統 hybrid array 並進入 NVIDIA AI factory standard architecture","columns":{"2Y 驗證點（2026-28）":"FY26 末：All-Flash 占系統安裝基數 ≥ 50%（目前 45%）；NVIDIA DGX SuperPOD 部署數 ≥ 30 個","5Y 驗證點（2028-31）":"FY30：All-Flash 占系統安裝基數 ≥ 70%；AFX disaggregated 在 hyperscaler reference design 中 ≥ 50% 共享","10Y 驗證點（2031-36）":"FY35：傳統 hybrid 業務","驗證指標":"All-Flash 占比，NVIDIA 認證系統部署數，AFX Rev","資料來源":"2Y: §6 / 5Y: §8 A 路線圖 / 10Y: §9 護城河趨勢"}},{"id":"H3","text":"估值重新評價，從「成熟 storage」（Fwd PE 14-15x）→「AI 數據基礎設施 + hybrid cloud 平台」（Fwd PE 18-22x）","columns":{"2Y 驗證點（2026-28）":"FY27：Fwd PE 進入 16-18x（修復至 5Y 均 19.36x 的 85-95%）","5Y 驗證點（2028-31）":"FY30：Fwd PE 進入 20-22x（PSTG 與 NTAP 折溢價收斂）","10Y 驗證點（2031-36）":"—","驗證指標":"Fwd PE 5Y 分位、PEG 比、與 PSTG fwd PE 折溢價","資料來源":"2Y/5Y: §13"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"PSTG 持續搶 hyperscaler 大單（Meta Mar 2026 已得手）；若 AWS/Azure/GCP 中任一將 NTAP 從 first-party 降為 second-party，moat 結構性受損","columns":{"對應假設":"H2","時間尺度":"🔥 中期（2-3 年）","監測指標":"三大雲 first-party status；hyperscaler RPO 占比","警戒閾值":"連 2 季 NetApp first-party Rev YoY"}},{"id":"R2","text":"Public Cloud services GM 結構性壓縮。目前 83%，目標 80-85%；hyperscaler 拆分搶 margin 後可能下行至 70-75%","columns":{"對應假設":"H3 + H2","時間尺度":"⚡ 短期（12 月）","監測指標":"Public Cloud GM","警戒閾值":"連 2 季 GM"}},{"id":"R3","text":"傳統 Hybrid Cloud 業務（佔 90%）成長失速 + 替代品（VAST Data、WEKA、DDN）侵蝕 AI 訓練 reference design","columns":{"對應假設":"H1 + H2","時間尺度":"🐢 長期結構（5+ 年）","監測指標":"Hybrid Cloud Rev YoY；VAST/WEKA/DDN AI training 部署數","警戒閾值":"Hybrid Cloud 連 4 季 YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":119.93,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NTAP","date":"2026-09-30","schema":"v15.2","contract":"v19","company_name":"NetApp, Inc."},"oneliner":"NetApp 生意變好是真的，但 FY27 盈餘墊了多一週、漲價轉嫁和提前採購；股價半年翻倍、遠期 20.9 倍已先反映，等回到 17 倍附近再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NTAP_20260930/scenario.json","answers":{"q1_business":{"verdict":"賺企業資料基礎設施的錢：賣硬體加 ONTAP 軟體當入口，再收 93% 毛利的支援年費與雲端原生服務；這一年營收被零組件漲價與提前採購墊高，利潤池正往上游記憶體廠移。","reasoning":"Q1 FY27（季末 2026-07-31）營收 20.25 億美元，年增 30%，剔除多一週約 26%。non-GAAP 營益率 31.9%，GAAP 23.9%。分部：Hybrid Cloud 18.2 億美元，其中產品 9.87 億（年增 51%）、支援 7.20 億（毛利率 93.2%）、專業服務 1.12 億；Public Cloud 2.06 億美元，毛利率 86.4%。產品占營收 49%，去年同期 42%，所以整體毛利率 70.6% 反而年減 50bp。錢卡在「企業資料放在誰的作業系統上」這一節點：ONTAP 裝機基礎帶來支援年費與雲端原生服務，硬體是入口。兩家經銷商約占營收 43%，屬通路集中，不是最終客戶集中。景氣階段判為擴張期：外接式儲存市場 2026 Q1 年增 22.7%（2025 全年約 4%），高階系統年增逾 60%；但 NetApp 自己的訂單已出現提前採購、零組件漲價轉嫁與存貨翻倍，屬擴張後段。上游 NAND 由三家寡占、產能優先給 HBM，這一輪漲價的利潤多數落在記憶體廠。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi7_remaining_performance_ob","f_kpi8_billings","f_kpi9_product_revenue_all_flas","f_kpi10_product_gross_margin_non","f_kpi5_guidance_q2_fy27","f_kpi6_guidance_fy27"],"verdict_values":{"revenue_quality":"約一半是一次性產品營收（占 49%，受零組件漲價與提前採購推升），其餘為支援年費、專業服務（含 Keystone）與雲端訂閱；RPO 56.5 億美元年增 14%、遞延收入 48.5 億美元年增 7%，重複性底盤長得比產品慢。","unit_econ_note":"產品毛利率 54.6%，季減 150bp（零組件成本上升，部分靠漲價抵銷）；支援 93.2%、雲端 86.4%、專業服務 36.6%。產品占比升高拉低整體毛利率到 70.6%，但毛利額年增 29%。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利儲存平台加支援年費，當期盈餘站在 NAND 漲價與 AI 換機週期上"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：上游 NAND 吃緊預計延續到 2027–2028（StorageSwiss、NAND Research），但 TrendForce 指 2027 年 NAND 供給趨緩；NetApp 營收裡的漲價與提前採購成分會隨上游鬆動回吐，AI 與現代化需求的持久部分尚未證實。","bargaining":{"up":"上游 NAND 三家集中、企業級 SSD 合約價大漲，NetApp 用商品化 SSD、無自有快閃，只能部分轉嫁（CEO：無法一對一抵銷）。","down":"兩家經銷商約占營收 43%，屬通路；最終客戶分散，以美元編預算，漲價後會改買混合快閃或延後低優先專案。","geo":"製造外包，10-K 點名中台緊張可能影響關鍵零組件取得，進口關稅變動可能造成重大不利影響。"},"profit_pool_dir":"利潤池目前往上游記憶體廠移：SNDK、SK hynix 營益率 60% 以上，NetApp 26%；系統廠靠轉嫁守住毛利率，沒有多分到。","tam_table":[{"item":"外接式企業儲存市場（2025）","value":"353 億美元，年增 4.3%（IDC，經 Blocks & Files）；另一聚合來源稱 3.9%"},{"item":"2026 Q1 市場","value":"92 億美元，年增 22.7%，高階系統年增逾 60%（聚合站轉述 IDC）"},{"item":"NetApp 份額","value":"2025 全年 8.1% 排第三；2025 Q3 9.4%；2026 Q1 升至第二；2026 Q2 年增 35.7%，成長第三快"},{"item":"段 CAGR（5 年）","value":"事實表未涵蓋"},{"item":"營業利益池占比 5 年前到現在","value":"事實表未涵蓋；當期上游記憶體廠營益率 60% 以上、NetApp 26%，方向往上游移"}]}}},"q2_moat":{"verdict":"護城河 B 級、方向持平：ONTAP 平台與三大雲第一方服務的轉換成本守住客戶，2026 年份額回升，但這一輪漲價的利潤多半被上游記憶體廠拿走，定價權沒有變強。","reasoning":"機制：ONTAP 統一儲存作業系統加資料管理（快照、異地複寫、網路安全），同一套軟體跑在自家硬體與 AWS、Azure、Google 第一方服務上；換掉要搬資料、重建複寫、重新認證、重訓人員。黏著度讀數：RPO 56.5 億美元年增 14%，支援毛利率 93.2%，FY24–FY26 整體毛利率守在 70.2–70.7%。方向：同業報酬率差距無法比（事實表同業列是 NAND 供應商，Everpure 無資料），改用份額軸。IDC 2025 全年份額 8.1% 排第三，2026 Q1 升到第二，Q2 年增 35.7% 為第三快，份額趨勢仍領先 Everpure。執行力 8 分：份額回升，Q1 每項財測都超過上緣。定價權 6 分：產品毛利率季減 150bp，管理層承認漲價無法一對一抵銷成本；上游記憶體廠營益率 60% 以上，NetApp 26%。合併 7 分，B 級。執行力擴大、定價權持平偏弱，合併判持平。","fact_refs":["f_peer_ntap_gross_margin_pct","f_peer_ntap_operating_margin_pct","f_peer_ntap_fcf_margin_pct","f_peer_sndk_operating_margin_pct","f_peer_000660_ks_operating_margin_pct","f_peer_005930_ks_operating_margin_pct","f_kpi10_product_gross_margin_non","f_kpi7_remaining_performance_ob"],"verdict_values":{"moat":{"mechanism":"ONTAP 統一儲存作業系統加資料管理服務，同一套軟體跑在自家硬體與 AWS、Azure、Google 第一方服務上；轉換成本來自資料搬遷、複寫架構、認證與人員訓練。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：IDC 2026 Q1 升到外接式儲存第二，Q2 年增 35.7% 且份額領先 Everpure。定價權持平偏弱：產品毛利率季減 150bp，漲價無法一對一轉嫁，但整體毛利率三年守在 70–71%。兩者合併為持平。","competitor_notes":[{"name":"SNDK","strategy_note":"上游 NAND 供應商，不是直接對手；營益率 61.6% 對 NetApp 26%，代表這一輪漲價的利潤多半落在上游。"},{"name":"000660.KS","strategy_note":"記憶體龍頭，營益率 68%；產能優先給 HBM，企業級 SSD 吃緊延續，是 NetApp 產品毛利率的成本端。"},{"name":"005930.KS","strategy_note":"記憶體加系統的綜合廠，同時是 NetApp 客戶（Q1 簽下 EDA 與 AI 中心合約），供應商與客戶兩重身分。"},{"name":"PSTG（Everpure）","strategy_note":"專注全快閃的主要對手，2025 Q3 成長快於 NetApp；2026 年 IDC 份額趨勢 NetApp 仍領先。事實表無其財報數字。"},{"name":"Dell","strategy_note":"外接式儲存第一，2025 Q2 重奪全快閃第一；美國公部門是與 NetApp 的兩強競爭。"},{"name":"VAST、WEKA 等 AI 原生儲存","strategy_note":"在 AI 訓練高階場景競爭；NetApp AFX 仍在客戶認證階段，管理層說需要時間。"}],"peer_na_reason":"事實表同業列為 NAND 供應商（SNDK、SK hynix、三星），不是儲存系統同業；Everpure（PSTG）無財報資料。同業報酬率差距無法比，改用 IDC 份額軸。","threats":[{"level":"🟡","text":"AWS 2026-04 為 S3 加入檔案存取，被報導對標 NetApp；雲端合作夥伴自建同類服務，點對點威脅雲端檔案服務的低階工作負載。","p":30,"evidence_refs":["end_markets#7"]},{"level":"🟡","text":"超大型雲業者缺貨時更願意認證新供應商，可能替新進者打開缺口；證據只有搜尋摘要轉述，未讀原頁。","p":30,"evidence_refs":["competitive_share_entrants#5"]},{"level":"🟡","text":"Dell 2025 Q2 重奪全快閃第一；專注快閃的新公司與鎖定 AI 的新進者在高階搶單，技術變化快、新舊產品交替有風險。","p":35,"evidence_refs":["end_markets#3","competitive_share_entrants#4","substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"推定高利益率×高周轉：營益率 24–32%、資本支出約占營收 5%、淨現金；投入資本口徑事實表未涵蓋，無法算數值","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是應用與資料團隊、決策者是基礎設施主管、付款者是 IT 預算，三環都成立；儲存是需要不是想要。但當期水位被急迫性墊高：CEO 說部分大客戶把多季建置擠到一季、同時延後低優先專案；客戶以美元編預算，漲價後會改買混合快閃。急迫性不等於持久性。讀數：下半年隱含年增約 9–10%，AI 案件數由約 500 降到約 350 筆。"},{"item":"決策層級","level":"🟢","text":"替代在工作負載層衡量：換掉 ONTAP 要搬資料、重建異地複寫與備援、重新認證（AFX 客戶需走認證流程）、重訓人員。讀數：RPO 56.5 億美元年增 14%、支援毛利率 93.2%；客戶在漲價時改買 NetApp 自家的混合快閃，而不是換廠商。"},{"item":"價值鏈分配","level":"🟡","text":"這一輪價值往上游移：NAND 三家寡占、產能給 HBM，SNDK 與 SK hynix 營益率 60% 以上，NetApp 26%；NetApp 用商品化 SSD、無自有快閃，只能靠漲價轉嫁，產品毛利率季減 150bp。整體毛利率仍守 70%，靠的是支援與雲端這兩段高毛利、難取代的環節。"},{"item":"社會容忍度","level":"🟢","text":"企業 IT 採購，無監管定價上限、不依賴授權；實際上限是客戶的美元預算，不是社會或政治壓力。關稅屬政策成本，不屬價格容忍問題。"}],"roiic":"事實表未涵蓋（缺投入資本口徑）","reinvest_rate":"低：事實表缺折舊攤銷與三筆併購金額；Q1 資本支出 1.02 億美元約占營收 5%，公司承諾最多把 100% 自由現金流還給股東","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率；再投資率＝（資本支出−折舊攤銷＋營運資金變動＋收購淨額）÷稅後營業利益。事實表缺投入資本、折舊攤銷與併購金額，數值無法算。方向判讀：公司幾乎全數配發自由現金流，再投資率低，內生天花板偏低；共識成長主要靠市場成長、營益率擴張、漲價轉嫁與回購，不是靠新投入的資本。"}}}},"q3_growth":{"verdict":"五年後跑道中等：全快閃占裝機基礎 48%，還有空間，但 AFX、Keystone 這些候選第二曲線還沒長到能單獨撐成長；這一年的高成長大半是漲價、提前採購和 AI 換機，管理層自己給的下半年增速只剩約 9–10%。","reasoning":"成長組成：Q1 產品營收年增 51%，裡面有三塊——AI 與資料湖約 350 筆新單（前季約 500 筆，管理層稱單筆變大但不量化）、全面的基礎設施現代化、零組件漲價轉嫁與部分大客戶提前採購。管理層隱含下半年年增約 9–10%，全年 17%。共識 EPS：FY27 10.01、FY28 11.12、FY29 12.36 美元；以 FY26 non-GAAP 約 8.10 美元為基期，三年年增約 15%；FY27 之後兩年約 11%。內生天花板偏低（見護城河段的再投資推導），缺口可歸因：營益率擴張（Q1 non-GAAP 營益率年增 6.1 個百分點到 31.9%）、每年約 1.5% 淨回購、漲價轉嫁；不屬無法歸因。跑道：全快閃占裝機基礎 48%，每季約升 1 個百分點，落在 35–70% 中段；Keystone、AFX 與雲端服務是候選第二曲線，但 AFX 仍在客戶認證、Keystone 認列在 1.12 億美元的專業服務裡，規模還小，不足以認定為下一條 S 曲線。衰退信號亮一個：毛利率連續年減（產品占比推動）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_guidance_fy27","f_kpi9_product_revenue_all_flas"],"verdict_values":{"growth":{"driver_mix":"量價併進：產品營收年增 51% 含零組件漲價轉嫁與提前採購（價）、AI 與資料湖現代化新單（量）；每股盈餘另有每年約 1.5% 淨回購；三筆併購為小型補強，貢獻可忽略。","runway_years":"約 5–6 年：全快閃占裝機基礎 48%，每季約升 1 個百分點，升到 70% 約需 5–6 年","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段再投資推導：投入資本與折舊資料缺，數值無法算；公司幾乎全數配發自由現金流，內生天花板判定低於共識三年 EPS 年增約 15%（FY26 約 8.10 到 FY29E 12.36）。缺口歸因：營益率擴張、每年約 1.5% 淨回購、零組件漲價轉嫁，可歸因。","segments":[{"item":"Hybrid Cloud 產品","value":"9.87 億美元，年增 51%，產品毛利率 54.6%，占營收 49%（去年 42%）"},{"item":"支援","value":"7.20 億美元，年增 11%（剔除多一週約 4%），毛利率 93.2%"},{"item":"專業服務（含 Keystone）","value":"1.12 億美元，年增 15%，毛利率 36.6%"},{"item":"Public Cloud","value":"2.06 億美元，年增 28%（剔除多一週約 19%），毛利率 86.4%"},{"item":"全快閃陣列（跨產品與服務口徑）","value":"13.09 億美元，年增 47%"}],"decay_signals":[{"item":"毛利率連兩季年減","lit":true,"note":"Q1 毛利率 70.6% 年減 50bp，Q2 財測 67–68%、全年 68.1–69.1% 低於 FY26 70.7%；主因產品占比升高"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"IDC 2026 Q1 升到第二、Q2 年增 35.7% 快於市場"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"漲價後部分客戶改買混合快閃、延後低優先專案，總量仍成長；監測"},{"item":"EPS 成長高於營收成長超過 5 個百分點","lit":false,"note":"FY27 財測 EPS 年增 22%、營收 17%，差 5 個百分點，貼線未亮"},{"item":"自由現金流÷淨利連兩年低於 0.75","lit":false,"note":"FY26 1.46 倍、FY25 1.13 倍"},{"item":"SBC 占營收超過 5% 且逐年上升","lit":false,"note":"Q1 4.8%；逐年趨勢事實表未涵蓋"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"外接式儲存 2026 Q1 年增 22.7%"},{"item":"產業估值倍數近三年系統性下移","lit":false,"note":"NetApp 倍數在四個年度端點中最高"},{"item":"維護性資本支出占自由現金流超過 60%","lit":false,"note":"Q1 資本支出 1.02 億美元、自由現金流 4.01 億美元"},{"item":"停止投資新產能且營收三年內下滑","lit":false,"note":"持續補強併購，營收成長中"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健：自由現金流高於淨利、承諾最多 100% 還給股東、股數年減約 1.5%；三筆 AI 與雲端小併購金額未揭露，報酬還看不出來；現價回購的報酬率已明顯變低。","reasoning":"FY26 自由現金流 18.69 億美元、淨利 12.76 億美元，轉換率 1.46 倍（FY25 1.13 倍）。Q1 FY27 自由現金流 4.01 億美元（營運現金流 5.03 億、資本支出 1.02 億）。Q1 還給股東 3.02 億美元（回購 2.00 億、股息 1.02 億），稀釋股數 2.00 億股、年減 1.5%；5 月加碼回購授權 10 億美元，並承諾最多把 100% 自由現金流還給股東。SBC 占營收 4.8%。淨現金 11 億美元（現金與短投 36 億、總負債 25 億）。存貨季增近一倍、週轉由 12 次降到 6 次，屬策略性備料，佔用營運資金。三筆併購（DataPelago、JetStream、PEAK:AIO）CFO 稱小型補強，金額未揭露。近三年現金去向四分、債務到期結構與回購均價事實表未涵蓋。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_kpi11_inventory_turns","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"三筆小型補強併購（DataPelago 2026-07、JetStream 2026-08、PEAK:AIO 待交割）金額未揭露，CFO 稱 small tuck-ins，無法算已實現報酬"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與十年期殖利率事實表未涵蓋；參考前份判斷時（2026-05）遠期本益比 14–15 倍，盈餘收益率約 6.7–7%；現價 20.9 倍約 4.8%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 4.8%，但回購抵銷後稀釋股數年減 1.5%，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：三筆為小型技術補強，現金去向以回購與股息為主；近三年現金去向細項事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 FY27 約 10 美元 EPS 是新起點、之後每年再長 11% 以上、倍數維持 20 倍左右；我不信這個分母是乾淨的——多一週、漲價轉嫁與提前採購都墊高了它。估值偏貴。","reasoning":"現價 209.18 美元：遠期本益比 20.9 倍（FY1 10.01）、FY2 約 18.8 倍；trailing 本益比 28.9 倍、P/S 5.56 倍、EV/S 5.42 倍，在四個年度端點裡全是最高。前份（2026-05-18，119.93 美元）遠期本益比 14–15 倍、5 年平均約 19.4 倍；前份多頭情境要 FY30 才到的 18–22 倍，四個月就到了。PEG：以 FY26 基期三年年增約 15% 算約 1.4；剔除 FY27 週期跳升、用 FY27 到 FY29 年增 11% 算約 1.9。賣方共識評等持有，平均目標價 190.69–195.79 美元，比現價低 6–9%，最高 225 美元；現價已走在賣方前面，支持觀望。反方最強論點：FY1 共識 3 個月上修 12.5%、Zacks 30 天上修 21.6% 且八升零降，上修期倍數通常撐得住。同業遠期倍數事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"遠期本益比（FY1 共識 non-GAAP EPS）加 PEG；對照自身歷史倍數","peers":{"expanded":false,"reason":"事實表同業列為 NAND 供應商而非儲存系統同業，Everpure（PSTG）無資料；缺同層級同業倍數，無法做同業對照"},"fwd_pe":20.9,"peg":1.4,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"遠期 20.9 倍高於自身 5 年平均約 19.4 倍，且分母 FY27 EPS 含多一週與漲價轉嫁；trailing 本益比、P/S、EV/S 在四個年度端點全在頂端（事實表只有四個年度端點，非五年連續分位）；PEG 1.4–1.9；股價高於賣方平均目標價 6–9%。偏貴，但盈餘仍在上修，不到極貴。","upside_short_pct":-7.6,"upside_mid_pct":9.7,"denominator_disputed":true,"denominator_note":"FY27 EPS 約 10 美元含三個非常態成分：Q1 多一週（約 6,500 萬美元營收）、零組件漲價轉嫁、部分大客戶提前採購（管理層兩度承認、不量化）。以常態化 EPS 計，實際倍數高於 20.9 倍，便宜論證不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯在分母：把漲價與提前採購墊高的一年當成新常態。一旦 2027 年 NAND 鬆動、客戶消化提前買的量，EPS 回落、倍數也回落，兩頭一起打。","reasoning":"管理層 5 月與 9 月兩次承認提前採購，並拒絕量化漲價占營收多少、長約鎖定多少 NAND、AI 占營收多少（前季與本季法說加兩場投資人會議，問答共 12 次迴避）；存貨翻倍、週轉降到 6 次。股價距 52 週均線約 +56%、距 104 週均線約 +74%、距 250 週均線約 +118%，26 週漲 106%，回撤路徑長。訴訟、監管、召回、SEC 調查事實表查無。歷史最大回撤、空方最強數字事實表未涵蓋。價值陷阱風險中等：衰退信號亮一個（毛利率連續年減，產品占比推動）。","fact_refs":["f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi11_inventory_turns"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期墊高的分母"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.01,"pe":20.9,"basis":"FY1（FY2027E，2027-04 年度結束）共識 non-GAAP 稀釋 EPS；終端倍數套在 FY2031E 同口徑 EPS"},"eps":{"bull":[10.3,11.6,13.0,14.6,16.3],"base":[10.0,10.8,11.7,12.6,13.5],"bear":[9.7,8.6,8.8,9.1,9.4]},"pe":{"bull":22,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.99,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-55,"hi":-35,"basis":"股價距 52 週均線 134 美元約 −36%、距 104 週均線 120 美元約 −42%；回到 26 週前起漲點（約 102 美元，由 26 週漲 106% 回推）約 −51%；空頭終點約 −42%。歷史最大回撤事實表未涵蓋。取 −35%～−55%。","trigger_time":null},"basis":{"bull":"AI 資料平台與混合快閃兩線都成：FY28 起營收年增低雙位數、non-GAAP 營益率升到約 33%，市場給 AI 資料基礎設施 22 倍（前份重估區間上緣）。","base":"FY27 落在財測上緣，之後漲價成分淡出、需求回到中高個位數成長，營益率守 30–31%；每年約 1.5% 淨回購已含在每股盈餘路徑內，所以淨回購殖利率填 0 避免重複計算。倍數回到 17 倍，介於過去 14–15 倍與 5 年平均約 19.4 倍之間；同業遠期倍數事實表未涵蓋。","bear":"2027 年 NAND 鬆動加提前採購消化，FY28 營收年減、營益率回到 28% 左右，Dell 與 AI 原生廠在高階搶單；倍數 13 倍。機率 30%：共識超過內生天花板，管理層兩度承認提前採購且拒絕量化，TrendForce 指 2027 年 NAND 供給趨緩。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026-05-28 與 2026-09-02 兩度承認提前採購，9/2 CEO 說部分大客戶把四座資料中心中的兩座提前到今年；存貨季增近一倍、週轉由 12 次降到 6 次；下半年隱含年增約 9–10%；TrendForce 指 2027 年 NAND 供給趨緩。","assumption":"提前採購只占很小比例，AI 與現代化需求撐得住下一年。","consequence":"FY28 營收年減、營益率回到 28% 左右、EPS 回到 8.5–9 美元，倍數回到 13 倍，股價約 110–125 美元；再疊上 Dell 或 AI 原生廠搶單，才會到 −50%。","ruling":"採納為空頭主路徑，機率 30%；與 Single Thing 是同一件事，不另立。","watch":"Q2、Q3 營收年增與產品營收年增、存貨週轉、FY28 首次財測。","evidence_refs":["competitive_share_entrants#4","end_markets#3"],"fact_refs":["f_kpi11_inventory_turns","f_kpi6_guidance_fy27"]},{"view":"論點成功但股東經濟變差","evidence":"NAND 三家寡占、產能轉向 HBM，企業級 SSD 合約價大漲、短缺可能延續到 2027–2028；IT 硬體成本 2026 年上升 15–30%（產業層）；上游 SNDK、SK hynix 營益率 60% 以上對 NetApp 26%；Q1 產品毛利率季減 150bp，CEO 承認無法一對一轉嫁。","assumption":"需求持久時，漲價轉嫁得掉，產品毛利率守在 50% 中段。","consequence":"營收照長，但產品毛利率跌到 50% 以下，營益率卡在 28–29%，每股盈餘成長低於營收成長。","ruling":"部分反駁：目前整體毛利率下滑主要來自產品占比（CFO 稱全年毛利率下修 solely driven by 產品組合），產品毛利率本身比 90 天前預期好；但價值鏈利潤往上游移是事實，列監測。","watch":"產品毛利率連兩季低於 52% 即減碼。","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#3","reg_tariff_export#2"],"fact_refs":["f_kpi10_product_gross_margin_non","f_peer_sndk_operating_margin_pct","f_peer_000660_ks_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"26 週漲 106%；遠期本益比 20.9 倍，高於自身 5 年平均約 19.4 倍，已達前份多頭情境 FY30 才要到的 18–22 倍；trailing 本益比、P/S、EV/S 在四個年度端點都最高；賣方平均目標價 190.69–195.79 美元，低於現價。","assumption":"FY27 約 10 美元 EPS 是新起點，之後每年再長 11%，倍數維持 20 倍左右。","consequence":"即使 Base 路徑成真，倍數回到 17 倍，5 年年化只剩約 3%（含股息）。","ruling":"採納，這是本次觀望的唯一約束。","watch":"遠期本益比回到 17 倍以下。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_week26_return_pct","f_pe_percentile","f_ps_percentile"]},{"view":"論點失敗","evidence":"財報風險揭露點名專注快閃的新公司與鎖定 AI 的新進者；超大型雲業者缺貨時更願意認證新供應商（搜尋摘要轉述，未讀原頁）；Dell 2025 Q2 重奪全快閃第一；AWS 2026-04 為 S3 加入檔案存取，被報導對標 NetApp；10-K 提到技術變化快、新舊產品交替有風險。","assumption":"ONTAP 平台與三大雲第一方地位讓份額守得住。","consequence":"全快閃成長落後市場、Public Cloud 成長掉到 10% 左右，護城河方向轉弱。","ruling":"目前反駁：2026 Q1 IDC 排名升到第二、Q2 年增 35.7% 為第三快且份額領先 Everpure；Public Cloud 剔除多一週仍年增 19%、毛利率 86.4%。超大型雲認證新供應商一條只有搜尋摘要，證據力弱。列監測，不扣分。","watch":"全快閃年增減 IDC 市場成長、Public Cloud 年增。","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","end_markets#3","end_markets#7","substitute_technology#0","substitute_technology#1"]},{"view":"論點失敗","evidence":"10-K：不直接控制製造，代工與供應商遍布各地；中台緊張可能影響關鍵零組件取得；進口關稅變動可能造成重大不利影響；IEEPA 關稅被否決後改課 10–12.5% Section 301 關稅（產業層）；兩家經銷商約占營收 43%。","assumption":"供給與通路穩定，關稅轉嫁得掉。","consequence":"斷供或關稅吃掉產品毛利率，或單一經銷商出狀況打斷出貨。","ruling":"不做預測，設損益層的吸收失敗判定線：因供給或關稅下修營收財測，或產品毛利率單季因關稅下滑 200bp 以上。2026-09-27 美中同意對 300 億美元商品降關稅，方向略偏正面。經銷商集中屬通路，不是最終客戶集中，信用風險分散。","watch":"財測下修原因、產品毛利率、10-Q 經銷商占比。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2","customer_concentration_credit#0"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 119.93 → 本次 209.18（+74.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=119.93","side_b":"本次 price_at_dd=209.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與評等","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份 2026-05-18：股價 119.93 美元、遠期本益比約 14–15 倍，估值中性，結論觀望偏進場，等 5/28 法說。","side_b":"本次：股價 209.18 美元（+74%），遠期本益比 20.9 倍，估值轉偏貴；同期 FY27 EPS 財測中點由 8.85 上修到 9.88（+12%），股價漲幅遠大於盈餘上修，結論維持觀望。","ruling":"翻面理由：前份觀望後股價漲 74%，錯在低估 5/28 與 9/2 兩次財測上修的幅度，等的是價格修復而不是證據，錯過了盈餘上修加倍數擴張的雙重推升。本次不翻成進場：上修有一大半已被倍數吸收，而上修來源含多一週、漲價轉嫁與提前採購，分母不乾淨。估值由中性轉偏貴純屬價格變動，基本面評等不變。","evidence_level":"事實表數字","settle_metric":"遠期本益比與 FY1 共識","if_then":["若遠期本益比回到 17 倍以下且 FY27 財測未下修，則首倉 2%","若股價續漲而 Q2 財報沒有再上修，則不追"],"evidence_refs":[]},{"axis":"價值陷阱與護城河方向","cause":"新證據","prior_field":["trap","moat_trend"],"side_a":"前份：價值陷阱風險低、護城河方向持平。","side_b":"本次：陷阱風險升為中等，護城河方向仍持平。新證據：Q1 毛利率年減 50bp，Q2 與全年財測續降（產品占比推升）；管理層 5 月與 9 月兩度承認提前採購；存貨週轉由 12 次降到 6 次；產品毛利率季減 150bp、漲價無法一對一轉嫁。護城河一邊是 2026 年 IDC 份額回升到第二，一邊是上游記憶體廠拿走更多利潤，兩相抵銷。","ruling":"陷阱風險上調採納：衰退信號亮一個、分母含週期成分。護城河方向維持持平。","evidence_level":"公司法說＋IDC 轉述","settle_metric":"產品毛利率、營收年增、IDC 份額","if_then":["若產品毛利率連兩季低於 52%，則減碼一半","若 IDC 份額連兩季下滑，則護城河方向改判轉弱"],"evidence_refs":["end_markets#3","supply_demand_durability#0"]},{"axis":"舊版未產出欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct","asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份為舊版格式，這些欄位未填（空值）。","side_b":"本次補上：五年後跑道中等；生意類型判為品質型成長兼具循環成分；景氣位置晚循環；最大回撤 −35%～−55%；情境機率多頭 20%、基本 50%、空頭 30%；多空 5 年價格、報酬不對稱比、基本情境年化報酬與 5 年期望值由程式從情境樹算出；定期定額裁決與角色由程式另判，本次不填。","ruling":"純屬方法變動，舊值不存在，無從比較，以本次為基準。","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件（空值），只寫等估值或時機修復。","side_b":"重新進場（首倉 2%）：遠期本益比回到 17 倍以下（以 FY1 共識 10.01 計約 170 美元）且 FY27 營收財測未下修、最近一季產品毛利率 ≥52%。","ruling":"前份用模糊的等修復觀望；本次點名唯一約束是價格，重新進場條件寫成該約束的否定，並加兩條基本面守門。","evidence_level":"方法","settle_metric":"遠期本益比、FY27 財測、產品毛利率","if_then":["若三條同時成立，則首倉 2%","若價格到了但財測下修，則不進場"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（空值）；舊風險表門檻為 Public Cloud 毛利率連兩季下滑、Hybrid Cloud 連四季年增失速。","side_b":"減碼：產品毛利率連兩季低於 52%；全快閃年增連兩季低於 IDC 市場成長；Public Cloud 年增（剔除多一週）連兩季低於 12%。清倉：FY28 首次財測營收中點低於 FY27 實際。","ruling":"舊門檻未寫具體數字，改成可量化版本；指標與資料來源保留，Public Cloud 毛利率一條因連三季高於長期區間上緣而退休。","evidence_level":"方法","settle_metric":"季報各項門檻","if_then":["若任一減碼門檻觸發，則減碼一半","若清倉門檻觸發，則清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"Single Thing：FY28 首次全年財測（約 2027-06 初）營收中點低於 FY27 實際營收。","ruling":"選這一項，因為它同時打到 EPS 與倍數，是情境樹裡敏感度最大的單一事件。","evidence_level":"方法","settle_metric":"FY28 營收財測中點 vs FY27 實際營收","if_then":["若 FY28 財測中點低於 FY27 實際，則清倉"],"evidence_refs":[]},{"axis":"前份風險門檻處置","cause":"新證據","prior_field":["thesis.R","thesis.H"],"side_a":"前份風險：R2 Public Cloud 毛利率可能由 83% 壓到 70–75%；R1 超大型雲把 NetApp 由第一方降為第二方；R3 Hybrid Cloud 成長失速、VAST／WEKA／DDN 侵蝕 AI 訓練架構。前份假設 H3：遠期本益比由 14–15 倍重估到 18–22 倍。","side_b":"Public Cloud 毛利率 86.4%，連三季高於 80–85% 長期區間上緣，R2 退休；R1、R3 併入本次競爭風險，門檻改為 Public Cloud 年增（剔除多一週）連兩季低於 12% 減碼、全快閃年增連兩季低於 IDC 市場成長減碼；Hybrid Cloud 年增 30%，失速未觸發。H3 已在四個月內達成（20.9 倍），由上行來源改為風險來源。","ruling":"R2 確實不成立才退休，理由是連三季毛利率在長期區間上緣之上；其餘門檻保留指標與資料來源，改成可量化版本。","evidence_level":"公司法說","settle_metric":"Public Cloud 年增與毛利率、全快閃年增","if_then":["若 Public Cloud 毛利率跌回 80% 以下，則 R2 復活"],"evidence_refs":[]},{"axis":"需求性質：結構性還是提前採購加漲價","cause":null,"prior_field":null,"side_a":"管理層（2026-09-02 CEO）：需求跨客戶規模、地區、產業全面走強，底層需求結構性改善；有能力提前採購的只是很小比例的客戶。2026-09-08 Citi 會議 CFO：通路沒有塞貨。","side_b":"同一場 CEO 承認部分大客戶把多季建置擠到一季、漲價帶來收益；2026-05-28 CEO 已說 probably some pull forward；AI 案件數由約 500 筆降到約 350 筆；下半年隱含年增只剩約 9–10%；漲價占營收、長約鎖定比例、AI 占營收三題都拒答。","ruling":"可調和（程度差異）：兩者同時存在，比例不明。管理層的一次性歸因不採信也不否定，標為未證、監測。預先登記證偽條件：FY27 Q3、Q4 營收年增任一季低於 5%，則「提前採購占比很小」的說法視為不成立。","evidence_level":"法說原話，比例無量化","settle_metric":"FY27 Q3、Q4 營收年增","if_then":["若 Q3、Q4 營收年增皆 ≥8%，則需求持久性成立，重新進場條件保留","若任一季低於 5%，則取消重新進場，等 FY28 財測"],"evidence_refs":[]},{"axis":"產品毛利率底部說法前後不一","cause":null,"prior_field":null,"side_a":"2026-05-28 CFO：7 月季（Q1）大致是產品毛利率底部，之後逐步改善；長期目標 50% 中段到高段不變。","side_b":"2026-09-02 CFO：Q1 產品毛利率 54.6% 超預期（有利組合幫忙），Q2 到 Q4 隱含比 90 天前預期的 50% 低段略好，等於後三季低於 Q1；2026-09-08 高盛會議 CEO 承認無法一對一轉嫁。","ruling":"可調和：Q1 是組合帶來的意外高點，不是底部說法被推翻；但原本的逐步改善路徑變成先回落。以 52% 為守門線，連兩季低於它代表轉嫁失靈。","evidence_level":"法說原話","settle_metric":"產品毛利率（單季）","if_then":["若 Q2、Q3 產品毛利率 ≥53%，則轉嫁有效","若連兩季低於 52%，則減碼一半"],"evidence_refs":[]},{"axis":"上游 NAND 供需：2027 年吃緊延續還是趨緩","cause":null,"prior_field":null,"side_a":"StorageSwiss：記憶體與快閃價格到 2027 都不回落；NAND Research：新產能 2027–2028 才出，Micron 新加坡廠 2028 下半年出貨；三家寡占、產能轉向 HBM。","side_b":"TrendForce（2026-07-30）標題：2027 年 DRAM 仍緊、NAND 供給趨緩。","ruling":"可調和（時點差異），2027 上半年合約價出來之前不可裁決。對 NetApp 兩頭都有代價：吃緊延續，產品毛利率受壓；趨緩，營收裡的漲價成分回吐。不論哪邊，FY27 都是條件最有利的一年，所以用 FY27 EPS 當起點的倍數要打折。","evidence_level":"產業研究（部分為標題層級）","settle_metric":"企業級 SSD 合約價、NetApp 產品毛利率與產品營收年增","if_then":["若 2027 上半年合約價轉跌且 NetApp 產品營收年增低於 5%，則空頭機率上調到 40%","若合約價續漲且產品毛利率連兩季低於 52%，則減碼一半"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#3"]},{"axis":"現在買的最強論證 vs 觀望","cause":null,"prior_field":null,"side_a":"現在就買：盈餘上修還在跑（FY1 共識 3 個月上修 12.5%、Zacks 30 天上修 21.6%、八升零降）；IDC 份額回升；下半年財測也比 90 天前高；FY2 本益比約 18.8 倍、PEG 約 1.7，對一家淨現金、自由現金流率 22% 的公司不算離譜；上修期倍數通常撐得住。","side_b":"觀望：分母含多一週、漲價轉嫁與提前採購；Base 路徑倍數回到 17 倍時，5 年年化只剩約 3%；賣方平均目標價低於現價 6–9%；26 週漲 106%。","ruling":"性質：方向相反的裁決題（不是論點矛盾）。選觀望。依據：Base 情境 5 年價格約 230 美元，只比現價高約 10%，報酬要靠機率 20% 的多頭情境。硬數據點：遠期本益比 20.9 倍對自身 5 年平均約 19.4 倍，FY27 EPS 分母含非常態成分。","evidence_level":"事實表數字＋法說","settle_metric":"遠期本益比、Q2 營收與全年財測","if_then":["若遠期本益比 ≤17 倍且財測未下修，則首倉 2%","若 Q2 營收 ≥21.75 億美元且全年財測再上修、FY1 共識升到 10.5 美元以上，則重新進場價位上移到 17 倍乘新共識，仍不追價","反向：若 Q2 營收低於 20.25 億美元或產品毛利率低於 52%，則取消重新進場，等 FY28 財測"],"evidence_refs":[]},{"axis":"產業態勢（競爭／結構／其他）","cause":null,"prior_field":null,"side_a":"結構轉好：外接式企業儲存 2026 Q1 年增 22.7%（2025 全年約 4%）、高階系統年增逾 60%；AI 推動資料基礎設施現代化；NetApp 2026 Q2 年增 35.7%。","side_b":"競爭與其他結構變數：Dell 2025 Q2 重奪全快閃第一、AI 原生新進者與 AWS 自建檔案服務；上游 NAND 寡占拿走利潤；Section 301 關稅與中台風險。","ruling":"雙向拉鋸：需求結構轉好有來源佐證，但持久性未證；競爭尚未造成份額流失（2026 年份額回升）；上游與關稅是成本端壓力。","evidence_level":"IDC 轉述＋10-K","settle_metric":"IDC 份額、產品毛利率","if_then":["若 IDC 份額連兩季下滑，則改判競爭惡化中"],"evidence_refs":["end_markets#3","end_markets#7","reg_tariff_export#2","competitive_share_entrants#4"]}],"triggers":[{"n":1,"text":"Q2 FY27 財報：營收達財測區間且全年財測維持或上修，H1 過第一關","type":"假設驗證","maps_to":"H1","metric":"Q2 FY27 營收、FY27 全年營收財測","threshold":"營收 ≥20.25 億美元且 FY27 財測下緣 ≥79.75 億美元","action":"維持觀望，不追；重新進場價位隨 FY1 共識上移","source_freq":"公司季報，每季","date":"2026-12"},{"n":2,"text":"下半年營收回吐提前採購","type":"風險","maps_to":"R1","metric":"季營收 vs 財測","threshold":"Q2 營收低於 20.25 億美元，或全年財測下修","action":"取消重新進場；持有者減碼一半","source_freq":"公司季報，每季","date":"2026-12"},{"n":3,"text":"產品毛利率連兩季跌破 52%，漲價轉嫁失效","type":"風險","maps_to":"R2","metric":"產品毛利率（non-GAAP，單季）","threshold":"連兩季低於 52%","action":"減碼一半；未持有則取消重新進場","source_freq":"公司季報，每季","date":"2027-03","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#3"]},{"n":4,"text":"Single Thing：FY28 首次財測營收中點低於 FY27 實際","type":"Single Thing","maps_to":"Single Thing","metric":"FY28 營收財測中點 vs FY27 實際營收","threshold":"中點低於 FY27 實際","action":"清倉","source_freq":"Q4 FY27 法說，一次","date":"2027-06"},{"n":5,"text":"估值回到可接受區間且基本面未破，重新進場","type":"估值rearm","maps_to":"H1","metric":"遠期本益比（FY1 共識）","threshold":"≤17 倍（以 FY1 10.01 計約 170 美元）且 FY27 營收財測未下修、最近一季產品毛利率 ≥52%","action":"首倉 2%","source_freq":"每週收盤＋季報","date":null},{"n":6,"text":"首倉後 Q3 營收年增 ≥8%、產品毛利率 ≥53%，需求持久性第二次確認","type":"加碼","maps_to":"H1","metric":"Q3 FY27 營收年增、產品毛利率","threshold":"營收年增 ≥8% 且產品毛利率 ≥53%","action":"加碼到 4%","source_freq":"公司季報","date":"2027-03"},{"n":7,"text":"份額回吐：全快閃成長連兩季落後市場，或雲端成長明顯放慢","type":"減碼","maps_to":"R3","metric":"全快閃營收年增減 IDC 外接式儲存市場成長；Public Cloud 年增（剔除多一週）","threshold":"前者連兩季為負，或後者連兩季低於 12%","action":"減碼一半","source_freq":"公司季報＋IDC 季度追蹤","date":null,"evidence_refs":["end_markets#3","end_markets#7","competitive_share_entrants#5","competitive_share_entrants#4"]},{"n":8,"text":"供給或關稅衝擊吃進損益","type":"風險","maps_to":"R4","metric":"營收財測下修原因、產品毛利率","threshold":"因供給或關稅下修營收財測，或產品毛利率單季因關稅下滑 ≥200bp","action":"減碼一半","source_freq":"公司季報與法說","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"n":9,"text":"Q2 財報後複審","type":"複審日期","maps_to":"H1","metric":"全部門檻","threshold":"Q2 FY27 財報公布後","action":"重跑判斷","source_freq":"一次","date":"2026-12"}],"kill_metrics":[{"metric":"產品毛利率（non-GAAP，單季）","bear_threshold":"連兩季低於 52%","window":"FY27 Q2 起滾動兩季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"FY28 首次全年營收財測中點 vs FY27 實際營收","bear_threshold":"中點低於 FY27 實際（清倉）","window":"約 2027-06 初 Q4 FY27 法說","source":"公司 Q4 FY27 新聞稿與法說","last_status":"unknown"},{"metric":"季營收年增率（剔除多一週）","bear_threshold":"FY27 Q3 或 Q4 低於 +5%","window":"2026-12 至 2027-06","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全快閃營收年增減 IDC 外接式儲存市場成長","bear_threshold":"連兩季為負","window":"滾動兩季","source":"公司季報＋IDC 季度企業儲存追蹤","last_status":"ok"},{"metric":"Public Cloud 營收年增（剔除多一週）","bear_threshold":"連兩季低於 12%","window":"滾動兩季","source":"公司季報新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"遠期本益比回到 17 倍以下（以 FY1 共識 10.01 計約 170 美元）且 FY27 營收財測未下修、最近一季產品毛利率 ≥52%","exec_line":"三條同時成立才建首倉 2%；Q3 FY27 營收年增 ≥8% 且產品毛利率 ≥53% 加到 4%；股價先漲而證據未到則不追；股價跌但門檻未破則分批買回，不停損；FY28 財測營收中點低於 FY27 實際則清倉。","holding_cap":"4%（循環成分與深回撤可能，上限低於一般品質股）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=105.97, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 與資料基礎設施現代化帶來的需求是結構性的，不只是提前採購和漲價：扣掉多一週與漲價成分後，營收仍維持中高個位數以上成長。","2y":"FY27 下半年兩季營收年增皆 ≥8%（管理層隱含約 9–10%）；FY28 首次財測營收中點年增 ≥5%","5y":null,"10y":null,"threshold":"FY27 Q3、Q4 營收年增 ≥8%；FY28 營收財測中點年增 ≥5%","source":"公司季報新聞稿與法說（Q2 約 2026-12 初、Q3 約 2027-03 初、Q4 與 FY28 財測約 2027-06 初）","drift_rule":"兩年期：營收 TTM 較本次 Base 路徑連兩季偏離 ≥5% 為削弱、連三季 ≥10% 為反轉"},{"id":"H2","text":"零組件漲價大致轉嫁得掉：產品毛利率守在 50% 中段，整體 non-GAAP 營益率 ≥30%。","2y":"FY27 各季產品毛利率 ≥52%、全年 non-GAAP 營益率落在 30.3–31.3% 財測內；FY28 non-GAAP 營益率 ≥30%","5y":null,"10y":null,"threshold":"產品毛利率單季 ≥52%；non-GAAP 營益率年度 ≥30%","source":"公司季報新聞稿、CFO 法說毛利率拆解","drift_rule":"兩年期：產品毛利率較 54.6% 起點連兩季偏離 ≥5%（約 2.7 個百分點）為削弱、連三季 ≥10% 為反轉"},{"id":"H3","text":"全快閃與雲端原生服務的份額持續往上：全快閃成長快於市場，Public Cloud 維持高十位數成長，IDC 外接式儲存排名守在前三。","2y":null,"5y":"FY27–FY31 全快閃營收年增高於 IDC 外接式儲存市場成長；Public Cloud 年增（剔除多一週）≥15%；全快閃占裝機基礎由 48% 升到 ≥65%","10y":null,"threshold":"全快閃年增 ≥ IDC 市場成長；Public Cloud 年增 ≥15%；IDC 排名前三","source":"公司季報、IDC 季度企業儲存追蹤（Blocks & Files 轉述）、法說裝機基礎揭露","drift_rule":"五年期：兩項指標連四季偏離門檻 ≥5% 為削弱、連六季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"提前採購與漲價墊高的營收在下半年回吐：Q2 營收低於財測下緣或全年財測下修。","h_ref":"H1","clock":"⚡","threshold":"Q2 FY27 營收低於 20.25 億美元，或 FY27 營收財測下修；連兩季低於財測中點即減碼","evidence_refs":[]},{"id":"R2","text":"上游 NAND 寡占、企業級 SSD 合約價長期偏高，漲價轉嫁跟不上成本，產品毛利率滑到 50% 以下，價值鏈利潤繼續往記憶體廠移。","h_ref":"H2","clock":"🔥","threshold":"產品毛利率連兩季低於 52% 減碼；連四季低於 52% 才大動作","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#3","reg_tariff_export#2"]},{"id":"R3","text":"競爭與替代：Dell 重奪全快閃第一，專注快閃與鎖定 AI 的新進者在高階場景搶單，超大型雲自建檔案服務（AWS S3 加入檔案存取）並在缺貨時認證新供應商。","h_ref":"H3","clock":"🔥","threshold":"全快閃年增連兩季低於 IDC 市場成長，或 Public Cloud 年增（剔除多一週）連兩季低於 12%","evidence_refs":["competitive_share_entrants#4","competitive_share_entrants#5","end_markets#3","end_markets#7","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"地緣與關稅：製造外包、關鍵零組件依賴台灣與亞洲供應鏈；Section 301 關稅與中台緊張可能推高成本或斷供。","h_ref":"H2","clock":"🐢","threshold":"因供給或關稅下修營收財測，或產品毛利率單季因關稅下滑 ≥200bp","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#2"]},{"id":"R5","text":"通路集中：兩家經銷商合計約占營收 43%，任一家信用或合作變動會打斷出貨。","h_ref":"H1","clock":"🐢","threshold":"單一經銷商占比升破 30%，或應收帳款天數年增 ≥15 天（10-K／10-Q）","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"FY28 首次全年財測（預計 2027 年 5 月底至 6 月初的 Q4 FY27 法說）營收中點低於 FY27 實際營收，等於管理層承認這一輪是提前採購加漲價的頂點。","why_fatal":"現價以 FY27 約 10 美元 EPS 當新起點、再年增 11%；若 FY28 營收轉負，EPS 回到 8.5–9 美元，倍數同時由約 21 倍回到 13–15 倍，兩頭一起打，股價可能回到 110–130 美元（約 −40%），是情境樹裡敏感度最大的一項。","if_happens":"持有者清倉；未持有者取消重新進場條件，等 FY28 上半年營收觸底再重跑研究。","how_monitor":"Q2（約 2026-12 初）與 Q3（約 2027-03 初）的產品營收年增與存貨週轉；企業級 SSD 合約價走勢；管理層對提前採購比重的說法是否改口。","probability":"約 25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.8,"peg_fy2":1.7,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":8.1,"FY2027E":10.01,"FY2028E":11.12,"FY2029E":12.36},"fy_end_month":4,"eps_basis":"non-GAAP 稀釋 EPS；FY2026A 8.10 由 Q1 FY27 法說「FY27 中點 9.88 對應年增 22%」反推（事實表未直接收錄 FY26 non-GAAP EPS，GAAP 稀釋 EPS 為 6.35）；共識取 Koyfin 2026-09-26 快照，家數事實表未涵蓋"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"FY27 Q2 財報與財測更新","impact":"高","watch":"營收是否 ≥20.25 億美元、產品毛利率、存貨週轉、全年財測"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY27 Q3 財報，下半年減速的第一季","impact":"高","watch":"營收年增是否 ≥8%、提前採購回吐跡象"},{"date":"2027-06","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與 FY28 首次全年財測","impact":"高","watch":"FY28 營收財測中點是否高於 FY27 實際"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"NAND 合約價方向（TrendForce 指 2027 年 NAND 供給趨緩）","impact":"中","watch":"企業級 SSD 合約價由漲轉平或轉跌"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"PEAK:AIO 收購交割（金額未揭露，需監管核准）","impact":"低","watch":"是否揭露金額與整合進 AFX 的時程"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
