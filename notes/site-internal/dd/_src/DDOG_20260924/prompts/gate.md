你是 DD 管線 v20 的判斷層閘（gate），標的 DDOG（20260924）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1121.454 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；YoY +35.6%（去年同期 826.760）、QoQ +11.4%（+115.0M，公司稱為史上最大單季增量）（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：Zacks 共識約 1.08B，超出約 3.8%（來源：Yahoo Finance／Zacks 轉載）；也高於公司自家 Q2 指引上緣 1.08B（指引 1.07–1.08B）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income／margin＝257.031 USD M（利益率 22.9%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；含 DASH 年會成本約 15M（CFO 電話會）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：高於公司自家指引 225–235M（利益率 21–22%）；分析師共識未查得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income／margin＝5.455 USD M（利益率 0.5%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得共識（GAAP 端與 non-GAAP 差 251.6M，主要是股權激勵）
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation（占營收／占 non-GAAP 營業利益）＝220.251 USD M（占營收 19.6%；占 non-GAAP 營業利益 85.7%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；分項：營收成本 9.256M、R&D 131.682M、S&M 47.098M、G&A 32.215M。GAAP 營業利益僅 5.5M，故不以 GAAP 為分母（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi8_non_gaap_gross_margin_pr`（q1_business）｜Non-GAAP gross margin（公司未單獨揭露 product gross margin）＝79.6 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）：non-GAAP 毛利 892M；GAAP 毛利 881.341M（78.6%）出自 8-K Ex-99.1（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得共識；管理層稱毛利率長期在 80% 上下波動
- `f_kpi9_customers_with_arr_100k`（q1_business）｜Customers with ARR ≥ $100k＝4720 家（占 ARR 約 91%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release；占 ARR 比率出自 Q2 財報電話會（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi11_ai_native_1m_1m_arr_ai`（q1_business）｜AI-native 客戶群：年支出 ≥$1M 家數（公司未揭露全公司 ≥$1M ARR 家數，此為 AI 群組口徑）＝31 家（其中年支出 ≥$10M 為 8 家；AI 客戶群共約 750 家）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[11]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi15_ai_yoy`（q1_business）｜非 AI 客戶營收 YoY 成長＝高 20%（high 20s） %（公司只給區間）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CEO／CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[15]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_kpi12_net_revenue_retention_tr`（q1_business）｜Net revenue retention（trailing 12 個月）／gross revenue retention＝NRR 低 120%（low 120s）；GRR 中後段 90%（mid- to high 90s） %（公司只給區間，未給精確值）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）（numbers.latest_quarter_kpis.items[12]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：不適用
- `f_peer_ddog_gross_margin_pct`（q2_moat）｜DDOG 毛利率＝79.51 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ddog_operating_margin_pct`（q2_moat）｜DDOG 營業利益率＝0.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ddog_fcf_margin_pct`（q2_moat）｜DDOG FCF 利潤率＝27.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pltr_operating_margin_pct`（q2_moat）｜PLTR 營業利益率＝42.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLTR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crm_operating_margin_pct`（q2_moat）｜CRM 營業利益率＝21.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRM.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_now_operating_margin_pct`（q2_moat）｜NOW 營業利益率＝11.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msft_operating_margin_pct`（q2_moat）｜MSFT 營業利益率＝46.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crm_fcf_margin_pct`（q2_moat）｜CRM FCF 利潤率＝34.49 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRM.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_now_fcf_margin_pct`（q2_moat）｜NOW FCF 利潤率＝31.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pltr_fcf_margin_pct`（q2_moat）｜PLTR FCF 利潤率＝54.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLTR.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msft_fcf_margin_pct`（q2_moat）｜MSFT FCF 利潤率＝20.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.53 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.97 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-19）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.75 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-19）
- `f_kpi13_rpo_current_rpo`（q1_business）｜RPO／current RPO＝3470 USD M（YoY +43%；cRPO YoY 約 +40%，RPO 期間拉長）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q2 2026 財報電話會 CFO 準備稿（2026-08-06）；公司稱營收比 billings／RPO 更能反映業務趨勢（numbers.latest_quarter_kpis.items[13]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得 RPO 共識
- `f_kpi5_guidance_q3_fy2026_reven`（q1_business）｜Guidance: Q3 FY2026 revenue＝1135–1145 USD M（YoY +28–29%）｜期間與口徑：Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 稱指引已計入最大客戶用量下降（該客戶已續約）（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026）
  - 註記：Q3 營收共識未查得
- `f_kpi7_guidance_fy2026_revenue_`（q1_business）｜Guidance: FY2026 revenue／non-GAAP operating income／EPS＝營收 4450–4470M（YoY +30%）；non-GAAP 營業利益 1010–1030M（利益率 23%）；non-GAAP EPS 2.50–2.54（約 376M 稀釋股數） USD M／USD per share｜期間與口徑：Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；CFO 另給：淨利息及其他收入約 180M、現金稅 30–40M、non-GAAP 稅率 21%、capex＋資本化軟體占營收 4–5%（numbers.latest_quarter_kpis.items[7]，as_of Q2 FY2026 財報公告於 2026-08-06，指引期間 FY2026）
  - 註記：FY1 EPS 共識 2.53（2026-09-19 快照，來源：dd_numbers_extra.py consensus_revision），落在指引 2.50–2.54 內
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝278.704 USD M（FCF 利益率 24.9%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）；營業現金流 315.872M，扣 capex 與資本化軟體後（Q2 單季由上半年累計減 Q1 推得約 9.9M + 27.3M）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未查得共識
- `f_kpi6_guidance_q3_fy2026_non_g`（q1_business）｜Guidance: Q3 FY2026 non-GAAP operating income／EPS＝營業利益 260–270M（利益率 23–24%）；non-GAAP EPS 0.63–0.65（約 378M 稀釋股數） USD M／USD per share｜期間與口徑：Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investors.datadoghq.com Q2 2026 press release（8-K Ex-99.1 核對）（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026 財報公告於 2026-08-06，指引期間 Q3 FY2026）
  - 註記：未查得 Q3 共識
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝251.49 USD｜期間與口徑：2026-09-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝99.4 x｜期間與口徑：2026-09-19／分母＝FY1 EPS 2.53，分子＝快照價 251.49｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-19）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝502.98 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／3 個年度端點內的分位＝40.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝22.77 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝21.83 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.55 %｜期間與口徑：2026-06-23 → 2026-09-19／FY1 共識 EPS 2.42 → 2.53（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-09-19）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝103.98 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：FinancialContent 評論文章稱：Palo Alto Networks 收購 Chronosphere、Snowflake 收購 Observe，是把資料儲存、資安與監控合併成單一平台的趨勢，文章形容為對 Datadog 的「Pincer」夾擊威脅；並稱 Dynatrace 是企業市場「chief rival」（Davis AI 歷來被視為較成熟，但 Bits AI 推出後差距縮小），Cisco 正把 Splunk 的日誌優勢與網通硬體整合、主攻傳統企業。此為第三方評論文章的描述，非份額數據。
  - 來源：FinancialContent：Datadog (DDOG) and the 2026 Observability Frontier: Navigating the AI Re-Architecting Phase — https://www.financialcontent.com/article/finterra-2026-1-27-datadog-ddog-and-the-2026-observability-frontier-navigating-the-ai-re-architecting-phase（as_of 2026-01-27）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Datadog's largest customer renewed a nine-figure agreement but reduced its usage; per the search summary of the TheStreet article, this affected the company's Q3 and full-year 2026 forecasts. Article body not retrieved (WebFetch returned 403), so the exact contract figures and whether the usage cut involved in-house or a second vendor are not confirmed.
  - 來源：TheStreet, 'Datadog's largest customer renews deal but cuts usage' https://www.thestreet.com/investing/stocks/datadogs-largest-customer-renews-deal-but-cuts-usage（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear、valuation、triggers
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：SaaStr states 'OpenAI is Datadog's biggest single customer' (analyst assessment, not a company-named disclosure), and that the AI-native cohort including it grew only 'high single digits' in Q1 2026.
  - 來源：SaaStr, 'Datadog Stock Is Up +66%. Here Are 5 Reasons Why...' https://www.saastr.com/datadogup/（as_of 2026-05-25）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#4`（customer_second_source｜方向 -｜狀態 ok）：Per the same secondary source, one large AI-native customer's decision in early 2024 to scale down and partially re-platform its observability stack onto internal tooling drove the public growth deceleration that began with the Q1 2024 print.
  - 來源：Mungomash, 'Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail' https://mungomash.com/orgs/datadog/financials/（as_of 2024-05-07）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Q2 2026 法說會：管理層不點名最大客戶，只說是「一家領先的 AI 公司」，使用 17 項 Datadog 產品，剛完成一筆「九位數美元」的續約。續約後用量有下降（usage reduction），已納入 Q3 與 FY2026 財測；CEO Pomel 稱今年剩餘時間的財測已「fully derisked」。
  - 來源：The Motley Fool, Datadog (DDOG) Q2 2026 Earnings Call Transcript, https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/（as_of 2026-08-13）｜affects：thesis.R、decision_inputs.bear、valuation、triggers
- `customer_concentration_credit#5`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K（2026-02-18 提交）有「AI-native cohort」一詞，並註明該客群「包含我們最大的客戶」；該客群對 2025 年 12 月底當季營收年增的貢獻約 7 個百分點。（二手來源轉述，未讀到 10-K 原文；未查到 10-K 是否列出單一客戶占營收 ≥10% 的具體百分比。）
  - 來源：mungomash.com「Datadog Financials — revenue, customer concentration, net retention, the OpenAI disclosure trail」（搜尋摘要轉述 FY2025 10-K；頁面 WebFetch 回 404，未能直接驗證）（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Gartner's observability report says more than 40 vendors compete in the space (20 evaluated in the Magic Quadrant), that 'questions about total cost of ownership are now standard', and that leading platforms must offer granular data retention controls, tiered storage and usage-based pricing.
  - 來源：Network World, 'In crowded observability market, Gartner calls out AI capabilities, cost optimization, DevOps integration' https://www.networkworld.com/article/4032218/in-crowded-observability-market-gartner-calls-out-ai-capabilities-cost-optimization-devops-integration.html（as_of 2025-08-06）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `supply_demand_durability#7`（supply_demand_durability｜方向 -｜狀態 ok）：Grafana Labs reached $400M+ ARR with 7,000 customers as of September 2025 (competitor scale figure cited in a vendor comparison blog; blog publish date not shown, as_of day set to the first of the stated month).
  - 來源：OpenObserve blog, '10 Best Datadog Competitors & Alternatives in 2026' https://openobserve.ai/blog/datadog-competitors/（as_of 2025-09-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：最大客戶出現用量下滑（同時簽了九位數美元續約）；管理層稱已把此影響完整反映在 Q3 與全年 2026 指引，並稱排除該客戶後整體趨勢與加速一致。
  - 來源：Motley Fool, Datadog Q2 2026 Earnings Call Transcript（WebFetch 摘要）https://www.fool.com/earnings/call-transcripts/2026/08/13/datadog-ddog-q2-2026-earnings-call-transcript/ ；GuruFocus Q2 2026 highlights（as_of 2026-08-06）｜affects：decision_inputs.bear、thesis.R、triggers
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：指引：Q3 營收 $1.135B–$1.145B（年增 28%–29%，低於 Q2 的 36%）；全年 2026 營收 $4.45B–$4.47B（年增約 30%）。
  - 來源：GuruFocus, Datadog Q2 2026 Earnings Call Highlights https://www.gurufocus.com/news/9014386/datadog-inc-ddog-q2-2026-earnings-call-highlights-revenue-surges-36-to-112b-aidriven-growth-accelerates（as_of 2026-08-06）｜affects：valuation、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：groundcover（Datadog 競品廠商）2026-07-29 的指南結論稱：2026 年可觀測性品類的轉變是架構面的——以 eBPF 取代語言 agent、以 BYOC（資料留在客戶自己的 VPC）取代純 SaaS、以「依基礎設施計價」取代「依用量計價」。此為競品自家行銷文章的說法，非中立第三方量測。
  - 來源：groundcover, 'Datadog Alternatives for Full-Stack Observability in 2026', https://www.groundcover.com/guides/datadog-alternatives-for-full-stack-observability（as_of 2026-07-29）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：IT Connection（Currentanalysis）2026 年觀測性預測稱：應用開發工具類新創將透過在自家產品組合內增加可觀測性功能，對整個可觀測性市場產生破壞性影響（標題：Makers of Dev Tools to Disrupt Space）。搜尋摘要只取得此論點，未取得內文細節與具體廠商名單。
  - 來源：IT Connection / Currentanalysis, 'Observability Predictions 2026: Makers of Dev Tools to Disrupt Space', https://itcblogs.currentanalysis.com/2026/01/29/observability-predictions-2026-makers-of-dev-tools-to-disrupt-space/（as_of 2026-01-29）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：搜尋摘要稱 Q2 上調全年指引的同時，公司揭露最大客戶用量下降，並引述企業需求與 AI 產品採用為上調依據；Simply Wall St 標題稱股價在此消息後下跌 14.9%（該文未在摘要中註明計算區間）。
  - 來源：Simply Wall St News — Datadog (DDOG) Is Down 14.9% After Raising 2026 Outlook And Deepening AI, Log Partnerships — https://simplywall.st/stocks/us/software/nasdaq-ddog/datadog/news/datadog-ddog-is-down-149-after-raising-2026-outlook-and-deep/amp（僅取搜尋摘要，未 fetch 原文）（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 23 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":450.0,"bear_5y_price":94.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":7.4,"ev5y_pct":4.3,"irr_base_pct":1.4,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.53,"pe":99.4,"basis":"FY2026E（FY1）非GAAP稀釋EPS共識2.53；終端倍數同樣套在當年度非GAAP EPS上"},"eps":{"bull":[3.15,4.05,5.05,6.2,7.5],"base":[2.97,3.75,4.45,5.2,6.0],"bear":[2.7,2.8,2.85,2.9,2.95]},"pe":{"bull":60,"base":45,"bear":32},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":13},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DDOG_Q1_2026_Earnings_Call_20260507.md
