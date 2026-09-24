你是 DD 管線 v20 的判斷層閘（gate），標的 CDNS（20260924）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1584.451 $M（YoY +24.2%，QoQ +7.5%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release；YoY／QoQ 由 Q2 2025 $1,275.441M、Q1 2026 $1,474.22M（H1 $3,058.671M 減 Q2）自算（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：共識 $1.577B（媒體報導，Benzinga／Yahoo 引述，非 IR）；公司自家 Q2 指引 $1.555–1.595B，落在區間內偏上
- `f_kpi1_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝45.5 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release（Q2 2025 為 42.8%）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：公司自家 Q2 指引 44.5–45.5%，落在區間上緣；第三方共識值未取得
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝28.4 %（營業利益 $450.3M）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release／8-K Ex99.1（Q2 2025 為 19.0%、營業利益 $241.8M）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：公司自家 Q2 指引 28.5–29.5%，實際略低於區間下緣 0.1pt；新聞稿調節表列併購／整合成本占營收 2.1%；第三方共識值未取得
- `f_kpi5_non_gaap_diluted_eps`（q1_business）｜Non-GAAP diluted EPS＝2.11 $（GAAP EPS $1.33）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：共識 $2.06（媒體報導，非 IR）；公司自家 Q2 指引 $2.02–2.08，高出上緣 $0.03
- `f_kpi6_backlog`（q1_business）｜Backlog（在手訂單）＝8.1 $B（創新高）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：無共識值可比
- `f_kpi7_rpo_12_crpo`（q1_business）｜RPO 未來 12 個月內認列（cRPO）＝4.2 $B｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.cadence.com Q2 2026 press release（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：無共識值可比
- `f_kpi9_guidance_fy2026`（q1_business）｜Guidance — FY2026（本次調升）＝營收 $6.26–6.34B（YoY +18–20%）；non-GAAP 營業利益率 43.75–44.75%；GAAP 營業利益率 27.75–28.75%；non-GAAP EPS $8.05–8.15；GAAP EPS $4.76–4.86；營運現金流約 $2.0B；non-GAAP／GAAP 稅率約 16.5%／26%；回購約占 FCF 50% 區間｜期間與口徑：Q2 FY2026 財報（公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2026 財報（公告於 2026-07-27））
  - 註記：2026-09-19 共識 FY2026 non-GAAP EPS $8.14（dd_numbers_extra.py consensus_revision），落在指引區間上緣；此為財報後共識，非財報前預期
- `f_peer_cdns_gross_margin_pct`（q2_moat）｜CDNS 毛利率＝85.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cdns_operating_margin_pct`（q2_moat）｜CDNS 營業利益率＝30.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cdns_fcf_margin_pct`（q2_moat）｜CDNS FCF 利潤率＝28.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CDNS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_snps_gross_margin_pct`（q2_moat）｜SNPS 毛利率＝72.38 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_snps_operating_margin_pct`（q2_moat）｜SNPS 營業利益率＝11.03 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_snps_fcf_margin_pct`（q2_moat）｜SNPS FCF 利潤率＝29.18 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNPS.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_arm_gross_margin_pct`（q2_moat）｜ARM 毛利率＝97.54 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_arm_operating_margin_pct`（q2_moat）｜ARM 營業利益率＝17.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_arm_fcf_margin_pct`（q2_moat）｜ARM FCF 利潤率＝28.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ARM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_gross_margin_pct`（q2_moat）｜QCOM 毛利率＝54.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_operating_margin_pct`（q2_moat）｜QCOM 營業利益率＝23.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_fcf_margin_pct`（q2_moat）｜QCOM FCF 利潤率＝23.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝8.14 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.55 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-19）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝11.15 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-19）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.26 %｜期間與口徑：2026-06-23 → 2026-09-19／FY1 共識 EPS 7.96 → 8.14（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-19）
- `f_kpi3_free_cash_flow_635m_53m`（q4_capital）｜Free cash flow（營運現金流 $635M 減資本支出 $53M）＝582 $M（占營收 36.7%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 CFO commentary（8-K Ex99.2，2026-07-27）；與 H1 營運現金流 $990.711M 減 Q1 $355.8M 對得上（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：無共識值可比；全年營運現金流指引由 Q1 時未提供，調升後為約 $2.0B
- `f_kpi4_sbc_gaap_sbc_146_89m_9_3`（q4_capital）｜SBC 占 GAAP 營業利益（SBC $146.89M，占營收 9.3%）＝32.6 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 SBC $146,890 千美元；營業利益 $450,315 千美元；占比自算（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-27））
  - 註記：不適用
- `f_ps_current`（q5_valuation）｜P/S（現值）＝14.58 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝40.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝14.77 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝43.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-23（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝309.09 USD｜期間與口徑：2026-09-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝37.97 x｜期間與口徑：2026-09-19／分母＝FY1 EPS 8.14，分子＝快照價 309.09｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-19）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝61.45 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝35.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝35.9 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝40.2 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝43.8 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝52.65｜期間與口徑：2026-09-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-09-23（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝9.84 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-09-24／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）
  - 原文：「price 309.09 / W52 324.73 / W104 313.03 / W250 257.51 / W250 13週斜率 0.7%」
- `f_kpi8_guidance_q3_fy2026`（q1_business）｜Guidance — Q3 FY2026＝營收 $1,595–1,625M（YoY +19–21%）；non-GAAP 營業利益率 43.5–44.5%；GAAP 營業利益率 27.5–28.5%；non-GAAP EPS $2.01–2.07；GAAP EPS $1.11–1.17；預計回購約 $200M 區間｜期間與口徑：Q2 FY2026 財報（公告於 2026-07-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 CFO commentary（8-K Ex99.2，2026-07-27）＋新聞稿 investor.cadence.com Q2 2026 press release（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2026 財報（公告於 2026-07-27））
  - 註記：Q3 共識值未取得；註：指引中點營收 $1.61B 較 Q2 僅 +1.6% QoQ，non-GAAP 營業利益率中點 44.0% 低於 Q2 實績 45.5%
- `f_ma_w52`（q5_valuation）｜52 週均線＝324.73 USD｜期間與口徑：2026-09-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）
- `f_ma_w104`（q5_valuation）｜104 週均線＝313.03 USD｜期間與口徑：2026-09-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）
- `f_ma_w250`（q5_valuation）｜250 週均線＝257.51 USD｜期間與口徑：2026-09-24／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-09-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-09-19／兩份 Koyfin 快照之間的 EPS 修正幅度（8.14 → 8.14）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-09-19）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Cadence agreed to plead guilty to conspiracy to commit export control violations (selling semiconductor design tools to a restricted PRC military university via its China subsidiary). Criminal penalties about $118M plus BIS civil penalty over $95M; after coordinated credits, combined net penalties and forfeiture exceed $140M. Cadence must implement an export compliance program; the release says the plea is subject to federal district judge approval.
  - 來源：U.S. Department of Justice, Office of Public Affairs, 'Cadence Design Systems Agrees to Plead Guilty and Pay Over $140 Million for Unlawfully Exporting Semiconductor Design Tools to a Restricted PRC Military University' https://www.justice.gov/opa/pr/cadence-design-systems-agrees-plead-guilty-and-pay-over-140-million-unlawfully-exporting（as_of 2025-07-28）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Cadence's Q2 2026 CFO commentary (8-K exhibit) lists in its forward-looking statements the company's 'ongoing obligations under its July 2025 settlement agreements with the U.S. Department of Justice and Bureau of Industry and Security', and the risk of 'any further inquiries or adverse actions by the DOJ, BIS or other governmental authorities and any impact of the settlements on Cadence's operations and business dealings'.
  - 來源：Cadence Design Systems Form 8-K, CFO Commentary Q2 2026 (Ex. 99.2) https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000089/cfocommentary07272026ex9902.htm（as_of 2026-07-27）｜affects：thesis.R、decision_inputs.bear、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：BIS 對 Cadence 課處 9,500 萬美元行政罰款，事由為未經許可向實體清單機構出口 EDA 硬體、軟體與晶片設計技術；Cadence 承認 2015 年 9 月至 2020 年 9 月間有 56 項違反 EAR，經由別名 Central South CAD Center 售予國防科技大學（NUDT），出口價值約 4,530 萬美元；同時與美國司法部達成協議，含 4,500 萬美元沒收。
  - 來源：BIS press release: Cadence Design Systems to Pay $95 Million Penalty to BIS for Unauthorized Exports to Chinese Entities (bis.gov); BIS Final Order 2025-07-28 (bis.gov/media/documents/cadence-design-systems-final-order-7.28.2025.pdf)（as_of 2025-07-28）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：Cadence FY2025 10-K 寫明：先前對中國的出口限制「have had, and any subsequent restrictions may have, an adverse effect on our business, results of operations or financial condition」。10-K 該段未拆出中國營收占比。
  - 來源：Cadence Design Systems Form 10-K for fiscal year ended 2025-12-31 (sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm)（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K risk factor: 'We depend on a single supplier or a limited number of suppliers for certain hardware components and contract manufacturers for production of our hardware products, making us vulnerable to supply disruption and price fluctuation.' The filing does not name the manufacturers, their locations or the FPGA supplier.
  - 來源：Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：On May 23, 2025 BIS informed Cadence that a license was required to export, re-export or transfer EDA software and technology where a party is in China or a Chinese military end user. On July 2, 2025 BIS rescinded those license requirements effective immediately.
  - 來源：Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：10-K states Cadence cannot predict whether or when further changes will eliminate, decrease or change the duration of the export restrictions, and that increased restrictions on China exports may lead to additional retaliation by the Chinese government and further escalate geopolitical tensions. It also states that trade regulations limiting or banning sales into certain countries or to certain companies have impacted its ability to transact business in certain countries and with certain customers.
  - 來源：Cadence Design Systems Form 10-K FY2025, https://www.sec.gov/Archives/edgar/data/813672/000081367226000016/cdns-20251231.htm（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q (quarter ended 2026-06-30) states BIS issued an interim final rule effective 2025-09-29 extending export restrictions to entities 50% or more owned by Entity List or Military End-User List parties. On 2025-11-11 BIS published a one-year suspension of that rule, currently set to expire 2026-11-09.
  - 來源：Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm（as_of 2026-06-30）｜affects：thesis.R、triggers
- `geo_supply_chain#5`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q states Cadence settled with BIS and DOJ in July 2025 over export violations that took place between 2015 and 2021; it paid aggregate net penalties and forfeitures of $140.6 million in the quarter ended 2025-09-30, agreed to plead guilty to one count of conspiracy to commit export controls violations, and booked a $128.5 million charge in Q2 2025.
  - 來源：Cadence Design Systems Form 10-Q for period ended 2026-06-30, https://www.sec.gov/Archives/edgar/data/0000813672/000081367226000092/cdns-20260630.htm（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Moonshot AI's Kimi K3 model reportedly completed a full semiconductor chip design flow autonomously in a single 48-hour run using only open-source EDA tools, with no licensed Cadence or Synopsys software. Demo chip: 4mm² die, 100MHz, Nangate 45nm Open Cell Library, over 8,700 tokens/s simulated inference throughput, no human intervention. CDNS fell 9.6% on the day and SNPS also fell sharply.
  - 來源：Investing.com, 'Why is Cadence Design Systems stock plummeting today?' https://www.investing.com/news/stock-market-news/why-is-cadence-design-systems-stock-plummeting-today-93CH-4798909（as_of 2026-07-17）｜affects：moat_trend、thesis.R、decision_inputs.bear、valuation
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Futurum notes TSMC-COUPE (co-packaged optics) becoming a production technology creates a near-term opening favoring vendors with cross-domain simulation capabilities already in hand. Cadence had not disclosed specific COUPE enablement, which could cede this segment to Synopsys.
  - 來源：Futurum Group, 'EDA Vendors Race to Align With TSMC's Angstrom-Era Roadmap at Technology Symposium' https://futurumgroup.com/insights/eda-vendors-race-to-align-with-tsmcs-angstrom-era-roadmap-at-technology-symposium/（as_of 2026-04-24）｜affects：moat_trend、thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2025-07-27 Cadence 與美國商務部 BIS 及司法部 DOJ 達成和解，解決 2015–2021 年間的出口違規事項（Cadence 子公司對中國客戶銷售價值合計 $45.3M 的產品與服務，並將相關技術轉給中國第三方，未取得 BIS 授權）；Cadence 於 2025 年前九個月支付 BIS 與 DOJ 合計淨罰款與沒收 $140.6M，和解含持續的稽核與合規義務。
  - 來源：CDNS Form 10-Q（期間 2025-09-30），法律程序／或有事項段 — https://www.sec.gov/Archives/edgar/data/813672/000081367225000148/cdns-20250930.htm（as_of 2025-07-27）｜affects：decision_inputs.bear、thesis.R、triggers