- 2026-05-07｜CEO Olivier Pomel｜guidance：CEO 表示 Q1 營收高於財測區間上緣（原話："year-over-year and above the high end of our guidance range"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 給 Q2 營收財測 10.7 億至 10.8 億美元（年增 29%–31%）（原話："in the range of $1.07 billion to $1.08 billion"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說 Q2 財測隱含季增 6400 萬至 7400 萬美元、季增 6%–7%（原話："$64 million to $74 million or 6% to 7%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 給 Q2 non-GAAP 營業利益率財測 21%–22%（原話："an operating margin of 21% to 22%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 說 DASH 用戶大會 Q2 成本約 1500 萬美元，已計入營業利益財測（原話："$15 million and which we have reflected in our operating"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 給 FY2026 營收財測 43 億至 43.4 億美元（年增 25%–27%）（原話："in the range of $4.3 billion to $4.34 billion"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 給 FY2026 non-GAAP 營業利益率財測 22%–23%（營業利益 9.4 億至 9.8 億美元）（原話："which implies an operating margin of 22% to 23%"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說明財測方法：以近月趨勢為基礎並打折（原話："apply conservatism on these growth trends"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說對最大客戶的財測與上季一樣採更高程度的保守（原話："a higher degree of conservatism to our largest customer"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 答分析師：最大客戶與整體的財測方法與上季相同、沒有改（原話："The answer is no. It's the same methodology"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 說 4 月的 ARR 成長延續 Q1 每月加速的趨勢（原話："a continuation of these healthy growth trends in April"）
- 2026-05-07｜CFO David Obstler｜guidance：CFO 重申看營收比看 billings 與 RPO 更能反映業務趨勢（口徑）（原話："we continue to believe revenue is a better indicator of"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 報 RPO 34.8 億美元、年增 51%（原話："RPO, was $3.48 billion, up 51% year-over-year"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 RPO 天期拉長，因 Q1 多年期合約占比上升（原話："RPO duration increased year-over-year as the mix"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 gross profit 8.07 億美元、毛利率 80.2%（上季 81.4%）（原話："gross profit was $807 million with a gross margin of 80.2%"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 解釋毛利率逐季波動的口徑：創新投入與效率措施互抵（原話："investments into innovations for our customers, offset by"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 OpEx 年增 31%（上季 29%）（原話："Our Q1 OpEx grew 31% year-over-year versus 29% last quarter"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 說 OpEx 成長反映招聘計畫的執行（原話："is an indication of our execution of our hiring plans"）
- 2026-05-07｜CFO David Obstler｜margin：CFO 報 Q1 營業利益率 22%（上季 24%）（原話："22% operating margin compared to 24% last quarter"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 報 Q1 自由現金流 2.89 億美元、FCF 利潤率 29%（原話："was $289 million and free cash flow margin was 29%"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 給 FY2026 資本支出加資本化軟體占營收 4%–5%（原話："together to be 4% to 5% of revenue in fiscal 2026"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 說多數工作負載跑在雲端，成本走 OpEx 不走 CapEx（原話："meaning you'll see all of that in OpEx, not in CapEx"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 承諾若資本支出模式改變會告知市場（原話："If it changes, we'll tell you"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 說正在加碼投資，特別是 R&D 與自家訓練的模型規模（原話："We are definitely ramping up our investments, in particular"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 說 go-to-market 投資與銷售產能擴張正在見效（原話："are paying off and were the right decision"）
- 2026-05-07｜CFO David Obstler｜capital_allocation：CFO 說公部門業務在 FedRAMP 認證之前就先投資業務與通路（原話："we invested ahead of the certifications"）
- 2026-05-07｜CEO Olivier Pomel｜capital_allocation：CEO 把 bring-your-own-cloud 產品列為投資方向之一（原話："area of investment is our bring your own cloud products"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說非 AI 客戶營收成長加速到 20% 中段（上季 23%）（原話："to mid-20s percent year-over-year up from 23% last quarter"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 AI 原生客戶成長明顯快於其餘業務（原話："AI native customer growth continues to significantly outpace"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 報 TTM 淨營收留存率低 120%（上季約 120%）（原話："the low 120%, up from about 120% last quarter"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說新客戶年化 bookings 創歷史新高（原話："New logo annualized bookings set a new all-time record"）
- 2026-05-07｜CFO David Obstler｜customer：CFO 說 Q1 ARR 新增分布廣、不集中（原話："was very broad-based and was not very concentrated"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說扣掉 Q4 簽下、Q1 貢獻營收最多的那位客戶，ARR 新增仍創紀錄（原話："we still had a record quarter in terms of ARR adds"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說 Q1 新簽了幾家目前尚無營收貢獻、預期未來會很大的客戶（原話："customers in Q1 that don't contribute any revenue yet"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說 Q1 與兩家大型科技公司的 AI 研究部門簽下一筆七位數與一筆八位數年化合約（原話："a 7-figure and an 8-figure annualized deals"）
- 2026-05-07｜CEO Olivier Pomel｜customer：CEO 說送出 AI 整合資料的客戶約占客戶數 20%、占 ARR 約 80%（原話："they represent about 80% of our ARR"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 56% 客戶使用 4 個以上產品（一年前 51%）（原話："56% of our customers now use 4 or more products"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說其餘 18 個較早期產品各自有潛力長到超過 1 億美元 ARR（原話："potential to grow to more than $100 million over time"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 Bits AI SRE agent 的調查次數 12 月到 3 月翻倍以上（原話："have more than doubled from December to March"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說 Bits Assistant 訊息數該期間成長 12 倍（原話："Bits Assistant messages increased by a factor of 12"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 把 AI 列為除數位轉型與雲端遷移之外的新增長期成長動能（原話："we now have an additional secular growth driver with AI"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 答 agent 與人類用量問題：看到 agent 用量大幅成長（原話："we see both a stratospheric increase of agent usage"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說用量由人或 agent 產生對計價模式沒差，因為是用量計價（原話："we don't care whether most of the usage is humans"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 自述與去年說法不同：去年說訓練還不是 Datadog 的市場（原話："workloads and training is not really a market for us yet"）
- 2026-05-07｜CEO Olivier Pomel｜product：CEO 說客戶自家環境部署（cloud prem）目前不是市場最大的部分（原話："Today, it's not the largest part of the market"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 預告 DASH 大會將發布多項新產品與公告（原話："sharing many new products and future announcements"）
- 2026-05-07｜CEO Olivier Pomel｜commitment：CEO 預告 agent 安全與權限機制的內容將在大會上多談（原話："you should expect to hear more about that at our conference"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說 Datadog 在規模上勝過所有競爭對手並在搶市占（原話："all of our competitors at scale, and we're taking share"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 描述客戶常見狀況：各部門散落多套工具，來找 Datadog 整併（原話："customers have 4, 6, 7, 15, 25 different things"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說超大型雲端業者通常有自己全部自建的文化（原話："typically have a culture of building everything themselves"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 說這些超大型雲端業者這季來找 Datadog 取代部分原本自用的東西（原話："like they come to us to replace some of the things"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 舉例：一家財星 500 大銀行把剩餘日誌資料遷入，完全取代原日誌供應商（原話："replacing their legacy log vendor"）
- 2026-05-07｜CEO Olivier Pomel｜competition：CEO 舉例：一家對沖基金以 Datadog 取代整個地端開源監控層（原話："replace their entire on-prem observability layer"）
- 2026-05-07｜CFO David Obstler｜risk：CFO 答地緣與消費景氣提問：目前在消費與電商業務尚未看到影響（原話："any particular effect in the consumer businesses"）
- 2026-05-07｜CEO Olivier Pomel｜risk：CEO 說超大型雲端業者訓練負載的採用還早，不宣稱勝利（原話："So again, it's too early in the product life cycle"）
- 2026-05-07｜CEO Olivier Pomel｜risk：CEO 說擁有異質晶片環境的公司目前仍是極少數（原話："that is still a very small number of companies"）

### DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md
- 2026-02-12｜David Obstler (CFO)｜guidance：毛利率規劃維持在正負 80% 左右，並保留彈性投資平台、資料中心與產品（原話："planning our gross margins plus or minus 80%"）
- 2026-02-12｜David Obstler (CFO)｜commitment：重申長期營業利益率目標 25% 以上，並稱與上一次投資人日所說相同（原話："long-term target of an operating margin at 25% plus"）
- 2026-02-12｜David Obstler (CFO)｜margin：R&D 占營收比重的目標約 30%，並稱有波動（原話："this has been our target around 30%"）
- 2026-02-12｜David Obstler (CFO)｜margin：稱 AI 的使用可能成為 R&D 占比的槓桿之一，未量化（原話："some things about the use of AI that might be levers here"）
- 2026-02-12｜David Obstler (CFO)｜margin：銷售與行銷費用占營收比重，原文下一行接「roughly the mid-20s range」（原話："keep that sales and marketing as a percentage of revenues"）
- 2026-02-12｜David Obstler (CFO)｜margin：G&A 占營收約 5%（原話："Thank you for all the hard work you do there at around 5%"）
- 2026-02-12｜David Obstler (CFO)｜margin：去年 non-GAAP 營業利益率 22%；前一句稱現金流利潤率 27%（原話："So, it's all non-GAAP, and it was 22%"）
- 2026-02-12｜David Obstler (CFO)｜margin：解釋營業利益率有波動：消費型模式的變動快過招聘速度（原話："that changes faster than we can hire people"）
- 2026-02-12｜Unknown Executive｜margin：答覆 $10M 客戶與 $10 萬客戶的獲利結構差異時，改談加權平均後毛利率大致不變（原話："maintain our margins the same at the gross"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：淨股數稀釋目標為 2.5% 至 3%（原話："our target in net share dilution, which is 2.5% to 3%"）
- 2026-02-12｜David Obstler (CFO)｜capital_allocation：併購策略強調審慎，過去聚焦補技術能力（前後文提到 Eppo、Metaplane）（原話："a thoughtful and disciplined acquisition strategy"）
- 2026-02-12｜Olivier Pomel (CEO)｜capital_allocation：長期以約 30% 營收投入 R&D，2025 年超過 $10 億、約 4,000 名工程師（原話："we've invested about 30% of revenues into R&D"）
- 2026-02-12｜Sean Walters (CRO)｜capital_allocation：宣布開始試行資安專屬銷售團隊（原話："we decided to start a pilot of security-focused sales teams"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：稱 R&D 支出約為最接近同業的 3 倍（原話："about 3x the R&D spend of our next closest peer"）
- 2026-02-12｜Sean Walters (CRO)｜competition：稱資安市場的競爭對手正在整併（原話："competitors in this space consolidating"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：承認事後排查類需求用 Claude Code 這類工具也能得到不錯結果（逐字稿拼作 Cloud Code）（原話："you can get a pretty good result if you ask Cloud Code"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱預防性、主動式場景無法靠通用 coding agent 完成，因資料不會流經它們（原話："that just doesn't work at all because the data doesn't flow"）
- 2026-02-12｜Michael Whetten｜competition：回應通用 LLM 的程式碼資安能力：稱自家優勢是看得到程式碼在正式環境的部署狀況（原話："we can see how that code is deployed in production"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱 coding agent 會持續存在且做更多，公司定位是補充而非取代（原話："the agents are here to stay and they're going to do more"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜competition：被問進入門檻時，承認小模型沒有明確的資金門檻，護城河放在資料品質（原話："don't think there's a clear financial barrier of entry"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：回應 OpenTelemetry：稱資料收集從來不是護城河（原話："The collection has never been the moat"）
- 2026-02-12｜Adam Blitzer (COO)｜competition：自我定位為觀測市場中的高價位產品（原話："Datadog is a premium product"）
- 2026-02-12｜Olivier Pomel (CEO)｜competition：稱觀測市場占有率仍只在十幾個百分點中段（原話："our market share is still only in the mid-teens"）
- 2026-02-12｜David Obstler (CFO)｜competition：觀測市場規模 $300 億以上；擴大到資安、軟體交付等後 TAM 稱超過 $1,000 億（原話："a $30 billion-plus market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：基礎設施監控 ARR 達 $16 億，日誌與 APM 各超過 $10 億（原話："$1.6 billion of ARR in infrastructure monitoring"）
- 2026-02-12｜Tim Knudsen｜product：資安產品 ARR 已超過 $1 億（原話："we've now surpassed $100 million in ARR"）
- 2026-02-12｜Tim Knudsen｜product：百萬美元客戶中 70% 用至少一項資安產品，但資安只占其 Datadog 支出 2%（原話："together is only 2% of their Datadog spend"）
- 2026-02-12｜Yrieix Garnier｜product：Flex Logs 的 ARR 接近 $1 億且快速成長（原話："approaching $100 million ARR and growing very rapidly"）
- 2026-02-12｜Yrieix Garnier｜product：BYOC（自帶雲）已有大型公司在預覽，並預期打開更多機會（原話："engaged with very large companies and previewing BYOC"）
- 2026-02-12｜Yanbing Li (CPO)｜product：Bits AI SRE 一月單月就有超過 2,000 家客戶跑調查（原話："more than 2,000 customers run investigation with Bits AI"）
- 2026-02-12｜Yuka Broderick｜product：Bits AI SRE 公開定價為每 20 次調查 $500（原話："Bits AI SRE $500 per 20 investigations"）
- 2026-02-12｜Yanbing Li (CPO)｜product：MCP server 自推出後用量呈指數式成長（原話："we've seen also exponential adoption and growth"）
- 2026-02-12｜David Obstler (CFO)｜product：LLM Observability 的 span 量一年增加 10 倍（原話："the last year, that has increased 10x"）
- 2026-02-12｜Alexis Le-Quoc (CTO)｜product：訓練時序模型 Toto 2025 年花費約 $75 萬（原話："We spent about $750,000 to train this"）
- 2026-02-12｜David Obstler (CFO)｜product：數位體驗監控（DEM）已大到公司也稱之為第四支柱（原話："we are also calling that a fourth pillar"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：承認對功能旗標與實驗平台的看法改變（過去視為商品化）（原話："we've changed our minds quite a bit on the topic"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：資料可觀測性過去被視為周邊市場，現在升到優先清單前列（原話："We thought also this was an interesting market"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：被問自主營運何時到來，稱無法判斷是一年或三年（原話："hard to tell whether we get there in a year or in 3 years"）
- 2026-02-12｜Unknown Executive｜product：被問自主營運的計價模式時，稱距離談定價還太遠（原話："too far away to be talking about pricing models"）
- 2026-02-12｜Olivier Pomel (CEO)｜product：預期今年會有相當多公司把 AI 寫程式的轉換推進（原話："I would expect quite a bit of that to happen this year"）
- 2026-02-12｜Unknown Executive｜guidance：把財測保守度歸因於用量計價模式（原話："some of the conservatism we put in guidance"）
- 2026-02-12｜Unknown Executive｜commitment：稱對中期走勢很有信心，短期用量則不確定（原話："we're very confident about where we'll be in the midterm"）
- 2026-02-12｜Sean Walters (CRO)｜commitment：銷售團隊剛開完年度啟動會，稱全面投入 AI 銷售並已訓練每位業務（原話："we are going all in on AI"）
- 2026-02-12｜Unknown Executive｜risk：承認短期用量走勢無法確知（原話："how the usage is going to trend in 1 month from now"）
- 2026-02-12｜Unknown Executive｜risk：承認客戶會定期做用量優化，有時是公司主動建議（原話："we do see optimization on a regular basis"）
- 2026-02-12｜Olivier Pomel (CEO)｜risk：稱多數公司仍處於 AI 寫程式轉換的早期（原話："most companies are still early in the transition there"）
- 2026-02-12｜David Obstler (CFO)｜customer：新增客戶貢獻每年 ARR 成長約四分之一（原話："about 1/4 of that ARR growth each"）
- 2026-02-12｜David Obstler (CFO)｜customer：ARR 成長其餘約四分之三來自既有客戶多用產品與交叉銷售（原話："the remaining approximately 3/4 comes from"）
- 2026-02-12｜David Obstler (CFO)｜customer：客戶數超過 32,000，占約 50 萬目標客戶的邏輯數僅 7%（原話："that's a penetration in logos of only 7%"）
- 2026-02-12｜David Obstler (CFO)｜customer：百萬美元客戶今年成長到超過 600 家（原話："our $1 million customers, which this year grew to over 600"）
- 2026-02-12｜David Obstler (CFO)｜customer：首度揭露年花費超過 $1,000 萬的客戶指標；逐字稿數字為「over 60% growth, and that's now 34%」，未給明確客戶數，原文口徑不清（原話："growing quite rapidly, over 60% growth, and that's now 34%"）
- 2026-02-12｜David Obstler (CFO)｜customer：AI 原生客戶去年底占營收約 11%（原話："at the end of last year was about 11% of revenues"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：前 20 大 AI 原生公司中有 14 家用 Datadog，AI 原生客戶群超過 650 家（原話："14 of the top 20 AI native companies are using Datadog"）
- 2026-02-12｜David Obstler (CFO)｜customer：整體毛留存率 97% 以上（企業 98% 以上，中小與中型 96% 以上）（原話："retention percentage. It's 97% plus in the company"）
- 2026-02-12｜David Obstler (CFO)｜customer：只有約一半客戶同時使用三大支柱（原話："only about half of our customers use all three pillars"）
- 2026-02-12｜David Obstler (CFO)｜customer：三大支柱都用的客戶，花費是其他客戶的 15 倍（原話："In fact, they spend 15x more"）
- 2026-02-12｜David Obstler (CFO)｜customer：一半客戶用 4 項以上產品，用 10 項以上的僅 9%（原話："half of our customers have 4-plus products"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 業務第二年的目標從開會數轉向營收與成交（原話："goals are shifted much more to revenue and closing deals"）
- 2026-02-12｜Sean Walters (CRO)｜customer：Key accounts 2025 年有比預期快的成交，且正快速擴張（原話："wins that are already expanding very rapidly"）
- 2026-02-12｜Sean Walters (CRO)｜customer：財星 500 大客戶的花費中位數不到 $50 萬（原話："is still modest at less than $0.5 million per customer"）
- 2026-02-12｜Sean Walters (CRO)｜customer：拉美約占營收 5%，成長遠快於整體（原話："they're growing far faster than our overall revenue"）
- 2026-02-12｜Sean Walters (CRO)｜customer：只稱 2025 訂單表現「stellar」，未給金額（原話："shows our bookings by year, including a stellar 2025"）
- 2026-02-12｜Adam Blitzer (COO)｜customer：計價為用量基礎並有量、承諾、多產品、期限等折扣，稱客戶越成長曲線越彎（原話："We have volume-based pricing"）
- 2026-02-12｜Unknown Executive｜customer：解釋客戶 ARR 出現短期下滑：簽更長期承諾換折扣時可能暫時下降（原話："it might drop you temporarily from where you were"）
- 2026-02-12｜Unknown Executive｜customer：承認過去幾年偏重從既有大客戶擴張，較少花力氣從零開發新客戶（原話："bit victims of our own success"）

### DDOG_Canaccord_Genuity_s_46th_Annual_Growth_Conference_20260812.md
- 2026-08-12｜David Obstler｜guidance：CFO 說明財測做法：拿長期觀察到的成長率，再打折留緩衝。（原話："we take that growth rate that we see over a long period"）
- 2026-08-12｜David Obstler｜guidance：CFO 稱過去 beat and raise 的實績是客戶實際支出高於財測扣掉的折數。（原話："spend more than the amount we're discounting"）
- 2026-08-12｜David Obstler｜guidance：CFO 稱公司每天看得到客戶用量，稱之為近乎完整的資訊（作為財測依據）。（原話："So it's almost perfect information."）
- 2026-08-12｜David Obstler｜guidance：CFO 稱每天早上醒來就能按客戶切分看到用量。（原話："I can see the usage when I wake up in the morning"）
- 2026-08-12｜William Kingsley Crane｜margin：分析師在提問中描述公司目前自由現金流在高 20% 區間（分析師口述，非管理層）。（原話："free cash flow in the high 20s"）
- 2026-08-12｜David Obstler｜margin：CFO 稱利潤率沒有變化。（原話："You can see our margins haven't changed, right?"）
- 2026-08-12｜David Obstler｜margin：CFO 把 token 支出描述為資源重新分配，而非利潤率侵蝕。（原話："it's more of a distribution than a margin erosion"）
- 2026-08-12｜David Obstler｜margin：CFO 稱研發投入的配置會更偏向 token，而非人力。（原話："is going to move more towards tokens than it is to humans"）
- 2026-08-12｜David Obstler｜margin：CFO 說明淨留存率的口徑：講的是 120% 出頭（low 120s）。（原話："net retention that we talked about in the 120s, low 120s"）
- 2026-08-12｜David Obstler｜margin：CFO 說明多產品採用數（cross-sell 指標）的口徑：每年擴大定義。（原話："we expand the definition of cross-sell"）
- 2026-08-12｜David Obstler｜commitment：CFO 稱銷售產能會繼續投資。（原話："So that we're going to continue to invest in."）
- 2026-08-12｜David Obstler｜commitment：CFO 稱研發會以高比率持續投入。（原話："invest at a high rate, but it's very likely"）
- 2026-08-12｜David Obstler｜commitment：CFO 說明揭露慣例：不預告某產品會做到 $1 billion。（原話："We don't go like we're going to have $1 billion of this"）
- 2026-08-12｜David Obstler｜commitment：CFO 說明揭露慣例：達到某個量級後才對外公布。（原話："when we get to certain amounts, we tell everybody"）
- 2026-08-12｜David Obstler｜commitment：CFO 劃定安全產品範圍：不做桌面安全。（原話："we're not saying we're going to secure desktops"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱全球銷售配額產能已成功擴張。（原話："successfully ramped quota capacity on a global basis"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱配額產能的擴張幅度與營收大致相當。（原話："it's been roughly in line with revenues"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 稱市場尚未飽和，銷售仍有拓展空間。（原話："we're not at the point where we saturated the market"）
- 2026-08-12｜David Obstler｜capital_allocation：CFO 提到公司剛完成一筆收購（分析師後續提問稱之為 Adaptive ML 研究實驗室，該名稱為分析師以 I think 帶出）。（原話："We just made an acquisition."）
- 2026-08-12｜David Obstler｜competition：CFO 稱平台整合帶動交叉銷售與搶市占。（原話："That's enabled us to cross-sell and also take market share"）
- 2026-08-12｜David Obstler｜competition：CFO 稱上一季營收環比增加 $115 million。（原話："I think we said sequentially, we grew $115 million of"）
- 2026-08-12｜David Obstler｜competition：CFO 把該季度增量以季度基礎看作超過 $400 million 的業務規模，並拿來與競爭對手比較。（原話："think of that as over $400 million of business"）
- 2026-08-12｜David Obstler｜competition：CFO 稱與競爭對手相比，市占增幅非常大。（原話："the market share gains are very substantial"）
- 2026-08-12｜David Obstler｜competition：CFO 稱大客戶自建與外購並存，但整體淨傾向是買 Datadog。（原話："towards not doing it yourself but buying Datadog"）
- 2026-08-12｜David Obstler｜competition：CFO 稱公司從零成長到超過 $4.5（下一行接 billion）；原文未標明是營收或 ARR。（原話："That's what's produced from 0 Datadog to over $4.5"）
- 2026-08-12｜David Obstler｜competition：CFO 稱在 observability 領域有很大的競爭優勢，不是在通用模型訓練上。（原話："there's just a tremendous competitive advantage"）
- 2026-08-12｜David Obstler｜competition：CFO 稱他人跨界進攻（Snowflake、Palo Alto、Splunk 之類）並未改變競爭態勢。（原話："And it hasn't changed the competitive dynamic"）
- 2026-08-12｜David Obstler｜competition：CFO 稱對這段期間來說，結果是 Datadog 的競爭地位增強而非削弱。（原話："a strengthening of the competitive position of Datadog"）
- 2026-08-12｜David Obstler｜product：CFO 稱目前主要監控生產環境，並開始做更多訓練端的監控。（原話："We're starting to do more in training."）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI 監控（Datadog for AI）領域成長良好。（原話："we've been seeing very good growth in that area"）
- 2026-08-12｜David Obstler｜product：CFO 指出已對外揭露的 AI 指標包括 agent 監控與 MCP 呼叫成長。（原話："the growth of agent monitoring, the growth of MCP calls"）
- 2026-08-12｜David Obstler｜product：CFO 稱這些指標成長率很高，但仍在早期。（原話："these things are growing at a very high rate"）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI 監控的變現方式是產品 GA 時公布定價。（原話："monetizing it through pricing we publish as we put into GA"）
- 2026-08-12｜David Obstler｜product：CFO 稱 AI for Datadog（Bits）有動能，管理層持樂觀態度。（原話："we're seeing traction in that, which we're optimistic"）
- 2026-08-12｜David Obstler｜product：CFO 稱推動需求的是客戶把 LLM 應用放上生產環境。（原話："clients are putting LLM-enabled applications in production"）
- 2026-08-12｜David Obstler｜product：CFO 稱公司投資於 observability 專用的智能。（原話："specialized intelligence that we're investing in"）
- 2026-08-12｜David Obstler｜product：CFO 描述產品方向是往自我修復（self-remediation）走。（原話："something that's going to move towards self-remediation"）
- 2026-08-12｜David Obstler｜product：CFO 承認自我修復尚未達成，仍在路上。（原話："We're not quite there yet, but that's what the vision is"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 的定價正在試驗（與分析師所述的按調查計價轉為按 token 計價有關）。（原話："We play around with pricing"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 新定價早期反應與使用良好。（原話："early signs are a lot of good reception and use"）
- 2026-08-12｜David Obstler｜product：CFO 稱 Bits 從可靠性調查擴展到安全與軟體開發。（原話："we're also investing in security and software creation"）
- 2026-08-12｜David Obstler｜product：CFO 稱安全業務聚焦在雲端工作負載相關領域。（原話："working on the security of modern cloud workloads"）
- 2026-08-12｜David Obstler｜risk：CFO 承認疫後 ZIRP 時期曾有一些過度使用。（原話："was probably some usage that was over usage"）
- 2026-08-12｜David Obstler｜risk：CFO 承認 AI 原生客群可能有波動。（原話："is there going to be volatility there? Yes, there might be"）
- 2026-08-12｜David Obstler｜risk：CFO 稱公司不是按席位計價，模式與工作負載由 agent 或人處理無關。（原話："we're not a seat model"）
- 2026-08-12｜David Obstler｜risk：CFO 稱收費依據是流經平台的工作負載。（原話："monetizing based on the workloads that go through"）
- 2026-08-12｜David Obstler｜customer：CFO 稱客戶端有強勁的平台投資，部分是為了 AI 做準備。（原話："there's a strong investment in platform right now"）
- 2026-08-12｜David Obstler｜customer：CFO 回答非 AI 原生客群時稱，企業客戶的加速已進入 upper 20s。（原話："upper 20s, and that's enterprises and stuff"）
- 2026-08-12｜David Obstler｜customer：CFO 稱 AI 原生客戶名單分散：750 個以上，其中 30 個以上超過 $1 million。（原話："We had over 750 names, over 30 of them having $1 million"）
- 2026-08-12｜David Obstler｜customer：CFO 稱 AI 原生客群佔 ARR 的比重比疫情高峰時小得多。（原話："a much smaller group as a percentage of ARR"）
- 2026-08-12｜David Obstler｜customer：CFO 說明合約結構：採 take-or-pay 合約。（原話："we have take-or-pay contracts"）
- 2026-08-12｜David Obstler｜customer：CFO 說明合約設有基本承諾額，客戶不能低於該額度。（原話："we have a base of commitment, so they can't spend less"）

### DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜CEO｜customer：CEO 憑記憶引述上季營收年增 36%，並先說明數字可能有些微出入（引述自一個月前財報，非本場新揭露）。（原話："we accelerated to the, I think, 36% year-over-year growth"）
- 2026-09-08｜CEO｜customer：CEO 說非 AI 客戶群一年前年增約 18%，現在已到 20% 後段（原話 high 20s）；數字為口述、非本場新揭露。（原話："18% year-over-year growth for that part of the business"）
- 2026-09-08｜CEO｜competition：CEO 說可觀測性大概是 AI 轉型後唯一留下的軟體類別。（原話："Observability is probably the only category that remains."）
- 2026-09-08｜CEO｜competition：CEO 引述自家在可觀測性市場的占有率約 13%–14%。（原話："We have about 13%, 14% market share."）
- 2026-09-08｜CEO｜guidance：CEO 說以現有市占與市場成長，光核心業務就有 5 到 10 倍成長空間；無時間框架、非正式財測。（原話："how we can grow 5 or 10x from that"）
- 2026-09-08｜CEO｜product：CEO 說 AI 建置約八九成與雲端建置相同。（原話："80% or 90% of the AI build-out actually looks like"）
- 2026-09-08｜CEO｜product：CEO 說目前成長最快的是「Datadog for AI」（觀察 AI 整條技術堆疊）。（原話："growing the fastest is Datadog for AI"）
- 2026-09-08｜CEO｜product：CEO 說 AI 技術堆疊今天約 7 到 8 成和非 AI 相同（與前面「AI 建置 8–9 成像雲端」是兩個不同口徑的比例）。（原話："like 70%, 80% of the stack is the same"）
- 2026-09-08｜CEO｜product：CEO 說 AI 介面（agent、traces）流量暴增，但那是指出未來方向，目前還不是營收主要驅動。（原話："rather than already today being the driving part"）
- 2026-09-08｜CEO｜product：被問 Bits AI 在財報哪裡看得到，CEO 說目前財報上還看不出來。（原話："you won't really see it yet on the results"）
- 2026-09-08｜CEO｜product：CEO 說 Bits AI 原本是單一調查用 SKU，正在改包成可跨多個介面使用的 AI credits。（原話："now we're packaging it to a set of AI credits instead"）
- 2026-09-08｜CEO｜commitment：CEO 說之後大概會對 Bits AI 改包裝再做說明，未給時間。（原話："we probably will comment on that in the future"）
- 2026-09-08｜CEO｜product：CEO 說整個業界還不確定怎麼替 agent 收費，Datadog 自己是完全用量計價。（原話："doesn't quite know how to charge for agents just yet"）
- 2026-09-08｜CEO｜product：CEO 提到已宣布把資安 agent 與 Cloud SIEM 脫鉤，可用在自家未收進來的資料上。（原話："the decoupling of our security agent from our Cloud SIEM"）
- 2026-09-08｜CEO｜product：CEO 說 AI credits 是疊加在原有資料用量之上另外賣。（原話："buy on top of the rest of the data consumption"）
- 2026-09-08｜CEO｜product：CEO 說 AI credits 目前客戶接受度看起來很好，並補一句還要再觀察，必要時可換包法。（原話："So far, it seems to be very well accepted."）
- 2026-09-08｜CEO｜customer：CEO 說客戶合約中跨產品的用量可互換（fungible），是客戶集中採購的原因之一。（原話："what they use across different parts of Datadog is fungible"）
- 2026-09-08｜CEO｜customer：CEO 說客戶合併成單一供應商，好處是只管一個承諾額度池，不必管理 12 個。（原話："one big pool of commitment and spending with one vendor"）
- 2026-09-08｜CEO｜customer：CEO 說公司進入了約一半的 Fortune 500。（原話："we are in about half of the Fortune 500"）
- 2026-09-08｜CEO｜customer：CEO 說平均年化合約約 40 萬美元；主持分析師當場插話說實際「高一點」，CEO 未再補數字。（原話："annualized contract is $400,000, something like that"）
- 2026-09-08｜CEO｜customer：CEO 說客戶完全滲透時，在可觀測性與資安等花費約占其雲端帳單的 10%–20%。（原話："around 10%, maybe between 10% and 20% of their cloud bill"）
- 2026-09-08｜CEO｜customer：CEO 說預期這個花費占比的某個版本在 AI 世界也會成立；無數字、無時間。（原話："some version of that will remain true in the AI world"）
- 2026-09-08｜CEO｜customer：CEO 解釋分開報 AI 原生客戶的口徑：這些公司實質上整個業務都在做 AI，即使不是新公司。（原話："because they're substantially all about AI"）
- 2026-09-08｜CEO｜customer：CEO 說長期來看可能不再把 AI 原生客戶分開揭露（揭露口徑可能改變，無時間點）。（原話："we probably won't separate them out anymore"）
- 2026-09-08｜CEO｜customer：CEO 說前沿實驗室的使用方式（同時操作數千上萬個 agent）與一般企業不同，有免費推論、誘因極端。（原話："you have free inference and all the incentives"）
- 2026-09-08｜Analyst (Fatima Boolani, Citi)｜customer：主持分析師稱 AI 原生客戶群約 750 家（分析師講的數字，CEO 未確認也未更正）。（原話："So that 750 customers in the AI native cohort."）
- 2026-09-08｜CEO｜risk：被問 AI 原生客戶集中風險，CEO 回顧疫情期間雲端/數位原生客戶曾占公司業務約 40%，之後遭遇收縮。（原話："it was about 40% of our business at peak"）
- 2026-09-08｜CEO｜risk：CEO 說對 AI 原生客戶的曝險比當年對雲端原生客戶小很多。（原話："the exposure we have to these AI is much smaller"）
- 2026-09-08｜CEO｜risk：CEO 說整體看上行空間大於潛在下行。（原話："we see a lot more upside there than potential downside"）
- 2026-09-08｜CEO｜customer：CEO 在談 AI 原生客戶時提到「其他 85% 的業務」在意成本；原話未明確給出 AI 原生占比。（原話："companies in the other 85% of our business"）
- 2026-09-08｜CEO｜competition：CEO 說 OpenTelemetry 降低導入門檻，對公司是順風。（原話："it's actually a tailwind for us"）
- 2026-09-08｜CEO｜customer：CEO 說最近一次財報電話會提到 5、6 件客戶整併案，通常包含把多個開源產品併進 Datadog。（原話："we call it like 5 or 6 customer consolidations"）
- 2026-09-08｜CEO｜margin：被問價格通縮與開源壓力，CEO 說公司一向擅長維持利潤率與交付給客戶的價值。（原話："we've been pretty good at maintaining margins"）
- 2026-09-08｜CEO｜margin：CEO 說產品毛利率相當高，因此有餘裕把約 30% 營收再投入研發。（原話："we can reinvest about 30% of our top line into R&D"）
- 2026-09-08｜CEO｜competition：CEO 說公司結構上的差異化之一是非常精實的銷售模式，能同時兼顧投資與獲利。（原話："very lean, very efficient go-to-market"）
- 2026-09-08｜CEO｜competition：CEO 說第二個差異化是身為 SaaS 廠商，握有可拿來訓練模型的乾淨營運資料。（原話："extremely clean, operationally relevant data"）
- 2026-09-08｜CEO｜product：CEO 說已發布兩個開源時間序列模型 Toto 與 Toto 2.0。（原話："we've released 2 models of Toto and Toto 2.0"）
- 2026-09-08｜CEO｜capital_allocation：CEO 提到數月前宣布收購 Adaptive ML（強化學習調校客製模型），團隊已併入研究團隊。（原話："the acquisition of Adaptive ML"）
- 2026-09-08｜CEO｜commitment：CEO 說之後會在自建模型這個主題上有更多消息；未給時間或規模。（原話："you should expect to hear and see more from us"）
- 2026-09-08｜CEO｜risk：CEO 承認有客戶決定自建可觀測性而流失，其中有些後來又回來。（原話："a number of them have churned off"）
- 2026-09-08｜CEO｜risk：CEO 說自建後流失的客戶只占客戶群很小一部分。（原話："It's a very small fraction of our customer base."）
- 2026-09-08｜CEO｜customer：CEO 說總體毛留存率在 90% 後段，口徑涵蓋從 SMB 到大型企業的整體業務。（原話："gross retention is extremely high. It's in the high 90s"）
- 2026-09-08｜CEO｜customer：CEO 說有數家最大的超大規模雲端業者（原本全自建）回頭找 Datadog，並說幾次財報前已提過。（原話："a number of the largest hyperscalers come to us"）
- 2026-09-08｜CEO｜customer：CEO 轉述這些超大規模業者的說法：AI 建置需要 Datadog 協助。（原話："For our AI build-out, we need your help."）
- 2026-09-08｜CEO｜margin：CEO 說研發投入的總額度大致不變（約營收 30%），但內部組成會改變。（原話："the overall envelope doesn't change all that much"）
- 2026-09-08｜CEO｜margin：CEO 說內部工程師用 agent 讓 token（模型用量）與算力帳單暴增，且還不清楚多少是必要的。（原話："we're seeing our compute bill or token bill explode"）
- 2026-09-08｜CEO｜margin：CEO 說公司也開始在 GPU 上花更多錢（訓練自家模型）。（原話："we also started spending a lot more on GPUs"）
- 2026-09-08｜CEO｜guidance：CEO 說模型訓練規模會擴大，後續在這塊會看到更多支出；純定性，無金額。（原話："you should see more spend there also"）
- 2026-09-08｜CEO｜margin：CEO 說客服工單需要的人力過去隨客戶數成長，現在這條曲線反過來了，人力轉去做主動服務。（原話："Now that curve has gone the other way."）
- 2026-09-08｜CEO｜commitment：被問 AI 生產力是否減少招聘需求，CEO 說工程團隊還在擴編。（原話："we're definitely still scaling the engineering teams"）
- 2026-09-08｜CEO｜commitment：CEO 說如果每一塊研發投入產出變多，公司會做更多研發而非縮減。（原話："we will just do more R&D"）
- 2026-09-08｜CEO｜product：CEO 說公司的限制在內部能做出多少產品，而非客戶需求。（原話："We're more limited internally by what we can produce."）
- 2026-09-08｜CEO｜competition：CEO 說過去三個月資安工具被徹底顛覆，數年前做的資安產品幾乎都過時。（原話："security tooling has been completely upended"）
- 2026-09-08｜CEO｜competition：CEO 說這讓資安領域被抹平，在位者優勢消失；他預期未來幾年逐步展開。（原話："completely flattens the space and negates any advantage"）
- 2026-09-08｜Analyst (Fatima Boolani, Citi)｜product：主持分析師稱資安 SKU 約滲透 1/4 客戶群、約 1 億美元 ARR（分析師數字，CEO 未確認）。（原話："It's a $100 million ARR franchise."）
- 2026-09-08｜CEO｜competition：CEO 說資安產品用戶群很小，Datadog 的差異是讓開發與維運大量使用者每天用。（原話："Security products have a very small user bases."）
- 2026-09-08｜CEO｜competition：CEO 說做不到被業務員硬綁在一起的孤島產品，要靠整合平台。（原話："siloed products that just happen to be bundled together"）
- 2026-09-08｜CEO｜product：CEO 說公司過去講三支柱（指標、追蹤、日誌），現在把數位體驗拆出來當第四支柱。（原話："now we consider that we have 4 pillars"）
- 2026-09-08｜CEO｜product：CEO 說第四支柱（RUM 與 Synthetic Testing）成長快，且隨規模變大成長率還在加速。（原話："accelerating growth over time as it gets bigger"）
- 2026-09-08｜CEO｜commitment：CEO 說新產品的目標是做到 1 億美元以上，並希望有機會跨過 10 億美元。（原話："we have hopes that they can cross the $1 billion mark"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說沒有哪個類別是非買不可，做法是機會主義；過去收購多半是為了買團隊，省下 2、3 年。（原話："there's no category where we think, oh, we need to buy there"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說歷史上收購主要是為買團隊與產品優勢，省下的時間約 2、3 年。（原話："we're going to take a shortcut of maybe 2, 3 years"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說若某公司能帶來差異化通路，也可能為通路而收購。（原話："We might also do the same thing for distribution."）
- 2026-09-08｜CEO｜capital_allocation：CEO 說大型併購合適標的機率很低。（原話："are very, very low for larger deals"）
- 2026-09-08｜CEO｜capital_allocation：CEO 說只要能加速通往目標並整合進統一平台，什麼都可以考慮，包括大型併購。（原話："nothing is out of the question"）
- 2026-09-08｜CEO｜competition：CEO 說這個市場最後會是 Datadog 加上一兩家其他公司。（原話："It's going to be us, maybe 1 or 2 other companies."）

### DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md
- 2026-09-10｜David Obstler｜guidance：CFO 說明因投資人關注最大客戶波動，公司把財測改成只放進合約承諾額（commitment）。（原話："putting in our guidance only the commitment"）
- 2026-09-10｜David Obstler｜guidance：CFO 補充該客戶在財測裡的下限就是承諾額。（原話："It can't go below the commitment."）
- 2026-09-10｜David Obstler｜customer：CFO 說上季財報已講過，最大客戶續約、續留 Datadog 並延長合約。（原話："that customer renewed with us, staying with Datadog"）
- 2026-09-10｜David Obstler｜customer：CFO 說最大客戶一直在成長，且用量高於合約承諾額（「一直以來的說法」）。（原話："growing rapidly and spending above the commitment"）
- 2026-09-10｜David Obstler｜risk：CFO 承認最大客戶的用量有波動，這是改財測寫法的原因之一。（原話："So we had some volatility."）
- 2026-09-10｜David Obstler｜risk：CFO 說把超大客戶自建可觀測性視為邊緣情況。（原話："we've always said that's a fringe case"）
- 2026-09-10｜David Obstler｜customer：CFO 給出毛留存率口徑：高 90 多趴，大型企業客戶落在高端。（原話："upper 90s with larger enterprise being at the high end"）
- 2026-09-10｜David Obstler｜risk：CFO 直說並非每個客戶都留得住。（原話："we don't retain every customer"）
- 2026-09-10｜David Obstler｜risk：CFO 表示雲端軟體永遠有成長與優化交替，看的是加權平均。（原話："a yin and yang of growth and optimization in cloud software"）
- 2026-09-10｜David Obstler｜risk：CFO 對比 2021-2023 優化期：當時成長約 70%，現在成長良好但不是 70%。（原話："We're growing well, but we're not growing at 70%."）
- 2026-09-10｜David Obstler｜risk：CFO 說當年雲原生客戶占比比現在高很多。（原話："We also had a much higher percentage of these cloud-natives"）
- 2026-09-10｜David Obstler｜customer：CFO 以淨留存率上升為據，稱目前整體處在成長環境。（原話："we're net-net in a growth environment"）
- 2026-09-10｜David Obstler｜risk：CFO 稱公司如今更大、更分散（地理與客戶類型）。（原話："We're much more diversified in all ways"）
- 2026-09-10｜David Obstler｜customer：CFO 說高成長的 AI 原生客戶很重要，但規模遠小於雲原生客戶群。（原話："it's much smaller than that cloud native"）
- 2026-09-10｜David Obstler｜risk：CFO 稱客戶群沒有忘記上一輪優化期，行為更節制。（原話："our customer base has not forgotten what happened"）
- 2026-09-10｜David Obstler｜risk：CFO 列出降低優化風險的工具：合約延長、量價折扣等。（原話："volume pricing, a number of things to ameliorate the risk"）
- 2026-09-10｜David Obstler｜margin：CFO 說把客戶轉到 Infinite Cardinality SKU，對留存和毛利兩邊都有利。（原話："retentive and also margin enhancing for us"）
- 2026-09-10｜David Obstler｜product：CFO 說公司主動把適用客戶轉到 Infinite Cardinality SKU（與 Flex Logs、Frozen Logs、Metrics Without Limits 同屬一組產品創新）。（原話："proactively converting those customers that can benefit"）
- 2026-09-10｜David Obstler｜product：CFO 說明 Federated Logs：不必所有日誌都流入 Datadog。（原話："not all logs have to flow into Datadog"）
- 2026-09-10｜David Obstler｜product：CFO 說 Federated Logs 目前對接的外部儲存是 ClickHouse 和 Databricks。（原話："In this case, it was ClickHouse and Databricks."）
- 2026-09-10｜David Obstler｜product：CFO 說這類開放架構（Federated Logs、Bring Your Own Cloud）可接到原本拿不到的業務。（原話："business that we would not have had otherwise"）
- 2026-09-10｜David Obstler｜customer：CFO 回答日誌外放的取捨：用戶越集中在 Datadog，每客戶平均營收越高（未給數字）。（原話："we get higher average revenue per customer"）
- 2026-09-10｜David Obstler｜margin：CFO 說請客戶少送用不到的日誌進 Datadog，在許多情況下對公司毛利有利。（原話："in many cases, is margin enhancing for us"）
- 2026-09-10｜David Obstler｜product：CFO 說公司近期收購 Adaptive ML（專長強化學習，用在 IT 管理與可觀測性）。（原話："an acquisition of a company called Adaptive ML"）
- 2026-09-10｜David Obstler｜product：CFO 提到公司先前已推出自家時序模型 Toto。（原話："we put out a model a while ago called Toto"）
- 2026-09-10｜David Obstler｜competition：CFO 稱用自有觀測數據訓練的模型，預期會成為競爭優勢。（原話："what we think will be a very strong competitive advantage"）
- 2026-09-10｜David Obstler｜commitment：CFO 說公司正在人力、GPU、推論上加碼投入自有 AI 模型。（原話："both in terms of people, the GPUs, the inferences"）
- 2026-09-10｜David Obstler｜margin：CFO 預期把 GPU/token 成本逐步重新配置到自有模型（需要前期投入）。（原話："a reallocation of the cost of our GPU -- our token costs"）
- 2026-09-10｜David Obstler｜product：CFO 描述 Bits 自動修復願景：目前尚未達成。（原話："when we get there, we're not there yet"）
- 2026-09-10｜David Obstler｜product：CFO 說願景是讓客戶自選哪類問題可由平台自動修復，哪類仍需人工確認。（原話："the platform can auto remediate"）
- 2026-09-10｜David Obstler｜product：CFO 說 agent observability（監控 AI 應用）已有數千客戶使用。（原話："we're seeing thousands of customers use this"）
- 2026-09-10｜David Obstler｜product：CFO 說 agent observability 已開始產生營收（未給金額）。（原話："we're starting to get the revenue streams from it"）
- 2026-09-10｜David Obstler｜product：CFO 以 Bits 與 MCP Server 呼叫量作為 AI 應用活動增加的指標之一。（原話："MCP Server calls and other indications, a lot of activity"）
- 2026-09-10｜David Obstler｜customer：CFO 說 AI 原生客戶有外包給 Datadog（而非自建）的趨勢。（原話："we're seeing a pattern of outsourcing to Datadog"）
- 2026-09-10｜David Obstler｜customer：CFO 說 AI 原生客戶的主要現象是成長加速。（原話："But the main thing we're seeing is accelerated growth."）
- 2026-09-10｜David Obstler｜customer：CFO 說有大型雲端業者等客戶要把 Datadog 用在訓練與後訓練工作負載，公司原本沒預期。（原話："we want to use you for training or post-training workloads"）
- 2026-09-10｜David Obstler｜competition：敘事變化：CFO 說公司原本認為 Datadog 是生產環境（推論）公司，不會有多少訓練需求，後來被大客戶的訓練用途打破此預期。（原話："We're really not going to see a lot of demand on training."）
- 2026-09-10｜David Obstler｜risk：CFO 對訓練用途設下保留：證據還不夠說公司會成為訓練領域的公司。（原話："We don't believe we have the evidence to say"）
- 2026-09-10｜David Obstler｜competition：CFO 稱極少或沒有公司能有機成長出整合式可觀測性平台，多半靠併購拼湊。（原話："have been able to organically grow an integrated platform"）
- 2026-09-10｜David Obstler｜competition：CFO 稱有一家（未點名）公司正在對外談要做同樣的事。（原話："It's easier said than done."）
- 2026-09-10｜David Obstler｜competition：CFO 說能否守住位置取決於自己是否持續創新，並提到「AI for Datadog、Datadog for AI」兩條線。（原話："This is AI for Datadog and Datadog for AI."）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說 R&D 一貫占營收約 30%，金額超過 10 億美元。（原話："consistently invested 30% of its revenues in R&D"）
- 2026-09-10｜David Obstler｜competition：CFO 稱 Datadog 的研發投入超過市場上其他人。（原話："That is out investing everybody else in the market"）
- 2026-09-10｜David Obstler｜commitment：CFO 承諾持續大幅投入研發以維持創新領先。（原話："that's why we're investing significantly"）
- 2026-09-10｜David Obstler｜customer：CFO 引用研究機構說法：雲端應用占比約高 20 多到 30%。（原話："somewhere upper 20s, 30% of applications are in the cloud"）
- 2026-09-10｜David Obstler｜customer：CFO 稱雲端遷移與現代化的急迫性因 AI 上升，並點出非 AI 業務在加速。（原話："we're seeing the non-AI business accelerate"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說由下而上的銷售需要越來越多由上而下的企業銷售補強。（原話："has to increasingly be complemented by top-down"）
- 2026-09-10｜David Obstler｜capital_allocation：敘事變化：CFO 說公司先前以為銷售週期是離散的、佣金制度也照此設計，現改設重點客戶組，每位業務只負責 1–2 個大帳戶。（原話："Our commission plans were done that way."）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說大型企業客戶的業務員不能一人負責 10 個帳戶。（原話："can't have an enterprise salesperson covering 10 accounts"）
- 2026-09-10｜David Obstler｜customer：CFO 舉財報中提到的產業案例：銀行、保險、汽車、製造、航空。（原話："banking, insurance, automotive, manufacturing, airlines"）
- 2026-09-10｜David Obstler｜product：CFO 說公司開始看到用 coding agents 提高研發速度的實際效率跡象，但仍在早期。（原話："we are starting to see signs of real efficiency"）
- 2026-09-10｜David Obstler｜product：CFO 說公司用 A/B 團隊測試 coding 工具的取用程度對產出的影響。（原話："we have teams that are access to more of the coding tools"）
- 2026-09-10｜David Obstler｜commitment：CFO 說公司過去快速擴編人力，預期仍需繼續增加人力投資。（原話："we believe we'll continue to have to do that"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說公司在自有模型上大量投入。（原話："we are investing significantly behind our own models"）
- 2026-09-10｜David Obstler｜capital_allocation：CFO 說研究實驗室的投入開始在研發預算中占到一定比重。（原話："starting to result in the weight of the R&D budget"）