- `major_events#4`（major_events｜方向 -｜狀態 ok）：2025-05-23 BIS 通知 Cadence：對含中國或中國「軍事終端使用者」為交易一方的 EDA 軟體與技術（ECCN 3D991、3E991）之出口／再出口／境內轉移，改為須申請許可；Cadence 表示正與 BIS 洽談進一步釐清並評估對業務與財務結果的影響。（此事件日期早於近 12 個月窗口起點，列為背景。）
  - 來源：StreetInsider：Cadence Design Systems (CDNS) is engaging with BIS to obtain further clarification on license — https://www.streetinsider.com/Corporate+News/Cadence+Design+Systems+(CDNS)+is+engaging+with+BIS+to+obtain+further+clarification+on+license/24870481.html（as_of 2025-05-23）｜affects：decision_inputs.bear、thesis.R
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：2025-05-23 BIS 通知 Cadence：對含中國或中國「軍事終端使用者」為一方的 EDA 軟體與技術（ECCN 3D991、3E991）之出口／再出口／境內轉移，改為須申請許可。這是出口管制通知，不是產品召回，也不是 FDA warning letter。
  - 來源：StreetInsider：Cadence Design Systems (CDNS) is engaging with BIS to obtain further clarification on license — https://www.streetinsider.com/Corporate+News/Cadence+Design+Systems+(CDNS)+is+engaging+with+BIS+to+obtain+further+clarification+on+license/24870481.html（as_of 2025-05-23）｜affects：decision_inputs.bear、thesis.R
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：2025-07-27 Cadence 與 BIS 及 DOJ 達成和解，解決 2015–2021 年間出口違規（對中國客戶銷售價值合計 $45.3M，並轉移技術給中國第三方，未取得 BIS 授權）；2025 年前九個月支付合計淨罰款與沒收 $140.6M，含持續稽核與合規義務。此為 DOJ/BIS 執法，不是 SEC 調查。
  - 來源：CDNS Form 10-Q（期間 2025-09-30）法律程序段 — https://www.sec.gov/Archives/edgar/data/813672/000081367225000148/cdns-20250930.htm（as_of 2025-07-27）｜affects：decision_inputs.bear、thesis.R、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 14 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":691.2,"bear_5y_price":206.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":57.2,"ev5y_pct":46.7,"irr_base_pct":9.5,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.14,"pe":37.97,"basis":"FY2026 共識非 GAAP 稀釋 EPS（前瞻一年）；終端倍數套在 FY2031E，同為前瞻一年口徑"},"eps":{"bull":[9.75,11.7,13.9,16.4,19.2],"base":[9.55,11.15,12.8,14.5,16.2],"bear":[8.9,9.3,8.8,9.1,9.4]},"pe":{"bull":36,"base":30,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CDNS_Q1_2026_Earnings_Call_20260427.md
- 2026-04-27｜CEO｜guidance：CEO 說 2026 營收成長展望上調到 17%（原話："we are raising our 2026 revenue growth outlook to 17%"）
- 2026-04-27｜CEO｜guidance：CEO 說預期首次達成 Rule of 60（同一句前半為上調 17% 展望）（原話："60 for the first time"）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年營收區間 $6.125B–$6.225B（原話："revenue in the range of $6.125 billion to $6.225 billion"）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年 non-GAAP 營業利益率 43.5%–44.5%（標籤在前一行）與 GAAP EPS $4.39–$4.49（原話："43.5% to 44.5%. GAAP EPS in the range of $4.39 to $4.49."）
- 2026-04-27｜CFO｜guidance：CFO 給 2026 全年 non-GAAP EPS 區間下緣 $7.85（上緣 $7.95 在下一行）（原話："Non-GAAP EPS in the range of $7.85 to"）
- 2026-04-27｜CFO｜guidance：CFO 給 Q2 營收區間 $1.555B–$1.595B（原話："revenue in the range of $1.555 billion to $1.595 billion"）
- 2026-04-27｜CFO｜risk：CFO 說財測含出口管制維持與現況大致相同的常規假設（原話："regulations that exist today remain substantially similar"）
- 2026-04-27｜CEO｜guidance：CEO 說 $8B 記錄積壓訂單優於計畫（原話："Our record backlog of $8 billion was ahead of plan"）
- 2026-04-27｜CFO｜guidance：CFO 說 Q1 訂單優於預期（原話："First quarter bookings were ahead of expectations"）
- 2026-04-27｜CFO｜margin：CFO 報 Q1 non-GAAP 營業利益率 44.7%（原話："Non-GAAP operating margin was 44.7%"）
- 2026-04-27｜CFO｜guidance：CFO 說 Hexagon 設計與工程事業今年貢獻約 $160M 營收，已在財測內（原話："we expect $160 million of revenue this year"）
- 2026-04-27｜CFO｜margin：CFO 說 Hexagon 預期對 2026 EPS 稀釋約 $0.28（原話："We expect it to be dilutive to the tune of about $0.28"）
- 2026-04-27｜CFO｜margin：CFO 說 Hexagon $160M 營收的利潤率影響落在 5%–10% 區間（前文為 margin impact on the $160 million）（原話："in the 5% to 10% range"）
- 2026-04-27｜CFO｜capital_allocation：CFO 解釋 Hexagon 稀釋主因：收購價 30% 以股票、70% 以現金支付，損失利息收入（原話："because we paid 30% of the acquisition price in"）
- 2026-04-27｜CFO｜commitment：CFO 預期 Hexagon 2027 年轉為增益（原話："We'd expect it to be accretive in 2027."）
- 2026-04-27｜CFO｜margin：CFO 把 2026 定位為整合年（原話："2026 is an integration year"）
- 2026-04-27｜CFO｜margin：CFO 說營收上調、但 EPS 與營業利益率低於二月財測（原話："while EPS and operating margin are lower"）
- 2026-04-27｜CFO｜margin：CFO 說 Q1 Hexagon 約貢獻 $20M 營收，EPS 稀釋僅約 $0.01（前後句）（原話："we had about $20 million of revenue from Q1 from Hexagon"）
- 2026-04-27｜CFO｜margin：CFO 說有機成長的增量利潤率（organic incremental margin）接近 60%（原話："margin, it's closer to 60% these days than 50%"）
- 2026-04-27｜CFO｜margin：CFO 說併購案通常要 12 到 18 個月才把獲利拉近公司預期（原話："takes us 12 to 18 months to improve the profitability"）
- 2026-04-27｜CFO｜commitment：CFO 預期 Hexagon 在 26／27 年重演 BETA 收購後的利潤率先稀釋再改善模式（原話："a similar pattern for '26 and '27 when it comes to Hexagon"）
- 2026-04-27｜CFO｜guidance：CFO 說扣除 Hexagon 後，全年營收在中點上調 $65M（原話："raising the year by $65 million at the midpoint for revenue"）
- 2026-04-27｜CFO｜guidance：CFO 說營運現金流財測含約 $180M Hexagon 收購前稅負，會計上歸類為營運現金流（原話："$180 million of preclose Hexagon tax liabilities"）
- 2026-04-27｜CFO｜guidance：CFO 說調整該稅負後的營運現金流展望約 $2.1B，比原財測高約 $100M（原話："operating cash flow outlook is approximately $2.1 billion"）
- 2026-04-27｜CFO｜guidance：CFO 形容下半年財測含適度審慎（原話："I'd describe as containing appropriate prudence."）
- 2026-04-27｜CFO｜guidance：CFO 說 Hexagon D&E 事業營收偏上半年集中（原話："more kind of first half weighted in terms of their profile"）
- 2026-04-27｜CFO｜guidance：CFO 說 Q1 太強所以提前上調財測，不等兩季（原話："We couldn't help but raise the guide"）
- 2026-04-27｜CFO｜commitment：CFO 說下半年財測要等到 7 月才更新（原話："we just wanted to wait until July to update the second"）
- 2026-04-27｜CFO｜guidance：CFO 說 2026 財測沒有假設 AI 變現出現階梯式跳升（原話："not assuming a sudden step function in AI monetization"）
- 2026-04-27｜CEO｜guidance：CEO 說 agentic AI 變現沒有放進財測（原話："we are not putting it in our guide"）
- 2026-04-27｜CEO｜product：CEO 說 agentic AI 變現可能早於他過去講的「兩個合約週期」（前文他稱長期說 2 contract cycles）（原話："agentic AI could happen sooner than 2 contract cycles"）
- 2026-04-27｜CFO｜guidance：CFO 說 2026 年到期續約的年化金額比 2025 年輕（原話："2026 is kind of lighter than 2025 for actual renewals"）
- 2026-04-27｜CFO｜guidance：CFO 對 Q1 訂單強勁的保留說法：只是一季（原話："But look, it's just one quarter."）
- 2026-04-27｜CEO｜guidance：CEO 說這是 Q1 最強的幾次財測上調之一（原話："this is one of the strongest raises we have had in Q1"）
- 2026-04-27｜CFO｜customer：CFO 說中國占 Q1 營收 13%（原話："China, it was 13% of Q1 revenue"）
- 2026-04-27｜CFO｜risk：CFO 說中國全年預期約占 13%（前句 we still expect China to be），並稱季度間可能不平均（原話："I think it can be lumpy from quarter-to-quarter"）
- 2026-04-27｜CEO｜product：CEO 報 IP 業務 Q1 年增 22%（原話："22% year-over-year revenue growth"）
- 2026-04-27｜CEO｜product：CEO 報核心 EDA 業務 Q1 年增 18%（原話："revenue growing 18% year-over-year"）
- 2026-04-27｜CEO｜product：CEO 報系統設計與分析（SD&A）Q1 年增 18%（原話："Design and Analysis business delivered 18% year-over-year"）
- 2026-04-27｜CEO｜product：CEO 說硬體（emulation）Q1 為史上最佳單季（原話："resulting in our best quarter ever"）
- 2026-04-27｜CEO｜product：CEO 說 ChipStack 引發大量客戶評估（原話："ChipStack generated tremendous customer interest"）
- 2026-04-27｜CEO｜product：CEO 說 AI 驅動與 agentic 方案正成為客戶續約與擴充的重要部分（原話："are becoming an important part of customer renewals"）
- 2026-04-27｜CEO｜product：CEO 說預期 super agents 會顯著擴大 EDA 使用量（consumption 在下一行）（原話："we expect them to materially expand EDA"）
- 2026-04-27｜CEO｜product：CEO 說新的 agentic 工具（過去客戶自己手做的環節）以訂閱加用量模式計價（原話："priced as a subscription plus consumption model"）
- 2026-04-27｜CEO｜product：CEO 說 base tool 的使用量正顯著上升（原話："our usage of base tool is going up"）
- 2026-04-27｜CFO｜product：CFO 說訂閱模式仍是與客戶的主軸安排；agentic 加值走用量與 token／card 模式（原話："Our subscription model remains the anchor"）
- 2026-04-27｜CFO｜product：CFO 說 agentic AI 不取代核心 EDA 引擎，而是更頻繁且更聰明地呼叫（原話："It calls them more often and it calls them intelligently"）
- 2026-04-27｜CFO｜customer：CFO 說定價環境已改善，且仍為價值導向定價（原話："has improved. Pricing obviously remains value-based"）
- 2026-04-27｜CEO｜competition：CEO 回應 AI 寫軟體疑慮：不擔心別人能寫出更好的 base tool（原話："other party will be able to write any better base tools"）
- 2026-04-27｜CEO｜competition：CEO 說數位（digital）平台在先進製程持續搶市占（原話："our digital platform continues to gain share"）
- 2026-04-27｜CEO｜competition：CEO 說 Palladium Z3 是 emulation 的黃金標準並搶下多個競品客戶（原話："continues to be the gold standard for emulation"）
- 2026-04-27｜CEO｜competition：CEO 說 Palladium 領先至少 10 年（因自研晶片）（原話："at least a 10-year lead in that in Palladium"）
- 2026-04-27｜CEO｜competition：CEO 說客戶看過 super agents 後認為不必自寫同類 agent（原話："there's no point writing these kind of agents"）
- 2026-04-27｜CEO｜competition：CEO 承認大多數客戶仍會自寫部分 agent（原話："most of our customers are writing some of their own agents"）
- 2026-04-27｜CEO｜customer：CEO 說客戶對 agentic 方案沒有抵制，只要能給生產力就願意採用（原話："the customer is more than willing to engage"）
- 2026-04-27｜CEO｜customer：CEO 轉述一位大客戶說每個新設計需要 2 倍工程師（原話："every new design, they require 2x more engineers"）
- 2026-04-27｜CEO｜customer：CEO 說客戶端環境在過去 3 到 6 個月明顯改善（原話："So that's actually a pretty marked improvement"）
- 2026-04-27｜CEO｜customer：CEO 說客戶為產能分散多個晶圓廠或節點會直接增加設計活動（原話："So that would directly lead to more design activity for us"）
- 2026-04-27｜CEO｜customer：CEO 說 EDA 占客戶 R&D 比重從約 7% 升到約 11%（原話："EDA used to be 7% of R&D and now it's more like 11% of R&D"）
- 2026-04-27｜CEO｜customer：CEO 說與 MediaTek 的合作擴大到 agentic AI 與核心 EDA 等（原話："we furthered our long standard partnership with MediaTek"）
- 2026-04-27｜CEO｜customer：CEO 說與一家領先全球晶圓廠簽下創紀錄 IP 交易（原話："We closed a record deal with a leading global foundry"）
- 2026-04-27｜CEO｜customer：CEO 說該 IP 大單由新先進節點（2 奈米）與更多 IP 內容驅動（原話："more specifically 2-nanometer and more content in IP"）
- 2026-04-27｜CEO｜customer：CEO 澄清該 IP 大單的晶圓廠不是 Intel（原話："And just to clarify, that is not Intel, okay?"）
- 2026-04-27｜CEO｜customer：CEO 說 Intel 體認到 14A 需要投入更多（原話："Intel realizes they need to invest more in 14A"）
- 2026-04-27｜CEO｜commitment：CEO 說與 Intel 的合作近期會有更多可說（原話："soon, we'll have more to say on our engagement"）
- 2026-04-27｜CEO｜commitment：CEO 保證 2030 年前會有 Z4 系統（原話："we'll have a Z4 system before 2030"）
- 2026-04-27｜CEO｜commitment：CEO 說會整合 SD&A 的整套方案（CFD、結構、多體動力學、前後處理）（原話："we will integrate the whole solution"）
- 2026-04-27｜CEO｜commitment：CEO 說將推出用於系統設計的 agentic flow（原話："you will see from us an agentic flow to do system design"）
- 2026-04-27｜CFO｜capital_allocation：CFO 報 Q1 用 $200M 回購股票（原話："we used $200 million to repurchase Cadence shares"）
- 2026-04-27｜CFO｜capital_allocation：CFO 說 2026 預計用約 50% 自由現金流回購股票（approximately 在前一句尾／同行）（原話："50% of our free cash flow to repurchase Cadence shares"）
- 2026-04-27｜CFO｜capital_allocation：CFO 報未償債務本金為 $2.925B（原話："principal value of debt outstanding was $2.925 billion"）
- 2026-04-27｜CEO｜capital_allocation：CEO 說併購 Hexagon 同時收購了經銷商以強化 go-to-market（原話："we also acquired some resellers to strengthen"）
- 2026-04-27｜CEO｜product：CEO 說 physical AI 會遠大於資料中心 AI（他稱五年來一直這樣說）（原話："physical AI will be bigger than data center AI"）
- 2026-04-27｜CEO｜product：CEO 說併購後 SD&A 營收規模約 $1B 年化（billion 在此行開頭，roughly $1 在前一行）（原話："billion of run rate"）

### CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年營收成長約 19%。（原話："We're growing this year at a clip of 19%"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管給今年 non-GAAP 營業利益率 44.25%。（原話："44.25% of kind of non-GAAP op margin"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年成長率加營業利益率會超過 Rule of 60。（原話："we're going to surpass Rule of 60 this year"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說最近一季（Q2）營收成長約 24%。（原話："the revenue is growing like 24%, okay?"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 核心 EDA 成長 18%–19%。（原話："the core EDA is growing 18% to 19%"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 系統設計與分析（SD&A）成長約 35% 以上。（原話："SD&A growing at about like 35% -- north of 35%"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管給 Q2 IP 成長 40% 以上。（原話："IP growing north of 40%, okay?"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說公司約 70% 業務在「Codea」（逐字稿原字，疑為轉錄用字）。（原話："70% of our business is in Codea"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管把公司整體增量利潤率目標說成 50%。（原話："that 50% incremental margin in general for the company"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：回答 IP 占比上升與利潤率的問題時，IR 主管說要在 IP 高成長下不犧牲公司整體利潤率。（原話："not sacrificing the overarching company margin"）
- 2026-08-26｜Richard Gu (Head of IR)｜commitment：IR 主管稱利潤率成長與 EPS 成長是公司的北極星。（原話："EPS growth is always a North Star for us"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 年底前將達到年化 10 億美元的規模。（原話："going to be at a $1 billion clip by the end of the year"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 策略是聚焦先進製程與連接類 IP（HBM 等）。（原話："focus on the advanced nodes IP designs, IP titles, HBM"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 IP 策略不是包山包海。（原話："we're not going to be everything for everyone"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管以成長率說公司正在市場中拿下份額。（原話："you can tell we're gaining share in the market"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：談中國本土競爭者，IR 主管說它們規模還小。（原話："they're still a lot smaller"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說本土競爭者只有點工具、沒有完整流程。（原話："they don't have full flow"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說本土競爭者不是近中期威脅。（原話："it's not a near-term or medium-term threat for us"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：被問與最大對手的份額變化，IR 主管表示對相對地位有信心，未給分產品的份額數字。（原話："versus our peer company, we feel very confident"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說今年中國成長「至少」與公司平均相同。（原話："going to grow at least at the company average this year"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管把 Q2 中國強勁歸因於過去幾季的加購與訂單。（原話："add-on deals we had for the past couple of quarters"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管說晶圓代工生態已不只台積電、英特爾，也含三星與 Rapidus，且公司都有合作。（原話："it's not just TSMC, Intel, it's Samsung, it's Rapidus"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管提到與英特爾簽了協助其 14A 製程設計的合約，並稱其對 EDA 工具與 Agentic AI 產品也有幫助。（原話："we signed a meaningful kind of deal with Intel"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說公司已推出包含 ChipStack 在內共 4 個 super agent，涵蓋前段驗證到後段與封裝。（原話："ChipStack and also the other 3 super agents we launched"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 4 個 super agent 會另設價目表。（原話："separate price books for these 4 super agents"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 super agent 的定價比照人類設計師技能，數萬美元等級。（原話："it will be worth tens of thousands of dollars"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說客戶用量超出約定工作量時，會再依 token 與額外用量計費。（原話："additional consumption in terms of tokens and extra usage"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 agent 是人類設計師的替代，對公司是全新（greenfield）市場。（原話："This is a complete greenfield for us."）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說設計工作量未來 5、6 年將成長 30 至 40 倍。（原話："for the next 5, 6 years to the tune of even 30, 40x"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說目前 EDA 占設計端 R&D 支出的比重約 10%–11%。（原話："it's still like low teens, call it, 10%, 11%"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管說有客戶告知願意把花在人類設計師的 50% 以上再投入自動化。（原話："spend more than 50% of what we spent on a human being"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管把上述客戶說法換算成約占 R&D 預算的 33%。（原話："it's almost like 33% of the R&D budget"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管以 Cerebrus 為例，說新產品可拉動既有數位全流程工具的用量。（原話："One copy of Cerebrus can drive 10 copies of the full flow"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說最複雜的晶片電晶體數將在 5 至 6 年內成長到 1 兆（逐字稿現況數字為「[ 10 billion ]」，標為不確定）。（原話："grow to like 1 trillion in a matter of 5 to 6 years"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說定價仍有調升空間，與工作量成長並列為營收驅動。（原話："still an opportunity for us to flex further"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管轉述 Jensen 提到 40 倍生產力提升（逐字稿寫 the CHIPS Act）。（原話："they are seeing 40x productivity benefit"）
- 2026-08-26｜Richard Gu (Head of IR)｜customer：IR 主管稱客戶從標準品走向 ASIC、混合 COT、COT 的路徑，客戶越多走這條路對公司越有利。（原話："going from merchandise to ASIC to hybrid COT to COT"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：IR 主管說 EDA 只能買、不能自建。（原話："EDA can only buy, you cannot build"）
- 2026-08-26｜Richard Gu (Head of IR)｜competition：被問 EDA 是否不受自研軟體與 AI 影響，IR 主管稱 EDA 是決定性、物理精確的，位置不可取代。（原話："The position of EDA is unassailable and impracticable."）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：被問 R&D 下行週期時，IR 主管承認半導體客戶會經歷週期。（原話："Semis and our customers will go through cycles"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：同一段回答中，IR 主管說這次 AI 週期可能不同（未說明如何不同）。（原話："I think AI could be different."）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說客戶的 R&D 是最受保護、最不易被砍的支出。（原話："R&D typically is the most sacred, right, most insulated"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說公司較不受出貨量面影響。（原話："much more insulated from the volume side of the equation"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管稱過去 10–20 年公司營收平滑成長、利潤率擴張，EPS 成長快於營收。（原話："EPS will outpace the revenue growth"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：被問 AI capex 見頂的疑慮，IR 主管說公司是 AI 受益者。（原話："Cadence will be an AI beneficiary and winner regardless"）
- 2026-08-26｜Richard Gu (Head of IR)｜risk：IR 主管說公司營收驅動是設計案數與設計複雜度，而非出貨量。（原話："It's driven by design starts and design complexities"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說 Q2 底積壓訂單（backlog）為創紀錄的 81 億美元。（原話："the $8.1 billion record backlog exiting Q2"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說該 backlog 是在兩個訂單季節性偏淡的季度中依序累積出來的。（原話："in 2 seasonally down quarter from a booking standpoint"）
- 2026-08-26｜Richard Gu (Head of IR)｜margin：IR 主管給 Q2 cRPO 占 RPO 的覆蓋比率約 58%（他說高於同業）。（原話："Our ratio in Q2 is about 58%"）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說 EDA 軟體合約週期通常 2.5 至 3 年，且按期認列。（原話："Our contract cycle typically runs for 2.5 to 3 years."）
- 2026-08-26｜Richard Gu (Head of IR)｜guidance：IR 主管說硬體是約 6 個月的管線型業務，財測每約 6 個月更新一次。（原話："we'll update the guide every kind of 6 months"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：被問 Hexagon 整合進度，IR 主管說符合預期，並說已與 BETA CAE 整合成一個完整流程。（原話："It's tracking well against our expectations."）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：被拿來與對手大額併購比較時，IR 主管說公司不需要買下整間百貨公司。（原話："you don't need to buy the entire department store"）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：IR 主管說 SD&A 只聚焦兩個「capstone」領域（貼近矽的封裝／3D-IC，與運算最吃重的實體模擬）。（原話："we are focused on the 2 capstone areas in the SD&A"）
- 2026-08-26｜Richard Gu (Head of IR)｜capital_allocation：IR 主管提到公司的現金流與股票回購計畫，作為長期複利模式的一部分。（原話："great kind of cash flow and share buyback kind of program"）
- 2026-08-26｜Richard Gu (Head of IR)｜product：IR 主管說 Millennium 已獲 NVIDIA 公開背書，並稱生產力提升 50 至 60 倍。（原話："I think we talked about the productivity of 50 to 60x."）
- 2026-08-26｜Richard Gu (Head of IR)｜commitment：被問未來 12–18 個月該追蹤什麼，IR 主管說公司自己盯的是經常性營收成長。（原話："we're closely watching is the recurring revenue growth"）

### CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md
- 2026-09-09｜CEO｜customer：CEO 說 2026 年半導體、系統公司、超大規模雲端業者整體都好，對晶片的投入是他見過最強的（原話："the commitment to silicon is the strongest that I have seen"）
- 2026-09-09｜CEO｜guidance：CEO 對這波景氣還能走多久的定性說法，無財測數字（原話："it looks like party is only getting started"）
- 2026-09-09｜CEO｜competition：CEO 列出成長三個原因之一：產品表現好、相對競爭位置強（原話："our comparative position is very strong"）
- 2026-09-09｜CEO｜product：CEO 說 agentic 是傳統產品之上的新增 TAM，頂層原本由人做的工作（原話："the top layer is a brand-new TAM opportunity for us"）
- 2026-09-09｜CEO｜product：CEO 談三層蛋糕（運算資料／物理模擬／AI agent），主張價值最終落在垂直應用而非水平層（原話："the real value will accrue to the vertical application"）
- 2026-09-09｜CEO｜competition：回應「前沿模型從 prompt 直接自動化晶片設計、繞過商用 EDA」的看空論點，CEO 稱沒有晶片不用 Cadence 工具設計（原話："There's no chips being designed without using our tools"）
- 2026-09-09｜CEO｜competition：CEO 主張 AI 模型做不了古典物理模擬的中間層，需與物理引擎並用（原話："mathematically, it's not possible to do the middle layer"）
- 2026-09-09｜CEO｜competition：被問為何不能由他人提供頂層或底層，CEO 承認有客戶自寫 agent 去呼叫 Cadence 工具（原話："some customers are writing some agents that call our tools"）
- 2026-09-09｜CEO｜competition：CEO 稱外部 agent 呼叫 Cadence 工具在部分情境可行，但效率較差；Cadence 自己寫了中間層與頂層，能取用未對外開放的內部介面（原話："agent could call our tools, but it is not that efficient"）
- 2026-09-09｜CEO｜competition：CEO 表示頂層 agent 市場不需要百分之百由 Cadence 拿下，客戶可有約 10 個 agent，4 個大的由 Cadence 提供（原話："we don't need to get 100% of that market"）
- 2026-09-09｜CEO｜product：CEO 說頂層有 4 個 super agent（同段點名：前端設計、實體設計、類比設計、PCB 與封裝），中間層約 30、40 個產品（原話："The top layer, we have 4 super agents"）
- 2026-09-09｜CEO｜capital_allocation：CEO 提到研發團隊規模，同時撰寫頂層與中間層（原話："We have like 10,000 people in R&D"）
- 2026-09-09｜CEO｜product：被問 agentic 怎麼變現，CEO 說頂層採新商業模式（消費加訂閱），中間層維持原有模式；未給營收數字（原話："which is consumption plus subscription"）
- 2026-09-09｜CEO｜risk：針對「效率提升 5 倍就只買 1/5 中間層」的市場疑慮，CEO 以 2006 年模擬器快 10 倍的舊例反駁（原話："people will buy like 10x less, but that never happens"）
- 2026-09-09｜CEO｜customer：CEO 引述 TSMC 路線圖：未來 5 年晶片複雜度或尺寸成長倍數，作為工作量呈指數成長的依據（原話："chips complexity or size will go up by 48x"）
- 2026-09-09｜CEO｜customer：CEO 稱客戶要靠 5 到 10 倍的自動化才撐得住設計規模成長，不可能等比例增聘工程師（原話："this 5 to 10x improvement to even sustain the growth"）
- 2026-09-09｜CEO｜customer：CEO 對比歷史：90 年代末、2000 年代初設計 CPU 約 5 年、500 人，現在的人力與時程（原話："you can design a CPU with 30, 40 people within 6 months"）
- 2026-09-09｜CEO｜customer：CEO 引述 Imec 路線圖，稱指數成長預計持續到 2042 年（原話："exponential is still projected to go until 2042"）
- 2026-09-09｜CEO｜product：被問 agentic 與過去 Cerebrus／GenAI 有何不同，CEO 稱 agentic 對 Cadence 的意義大於 GenAI（原話："agentic is much more meaningful to us than GenAI"）
- 2026-09-09｜CEO｜product：CEO 說人一次約跑 3、4 個實驗，agent 跑的實驗數量（同段對比）（原話："when the agent runs it, it runs, like, 100 experiments"）
- 2026-09-09｜CEO｜product：CEO 稱 agentic 帶動底層基礎工具用量上升，並說在財報中看得到（原話："the usage of the base tools is also going up"）
- 2026-09-09｜CEO｜customer：CEO 稱已與頂尖客戶接洽全套 agentic 方案（原話："we have engaged with all the top companies"）
- 2026-09-09｜CEO｜competition：被問競爭優勢在哪，CEO 稱 Cadence 在 agentic 領先（原話："we are definitely leading in agentic"）
- 2026-09-09｜CEO｜competition：CEO 稱現在各產品線同時表現良好、不依賴單一領域（原話："we are hitting in all cylinders"）
- 2026-09-09｜CEO｜product：CEO 給 IP 業務今年成長幅度；原文未說明是營收、訂單或其他口徑（原話："our business is up 30% this year"）
- 2026-09-09｜CEO｜product：CEO 談 IP 去年成長幅度，用語帶不確定（I think、probably）（原話："Was up, I think, 30% last year, probably"）
- 2026-09-09｜CEO｜capital_allocation：CEO 承認 IP 過去是 Cadence 的弱項，先前投入較少（原話："IP was the weak point of cadence historically"）
- 2026-09-09｜CEO｜margin：CEO 說明過去少投資 IP 的原因：獲利性不如 EDA（未給利潤率數字）（原話："because it's not as profitable as EDA"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說現在因 AI 與 3D IC，看到 IP 有更多機會（與前述「過去少投資」對照）（原話："there is more opportunities in IP"）
- 2026-09-09｜CEO｜product：CEO 說 IP 聚焦先進製程與 HPC，並選 5、6 種關鍵 IP（SerDes、PCIe、UCIe、HBM、DDR）（原話："we focus on lower nodes and HPC IP"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說其他晶圓廠（Samsung、Intel、Rapidus）也要進入，Cadence 需為它們開發 IP（原話："we need to develop IPs for them"）
- 2026-09-09｜CEO｜product：CEO 談硬體（模擬驗證系統）需求，稱近 6 年來每年創紀錄；原文未指明指標與數字（原話："it has been a record year for, I don't know, last 6 years"）
- 2026-09-09｜CEO｜guidance：CEO 對硬體需求的定性看法，無財測數字（原話："I don't think that's going to slow down"）
- 2026-09-09｜CEO｜product：CEO 拆解硬體需求三個來源之一：硬體採購量與晶片尺寸成正比（原話："hardware you buy is proportional to the size of the chip"）
- 2026-09-09｜CEO｜competition：CEO 稱 Cadence 自研硬體系統領先 10 到 15 年（並說是唯一在 TSMC 自行設計晶片的公司）（原話："a 10-, 15-year lead in designing our own"）
- 2026-09-09｜CEO｜competition：CEO 稱這類硬體系統是複雜晶片設計不可缺（用來在晶片回來前跑 OS／軟體驗證）（原話："cannot design any complicated chip without these systems"）
- 2026-09-09｜CEO｜product：被問 SDA 對 Boeing 與 NVIDIA 是否策略不同，CEO 稱兩者相近，並說 SDA 演算法比 EDA 簡單（原話："SDA is easier than EDA"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說明 SDA 的擴張範圍：做與晶片設計有綜效的項目（熱、電磁、3D IC）（原話："things which are synergistic to chip design"）
- 2026-09-09｜CEO｜commitment：CEO 陳述一貫優先順序：EDA 要做到第一，避免擴張時失去核心焦點（原話："our always focus from the beginning is EDA should be #1"）
- 2026-09-09｜CEO｜risk：CEO 談三個垂直應用（資料中心、實體 AI、科學 AI）各有自己的高峰期，說資料中心目前在高峰（原話："I think data center is in peak"）
- 2026-09-09｜CEO｜guidance：CEO 對實體 AI 週期高峰時點的看法（同段稱科學／生命科學約 5 到 10 年後）；無營收數字（原話："physical AI may peak in the next 3 to 7 years"）
- 2026-09-09｜CEO｜capital_allocation：CEO 說明為實體 AI 布局，投資 Hexagon D&E 業務取得模擬能力（原話："we invested in Hexagon D&E business for simulation"）
- 2026-09-09｜CEO｜commitment：CEO 陳述投資原則：在大趨勢之前提前投入，幅度不會太大（原話："we always over invest ahead of it, not too much"）
- 2026-09-09｜CEO｜commitment：CEO 表示三個垂直應用（資料中心、實體 AI、科學 AI）都要投資（原話："we want to invest in all these three slices"）
- 2026-09-09｜CEO｜customer：CEO 稱與所有 Mag 7 合作，並說可在財報看到（原話："We are working with all the Mag 7"）
- 2026-09-09｜CEO｜customer：CEO 談剛從中國回來，前一句點名 Xiaomi、BYD、NIO 都在設計晶片，稱它們是客戶（原話："they're all designing chips, they're all our customers"）
- 2026-09-09｜CEO｜customer：CEO 說核心 EDA 與 TSMC、ARM 長期合作，現在也與 Intel、Samsung 合作（原話："and now with Intel and Samsung"）