### 問答異常語氣（迴避／改口／保留）
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Patrick Colville（Scotiabank）確認「對最大客戶更高程度保守」的說法，並問是相對其他客戶還是相對過往財測｜答法：CFO 先答「兩者都是」並稱措辭很明確；CEO 隨後說「不要對特定措辭賦予太多意義」；CFO 再補一句方法沒變
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Karl Keirstead（UBS）問 Q2 財測信心來源，以及一家 Q4 續約、一家剛簽的大型研究實驗室 Q2 的放量情況｜答法：CFO 與 CEO 都以 Q1 ARR 新增創紀錄且分散回答；沒有直接談那兩家實驗室 Q2 的放量幅度；CEO 只說 Q1 有幾家新客戶尚無營收貢獻
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Gabriela Borges（Goldman Sachs）問訓練相對推論的觀測性支出附著率，以及觀測性占推論支出比例是否改變｜答法：CFO 沒給占比或基準數字，改引用 6,500 位客戶、占客戶 20%、占 ARR 80% 的整合附著數據，並說訓練還早
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Fatima Boolani（Citi）問遙測量暴增下如何維持資本密集度與毛利率｜答法：CEO 只談資本支出（雲端跑、走 OpEx）與資料主權投資，沒有回應毛利率的部分
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Sanjit Singh（Morgan Stanley）問 agent 大量使用平台時，計價模式是否會出現新形態｜答法：CEO 說難以預測四五年後，並稱用量計價不在乎用量來自人或 agent；沒有直接回答是否會有新的計價模式
- DDOG_Q1_2026_Earnings_Call_20260507.md｜問：Mark Murphy（JPMorgan）問異質晶片環境是否帶來順風｜答法：CEO 自述立場改變：去年說訓練還不是市場，現在說開始看到訓練成為市場，並拿超大型雲端業者客戶的超級智慧實驗室當驗證
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Sanjit Singh (Morgan Stanley)：自主營運一年後、三年後長什麼樣？是否需要自己掌握軟體交付管線（build vs buy）？｜答法：Olivier Pomel 稱時程 'hard to tell whether we get there in a year or in 3 years'，未給具體里程碑；build vs buy 只點名功能旗標與資料可觀測性兩個已改變看法的領域，並稱 'a few other areas... I'm not going to tell you about it'
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：自主營運商業化後，計價模式是否會根本改變（結果導向計價）？｜答法：回答 'too far away to be talking about pricing models'、'It doesn't mean we have a pricing packaging in mind just yet'，未給計價方向，改談用量計價較容易適應
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Fatima Boolani (Citi)：$1,000 萬客戶與 $10 萬客戶的增量獲利／單位經濟是否有實質差異？｜答法：Unknown Executive 只答量折扣與加權平均後毛利率大致不變，未直接拆解大客戶的獲利結構差異
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Andrew Sherman (TD Cowen)：三大支柱使用率 53% 通常缺哪一塊產品？未來幾年會到多少？｜答法：Sean Walters 稱每個客戶情境不同、不強推三支柱，Yuka Broderick 補 'I wouldn't think of it as one particular pillar that's missing'；兩人都沒給未來使用率數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Keith Bachman (BMO)：資安產品組合的邊界在哪、哪些領域不打？｜答法：Tim Knudsen 談既有成熟預算與統一平台優勢、AI 帶來新領域，未指出任何不打的領域
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Ittai Kidron (Oppenheimer)：小模型成本只要 $75 萬，第三方進入門檻多高？AI 對公司業務的風險是什麼？｜答法：Alexis Le-Quoc 談資料與評測集的護城河、並承認沒有明確的資金門檻；Olivier Pomel 補 R&D 投入金額；兩人都沒列出 AI 對業務的具體風險
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Koji Ikeda (BofA)：財星 500 大客戶如何把花費中位數拉高？2025 年 TCV 訂單（分析師稱 $45 億以上）中大客戶與中型客戶各占多少？｜答法：Unknown Executive 談長銷售週期、工具整併與 key accounts，未拆分 TCV 訂單的客群貢獻，也未確認分析師提出的 $45 億數字
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Eric Heath (KeyBanc)：BYOC 的可服務客群、何時廣泛推出、進入市場策略？｜答法：Yrieix Garnier 稱已在預覽並有付費客戶，客群點名資料在地化與合規產業、超大規模客戶；未給一般上市時程
- DDOG_Analyst_Investor_Day_Datadog_Inc_20260212.md｜問：Arti Vula (JPMorgan)：目前 AI 產生的程式碼量能否量化、是否已進到正式環境並帶動用量？｜答法：Unknown Executive 只做定性回答（訊號與開源都顯示程式碼變多），稱多數公司仍在早期，未給量化數字；改以 'we should see where we are at the end of the year' 收尾
- DDOG_Canaccord_Genuity_s_46th_Annual_Growth_Conference_20260812.md｜問：分析師問 agent 流量占比上升後，這塊業務可能做到多大、客戶是否在改變。｜答法：CFO 沒給任何規模數字，回答為「Where it's going to wind up, I don't know」，改談 Datadog 不是按席位計價。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問目前業務中有多少來自「觀察 AI 系統」與「用 AI 強化 Datadog」，請他們切分規模與對業務的影響。｜答法：CEO 講品牌框架與哪塊成長較快（Datadog for AI），並給「堆疊 70%–80% 相同」的比例，未給兩塊各占營收多少的數字。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師指出大型資安公司與 ServiceNow 等正切入可觀測性，問 go-to-market 訊息如何改變。｜答法：CEO 回到自家整合平台與使用者規模的差異，未直接回應資安大廠與 ServiceNow 進入可觀測性這件事。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問下一個 10 億美元產品線會是哪一個。｜答法：CEO 只說內部有數個候選，未點名；轉去講第四支柱（數位體驗）成長，再談新產品目標 1 億美元以上、希望跨過 10 億。
- DDOG_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問「大於歷來規模」的併購，門檻與參數長什麼樣。｜答法：CEO 說沒有硬性規則、大型交易少見，未給任何規模或條件參數，只說「nothing is out of the question」。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：怎麼知道我們不是快要進入新一輪優化期？公司用什麼預測工具、為何這次不同？｜答法：沒有說明任何預測工具或領先指標，改用與 2021–2023 的結構差異（成長率、雲原生占比、多元化）和淨留存率作答。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：會不會有更多大客戶願意承擔自建（DIY）複雜度來省錢？｜答法：沒有量化大客戶占比或自建趨勢；以毛留存率『高 90 多趴』、最大客戶續約、『邊緣情況』作答，並承認最大客戶用量有波動。
- DDOG_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：分析師問：客戶群是否正從外部前沿模型 API 轉向自建/自營 AI 堆疊？｜答法：只說在『前面提到的用量指標』看到，未說明是哪個指標或數字，並轉去談 Datadog 自己把 token 成本轉向自有模型。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | found | 5 | 4 |
| customer_concentration_credit | found | 8 | 4 |
| supply_demand_durability | found | 8 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 1 | 4 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 11 | 6 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 1 | 4 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：DDOG Datadog antitrust OR monopoly investigation 2026；Datadog regulation OR regulatory scrutiny observability cloud software 2026；DDOG Datadog DOJ OR FTC OR EU competition 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260516","verdict":"觀望（衛星候選 B，thesis 完整但估值🔴 + 4 週 +45% 漂移 + BB 上軌外 14%，等回測 BB 中軌 $131 或 W52 $139 + Fwd PE 修復至 55-60x 再分批）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Datadog 是 AI inference 經濟學的觀測層核心玩家，AI native cohort 持續高增長","columns":{"2Y 驗證點":"AI native cohort YoY +60%（vs 當前 +90~240%）；OpenAI 客戶分散度提升（top 3 AI 客戶","5Y 驗證點":"AI native ARR > $1B；LLM Observability ARR > $500M（從 Q1 26 估 $250M annualized）","10Y 驗證點":"AI inference 經濟學 TAM 觸 $50B+ 時 DDOG 觀測層市佔 > 25%","具體數字門檻":"AI native cohort YoY +60% 連 4 季（從當前 +90~240% 衰減但維持高位）","信息來源":"Datadog Q1 26 earnings call + Investor Day 揭露","漂移觸發":"連 2 季 TTM AI native YoY"}},{"id":"H2","text":"Non-GAAP OM 從 FY25 22% 擴張至 FY28 26-28%，在 Rev 繼續 22%+ 下達成","columns":{"2Y 驗證點":"FY26 Q4 Non-GAAP OM ≥ 23%；GM ≥ 78%（LLM infra 壓力可控）","5Y 驗證點":"FY27 OM ≥ 25%；FY28 OM ≥ 27%；SBC/Rev 從 22% 壓至 18%","10Y 驗證點":"FY30 OM ≥ 30%；FCF Margin > 30%（vs FY25 27%）","具體數字門檻":"FY26 全年 Non-GAAP OM ≥ 22%（guide 22-23%）","信息來源":"FY26 guidance 法說","漂移觸發":"連 2 季 TTM OM"}},{"id":"H3","text":"市場給予 Datadog AI infra 觀測層的「pure-play premium」，Fwd PE 維持 50-80x range","columns":{"2Y 驗證點":"NTM Fwd PE 5Y 分位 30-70%；vs CRWD 倍數 ratio","5Y 驗證點":"Fwd PE 50-65x（成熟期）；ARR > $7B","10Y 驗證點":"Fwd PE 40-50x（穩定期）","具體數字門檻":"NTM Fwd PE 維持 60-75x range 連 8 季","信息來源":"Macrotrends + Yahoo Finance 倍數歷史","漂移觸發":"NTM Fwd PE > 90x 連 2 季 → R4 觸發（同業溢價極端）；"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"LLM Observability inference cost 結構性壓 GM","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Non-GAAP GM 連續季度；FY26 GM guide","警戒閾值":"連 2 季 GM"}},{"id":"R2","text":"OpenAI / 大型 AI native 自建 monitoring stack 或合約縮減","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"10-K 揭露 single customer concentration；OpenAI 雲端 spend 變化","警戒閾值":"10-K 單一客戶 > 10% = 觸發風險警示；OpenAI 縮減合約或 self-host monitoring 公告 → 護城河 -1 分"}},{"id":"R3","text":"Cisco Splunk + AppDynamics + Galileo 推 unified observability 大規模搶大客戶","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Cisco unified observability launch；DDOG 大客戶流失公告（DBNR","警戒閾值":"Cisco unified launch 後 6 個月內 DDOG DBNR 連 2 季"}},{"id":"R4","text":"SaaS 同業溢價收斂：CRWD/SNOW/ZS 為比較組，市場校準合理倍數","columns":{"對應假設":"H3","時間尺度":"🔥 中期","監測指標":"DDOG/CRWD forward PE ratio（當前 ~1.0x）；SaaS ETF 倍數","警戒閾值":"NTM Fwd PE > 90x 連 2 季 = 極端化 → 觸發 mean revert → -30%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":207.98,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"DDOG","date":"2026-09-24","schema":"v15.2","contract":"v19","company_name":"Datadog, Inc."},"oneliner":"雲端與AI系統觀測平台龍頭：非AI業務連5季加速、毛留存90%中後段，生意沒變壞；但股價約99倍今年EPS，Base情境五年年化約1%，要等回到185美元附近再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DDOG_20260924/scenario.json","answers":{"q1_business":{"verdict":"賺企業維運雲端與AI系統的錢：年度承諾額打底、超用按量計費；錢卡在「工程師天天用、財務長年年想砍帳單」這一節點，工程端黏著決定續約，財務端的用量優化決定成長斜率。","reasoning":"單一營運分部，公司不揭露分部損益，改看產品線ARR：基礎設施監控逾16億美元、日誌與APM各逾10億美元（2025年底口徑，2026-02-12投資人日），RUM逾2億美元且年增逾50%（Q2 FY2026）。最新一季（Q2 FY2026）營收11.21億美元、年增35.6%，高於指引上緣；非GAAP毛利率79.6%、非GAAP營業利益率22.9%，GAAP營業利益率只有0.5%，差額主要是股權激勵（占營收19.6%）。年ARR達10萬美元以上客戶4,720家、貢獻約91%ARR，客戶基礎分散，但單點依賴明確存在：最大客戶是一家AI公司（市場推測為OpenAI，公司未證實），用17項產品、剛續簽九位數合約但Q3起減量；最大客戶所屬的AI原生客群去年底約占營收11%（2026-02-12投資人日CFO），並貢獻2025年Q4約7個百分點的年增。產業時鐘判在擴張期：營收年增從25%（Q1 2025）到32%（Q1 2026）再到36%（Q2 2026），非AI客戶年增從18%升到20%後段，依據是客戶用量與新客戶放量，不是股價。供需耐久性：核心雲端遷移需求屬結構性持久（CFO引研究機構估雲端應用占比僅約高20多到30%，2026-09-10），AI原生客群用量屬週期性、可逆性高，這部分餵給Bear機率。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi4_stock_based_compensation","f_kpi8_non_gaap_gross_margin_pr","f_kpi9_customers_with_arr_100k","f_kpi11_ai_native_1m_1m_arr_ai","f_kpi15_ai_yoy","f_kpi12_net_revenue_retention_tr"],"verdict_values":{"revenue_quality":"高但有用量波動：年度承諾額加超用計費，TTM淨營收留存率120%出頭、毛留存90%中後段；承諾額以上的用量隨客戶優化起伏，最大客戶續約後減量即為例子","unit_econ_note":"非GAAP毛利率79.6%，管理層長期規劃80%上下；量價折扣後大客戶加權毛利率大致不變（2026-02-12投資人日）；FCF率24.9%，但扣掉股權激勵後只剩約5%（278.7−220.3＝58.5百萬美元，除以營收1,121百萬美元）","archetype":{"primary":"品質複利成長","secondary":"未獲利高成長","confidence":"中","fingerprint":"毛利率約80%、FCF率25–27%、營收年增30%上下，但GAAP獲利被股權激勵吃光，股東經濟介於兩型之間"},"industry":{"clock_phase":"II","sd_verdict_source":"核心雲端遷移需求屬結構性持久（CFO引研究機構估雲端應用占比約高20多到30%，2026-09-10）；AI原生客群用量屬週期性、可逆性高（最大客戶續約後減量，2024年另有AI原生客戶部分改自建）","bargaining":{"up":"上游是公有雲基礎設施，工作負載成本走營業費用而非資本支出（2026-05-07 CEO）；毛利率多年守在80%上下，上游議價有限，但自建模型開始增加GPU與token支出（2026-09-08 CEO）","down":"下游議價力兩極：一般企業多產品整併後轉換成本高；超大客戶與AI實驗室有自建能力與量價折扣籌碼，最大客戶續約後減量即為例證","geo":"約44%員工在美國以外、其中34%在法國（FY2025年報）；美洲是AI活動主場，拉美約占營收5%且成長最快；無實體製造與中國台灣供應鏈依賴"},"profit_pool_dir":"觀測性利潤池向整合平台集中（CFO稱少有公司能有機長出整合平台，2026-09-10），但資料儲存層正被Snowflake、Databricks、ClickHouse分走；公司推聯邦日誌讓資料留在外部，等於讓出部分儲存環節換取留存","tam_table":[{"item":"觀測性市場規模（公司口徑）","value":"300億美元以上；加資安與軟體交付後逾1,000億美元（2026-02-12投資人日CFO）"},{"item":"第三方市場規模估計","value":"2026年33.5億至341億美元，差十倍；CAGR 11%–16%。最低一家低於公司自身年營收，定義過窄不採用"},{"item":"Gartner觀測平台市場","value":"2028年142億美元"},{"item":"公司市占","value":"13%–14%（2026-09-08 CEO），投資人日稱十幾個百分點中段"},{"item":"客戶滲透","value":"約32,000家對目標約50萬家＝7%（2026-02-12投資人日）；Q2 FY2026客戶數33,400"},{"item":"完全滲透客戶的觀測加資安支出","value":"約占其雲端帳單10%–20%（2026-09-08 CEO）"},{"item":"營業利益池占比5年前到現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行面擴大、定價面小幅讓利，兩者相抵；機制是整合平台與共用承諾額度池，不是資料收集。","reasoning":"機制：四大支柱（指標、追蹤、日誌、數位體驗）共用同一份資料、同一個承諾額度池，客戶跨產品用量可互換（2026-09-08 CEO），多產品滲透一年內明顯加深：用4項以上產品的客戶58%（一年前52%）、6項以上37%（29%）、10項以上13%（7%）。可證方向取留存與份額：TTM淨營收留存120%出頭、毛留存90%中後段，屬高黏著；Ramp統計的採用率34%、年比持平，份額擴大沒有外部證據，管理層的大幅搶市占（2026-08-12 CFO）是以營收增量推論。執行面判擴大：非AI業務連5季加速、Q2季增1.15億美元創紀錄、Gartner觀測平台連6年領導者且執行力軸最高、研發約為最接近同業3倍（投資人日）。定價面判穩定偏縮：財務長層級持續抱怨帳單（2026-08-06法說分析師轉述）、第三方稱企業議價可壓牌價35%–55%，公司主動推無限基數指標、聯邦日誌、自帶雲，降低客戶單位成本換留存（2026-09-10 CFO稱對留存與毛利兩利）；另最大客戶續約後減量，領先者在最大客戶的份額下滑，不能判擴大。執行9分、定價7分，扣一個生態攻擊威脅後落B級。同業對照只給利潤率不給投入資本，無法算報酬率差距：GAAP營業利益率0.43%落後PLTR、CRM、NOW、MSFT全部同業，FCF率27.0%居中（高於MSFT、低於CRM、NOW、PLTR），差距主因是股權激勵。產業態勢判雙向拉鋸：競爭面有資安與資料平台跨界整併（Palo Alto收Chronosphere、Snowflake收Observe），結構面雲端遷移與AI工作負載持續擴大需求，商業模式面則有按基礎設施計價與自帶雲的壓力。","fact_refs":["f_kpi12_net_revenue_retention_tr","f_kpi9_customers_with_arr_100k","f_kpi8_non_gaap_gross_margin_pr","f_peer_ddog_gross_margin_pct","f_peer_ddog_operating_margin_pct","f_peer_ddog_fcf_margin_pct","f_peer_pltr_operating_margin_pct","f_peer_crm_operating_margin_pct","f_peer_now_operating_margin_pct","f_peer_msft_operating_margin_pct","f_peer_crm_fcf_margin_pct","f_peer_now_fcf_margin_pct","f_peer_pltr_fcf_margin_pct","f_peer_msft_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"整合平台加資料引力：四大支柱共用同一份資料與同一個承諾額度池，多產品客戶比率逐年升；轉換成本在重建告警、儀表板與跨團隊工作流，不在資料收集（2026-02-12 CEO：收集從來不是護城河）","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（非AI業務連5季加速、新企業客戶年化訂單年增逾一倍、超大雲端業者AI實驗室改外包給公司）；定價面穩定偏縮（主動推降低帳單的計價、最大客戶續約後減量、Ramp採用率年比持平）","competitor_notes":[{"name":"Dynatrace","strategy_note":"企業市場最直接對手，AI根因分析起步較早，但公司Bits AI推出後差距縮小；網站偵測占比3.38%低於公司5.78%"},{"name":"Cisco（Splunk）","strategy_note":"把Splunk日誌優勢和網通硬體綁在一起攻傳統企業，屬捆綁銷售而非產品領先"},{"name":"Palo Alto Networks（Chronosphere）","strategy_note":"從資安端收購觀測性，打資安與觀測合一的平台，是最值得盯的生態攻擊"},{"name":"Snowflake（Observe）","strategy_note":"從資料儲存端切入，主張遙測資料留在自家資料平台；公司以聯邦日誌對接外部儲存回應"},{"name":"Grafana Labs","strategy_note":"開源路線，ARR逾4億美元、7,000家客戶（2025年9月），吃價格敏感與自建派客群"},{"name":"groundcover","strategy_note":"主打eBPF、資料留在客戶雲內、按基礎設施計價，是計價模式挑戰者，規模未揭露"},{"name":"超大雲端業者與AI實驗室自建","strategy_note":"有自建文化但本輪反向外包給公司（2026-05-07、2026-09-08 CEO）；2024年曾有AI原生客戶部分改自建"},{"name":"PLTR","strategy_note":"非直接競爭；營業利益率42.8%、FCF率54.6%，示範軟體平台規模化後的利潤上限"},{"name":"CRM","strategy_note":"非直接競爭；營業利益率21.5%，成熟應用軟體的利潤參照"},{"name":"NOW","strategy_note":"IT營運流程平台，正往可觀測性延伸（2026-09-08分析師提問），潛在跨界者；營業利益率11.4%"},{"name":"MSFT","strategy_note":"Azure原生監控是雲端內建替代品，但多雲客戶仍需中立平台；營業利益率46.8%"}],"spread_notes":{"basis":"只有利潤率","note":"GAAP營業利益率落後全部同業，FCF率居中；缺投入資本，報酬率差距無法計算"},"peer_na_reason":"事實表同業對照未含投入資本與ROIC，只能以營業利益率、FCF率替代","threats":[{"level":"🔴","text":"生態攻擊：Palo Alto收Chronosphere、Snowflake收Observe、Cisco整合Splunk，把觀測性綁進資安或資料平台賣，壓縮獨立平台的整併空間","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"計價與架構挑戰：eBPF取代語言代理、資料留在客戶雲內、按基礎設施計價（競品行銷說法）；公司已自推自帶雲接招，但會壓低單位收費","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"開發工具廠商把可觀測性做進自家產品；coding agent已能處理部分事後排查（2026-02-12 CEO承認）","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"開源與低價對手：Grafana ARR逾4億美元；Gartner稱逾40家廠商、總持有成本已成標準提問","p":"30%","evidence_refs":["supply_demand_durability#7","supply_demand_durability#1"]},{"level":"🟡","text":"超大客戶自建：2024年一家大型AI原生客戶縮減並部分改用內部工具，造成成長放緩；本輪最大客戶續約後減量","p":"30%","evidence_refs":["customer_second_source#4","customer_second_source#0"]}],"roic_durability":{"quadrant":"非GAAP口徑高利益率×高周轉（輕資產、預收款使營運資金為負）；GAAP口徑因股權激勵占營收19.6%，利益率近零。投入資本事實表未涵蓋，當期ROIC數值不算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（工程師）、決策者（平台與工程主管）、付款者（財務長）分開看：前兩者的需求是系統掛掉就賠錢的必需品，DASH上工程師高度肯定產品；付款端有帳單抱怨，但毛留存仍在90%中後段，需求轉得成收入。要解決的問題（維運雲端與AI系統）會持續，公司的解法可被替代但替代成本高"},{"item":"決策層級","level":"🟡","text":"替代要在最小決策單位看：單一團隊決定哪些日誌送進來、哪些指標加標籤，可以逐項外移（聯邦日誌、自帶雲、開源收集標準讓收集層無鎖定）；整體換平台則要重建告警、儀表板與跨產品工作流，毛留存90%中後段顯示整體替代少，但最大客戶續約後減量說明局部替代正在發生"},{"item":"價值鏈分配","level":"🟡","text":"完全滲透客戶把雲端帳單10%–20%花在觀測與資安（2026-09-08 CEO），占比高、易被財務盯上；上游雲端與資料平台（Snowflake、Databricks、ClickHouse）同時想分這塊，公司以聯邦日誌讓出部分儲存環節；AI實驗室與超大雲端業者具自建能力，買方集中處議價力偏向客戶"},{"item":"社會容忍度","level":"🟡","text":"無監管授權依賴，FedRAMP屬認證而非獨占；真正的天花板是客戶預算容忍度：公司刻意推無限基數指標等降低帳單的計價、不把價格推到經濟上限，等於付保費換留存，實際定價上限是客戶財務長能接受的帳單占比"}],"roiic":"公式口徑不適用：成長投入費用化（研發約營收30%），資本支出加資本化軟體只占營收4%–5%，營運資金因預收款為負，按公式再投資率趨近零或為負，增量報酬無意義","reinvest_rate":"同上；折舊攤銷與營運資金變動事實表亦未涵蓋","endo_ceiling":25,"formula_note":"改用留存口徑代理：TTM淨營收留存120%出頭，既有客戶約貢獻20個百分點成長；新客戶占年增量約30%（Q2 FY2026），推得營收內生成長約20÷0.7≈28.6%；扣管理層淨稀釋目標2.5%–3%（投資人日）且利益率持平，每股EPS內生上界約25%。資本配置評為最低一級時再打八折＝20%"}}}},"q3_growth":{"verdict":"五年後仍有寬跑道：市占13%–14%、目標客戶滲透7%，資安（ARR逾1億美元）與AI觀測兩條第二曲線已出現；成長以用量與交叉銷售為主。","reasoning":"成長來源：量（既有客戶的雲端與AI工作負載用量，約七成成長來自既有客戶）加交叉銷售（多產品滲透加深）；併購只是小額補技術（2026上半年三筆合計1.915億美元），沒有回購，反而每年淨稀釋2.5%–3%。共識EPS FY2026 2.53、FY2027 2.97、FY2028 3.75，兩年CAGR約21.7%（FY2025實際EPS事實表未涵蓋，三年CAGR無法算）。對照內生上界：留存口徑約25%，資本配置最低一級打八折後20%，共識高出約1.7個百分點，可歸因於利益率擴張：非GAAP營業利益率由FY2026指引23%走向長期目標25%以上（投資人日CFO），兩年約多出2個百分點EPS年增。跑道年數：市占取13.5%，公司年增25%、市場年增12%（第三方CAGR 11%–16%中位）時，市占每年約放大1.116倍，約7年到30%，屬中等折扣；五年後市占約23%，仍低於35%，且有第二曲線，判寬。AI淨增量：AI原生客群與AI觀測產品帶來的新營收目前大於被替代的收入，但Bits AI在財報上還看不出來（2026-09-08 CEO）；附著點長在公司自有的營運資料上屬強化，coding agent繞過平台做事後排查屬替代，分界年約2028年。衰退信號十類無一確認亮起，毛利率年比與股權激勵兩項列觀察。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi12_net_revenue_retention_tr","f_kpi15_ai_yoy","f_kpi13_rpo_current_rpo","f_kpi5_guidance_q3_fy2026_reven","f_kpi7_guidance_fy2026_revenue_"],"verdict_values":{"growth":{"driver_mix":"量為主（既有客戶用量約占成長七成）加交叉銷售；新客戶占年增量30%；小額併購補技術；無回購、每年淨稀釋2.5%–3%","runway_years":7,"runway_post_y5":"🟢","endo_ceiling_basis":"引護城河題的留存口徑代理：營收內生約28.6%、扣淨稀釋後EPS約25%，資本配置最低一級打八折＝20%；兩年共識CAGR 21.7%高出1.7個百分點，歸因於營業利益率由23%走向25%以上","segments":[{"item":"基礎設施監控ARR","value":"逾16億美元（2025年底）"},{"item":"日誌管理ARR","value":"逾10億美元，年增30%中段（2025年底）"},{"item":"APM ARR","value":"逾10億美元，年增30%中段（2025年底）"},{"item":"RUM ARR","value":"逾2億美元，年增逾50%（Q2 FY2026）"},{"item":"資安產品ARR","value":"逾1億美元（2026-02-12投資人日）；百萬美元客戶中資安僅占其支出2%"},{"item":"Flex Logs ARR","value":"接近1億美元（2026-02-12投資人日）"},{"item":"非AI客戶營收年增","value":"20%後段（Q2 FY2026），Q1為20%中段、一年前18%"}],"decay_signals":[{"signal":"毛利率連2季年比下滑","status":"觀察","note":"Q2 79.6%較一年前80.9%降1.3個百分點；Q1年比事實表未涵蓋，未確認連2季"},{"signal":"核心市占近12個月縮減","status":"未亮","note":"Ramp採用率34%年比持平"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"未見提價，反而主動推降低帳單的計價"},{"signal":"EPS CAGR高於營收CAGR逾5個百分點","status":"未亮","note":"FY2027共識EPS年增17.4%低於營收共識年增22.5%"},{"signal":"FCF對淨利低於0.75連2年","status":"未亮","note":"FCF遠高於淨利"},{"signal":"股權激勵占營收高於5%且逐年上升","status":"觀察","note":"19.6%遠高於5%，逐年序列事實表未涵蓋"},{"signal":"TAM萎縮或被替代技術壓縮","status":"未亮","note":"第三方CAGR 11%–16%"},{"signal":"產業估值倍數近3年系統性下移","status":"未亮","note":"公司P/S位於4個年度端點最高"},{"signal":"維持性資本支出占FCF高於60%","status":"未亮","note":"資本支出加資本化軟體僅營收4%–5%"},{"signal":"停止投資新產能且收入3年內下滑","status":"未亮","note":"研發維持約營收30%"}],"trap_rating":"🟢"}}},"q4_capital":{"verdict":"資本配置偏弱：現金流厚，但股權激勵每年淨稀釋2.5%–3%，沒有回購抵銷；併購小而分散，報酬無從量測。","reasoning":"最新一季FCF 2.787億美元、FCF率24.9%，但同季股權激勵2.203億美元，扣掉後的自由現金流約0.585億美元、占營收約5%；FCF高於非GAAP淨利，主要來自預收款與現金稅低（FY2026現金稅僅0.3–0.4億美元），不是營運特別省錢。現金去向：帳上現金與有價證券約50億美元（Q2 FY2026），資本支出加資本化軟體占營收4%–5%，2026上半年併購現金淨額0.985億美元，不配息、未見回購；近三年去向四分與債務結構事實表未涵蓋。評分三項：併購報酬：三筆合計1.915億美元，約占市值0.2%（251.49美元×約3.78億股≈950億美元），公司認定不重大，不適用；回購收益率：未見回購，不適用；股權激勵淨稀釋：管理層目標每年2.5%–3%（2026-02-12投資人日CFO），高於1.5%門檻，不過關。營運槓桿：Q2營業費用年增26%，低於營收年增36%，非GAAP營業利益率由20%升到23%，沒有壓縮。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation","f_kpi2_gaap_operating_income_ma","f_kpi1_non_gaap_operating_incom","f_kpi7_guidance_fy2026_revenue_","f_kpi6_guidance_q3_fy2026_non_g","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"2026上半年三筆收購合計1.915億美元（10-Q），約占市值0.2%，公司認定不重大，已實現報酬無從量測"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見回購；管理層只給淨稀釋目標"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"淨稀釋目標每年2.5%–3%（2026-02-12投資人日CFO），高於1.5%；股權激勵占營收19.6%（Q2 FY2026）"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：兩個期間的收購各約1.8–1.9億美元、占市值不到0.3%；不配息、未見回購，沒有可展開的股東回饋紀錄"}}}},"q5_valuation":{"verdict":"現價要求五年EPS年增約22%、且第五年市場仍給60倍，才換得年化10%；這接近本輪樂觀情境，我不信。","reasoning":"口徑用非GAAP Fwd P/E與PEG：GAAP盈餘被股權激勵吃掉（GAAP營業利益率0.5%），trailing P/E約503倍沒有意義。現價251.49美元＝FY2026共識EPS 2.53的99.4倍、FY2027 2.97的84.7倍；兩年EPS CAGR約21.7%，PEG約4.6，屬貴。P/S 22.8倍、EV/S 21.8倍，都在4個年度端點的最高位；連續五年分位事實表未涵蓋。反推：Base情境（FY2031E EPS 6.00、終端45倍）五年價值270美元，年化約1.4%；要年化10%需第五年405美元，等於EPS年增約22%且仍給60倍。賣方46位目標價均值285.28美元、中位數295美元、區間158–330美元（最高除以最低約2.1倍），現價低於均值約12%，方向上支持多頭，本裁決比共識悲觀；差異在框架：賣方沿用Q2的36%成長，我看Q3指引已降到28%–29%、FY2027營收共識年增22.5%，這個成長率配不上近百倍。最大客戶減量的利空已進入指引與賣方模型：FY2026 EPS共識2.53落在指引2.50–2.54之間，近3個月還上修4.55%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_kpi5_guidance_q3_fy2026_reven"],"verdict_values":{"valuation":{"basis":"非GAAP Fwd P/E（FY1與FY2）加PEG；GAAP盈餘被股權激勵吃掉，不採用","tier":"高成長基礎軟體平台","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率沒有倍數，同業Fwd P/E未涵蓋，不能拿來當倍數錨；終端倍數改以公司自身前份區間（成熟期50–65倍、穩定期40–50倍）與成長率對照"},"fwd_pe":99.4,"peg":4.6,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY1 Fwd P/E 99.4倍、FY2 84.7倍；PEG約4.6（高於2為貴）；P/S位於4個年度端點最高；Base情境五年年化約1.4%，低於8%及格線，結論為最貴一級。上行空間：短期＝12個月後FY2027共識EPS 2.97×80倍≈238美元，約−5.5%；中期＝五年Base 270美元，約+7.4%","targets":{"sellside_mean":285.28,"sellside_median":295,"sellside_high":330,"sellside_low":158,"sellside_count":46},"upside_short_pct":-5.5,"upside_mid_pct":7.4,"denominator_disputed":false,"denominator_note":"非GAAP EPS排除占營收19.6%的股權激勵，若以GAAP計倍數更高；分母口徑不影響偏貴的結論"}}},"q6_how_wrong":{"verdict":"最可能看錯的是價格而不是生意：現價已隱含接近樂觀情境；生意面最大的看錯點是AI原生客群與最大客戶的用量波動。","reasoning":"價值陷阱風險低：十類衰退信號無一確認亮起，留存、毛利、FCF都穩。三個方向的反證見反證紀錄：論點失敗的故事是AI原生客群退潮加上最大客戶自建，重演2021–2023年優化期；論點成功但股東經濟變差的故事是營收照長、每股盈餘被股權激勵與自建模型的GPU支出稀釋；價格已反映太多的故事是26週漲104%後倍數近百。最大回撤範圍−45%至−70%：起點FY1 Fwd P/E 99.4倍，一次下修指引倍數腰斬到55倍（2.53×55≈139美元，約−45%），成長熄火到10%上下倍數壓到30倍（2.53×30≈76美元，約−70%）；Q2財報揭露最大客戶減量後股價曾跌14.9%，單一事件就能打出雙位數跌幅。論點本身完整，深回撤是價格風險，持有者要有心理準備，不因波動本身砍倉。","fact_refs":["f_fwd_pe_latest","f_week26_return_pct","f_price_at_dd","f_consensus_eps_fy1","f_kpi12_net_revenue_retention_tr"],"verdict_values":{"trap":{"verdict":"🟢","label":"生意不是陷阱，價格才是風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.53,"pe":99.4,"basis":"FY2026E（FY1）非GAAP稀釋EPS共識2.53；終端倍數同樣套在當年度非GAAP EPS上"},"eps":{"bull":[3.15,4.05,5.05,6.2,7.5],"base":[2.97,3.75,4.45,5.2,6.0],"bear":[2.7,2.8,2.85,2.9,2.95]},"pe":{"bull":60,"base":45,"bear":32},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":13},"max_dd":{"lo":-70,"hi":-45,"basis":"起點FY1 Fwd P/E 99.4倍（EPS 2.53）。高點端：一次下修指引或AI原生客群轉弱，倍數腰斬到55倍，2.53×55≈139美元，約−45%；低點端：成長熄火到10%上下，倍數壓到30倍，2.53×30≈76美元，約−70%，並涵蓋Bear情境終點約−62.5%；Q2財報揭露最大客戶減量後股價曾跌14.9%，佐證單一事件即可打出雙位數跌幅","trigger_time":null},"basis":{"bull":"非AI業務維持20%以上、AI觀測與資安各長成10億美元級產品線，營收年增維持20%以上、營業利益率達27%：EPS年增約24%，貼近內生上界；第五年仍給60倍","base":"FY2027–2028照共識（2.97、3.75），之後EPS年增由19%遞減到15%；營收年增從約22%滑到17%、營業利益率走向25%以上、每年淨稀釋約2.5%；第五年成長約15%給45倍，低於前份成熟期區間下緣，因股權激勵仍占營收高位；同業現值倍數事實表未涵蓋","bear":"AI原生客群退潮、最大客戶轉自建，疊加自建模型的GPU與token支出吃掉利益率擴張：營收年增降到10%上下，EPS五年幾乎不動（FY2031E 2.95，不超過FY2027共識2.97）；倍數按成長熄火到10%給32倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2024年一家大型AI原生客戶縮減並部分改用內部工具，直接造成當年成長放緩；本輪最大客戶續約後減量，其所屬的AI原生客群2025年Q4貢獻約7個百分點年增；另有報導稱AI原生客群2026年Q1只成長個位數高段","assumption":"非AI業務的加速能長期抵銷AI原生客群的波動，且公司對AI原生曝險遠小於疫情時雲原生客群的約40%","consequence":"若AI原生客群集體優化、同時企業進入新一輪用量優化，成長從30%掉到15%以下，倍數由近百倍壓到30倍上下，五年後虧損五成以上","ruling":"部分採納：這是Bear情境的主軸，機率給30%、最大回撤低點端−70%；不全採，因管理層稱扣掉最大客戶後其餘業務成長率幾乎相同、非AI業務連5季加速、毛留存90%中後段。與唯一致命點部分重疊：唯一致命點是下修全年指引這個離散事件，本條是其背後最可能的成因","watch":"每季非AI營收年增、公司是否再揭露最大客戶減量、FY2026年報是否揭露單一客戶占營收10%以上","evidence_refs":["customer_second_source#4","customer_concentration_credit#5","customer_second_source#1","customer_concentration_credit#0"],"fact_refs":["f_kpi15_ai_yoy","f_kpi11_ai_native_1m_1m_arr_ai"]},{"view":"論點成功但股東經濟變差","evidence":"股權激勵占營收19.6%、占非GAAP營業利益85.7%，扣掉後FCF率只剩約5%；管理層淨稀釋目標每年2.5%–3%；CEO稱內部token與算力帳單暴增、開始在GPU上花更多錢訓練自家模型，且後續支出還會增加（2026-09-08）；公司同時推降低客戶帳單的計價換留存，總持有成本已是客戶標準提問","assumption":"營業利益率能從23%走向25%以上，股權激勵占比逐年下降","consequence":"營收照樣年增20%以上，但每股EPS年增只有十幾%，股東拿到的遠少於營收成長","ruling":"採納：Base情境EPS年增約19%，低於前兩年營收成長，資本配置評為偏弱；股權激勵占營收若連2季高於20%，或全年非GAAP營業利益率跌破22%，視為此路徑成立","watch":"每季股權激勵占營收、稀釋股數年增、非GAAP營業利益率、資本支出加資本化軟體占營收","evidence_refs":["substitute_technology#0","supply_demand_durability#1"],"fact_refs":["f_kpi4_stock_based_compensation","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow"]},{"view":"價格已反映太多","evidence":"26週漲104%；Fwd P/E 99.4倍（FY1）、P/S位於4個年度端點最高；Q3指引年增28%–29%，低於Q2的36%；Q2財報揭露最大客戶減量後股價曾跌14.9%","assumption":"市場會繼續用Q2的加速外推，並在第五年仍給60倍以上","consequence":"即使生意照Base走，五年年化只有約1%；任何一季成長不及預期都會先殺倍數","ruling":"採納：這是本輪觀望的綁定約束；股價回到185美元以下（FY2027共識EPS約62倍），Base五年年化才到約8%","watch":"FY2 Fwd P/E、每季營收相對指引上緣的超出幅度、FY2027共識EPS修正","evidence_refs":["end_markets#3","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_ps_percentile","f_kpi5_guidance_q3_fy2026_reven"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 207.98 → 本次 251.49（+20.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=207.98","side_b":"本次 price_at_dd=251.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"最大客戶的財測方法前後說法","cause":null,"prior_field":null,"side_a":"2026-05-07 Q1法說CFO：對最大客戶與上季一樣採更高程度保守，方法沒有改","side_b":"2026-08-06 Q2法說CEO：這次對最大客戶權重放得不一樣、完全去風險；2026-09-10高盛會議CFO：改成只把合約承諾額放進財測","ruling":"可調和、屬程度差異：方法確實改了，從打折用量變成只算承諾額，原因是該客戶用量已低於過去軌跡。好處是該客戶在財測裡有下限（CFO：不能低於承諾額），Q3與Q4下行有底；壞處是承諾額以上的用量不再算數，代表用量波動比公司過去說的大","evidence_level":"管理層原話（法說與會議逐字稿）","settle_metric":"Q3 FY2026營收相對指引上緣11.45億美元的超出幅度","if_then":["若Q3營收超出指引上緣3%以上且公司未再提最大客戶減量→視為減量已被承諾額兜住，維持觀望、不調機率","若公司再次揭露最大客戶減量或下修全年指引→Bear機率上調到35%，持有者減碼一半"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","end_markets#2"]},{"axis":"成長是在加速還是減速","cause":null,"prior_field":null,"side_a":"Q2營收年增35.6%、非AI客戶加速到20%後段、RPO年增43%、cRPO約40%、billings年增38%","side_b":"Q3指引年增28%–29%，FY2027營收共識年增22.5%","ruling":"可調和、屬程度差異：Q2指引29%–31%，實際做到35.6%，公司指引一向保守；Q3指引已計入最大客戶減量。cRPO約40%年增高於指引，支持Q3實際高於指引；但FY2027共識22.5%才是估值該用的成長率","evidence_level":"公司財報與指引","settle_metric":"Q3 FY2026實際營收年增率","if_then":["若Q3年增≥32%且Q4指引年增≥27%→FY2027共識EPS可能上修，重啟價位隨共識上修等比上調","若Q3年增低於30%→保守緩衝變薄，不追、停止加碼"],"evidence_refs":["end_markets#3"]},{"axis":"份額方向","cause":null,"prior_field":null,"side_a":"CFO：與競爭對手相比市占增幅非常大（2026-08-12）；CEO：規模上勝過所有對手並在搶市占（2026-05-07）","side_b":"Ramp：採用觀測性廠商的組織中34%用公司，年比持平；網站偵測占比5.78%排第三","ruling":"可調和、屬口徑差異：Ramp與網站偵測看的是有沒有用，不看花多少；公司靠既有客戶多買產品擴大錢包份額，採用家數持平與營收份額上升可以同時成立。但這也表示新客戶滲透加速沒有外部證據，護城河方向不判擴大","evidence_level":"第三方採購資料對管理層陳述","settle_metric":"Ramp採用率年比變化、新客戶占年增量比例","if_then":["若Ramp採用率年比下滑超過2個百分點→份額縮減列為衰退信號亮燈，護城河方向重評","若新客戶占年增量連2季≥30%→新客戶滲透加速成立"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"跨界整併是否削弱公司地位","cause":null,"prior_field":null,"side_a":"CFO：Snowflake、Palo Alto、Splunk之類的跨界進攻沒有改變競爭態勢，結果是公司地位增強（2026-08-12）","side_b":"第三方評論稱Palo Alto收Chronosphere、Snowflake收Observe形成夾擊；競品稱eBPF、自帶雲、按基礎設施計價是架構轉變；Gartner稱逾40家廠商、總持有成本已成標準提問","ruling":"方向相反、不可調和；裁定採管理層一側，依據是硬數據：非AI業務連5季加速到20%後段、毛留存90%中後段、Q2新企業客戶年化訂單年增逾一倍、多產品滲透一年內明顯加深；若夾擊已生效，這些數字應先轉弱。但定價面已被迫讓利（無限基數、聯邦日誌、自帶雲），所以護城河方向只判穩定不判擴大","evidence_level":"公司財報數據對第三方評論與競品行銷","settle_metric":"TTM淨營收留存率與非GAAP毛利率","if_then":["若淨營收留存連2季降到110%後段以下且非GAAP毛利率低於78%→改判夾擊生效，護城河方向下調為縮減，持有者減碼至一半","反向條件：若淨營收留存維持120%出頭且非AI年增連2季≥25%到2027年Q1→護城河方向可回到擴大"],"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","supply_demand_durability#1","supply_demand_durability#7"]},{"axis":"AI原生客群曝險大小","cause":null,"prior_field":null,"side_a":"CEO：對AI原生客戶的曝險比當年雲原生客戶（高峰約40%）小很多，上行大於下行（2026-09-08）","side_b":"AI原生客群去年底約占營收11%（投資人日），2025年Q4貢獻約7個百分點年增、2026年Q1仍是個位數高段；最大客戶就在這個客群","ruling":"可調和：營收占比確實小，但對成長率的貢獻遠高於占比；它是加速的邊際來源，不是營收主體。估值用的成長率要扣掉這部分的波動","evidence_level":"管理層陳述與年報、季報轉述","settle_metric":"AI原生客群對年增的貢獻百分點","if_then":["若AI原生客群對年增貢獻降到3個百分點以下而總成長仍≥25%→核心自給自足，Bear機率下調5個百分點","若AI原生客群貢獻轉負→停止加碼並檢查Bear情境"],"evidence_refs":["customer_concentration_credit#5","customer_second_source#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"公司指引一向先保守後上修：FY2026營收指引一年內從40.6–41.0億美元上調到43.0–43.4億、再到44.5–44.7億美元；CFO稱每天看得到逐客戶用量、幾近完整資訊（2026-08-12）；cRPO年增約40%、非AI連5季加速、超大雲端業者改外包、FY1共識近3個月上修4.55%。若FY2027 EPS最後做到3.4美元，現價只有74倍","side_b":"就算FY2027做到3.4美元，74倍仍需五年EPS年增20%以上且終端仍給50倍以上才有年化8%；Q3指引已降到28%–29%，最大客戶減量顯示AI原生用量可逆","ruling":"部分採納：上修空間真實存在，所以重啟條件加一條FY2027共識EPS上修到3.40美元以上時門檻同比上調；但在現價，Base五年年化約1.4%，不足以建倉","evidence_level":"公司指引紀錄與管理層原話","settle_metric":"FY2027共識EPS","if_then":["若FY2027共識EPS上修到3.40美元以上而股價漲幅未超過10%→重跑判斷，視為估值落差收斂","若FY2027共識EPS下修→重啟價位同比下調"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"綜合評級與估值（前份漂移）","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-16，股價207.98美元）：綜合評級B、估值最貴一級","side_b":"本輪（股價251.49美元，+20.9%）：綜合評級B、估值最貴一級，兩欄都不變；FY1 Fwd P/E 99.4倍、PEG約4.6","ruling":"結論不變但更貴：股價漲20.9%，同期FY1共識EPS近3個月只上修4.55%，漲幅遠大於盈餘上修；生意品質沒有退步，綜合評級仍是B","evidence_level":"事實表價格與共識快照","settle_metric":"FY2 Fwd P/E","if_then":["若FY2 Fwd P/E回到62倍以下→估值結論降一級並重跑判斷","若FY2 Fwd P/E升破100倍→維持觀望、不追"],"evidence_refs":[]},{"axis":"護城河方向與陷阱風險（前份漂移）","cause":"新證據","prior_field":["moat_trend","trap"],"side_a":"前份：護城河方向擴大；價值陷阱風險低","side_b":"本輪：護城河方向穩定；價值陷阱風險低不變","ruling":"方向由擴大調為穩定：2026-08-06揭露最大客戶續約後減量（領先者在最大客戶的份額下滑，不能判擴大）、Ramp採用率年比持平、公司主動推降低帳單的計價換留存；執行面仍在擴大，定價面小幅讓利，淨為穩定。陷阱風險維持低：十類衰退信號無一確認亮起","evidence_level":"公司法說揭露與第三方採購資料","settle_metric":"TTM淨營收留存率、Ramp採用率年比","if_then":["若淨營收留存維持120%出頭且Ramp採用率年比上升≥2個百分點→方向回到擴大","若淨營收留存連2季降到110%後段以下→方向下調為縮減"],"evidence_refs":["customer_second_source#0","customer_concentration_credit#0","competitive_share_entrants#0"]},{"axis":"前份空白欄位補齊（前份漂移）","cause":"方法變動","prior_field":["dca_verdict","dca_role","runway_post_y5","archetype","cycle_position","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位全為空白：舊流程把裁決寫成一段文字，沒有落欄，也沒有情境樹機率與最大回撤","side_b":"本輪：五年後跑道判寬、生意型態判品質複利成長；情境樹三支路徑（Bull 60倍、Base 45倍、Bear 32倍）與機率25／45／30、最大回撤−45%至−70%，報酬與不對稱比由程式算出；裁決與角色由決策矩陣算出；循環位置不適用（非循環股）仍留空","ruling":"屬方法變動而非判斷翻面：前份沒有這些欄可比，本輪首次落值，不代表基本面變化","evidence_level":"流程口徑","settle_metric":"無（口徑對齊）","if_then":["下次複審起這些欄位逐欄對帳，任何變動需歸因到價格、新證據或方法"],"evidence_refs":[]},{"axis":"重啟門檻（前份漂移）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"等回測 BB 中軌 $131 或 W52 $139 + Fwd PE 修復至 55-60x 再分批","side_b":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","ruling":"重啟首倉（分批加碼）的門檻從技術位階加倍數區間，改成報酬率錨：以Base情境五年價值270美元反推年化8%的買點。前份131美元與139美元是技術位置，現在52週均線已升到177.7美元，舊門檻失去意義；55–60倍的倍數條件以FY2027共識EPS 2.97換算落在163–178美元，與新門檻185美元相近","evidence_level":"情境樹反推與週線均線","settle_metric":"股價相對185美元","if_then":["若股價≤185美元且最近一季非AI營收年增≥20%→重跑判斷，通過後分批首倉三分之一","若FY2027共識EPS上修到3.40美元以上→門檻同比上調到約212美元"],"evidence_refs":[]},{"axis":"出場指標（前份漂移）","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（空白）","side_b":"非AI營收年增連3季低於18%；全年營收指引任一次下修；TTM淨營收留存連2季降到110%後段以下；股權激勵占營收連2季高於20%；非GAAP毛利率連2季低於77%","ruling":"新設理由是2026-08-06揭露的最大客戶減量，讓用量可逆性成為可量測風險：全年指引下修觸發清倉，非AI年增與留存轉弱觸發減碼一半，股權激勵與毛利率觸發停止加碼","evidence_level":"公司法說揭露","settle_metric":"各出場指標每季讀數","if_then":["任一清倉條件觸發→持有者清倉並重跑判斷","兩項減碼條件同時觸發→持有者減碼一半"],"evidence_refs":["end_markets#2"]},{"axis":"Single Thing（前份漂移）","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"公司下修全年營收指引，打破一向先保守後上修的模式；最可能成因是最大客戶或AI原生客群進一步減量","ruling":"Single Thing新設：最大客戶續約後減量（2026-08-06）與財測方法改為只算承諾額（2026-09-10），讓指引下修成為近百倍倍數最敏感的單一離散事件；發生即清倉","evidence_level":"公司法說與會議原話","settle_metric":"每季全年指引中值對比前次","if_then":["若下修→持有者清倉","若連續兩季上修且非AI年增≥25%→機率由15%下調到10%"],"evidence_refs":["customer_concentration_credit#0"]}],"triggers":[{"n":1,"text":"非AI客戶營收年增守住20%","type":"假設驗證","maps_to":"H1","metric":"非AI客戶營收年增率（公司季報口徑）","threshold":"連2季低於19%＝削弱；連3季低於18%＝反轉","action":"削弱→停止加碼；反轉→持有者減碼一半","source_freq":"季報電話會，每季","date":"2026-11（Q3 FY2026財報）"},{"n":2,"text":"最大客戶與AI原生客群用量","type":"風險","maps_to":"R1","metric":"公司是否再揭露最大客戶減量；下季營收指引年增率","threshold":"再次揭露減量，或下季指引年增低於20%","action":"持有者減碼一半；未持有者取消重啟","source_freq":"季報，每季","date":"2026-11（Q3 FY2026財報）","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","end_markets#2","customer_second_source#1"]},{"n":3,"text":"下修全年營收指引","type":"Single Thing","maps_to":null,"metric":"全年營收指引區間中值","threshold":"任何一次低於前次指引中值","action":"持有者清倉；未持有者重跑完整判斷後才考慮","source_freq":"季報新聞稿，每季","date":"2026-11（Q3 FY2026財報）","evidence_refs":["end_markets#3"]},{"n":4,"text":"估值回到可分批區","type":"估值rearm","maps_to":null,"metric":"股價與FY2027共識EPS倍數","threshold":"股價≤185美元（約FY2027共識EPS 62倍）；FY2027共識EPS上修到3.40美元以上時門檻同比上調","action":"重跑判斷，通過後分批首倉三分之一","source_freq":"每日股價、每月共識快照","date":null},{"n":5,"text":"留存與定價力","type":"風險","maps_to":"R2","metric":"TTM淨營收留存率、非GAAP毛利率","threshold":"淨營收留存連2季降到110%後段以下，且非GAAP毛利率低於78%","action":"護城河方向下調為縮減，持有者減碼至一半","source_freq":"季報電話會，每季","date":null,"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","supply_demand_durability#7"]},{"n":6,"text":"股東經濟：股權激勵與利益率","type":"風險","maps_to":"R3","metric":"股權激勵占營收、非GAAP營業利益率","threshold":"股權激勵占營收連2季高於20%，或全年非GAAP營業利益率低於22%","action":"下修Base情境EPS路徑，停止加碼","source_freq":"季報新聞稿，每季","date":null},{"n":7,"text":"年報複審：客戶集中度與FY2027指引","type":"複審日期","maps_to":null,"metric":"年報單一客戶占營收揭露、FY2027營收指引年增","threshold":"單一客戶占營收≥10%，或FY2027指引年增低於20%","action":"重跑完整判斷","source_freq":"年報，每年","date":"2027-02"}],"kill_metrics":[{"metric":"非AI客戶營收年增率","bear_threshold":"連3季低於18%","window":"每季，至2028年Q2","source":"公司季報電話會","last_status":"ok"},{"metric":"全年營收指引","bear_threshold":"任一次下修至低於前次指引中值","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"TTM淨營收留存率","bear_threshold":"連2季降到110%後段以下","window":"每季","source":"公司季報電話會","last_status":"ok"},{"metric":"股權激勵占營收","bear_threshold":"連2季高於20%","window":"每季","source":"公司季報新聞稿","last_status":"warning"},{"metric":"非GAAP毛利率","bear_threshold":"連2季低於77%","window":"每季","source":"公司季報電話會","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至185美元以下（約FY2027共識EPS 62倍、Base五年年化約8%）才重跑判斷分批；共識上修時門檻同比上調","exec_line":"觀望不建倉。綁定約束是估值：股價≤185美元且最近一季非AI營收年增≥20%，重跑判斷通過後分批首倉三分之一；已持有者遇下修全年指引即清倉，非AI年增連2季低於19%減碼一半，波動本身不砍倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場沿用Q2的36%成長並給近百倍FY1非GAAP盈餘；但Q3指引已降到28%–29%、FY2027營收共識年增22.5%，且非GAAP盈餘排除了占營收19.6%的股權激勵，這個成長率配不上現價倍數","momentum_overheated":false,"cycle_gates_pass":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場沿用Q2的36%成長並給近百倍FY1非GAAP盈餘；但Q3指引已降到28%–29%、FY2027營收共識年增22.5%，且非GAAP盈餘排除了占營收19.6%的股權激勵，這個成長率配不上現價倍數"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='→', week26=103.98, valuation_dependent=False","input_gap":["week26_return_pct 落 100-150% 邊界帶，QC-42 反動能閘裁量範圍，本腳本無法自動判定，預設不放行"]},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"核心非AI業務維持20%以上成長，總營收在最大客戶減量後仍守住20%以上","2y":"2028年Q2前非AI客戶營收年增每季≥20%；FY2027營收年增≥20%","5y":null,"10y":null,"threshold":"非AI客戶營收年增≥20%（目前20%後段）；FY2027營收年增≥20%（共識22.5%）","source":"公司季報電話會非AI營收年增口徑；FY2027全年指引","drift_rule":"連2季低於門檻5%以上（低於19%）＝削弱；連3季低於門檻10%以上（低於18%）＝反轉"},{"id":"H2","text":"整合平台讓客戶越用越多產品，留存維持高檔、錢包份額持續擴大","2y":null,"5y":"2031年前用6項以上產品的客戶比率從37%升到≥50%，TTM淨營收留存維持≥115%","10y":"2036年觀測性市占由13%–14%升到≥25%","threshold":"TTM淨營收留存≥115%、毛留存維持90%中段以上","source":"公司季報電話會留存與多產品揭露；管理層會議市占陳述","drift_rule":"5年期：留存連4季低於門檻5%以上＝削弱、連6季低於門檻10%以上＝反轉；10年期：市占跨2個年度未升＝削弱、跨3個年度＝反轉"},{"id":"H3","text":"營業槓桿與股權激勵下降，讓營收成長轉成每股盈餘","2y":null,"5y":"FY2028非GAAP營業利益率≥25%、股權激勵占營收≤16%、淨稀釋每年≤3%","10y":null,"threshold":"FY2028非GAAP營業利益率≥25%（長期目標25%以上）且股權激勵占營收≤16%（Q2 FY2026為19.6%）","source":"公司季報新聞稿；2026-02-12投資人日長期目標","drift_rule":"連4季TTM偏離門檻路徑5%以上＝削弱；連6季偏離10%以上＝反轉"}],"R":[{"id":"R1","text":"最大客戶與AI原生客群用量可逆：續約後減量，2024年已有AI原生客戶部分改自建","h_ref":"H1","clock":"⚡","threshold":"再次揭露最大客戶減量，或下季營收指引年增低於20%；連2季即減碼","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#5","end_markets#2"]},{"id":"R2","text":"跨界平台捆綁與計價模式轉變壓低單位收費，留存與毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"TTM淨營收留存連4季低於115%，或非GAAP毛利率連2季低於78%","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1","supply_demand_durability#1","supply_demand_durability#7"]},{"id":"R3","text":"自建模型的GPU與token支出加上高股權激勵，吃掉營業槓桿：2026-05-07 CEO說工作負載走營業費用、若資本支出模式改變會告知；2026-09-08 CEO已說token與算力帳單暴增、GPU支出增加且還會更多","h_ref":"H3","clock":"🐢","threshold":"全年非GAAP營業利益率低於22%，或股權激勵占營收連2季高於20%，或資本支出加資本化軟體占營收超過5%","evidence_refs":[]}],"single_thing":{"description":"公司下修全年營收指引，打破一向先保守後上修的模式；最可能的成因是最大客戶或AI原生客群進一步減量","why_fatal":"現價約99倍FY1 EPS，隱含每季持續超出並上修；公司自稱每天看得到逐客戶用量，一旦下修代表需求真的斷了而非保守過頭，倍數會先腰斬（55倍×2.53≈139美元，約−45%）","if_happens":"持有者清倉；未持有者不承接，等下一季數字重跑完整判斷","how_monitor":"每季財報的全年指引中值對比前次；最大客戶相關揭露；FY2026年報客戶集中度","probability":"12–24個月約15%：最大客戶已改為只以承諾額入財測，Q3與Q4有下限，但AI原生客群用量可逆"}},"appendix_a":{"growth_durability":8,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":84.7,"peg_fy2":3.9,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":2.53,"FY2027E":2.97,"FY2028E":3.75},"fy_end_month":12,"eps_basis":"非GAAP稀釋EPS，Koyfin共識2026-09-19快照；FY2025實際EPS事實表未涵蓋，故基期留空"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 FY2026財報與Q4指引","impact":"高","watch":"營收是否超出指引上緣11.45億美元3%以上；非AI營收年增是否維持20%後段；是否再提最大客戶減量"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026年報與FY2027全年指引","impact":"高","watch":"FY2027營收指引年增是否≥20%；年報是否揭露單一客戶占營收10%以上"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"Bits AI改為AI credits計價的後續說明","impact":"中","watch":"AI credits是否開始在營收或ARR揭露中看得到"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