### 問答異常語氣（迴避／改口／保留）
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Andrew DeGasperi (BNP)：那家擴大使用 sign-off 的 marquee AI infrastructure 公司是不是雲端業者｜答法：CEO 未回答是或否，只說「主要的 AI infrastructure/ASIC 公司」，轉談 Innovus 與 sign-off 在 TSMC 的採用
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Gianmarco Conti (Deutsche)：Palladium／Protium 下一代（Z4、X4）是否 12–18 個月內推出｜答法：CEO 明說不談新品時程，改談 Z3 容量足夠與競爭領先，只承諾 2030 年前會有 Z4
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Joseph Quatrochi (Wells Fargo)：EDA 占客戶 R&D 比重未來可以到多少｜答法：CEO 給歷史 7%→11%，但說寧可印出結果不預測，「多少我們看看」，未給目標數字
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Lee Simpson (Morgan Stanley)：physical AI 的價值何時會出現在數字裡｜答法：CEO 談三層蛋糕、TAM 與矽晶片需求，沒有給何時反映在財報的時點
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Harlan Sur (JPMorgan)：財測隱含下半年季均營收略低於 Q2，是 Hexagon 還是核心業務不均｜答法：CFO 用「appropriate prudence」與 Hexagon 上半年偏重回應，說等 7 月再更新下半年，未給下半年拆解數字
- CDNS_Q1_2026_Earnings_Call_20260427.md｜問：Siti Panigrahi (Mizuho)：Rapidus、Intel Foundry 等新晶圓廠是否已對 IP 需求有實質貢獻｜答法：CEO 未量化貢獻，稱與 Intel 進展良好但「soon we'll have more to say」，並澄清創紀錄大單不是 Intel
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：市場對 EDA 與 AI capex 見頂的疑慮，到底看錯了什麼？｜答法：先說「the market is the market」，再轉談策略、領導團隊與「AI 受益者」，沒有直接回答市場哪裡看錯，也沒談 capex 見頂情境的數字。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：若客戶 R&D 進入下行週期，公司營收是否有一個底？｜答法：沒有正面確認「有底」，也沒給數字；回頭講過去 10–20 年平滑成長、R&D 最受保護，並加了一句「I think AI could be different」，語氣有保留。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：81 億 backlog 的能見度與長期目標拆分？是否考慮其他領域的併購（bolt-on）？｜答法：回答 backlog 品質（cRPO 覆蓋率 58%）、合約週期與 Hexagon 整合，沒有回應是否找其他 bolt-on，也沒給 backlog 分業務拆分。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：3 年後中國在公司成長中扮演什麼角色？｜答法：只回答今年（至少與公司平均相同）與 Q2 加購訂單，未談 3 年後；結尾用「We'll keep a close eye on it」帶過。
- CDNS_Deutsche_Bank_2026_Technology_Conference_20260826.md｜問：R&D 預算中軟體占比何時會到 20%–25%？｜答法：沒給時點；改引客戶說願意花人力成本 50% 以上於自動化、換算約 33% 的說法，並轉談長期順風。
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：agentic 與過去 Cerebrus 等 AI 功能相比，以營收角度看，什麼在推動經常性收入加速成長？｜答法：CEO 回答談 agent 跑實驗數量（約 100 個 vs 人跑 3、4 個）、workflow 與生產力，未提供 agentic 營收、占比或貢獻幅度的任何數字；前一題問變現時也只答商業模式（消費加訂閱）
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：你曾說硬體需求受供給限制，結構上是什麼在推動需求？｜答法：CEO 回答談硬體不可取代、設計數量增加、晶片尺寸變大三點，未回應「供給受限」這個前提，也未提交貨或產能
- CDNS_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260909.md｜問：分析師問：實體 AI 長期對 Cadence 營收貢獻的量級該怎麼看？｜答法：CEO 回答談市場是兆美元級、週期高峰在未來 3 到 7 年、已收購 Hexagon D&E，未給對 Cadence 營收的任何量級或時程數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 4 |
| customer_second_source | found | 1 | 4 |
| customer_concentration_credit | found | 1 | 4 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 7 | 4 |
| end_markets | found | 8 | 6 |
| substitute_technology | found | 4 | 4 |
| channel_business_model_shift | found | 4 | 4 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 5 | 6 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段","irr_base_pct":10.7,"ev5y_pct":50.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟡","ma":"-","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":3.7,"ev5y_pct":50.8,"irr_base_pct":10.7,"max_dd_pct":-50,"bull_5y_price":669.6,"bear_5y_price":206.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段","price_at_dd":292.7,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CDNS","date":"2026-09-24","schema":"v15.2","contract":"v19","company_name":"Cadence Design Systems"},"oneliner":"EDA 寡占龍頭：Q2 營收年增 24%、在手訂單 $8.1B 創新高，護城河與跑道都在；但 38 倍前瞻本益比已吃進兩年共識，現價不追，回到 $260 附近或 11 月出口規則落地且 EDA 未受限再加","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CDNS_20260924/scenario.json","answers":{"q1_business":{"verdict":"賺晶片設計公司與系統公司研發預算的錢；錢卡在先進製程的實作、簽核與硬體驗證這幾個節點，客戶只能買、很難自建","reasoning":"收錢方式：約八成經常性（軟體授權，合約 2.5–3 年按期認列），兩成前期認列（硬體與部分 IP）；CFO 在 2026-07-27 維持全年八二比。Q2 營收 $1,584M、年增 24.2%，非 GAAP 營業利益率 45.5%，GAAP 28.4%（比指引下緣低 0.1 點，併購整合費用占營收 2.1%）；近四季毛利率 85.9%。分部：核心 EDA 約占七成、年增 18%；IP 年增 40% 以上；SD&A 年增 37%（含 Hexagon）；三塊都是雙位數。產業時鐘在擴張期，依據是設計活動而非股價：上半年訂單年增約 55%，在手訂單 $8.1B、年增 27%。供需持久度屬結構性持久：營收跟設計案數與設計複雜度走，不跟出貨量走；但 CEO 自己說資料中心 AI 在高峰，這段需求帶週期成分。議價：下游沒有單一客戶占營收或應收 10% 以上（10-Q），錢卡在 Cadence；上游只有硬體零件與代工仰賴少數供應商，占營收比重小。單點依賴：沒有客戶集中；最大的單一曝險是中國約 13% 營收（CFO 2026-04-27），受美國出口管制左右。產業態勢三軸：競爭面三家同推 agent，結構面 EDA 占客戶研發支出由約 7% 升到約 11%，兩者拉鋸；另有出口管制與開源替代兩個結構變數在動。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_margi","f_kpi2_gaap_operating_margin","f_kpi5_non_gaap_diluted_eps","f_kpi6_backlog","f_kpi7_rpo_12_crpo","f_kpi9_guidance_fy2026","f_peer_cdns_gross_margin_pct"],"verdict_values":{"revenue_quality":"約 80% 經常性、20% 前期認列（CFO 2026-07-27）；在手訂單 $8.1B，其中 $4.2B 在 12 個月內認列，覆蓋約 58%（IR 2026-08-26）","unit_econ_note":"近四季毛利率 85.9%；Q2 非 GAAP 營業利益率 45.5%、年增 2.7 點；管理層稱有機增量利潤率 50–60%","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高毛利寡占設計工具、八成經常性長約、需求跟客戶研發預算與設計複雜度走"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：營收由設計案數與複雜度驅動（CEO 2026-09-09 引台積電路線圖稱 5 年晶片複雜度約 48 倍），但資料中心段 CEO 自稱在高峰，屬週期性風險","bargaining":{"up":"硬體驗證的零件與代工仰賴單一或少數供應商（10-K），上游議價弱，但占營收小","down":"無單一客戶占營收或應收 10% 以上（10-Q）；換流程要重做晶圓廠認證，議價在 Cadence","geo":"中國約占營收 13%，受美國出口管制與關係企業規則左右"},"profit_pool_dir":"流向設計端：EDA 占客戶研發支出由約 7% 升到約 11%（CEO 2026-04-27）；5 年前的營業利益池占比事實表未涵蓋","tam_table":[{"item":"EDA 占客戶研發支出","value":"約 7%→約 11%（CEO 2026-04-27）；IR 2026-08-26 說 10–11%"},{"item":"agent 頂層（新品類）","value":"公司稱全新市場；有客戶願把人力成本 50% 以上投入自動化，IR 換算約占研發預算 33%——屬公司說法，未經獨立驗證，且不在財測內"},{"item":"IP","value":"接近年化 10 億美元，Q2 年增 40% 以上，CEO 2026-09-09 稱今年約 30%"},{"item":"SD&A","value":"併購後約年化 10 億美元，Q2 年增 37%（含 Hexagon）"},{"item":"滲透率","value":"傳統 EDA 在晶片設計已近全面滲透；成長靠設計複雜度與 agent 新層"},{"item":"利潤池 5 年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河向上：先進製程的簽核、晶圓廠認證流程與自研硬體驗證形成轉換成本，Intel、Samsung 關係正常化擴大覆蓋；威脅在頂層 agent 的議價分散，不在中間層工具被取代","reasoning":"機制：先進製程要用經晶圓廠認證的流程才能投片，換工具等於整條流程重驗；硬體驗證用自研晶片，CEO 稱領先 10–15 年。可證方向：同業 ROIC 事實表未涵蓋，改看利潤率。近四季營業利益率 30.8%，Synopsys 11.0%；FCF 利潤率 28.6% 對 29.2%，大致持平。帳面領先、現金面沒被追上。執行面擴大：Intel 14A 多年合約（CEO 稱是十到二十年沒解決的關係）、Samsung 2 奈米合作、IP 拿到兩年前進不去的案子、數位簽核與類比 Spectre 各有競品替換、硬體新增 12 個客戶。這些多是公司自述，第三方佐證只有台積電論壇上節點覆蓋最廣（Futurum）。定價面穩定：價值定價環境改善（CFO 2026-04-27），agent 另立價目表、以人力成本計價。反向證據：Kimi K3 開源示範、Synopsys 同步推自主驗證、COUPE 支援未揭露、客戶要求自選大模型。評分：執行 9、定價 9。報酬持續期：當期 ROIC 算不出來（投入資本事實表未涵蓋），以高利益率加輕資產推定為高利益率×高周轉；四檢查點兩綠兩黃，持續期風險在頂層分配與出口管制，不在需求。增量報酬：唯一可量化的大額增量投資 Hexagon，首年報酬偏低。AI 曝險屬淨增量：agent 附著在自家引擎上、呼叫次數變多，不是繞過；分界年事實表未涵蓋，以 2028 年前揭露 agent 營收作檢驗。","fact_refs":["f_peer_cdns_gross_margin_pct","f_peer_cdns_operating_margin_pct","f_peer_cdns_fcf_margin_pct","f_peer_snps_gross_margin_pct","f_peer_snps_operating_margin_pct","f_peer_snps_fcf_margin_pct","f_peer_arm_gross_margin_pct","f_peer_arm_operating_margin_pct","f_peer_arm_fcf_margin_pct","f_peer_qcom_gross_margin_pct","f_peer_qcom_operating_margin_pct","f_peer_qcom_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"先進製程流程鎖定：晶圓廠認證的實作與簽核流程＋自研晶片的硬體驗證，換供應商等於重驗整條流程","execution":9,"pricing":9,"grade":"A","trend":"↑","trend_evidence":"執行面擴大：Intel 14A 多年合約、Samsung 2 奈米、IP 競品替換、數位簽核與類比各有勝單、硬體新增 12 個客戶；定價面穩定：價值定價環境改善，agent 另立價目表。反向是客戶自選大模型、自寫 agent，頂層議價權分散；最大客戶份額下滑的證據不存在","competitor_notes":[{"name":"SNPS","strategy_note":"近四季營業利益率 11.0%，遠低於 CDNS 的 30.8%，但 FCF 利潤率 29.2% 與 CDNS 相近，帳面差距的原因事實表未拆解；DAC 推出自主驗證 agent（自稱快 50 倍），在 COUPE 共封裝光學可能先卡位，是最直接的對手"},{"name":"Siemens EDA","strategy_note":"財務不在對照表；主打 agent 編排而非節點廣度，Fuse EDA AI Agent 自稱庫特性化快 10 倍以上"},{"name":"ARM","strategy_note":"IP 授權模式，毛利率 97.5%、營業利益率 17.3%、研發密度 57%；在 IP 上是相鄰對手，不在 EDA 流程上競爭"},{"name":"QCOM","strategy_note":"客戶側參照（毛利率 54.2%、營業利益率 23.3%），代表大型晶片設計公司的研發預算承受力，不是對手"},{"name":"688521.SH","strategy_note":"中國本土 EDA／IP，事實表無財務資料；IR 稱本土對手規模小、只有點工具、無完整流程，非近中期威脅（公司說法）"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營業利益率與 FCF 利潤率替代","threats":[{"level":"🟡","text":"開源 EDA 加大模型 agent 自動跑完整設計流程：Kimi K3 以 45 奈米、100MHz 小晶片在 48 小時內完成、未用商用授權，消息當天股價 −9.6%；目前只到舊製程，先進製程替代機率低，但成熟製程部分設計工作可能被分流","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"頂層 agent 的模型選擇權在客戶：客戶要求自選大模型、自寫 agent 呼叫 Cadence 工具（CEO 2026-07-27、2026-09-09），頂層定價權可能被分散","p":"30%","evidence_refs":[]},{"level":"🟡","text":"Synopsys、Siemens 同步推自主 agent，Synopsys 自稱驗證快 50 倍，三家朝同一方向、都以 NVIDIA 與 AMD 為領頭客戶（Futurum）","p":"25%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🟡","text":"台積電 COUPE 共封裝光學進入量產，Cadence 未揭露具體支援，這個細分可能讓給 Synopsys（Futurum 2026-04）","p":"30%","evidence_refs":["substitute_technology#3"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是設計工程師、決策者是研發主管、付款者是晶片與系統公司，三角色都成立；這是需要不是想要，不用經認證的 EDA 就無法在先進製程投片，延後購買的代價是產品延期。客戶要解決的是設計複雜度，公司的解法會變（agent），問題本身不會消失"},{"item":"決策層級","level":"🟢","text":"替代性要在整條設計流程衡量：換流程要重做晶圓廠認證、重訓工程師，合約 2.5–3 年；一套 Cerebrus 可帶動 10 套全流程授權（IR 2026-08-26）。無單一客戶占營收或應收 10% 以上。漲價後流失率與分客群續約率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"EDA 占客戶研發支出由約 7% 升到約 11%，分配在往 Cadence 移；但頂層 agent 的價值可能分給客戶自選的大模型與客戶自寫的 agent（CEO 兩次承認），晶圓廠握有製程設計套件，Cadence 靠與台積電、Intel、Samsung 綁定維持位置"},{"item":"社會容忍度","level":"🟡","text":"不是民生必需品，價格不受社會壓力；上限來自國安：美國政府可限制對中國銷售（2025 年 5 月曾要求許可、7 月撤回；關係企業 50% 規則暫停到 2026-11-09），公司也在出口違規和解後的持續義務中。政策上限等於中國約 13% 營收的市場准入"}],"roiic":"投入資本事實表未涵蓋，無法算全公司增量報酬；唯一可量化的增量投資 Hexagon D&E（約 €2.70bn），2026 年營收約 $160M、利潤率 5–10%（CFO 2026-04-27），首年報酬不到 1%，公司承諾 2027 轉增益","reinvest_rate":"以現金流看：2026 營運現金流約 $2.0B，約一半回購；資本支出每季約 $53M；再投資主要走研發費用（占營收約 33%）與併購。資本支出減折舊、營運資金變動事實表未涵蓋，公式口徑算不出","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，但投入資本、折舊攤銷、營運資金變動都未涵蓋；且研發全數費用化，這條公式對軟體公司會系統性低估。上限算不出來，就無法證明共識成長落在上限內，所以情境輸入保守標成超出上限，下行機率不低於 30%"}}}},"q3_growth":{"verdict":"成長跑道寬：核心 EDA 靠設計複雜度續長，IP、SD&A 兩條第二曲線各已接近年化 10 億美元；agent 是第三條，但還沒進財測","reasoning":"成長組成：量（設計案數與複雜度）為主；價次之（價值定價＋agent 新價目表）；併購約貢獻經常性營收成長 4 點（Hexagon，CFO 2026-07-27）；回購每年約 1%。共識 EPS：FY2026 $8.14、FY2027 $9.55、FY2028 $11.15，兩年年增約 17%。FY2025 實際值事實表未涵蓋，算不足三年；共識家數也未涵蓋，目標價樣本為 27 位分析師。FY2027 共識營收年增 13.4%、EPS 年增 17.2%，差 3.8 點。內生上界算不出來（見護城河題）。缺口歸因：利潤率擴張約 3 點（有機增量利潤率 50–60%、Hexagon 2027 轉增益），淨回購約 0.5–1 點；可歸因，不靠倍數上調。跑道：傳統 EDA 已近全面滲透，但 EDA 占客戶研發支出在升，IP 與 SD&A 有營收、有成長，屬已看得到的下一條曲線，所以給寬；年數以約 10 年計（CEO 引 Imec 路線圖稱複雜度指數成長到 2042，屬公司引述）。衰退信號十類：確認亮燈 0 個；SBC 占營收 9.3% 已超過 5%，但逐年趨勢事實表未涵蓋，列半亮觀察。AI 淨增量：CEO 說人一次跑 3–4 個實驗、agent 跑約 100 個，底層工具用量上升；市場擔心效率高就少買授權，CEO 以 2006 年模擬器快 10 倍反而多買為反例，尚無數字驗證。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_backlog","f_kpi7_rpo_12_crpo","f_kpi9_guidance_fy2026"],"verdict_values":{"growth":{"driver_mix":"量為主（設計案數與複雜度）、價次之（價值定價與 agent 價目表）、併購約 4 點、回購約 1 點","runway_years":10,"runway_post_y5":"🟢","endo_ceiling_basis":"投入資本、折舊攤銷與營運資金變動事實表未涵蓋，算不出增量報酬×再投資率；研發全數費用化（約占營收三分之一）使公式低估。上限算不出來，無法證明共識落在上限內，所以情境輸入保守標成超出上限，下行機率不低於 30%（本次給 30%）。共識與營收成長的缺口可由利潤率擴張與回購解釋","segments":[{"item":"核心 EDA（含硬體驗證）","value":"約占七成（IR 2026-08-26），Q2 年增 18%；硬體連續創紀錄、Q2 新增 12 個客戶，CFO 說供給受限而非需求受限"},{"item":"IP","value":"Q2 年增 40% 以上、多數為有機；CFO 說季度波動大、不要年化，CEO 稱今年約 30%"},{"item":"SD&A","value":"Q2 年增 37%，含 Hexagon 貢獻；併購後約年化 10 億美元"},{"item":"agent 頂層","value":"四個 super agent，ChipStack 20 個以上客戶接洽、ViraStack 25 個以上；營收未揭露，不在財測內"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":null,"note":"季度毛利率事實表未涵蓋，只有近四季 85.9%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"無縮減證據，公司稱多處競品替換"},{"item":"提價後銷量下滑","lit":false,"note":"無證據"},{"item":"EPS 成長高於營收成長超過 5 點","lit":false,"note":"FY2027 共識差 3.8 點"},{"item":"FCF／淨利 <0.75 連 2 年","lit":false,"note":"推估 FCF 約為淨利 1.2 倍以上"},{"item":"SBC／營收 >5% 且逐年上升","lit":null,"note":"Q2 為 9.3%，已超過 5%；逐年趨勢事實表未涵蓋，半亮觀察"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"Kimi K3 僅在 45 奈米，列觀察"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"只有 4 個年度端點，本益比在 36 分位，不足以判斷"},{"item":"維持性資本支出占 FCF >60%","lit":false,"note":"資本支出每季約 $53M，對 FCF $582M"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"不適用"}],"trap_rating":"🟢"}}},"q4_capital":{"verdict":"資本配置中等：現金流強，回購吃一半 FCF 但收益率只有約 1%；最大一筆併購 Hexagon 首年報酬偏低，要等 2027 兌現","reasoning":"現金轉換：Q2 FCF $582M、占營收 36.7%；近四季 FCF 利潤率 28.6%，對 GAAP 營業利益率 30.8%、稅率約 26% 推估，FCF 約為稅後淨利 1.2 倍以上（淨利事實表未涵蓋）。SBC 占營收 9.3%、占 GAAP 營業利益 32.6%，是非 GAAP 與 GAAP 落差的主因之一。2026 現金去向：約一半 FCF 回購（Q1、Q2 各 $200M）；債務本金由 $2.925B 降到 $2.5B（Q1 對 Q2 法說）；Hexagon 現金對價約 €1.89bn；不配息。近三年現金去向四分事實表未涵蓋。三項計分：併購已實現增量報酬未過——Hexagon 約 €2.70bn 買 $160M 年營收、利潤率 5–10%，2026 EPS 稀釋約 $0.28，公司承諾 2027 轉增益，CFO 也說併購通常要 12–18 個月才拉近公司獲利水準。回購收益率未過——約 1.1%。SBC 淨稀釋過——回購金額高於 SBC。承諾對照：Q1 給 Q2 營收 $1,555–1,595M，實績 $1,584M；Q1 說全年成長 17%，Q2 上調到 19%；營運現金流 Q1 口徑約 $2.1B（扣 $180M Hexagon 稅負前），Q2 約 $2.0B（含稅負），前後一致。","fact_refs":["f_kpi3_free_cash_flow_635m_53m","f_kpi4_sbc_gaap_sbc_146_89m_9_3","f_peer_cdns_fcf_margin_pct","f_peer_cdns_operating_margin_pct","f_ps_current","f_ev_s_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Hexagon D&E 約 €2.70bn（七成現金、三成股票，發行 3,224,473 股），2026 年營收約 $160M、利潤率 5–10%、EPS 稀釋約 $0.28，2027 才轉增益（CFO 2026-04-27）；已實現增量報酬遠低於資金成本"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"2026 回購約 FCF 的 50%（每季約 $200M，年約 $0.8–1.0B）。市值由 P/S 14.58、EV/S 14.77 與淨負債約 $1.06B（債 $2.5B 減現金 $1.44B）反推：近四季營收約 $5.6B、市值約 $81B，回購收益率約 1.1%。十年期殖利率事實表未涵蓋，但任何正值都讓門檻高於 2%，未過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 每季 $146.9M、年約 $0.59B，約占市值 0.7%；回購金額高於 SBC，扣掉併購發股後股本淨稀釋推估低於 1.5%。實際股數變動事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主：Hexagon 約貢獻經常性營收成長 4 點（CFO 2026-07-27），扣除後仍有高十幾到 20%；近三年現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求未來五年非 GAAP EPS 年增約 15%，而且 2031 年市場還肯給約 30 倍，才有每年約一成的報酬；EPS 那一半我大致相信，倍數那一半不確定，所以不便宜也不離譜","reasoning":"倍數：前瞻本益比 38.0 倍（FY2026 共識 $8.14），FY2027 口徑 32.4 倍；以 FY2026→FY2028 共識年增約 17% 算 PEG 2.2，FY2027 口徑 1.9。近 4 個年度端點裡，本益比、股價營收比、EV／營收分別在 36、40、44 分位，在自身區間中下段、不在高檔；五年分位事實表未涵蓋（只有 4 個年度端點），不外推。同業倍數事實表未涵蓋，不做跨層級比較。分母：非 GAAP EPS 排除 SBC 與併購攤銷，FY2026 GAAP EPS 指引中點 $4.81，只有非 GAAP $8.10 的約六成；本報告不以便宜作進場理由，所以不列爭點，但用 GAAP 看倍數要再乘約 1.7。上檔：一年後以 FY2027 共識 $9.55 給 35 倍，約 $334，+8%；兩年後以 FY2028 共識 $11.15 給 33 倍，約 $368，+19%。賣方平均目標 $403，26 家評等中 24 家買進，看法一致；我的中期上檔比賣方低，差在倍數假設。RSI 52.7、26 週漲 9.8%，動能不過熱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG（品質複利股主尺）","tier":"EDA 寡占龍頭","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業前瞻本益比；估值改用自身年度端點與共識 EPS"},"fwd_pe":37.97,"peg":2.2,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 38.0 倍、PEG 2.2（FY2027 口徑 1.9），落在合理與偏貴的交界；本益比、股價營收比、EV／營收在自身 4 個年度端點的 36–44 分位，不在高檔。五年分位事實表未涵蓋（只有年度端點分位 35.9，口徑不同），不引用。預期報酬中等、無安全邊際，給中性偏貴","upside_short_pct":8,"upside_mid_pct":19,"denominator_disputed":false,"denominator_note":"非 GAAP EPS 排除 SBC（占營收 9.3%）與併購攤銷，FY2026 GAAP EPS 指引中點 $4.81 約為非 GAAP 的六成；本報告不用便宜當理由，所以不列爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在倍數，不在生意：AI 資料中心投資降溫和出口管制同時發生時，EPS 停滯、倍數壓到 20 倍出頭","reasoning":"三個看錯方向都寫在反證紀錄：一是 AI 設計投資見頂加中國再受限，論點失敗；二是營收照長，但 SBC、IP 占比上升與併購吃掉增量，股東經濟變差；三是 38 倍前瞻本益比已反映兩年共識。管理層迴避值得記下的三題：被問客戶研發下行時營收有沒有底，IR 沒正面答（2026-08-26）；被問 agent 營收貢獻，CEO 只談實驗數與商業模式，沒給數字（2026-09-09）；被問中國三年後的角色，只答今年。這三題正好對應下行情境的三個輸入。不是價值陷阱：成長、現金轉換與訂單能見度都在，確認的衰退信號為 0。Q3 指引營收中點季增僅 1.6%、非 GAAP 營業利益率中點 44.0% 低於 Q2，CFO 歸因於刻意投資，屬未證、監測。歷史最大回撤與空方最強數字事實表未涵蓋。","fact_refs":["f_kpi8_guidance_q3_fy2026","f_kpi2_gaap_operating_margin","f_kpi4_sbc_gaap_sbc_146_89m_9_3","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟢","label":"不是價值陷阱：風險在倍數與政策，不在生意變差"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.14,"pe":37.97,"basis":"FY2026 共識非 GAAP 稀釋 EPS（前瞻一年）；終端倍數套在 FY2031E，同為前瞻一年口徑"},"eps":{"bull":[9.75,11.7,13.9,16.4,19.2],"base":[9.55,11.15,12.8,14.5,16.2],"bear":[8.9,9.3,8.8,9.1,9.4]},"pe":{"bull":36,"base":30,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-50,"hi":-35,"basis":"下行情境終點約 −33%（EPS $9.4×22 倍）；途中若 AI 投資降溫與出口管制同時發生，前瞻 EPS 約 $8.9、倍數先殺到 18–20 倍，股價約 $160–178（−42% 到 −48%）；7/17 單日 −9.6% 顯示事件衝擊能在一天內發生。取 −35% 到 −50%。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"agent 授權與用量開始入帳、EDA 占客戶研發比重續升，EPS 年增近 19%，2031 年給 36 倍","base":"前兩年照共識（FY2027 $9.55、FY2028 $11.15），之後年增 15%→12%，利潤率小幅擴張加約 1% 回購；2031 年倍數收斂到 30 倍","bear":"AI 資料中心投資見頂加中國出口再受限，EPS 在 $9 上下停滯，倍數壓到 22 倍（成長降到一成的熄火情境）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CEO 2026-09-09 說資料中心在高峰；IR 2026-08-26 被問客戶研發下行時營收有沒有底，沒有正面回答；Q3 指引營收中點季增僅 1.6%；Kimi K3 以開源工具跑完設計流程；10-K 說出口限制已造成不利影響且無法預測後續","assumption":"客戶研發支出最不會被砍，設計案數與複雜度不隨出貨量波動","consequence":"AI 投資 2027–28 年降溫、客戶縮減設計案，加上中國再受限、agent 讓每位工程師用更少授權，EPS 在 $9 附近停滯三年，倍數壓到 20 倍出頭，股價落到 $190–210，五年虧三到四成；要虧到五成，倍數得殺到約 16 倍（$9.4×16.4 倍≈$155）","ruling":"部分採納：放進 30% 下行機率。反駁全面崩的部分：在手訂單 $8.1B、12 個月內認列 $4.2B、合約 2.5–3 年，下行會先表現為成長放緩，不是營收衰退。與唯一致命點（中國出口）部分重疊，已在該處回補","watch":"在手訂單年增、經常性營收有機年增、中國營收占比","evidence_refs":["geo_supply_chain#3"],"fact_refs":["f_kpi6_backlog","f_kpi7_rpo_12_crpo","f_kpi8_guidance_q3_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 9.3%、占 GAAP 營業利益 32.6%；GAAP 營業利益率 28.4% 略低於指引下緣；Hexagon 首年利潤率 5–10%、EPS 稀釋 $0.28；CEO 說 IP 獲利性不如 EDA，而 IP 成長最快；下半年刻意增加投資，Q3 非 GAAP 營業利益率指引中點 44.0% 低於 Q2 的 45.5%","assumption":"營收成長會以 50–60% 的增量利潤率落到每股","consequence":"營收照長，但 IP 與 SD&A 占比上升、SBC 與併購吃掉增量，非 GAAP EPS 年增降到一成出頭，GAAP 與非 GAAP 差距不收斂","ruling":"部分採納：資本配置只給中等；以 FY2027 非 GAAP 營業利益率 ≥45% 與 Hexagon 轉增益作檢驗。反駁的部分：FCF 占營收 36.7%、回購金額高於 SBC，每股層面目前沒被稀釋","watch":"FY2027 利潤率指引、SBC 占營收比趨勢、Hexagon 2027 增益","evidence_refs":["major_events#2"],"fact_refs":["f_kpi4_sbc_gaap_sbc_146_89m_9_3","f_kpi2_gaap_operating_margin","f_kpi3_free_cash_flow_635m_53m","f_kpi8_guidance_q3_fy2026"]},{"view":"價格已反映太多","evidence":"前瞻本益比 38 倍、PEG 約 2.2；26 家評等中 24 家買進、平均目標 $403；FY1 共識最近一次快照零修正","assumption":"市場會繼續給 30 倍以上，因為 EPS 能維持 15% 以上年增","consequence":"就算 EPS 照共識走，倍數從 38 倍收斂到 30 倍，會吃掉約四成的 EPS 成長帶來的漲幅，五年報酬只剩每年約一成","ruling":"採納：現價不追，只在 $260 附近加碼。不採泡沫說：本益比與股價營收比在自身 4 個年度端點只在 36–44 分位","watch":"股價對 FY2027 本益比、共識修正方向","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_consensus_rev_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 292.7 → 本次 309.09（+5.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=292.7","side_b":"本次 price_at_dd=309.09","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"護城河：開源加大模型能否繞過商用 EDA","cause":"新證據","prior_field":["moat_trend"],"side_a":"Kimi K3 用開源 EDA 在 48 小時自動完成設計流程、無人介入、未用 Cadence 或 Synopsys 授權，消息當天股價 −9.6%（2026-07-17）；DAC 三家同推 agent，Synopsys 自稱驗證快 50 倍；Cadence 未揭露 COUPE 支援","side_b":"示範用 45 奈米、100MHz 小晶片，落後 3／2 奈米數代；Cadence 在台積電論壇宣布支援 N3、N2、A16、A14，三家中最廣；CEO 說客戶自寫的 agent 仍呼叫 Cadence 工具，只是效率較差","ruling":"可調和（程度差異）：先進製程的替代目前不成立，護城河方向維持向上；但採納兩件事——成熟製程的部分設計工作會被分流，頂層 agent 的議價權會分散給客戶自選的模型。雙方都是單一示範或公司說法","evidence_level":"中","settle_metric":"7 奈米以下是否出現不經商用 EDA 的量產投片；核心 EDA 年增","if_then":["若 24 個月內出現前十大晶片設計公司以非商用工具在 7 奈米以下量產投片 → 護城河方向改持平、減碼一半並重跑研究","若核心 EDA 連 4 季年增 ≥15% 且 agent 營收揭露 → 維持向上、可加碼一段"],"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3","competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"成長持續性：這波設計投資還能走多久","cause":"新證據","prior_field":["runway_post_y5","trap","signal","archetype","cycle_position"],"side_a":"CEO 2026-09-09 說對晶片的投入是他見過最強、這波才剛開始；上半年訂單年增約 55%，而且今年是續約淡年；史上最大單季財測上調（17%→19%）","side_b":"同一場 CEO 也說資料中心在高峰；CFO 說 IP 高成長不要年化；Q3 營收指引季增僅 1.6%、下半年利潤率刻意下降；FY2027 共識營收年增只剩 13.4%","ruling":"可調和：成長由 20% 左右降到中雙位數，本來就是共識的樣子，不是反轉。跑道判斷不變（寬）、不是價值陷阱的判斷不變、品質複利型分類不變、整體評級不變；循環位置不適用，這不是循環股","evidence_level":"中","settle_metric":"FY2027 營收指引年增與在手訂單年增","if_then":["若 FY2027 營收指引年增 ≥13% 且在手訂單年增 ≥15% → 維持","若 FY2027 營收指引年增 <10% → 下修基本情境 EPS 並停止加碼"],"evidence_refs":["supply_demand_durability#4","end_markets#5"]},{"axis":"估值：股價上移，加上行情境 EPS 小幅上調","cause":"新證據","prior_field":["val","asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份：股價 $292.7；上行終點價 $669.6（以同為 36 倍反推，FY2031 EPS 約 $18.6）、下行終點價 $206.8；基本情境報酬每年 10.7%、上下行比 3.7、五年期望值 50.8%","side_b":"本次：股價 $309.09（+5.6%），FY2026、FY2027 共識沒變；上行 FY2031 EPS 調到 $19.2，×36 倍＝$691.2；基本情境 $16.2×30 倍＝$486、下行 $9.4×22 倍＝$206.8；基本情境報酬每年 9.5%、上下行比 3.1、五年期望值 46.7%","ruling":"拆成兩個來源，不全是價格。一、股價上漲 5.6%：基本情境終點 $486 放在前份股價 $292.7 下正好是每年 10.7%，所以基本情境報酬降到 9.5% 全部來自起點變貴；下行終點價沒動；估值判斷維持中性偏貴。二、上行情境輸入上調：終點價只由終點 EPS 乘倍數決定，跟起點價無關；$669.6 到 $691.2 是我把上行 FY2031 EPS 由約 $18.6 調到 $19.2（五年年增約 18.0% 到約 18.7%）。依據是 CEO 2026-09-09 說 agent 一次跑約 100 個實驗、底層工具用量上升，發生在前份之後；但只是公司說法、沒有營收數字，所以只小調。上下行比與五年期望值兩個來源都有：上行 EPS 若不動，現價下上下行比約 2.9、五年期望值約 45.0%；上調把兩者拉回 3.1 與 46.7%。降幅主要來自股價，上調只抵掉一小部分","evidence_level":"中","settle_metric":"股價對 FY2027 共識本益比；agent 營收是否揭露","if_then":["若股價回到 $260 以下且共識不下修 → 加碼一段","若股價漲破 $350 而共識未上修 → 不追，持有者不加","若 2028 年底前 agent 營收仍未揭露 → 上行 FY2031 EPS 退回約 $18.6"],"evidence_refs":[]},{"axis":"情境機率與最大回撤","cause":"新證據","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：上行 25%、下行 30%、最大回撤 −50%","side_b":"本次：上行 25%、下行 30%、回撤範圍 −35% 到 −50%","ruling":"新證據兩面都有：Q2 財測上調與在手訂單支持上行與基本情境；Kimi 事件、11/9 規則到期與 CEO 的高峰說法讓下行機率不宜下調。維持","evidence_level":"中","settle_metric":"Q3 財報與 11/9 規則結果","if_then":["若 11/9 後規則延長且 Q3 在手訂單 ≥$8.1B → 下次研究可把下行機率降到 25%"],"evidence_refs":["geo_supply_chain#4","substitute_technology#0"]},{"axis":"裁決與倉位角色","cause":"價格變動","prior_field":[],"side_a":"前份：進場","side_b":"本次裁決與角色由程式依本輪輸入重算","ruling":"基本面判斷（護城河、跑道、陷阱、估值）與前份一致；若本輪改列，來源是股價與週線位置的變動，不是生意變差","evidence_level":"高","settle_metric":"股價相對 52 週與 104 週均線","if_then":["若股價站回 104 週均線上方且基本面不變 → 回到前份做法"],"evidence_refs":[]},{"axis":"加碼條件更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價 ≤$260（FY2027 本益比 27x）或 token 營收首次揭露 → 加第二個三分之一；BIS 50% 規則落地無 EDA 許可 → 第三段","side_b":"價≤$260（約FY2027本益比27倍）加碼一段；11/9關係企業出口規則到期後EDA未受限且全年財測維持→再加一段","ruling":"加碼價格錨保留 $260（FY2027 共識沒變，仍約 27 倍）。把規則落地改成有日期的事件：暫停在 2026-11-09 到期（10-Q 新揭露）。把 token 營收揭露併入 agent 營收揭露，並加上核心 EDA 年增 ≥15% 的條件，避免只因揭露就加碼","evidence_level":"高","settle_metric":"股價、BIS 公告","if_then":["若 11/9 規則延長或未涵蓋 EDA 且財測維持 → 加碼一段"],"evidence_refs":["geo_supply_chain#4","reg_tariff_export#2"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"（前份未填唯一致命點）","side_b":"美國在 12–24 個月內恢復對中國 EDA 軟體與技術的出口許可要求，或 2026-11-09 關係企業規則到期後恢復並涵蓋主要中國客戶","ruling":"前份沒設 Single Thing，本次按數學上最大的單一離散衝擊選定：中國約 13% 營收、公司財測明寫假設出口規則不變；觸發時減碼至半倉","evidence_level":"中","settle_metric":"BIS 公告、公司 8-K 與財測","if_then":["若發生 → 減碼至半倉，等新財測"],"evidence_refs":["geo_supply_chain#2","major_events#4","product_recall_warning#0"]},{"axis":"kill 門檻新設（減碼與清倉條件）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"（前份未設 kill 門檻）","side_b":"經常性營收有機年增連兩季 <12% → 減碼一半；在手訂單年增轉負 → 減碼；中國占比 <10% 或因出口管制下修財測 → 減碼；7 奈米以下繞過商用 EDA 一例 → 減碼並重跑；新刑事指控 → 清倉","ruling":"前份沒有指標門檻，本次補上；每條都附資料來源與時間窗","evidence_level":"高","settle_metric":"各條指標","if_then":["任一條觸發 → 依該條動作執行，不再加碼"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"管理層說法前後對照","cause":"新證據","prior_field":null,"side_a":"CFO 2026-04-27：有機增量利潤率接近 60% 而非 50%；Q1 時給 Q2 營收 $1,555–1,595M、全年成長 17%、Hexagon 2027 轉增益、Intel 很快有更多可說","side_b":"Q2 實績 $1,584M 落在區間、全年上調到 19%、Intel 合約如預告落地；但 IR 2026-08-26 改用 50% 當全公司增量利潤率，CEO 2026-09-09 說 IP 今年約 30%，低於 Q2 的 40% 以上","ruling":"可調和：承諾大致兌現；利潤率口徑差異來自有機與全公司（含 IP 與併購）之別，本報告以 50% 作保守錨；IP 季度數字不外推","evidence_level":"中","settle_metric":"FY2027 財測隱含的增量利潤率","if_then":["若 FY2027 財測隱含增量利潤率低於 40% → 基本情境 EPS 下修一成"],"evidence_refs":[]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：史上最大單季財測上調、在手訂單年增 27%、續約淡年上半年訂單仍年增約 55%，Intel 新合約多數效益在後；股價低於 52 週與 104 週均線，倍數在自身區間中下段","side_b":"現在就賣：CEO 自己說資料中心在高峰，Q3 指引季增僅 1.6%、下半年利潤率下滑，agent 營收沒揭露也不在財測；38 倍前瞻本益比要求 17% EPS 年增延續，一次出口管制或 AI 投資降溫就是 −35% 級","ruling":"兩邊都成立：持有不賣、現價不追、$260 附近加碼","evidence_level":"中","settle_metric":"Q3 財報營收與在手訂單","if_then":["若 Q3 營收達指引上緣且在手訂單 ≥$8.5B → 可在 $290 以下先加一小段","若 Q3 營收低於指引下緣 $1,595M 或中國占比跌破 10% → 停止加碼，11/9 後再看"],"evidence_refs":["capital_markets_pricing#0","end_markets#5"]}],"triggers":[{"n":1,"text":"關係企業 50% 出口規則暫停到期","type":"風險","maps_to":"R1","metric":"BIS 是否延長暫停、EDA 是否納入","threshold":"到期未延長且涵蓋主要中國客戶","action":"減碼一半，等公司新財測","source_freq":"BIS 公告與 10-Q，事件型","date":"2026-11-09","evidence_refs":["geo_supply_chain#4","reg_tariff_export#2"]},{"n":2,"text":"美國恢復對中國 EDA 出口許可要求","type":"Single Thing","maps_to":"Single Thing","metric":"BIS 通知或公司 8-K","threshold":"發生即觸發","action":"減碼至半倉；中國占比跌破 8% 且全年 EPS 指引下修超過 5% → 重跑研究","source_freq":"事件型","date":null,"evidence_refs":["geo_supply_chain#2","major_events#4","product_recall_warning#0"]},{"n":3,"text":"Q3 FY2026 財報三項檢驗","type":"假設驗證","maps_to":"H1","metric":"營收、在手訂單、經常性營收有機年增","threshold":"營收 ≥$1,595M、在手訂單 ≥$8.1B、有機經常性年增 ≥15%","action":"三項都過 → 維持；任兩項未過 → 停止加碼","source_freq":"每季","date":"2026-10","evidence_refs":["end_markets#5"]},{"n":4,"text":"股價回到 $260 附近","type":"估值rearm","maps_to":"估值","metric":"股價對 FY2027 共識本益比","threshold":"≤$260（約 27 倍 FY2027 共識）","action":"加碼一段","source_freq":"每日","date":null,"evidence_refs":[]},{"n":5,"text":"agent 營收首次揭露","type":"加碼","maps_to":"H3","metric":"agent 營收或占比、核心 EDA 年增","threshold":"首次揭露，且當季核心 EDA 年增 ≥15%","action":"加碼一段，限 $300 以下","source_freq":"每季法說與投資人會議","date":null,"evidence_refs":["channel_business_model_shift#1"]},{"n":6,"text":"經常性營收有機成長失速","type":"減碼","maps_to":"H1","metric":"經常性營收有機年增（扣併購）","threshold":"連兩季低於 12%","action":"減碼一半","source_freq":"每季","date":null,"evidence_refs":[]},{"n":7,"text":"出口違規和解後再有刑事或行政處分","type":"清倉","maps_to":"R4","metric":"DOJ／BIS 公告、公司 8-K","threshold":"新刑事指控，或出口特權遭撤銷","action":"清倉","source_freq":"事件型","date":null,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#0"]},{"n":8,"text":"先進製程出現繞過商用 EDA 的量產投片","type":"風險","maps_to":"R3","metric":"7 奈米以下以非商用工具量產投片的公開案例","threshold":"前十大晶片設計公司出現 1 例","action":"減碼一半並重跑研究","source_freq":"產業新聞，事件型","date":null,"evidence_refs":["substitute_technology#0"]},{"n":9,"text":"Q4 財報與 FY2027 全年財測","type":"複審日期","maps_to":"H2","metric":"FY2027 非 GAAP 營業利益率指引、Hexagon 是否轉增益","threshold":"營業利益率指引 ≥45% 且 Hexagon 轉增益","action":"未達 → 下修基本情境 EPS 並複審","source_freq":"每年","date":"2027-02","evidence_refs":["major_events#2"]}],"kill_metrics":[{"metric":"經常性營收有機年增（扣併購）","bear_threshold":"連兩季低於 12%","window":"未來 4 季","source":"每季 CFO commentary 與法說","last_status":"ok"},{"metric":"在手訂單年增","bear_threshold":"轉為年減","window":"未來 4 季","source":"季報新聞稿","last_status":"ok"},{"metric":"中國營收占比","bear_threshold":"低於 10%，或公司以出口管制為由下修財測","window":"2026-11-09 後 2 季","source":"法說 CFO 口頭揭露與 10-Q","last_status":"ok"},{"metric":"7 奈米以下繞過商用 EDA 的量產投片","bear_threshold":"前十大晶片設計公司出現 1 例","window":"24 個月","source":"產業新聞、台積電技術論壇、法說","last_status":"ok"},{"metric":"FY2027 非 GAAP 營業利益率指引","bear_threshold":"低於 44%","window":"2027 年 2 月財測","source":"Q4 財報 CFO commentary","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"價≤$260（約FY2027本益比27倍）加碼一段；11/9關係企業出口規則到期後EDA未受限且全年財測維持→再加一段","exec_line":"現價 $309 不追；已持有續抱；$260 附近分批加碼；Q3 財報三項檢驗任兩項未過 → 停止加碼；出口許可要求恢復 → 減碼至半倉；新刑事指控 → 清倉"}},"decision_inputs":{"signal":"A","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場在 7 月把 45 奈米的開源示範當成先進製程替代，單日殺 9.6%，但之後 FY2026 共識 EPS 沒下修、FY2027 沒動；先進製程的簽核與硬體驗證沒有替代品。市場把頂層議價分散，誤讀成中間層被取代","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"進場","prior_role":"衛星"},"decision_out":{"role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場在 7 月把 45 奈米的開源示範當成先進製程替代，單日殺 9.6%，但之後 FY2026 共識 EPS 沒下修、FY2027 沒動；先進製程的簽核與硬體驗證沒有替代品。市場把頂層議價分散，誤讀成中間層被取代"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=9.84, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"進場"},"thesis":{"H":[{"id":"H1","text":"設計案數與設計複雜度帶動經常性營收維持中高雙位數有機成長","2y":"FY2027 經常性營收有機年增 ≥15%、在手訂單年增 ≥10%","5y":null,"10y":null,"threshold":"經常性營收有機年增 ≥15%（Q2 扣 Hexagon 約 4 點後為高十幾到 20%）","source":"每季 CFO commentary 與法說；在手訂單見季報新聞稿","drift_rule":"連 2 季低於門檻 5% 以上（<14.25%）為削弱；連 3 季低於門檻 10% 以上（<13.5%）為反轉"},{"id":"H2","text":"有機增量利潤率 50–60% 加上 Hexagon 轉增益，非 GAAP 營業利益率續擴張，EPS 成長快於營收","2y":"FY2027 非 GAAP 營業利益率 ≥45%（FY2026 指引中點 44.25%）","5y":null,"10y":null,"threshold":"FY2027 非 GAAP 營業利益率指引或實績 ≥45%","source":"2027 年 2 月全年財測、每季 CFO commentary","drift_rule":"連 2 季低於 42.75% 為削弱；連 3 季低於 40.5% 為反轉"},{"id":"H3","text":"agent 成為可揭露的新營收線，並帶動底層工具用量，EDA 占客戶研發預算續升","2y":null,"5y":"2028 年底前揭露 agent 營收或占比；2031 年 EDA 占客戶研發支出 ≥13%（現約 11%）","10y":null,"threshold":"首次揭露 agent 營收，且當期核心 EDA 年增 ≥15%","source":"法說、投資人會議、10-K","drift_rule":"核心 EDA 年增連 4 季低於 14.25% 為削弱；連 6 季低於 13.5% 為反轉"},{"id":"H4","text":"先進製程投片仍離不開商用 EDA 的簽核與硬體驗證，Cadence 在數位實作、類比、硬體驗證維持前二","2y":null,"5y":null,"10y":"到 2036 年，7 奈米以下量產投片仍全數使用商用簽核流程","threshold":"前十大晶片設計公司無一在 7 奈米以下以非商用工具量產投片","source":"產業新聞、台積電技術論壇、法說","drift_rule":"跨 2 個年度出現繞過案例為削弱；跨 3 個年度為反轉"}],"R":[{"id":"R1","text":"美國出口管制再收緊：關係企業 50% 規則暫停到 2026-11-09；2025 年 5 月曾要求對中國 EDA 出口許可、7 月撤回；10-K 承認已造成不利影響、無法預測後續，並可能招來中國報復。中國約占營收 13%","h_ref":"H1","clock":"⚡","threshold":"中國營收占比跌破 10%，或公司以出口管制為由下修全年財測","evidence_refs":["reg_tariff_export#4","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","major_events#4","product_recall_warning#0"]},{"id":"R2","text":"AI 資料中心投資見頂帶動客戶研發縮減：CEO 自稱資料中心在高峰（2026-09-09），IR 被問營收有沒有底時沒正面答（2026-08-26）","h_ref":"H1","clock":"🔥","threshold":"在手訂單年增轉負，或硬體營收連 2 季年減","evidence_refs":[]},{"id":"R3","text":"頂層被分走或被繞過：客戶要求自選大模型、自寫 agent 呼叫 Cadence 工具；Kimi K3 以開源工具在 45 奈米跑完流程，消息當天股價 −9.6%","h_ref":"H3","clock":"🐢","threshold":"前十大晶片設計公司在 7 奈米以下以非商用工具量產投片 1 例，或 agent 營收到 2028 年底仍未揭露","evidence_refs":["substitute_technology#0"]},{"id":"R4","text":"出口違規和解的後續義務：2025 年認罪協議、罰沒淨額合計 $140.6M、Q2 2025 認列 $128.5M 費用，需持續稽核與合規；財報明列 DOJ、BIS 可能再有行動","h_ref":"H1","clock":"🐢","threshold":"新的刑事或行政調查，或出口特權遭限制","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","reg_tariff_export#0","geo_supply_chain#5","major_events#3","sec_investigation_restatement#0"]},{"id":"R5","text":"硬體驗證仰賴單一或少數零件供應商與代工，供應中斷會卡住在手訂單出貨；CFO 說硬體目前是供給受限","h_ref":"H1","clock":"🔥","threshold":"硬體營收連 2 季年減且公司歸因供應","evidence_refs":["geo_supply_chain#1"]},{"id":"R6","text":"Hexagon 併購報酬：約 €2.70bn 買進 $160M 年營收、利潤率 5–10%，公司承諾 2027 轉增益","h_ref":"H2","clock":"🔥","threshold":"FY2027 財測未見 Hexagon 增益，或 SD&A 利潤率沒有改善","evidence_refs":["major_events#1","major_events#2"]}],"single_thing":{"description":"美國在 12–24 個月內恢復對中國 EDA 軟體與技術的出口許可要求（2025 年 5 月曾實施、7 月撤回），或 2026-11-09 關係企業規則到期後恢復並涵蓋主要中國客戶","why_fatal":"中國約占營收 13%（CFO 2026-04-27），以高毛利軟體為主；公司全年財測明寫假設出口規則不變。一次拿掉一半中國營收，約等於營收 −6% 到 −7%、EPS 約 −9%，並帶動倍數下修。這是數學上最大的單一離散衝擊，但不會毀掉先進製程的護城河","if_happens":"減碼至半倉，等公司新財測；若中國營收占比跌破 8% 且全年 EPS 指引下修超過 5% → 重跑研究","how_monitor":"BIS 公告、10-Q 風險揭露、每季法說的中國營收占比","probability":"約 25%：2025 年發生過一次又撤回，規則暫停到期日已確定，美中休戰讓恢復機率不低也不高"}},"appendix_a":{"growth_durability":8,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"高","fpe_fy2":32.4,"peg_fy2":1.9,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":8.14,"FY2027E":9.55,"FY2028E":11.15},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS；Koyfin 2026-09-19 共識快照；FY2025 實際值事實表未涵蓋"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 FY2026 財報（指引營收 $1,595–1,625M、非 GAAP EPS $2.01–2.07）","impact":"高","watch":"營收是否達指引下緣、在手訂單是否 ≥$8.1B、中國占比"},{"date":"2026-11-09","date_precision":null,"type":"regulatory","event":"BIS 關係企業 50% 出口規則暫停到期","impact":"高","watch":"是否延長、EDA 是否納入、公司是否調整財測"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 FY2027 全年財測","impact":"高","watch":"營收指引年增是否 ≥13%、非 GAAP 營業利益率是否 ≥45%、Hexagon 是否轉增益"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
