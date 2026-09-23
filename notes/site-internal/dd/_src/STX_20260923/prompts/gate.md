你是 DD 管線 v20 的判斷層閘（gate），標的 STX（20260923）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝3629 $M（YoY +48.5%，QoQ +16.6%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 investors.seagate.com Q4 FY26 press release（表格對照 SEC 8-K 附件 stxq42026pressreleasefinan.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：共識約 $3.48–3.50B（媒體彙整兩個版本 $3.48B／$3.50B，非單一權威來源）；亦高於公司 Q4 指引上緣 $3.55B（$3.45B ±$0.1B）
- `f_kpi1_non_gaap_gross_margin`（q1_business）｜Non-GAAP gross margin＝52.7 %｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：未取得共識
- `f_kpi2_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income／margin＝44.6 %（營業利益 $1,619M）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（QoQ +710 bps，non-GAAP opex $293M＝營收 8%）（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：未取得共識（僅查到營收與 EPS）
- `f_kpi11_exabytes_shipped`（q1_business）｜Exabytes shipped（總出貨）＝218 EB（YoY +34%，QoQ +9.5%；其中資料中心 195 EB，占 89%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）（numbers.latest_quarter_kpis.items[11]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：未取得
- `f_kpi12_revenue_per_exabyte_asp`（q1_business）｜Revenue per exabyte（ASP 替代指標，自算）＝16.6 $M／EB（營收 $3,629M ÷ 218 EB；QoQ +6.5%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：IR 新聞稿營收 ÷ 法說逐字稿總出貨 EB；公司未揭露單價（ASP）（numbers.latest_quarter_kpis.items[12]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：不適用
- `f_kpi13_price_per_exabyte_yoy`（q1_business）｜Price per exabyte（YoY）＝10 %（6 月季；9 月季指引隱含約 20% 以上，為 Morgan Stanley 分析師推算）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q4 FY26 法說 Q&A（Morgan Stanley 分析師引述公司數字，CFO 答覆確認供需缺口擴大、定價較佳；Koyfin 逐字稿）（numbers.latest_quarter_kpis.items[13]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：不適用
- `f_kpi15_nearline_exabyte_lta_bac`（q1_business）｜Nearline exabyte 長約（LTA）覆蓋（backlog 替代；公司未揭露數字 backlog／book-to-bill／產能利用率）＝vast majority 已配置至 CY2028 定性；HAMR 占 nearline exabyte 出貨run rate 約 40%（6 月）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：CEO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）；訂單須先簽約定義規格與價格才開始生產，涵蓋整個 CY2027（numbers.latest_quarter_kpis.items[15]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：不適用
- `f_kpi7_guidance_q1_fy2027_reven`（q1_business）｜Guidance — Q1 FY2027 revenue＝4100 $M（區間 $4,000–4,200M；中點 YoY +56%）｜期間與口徑：Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（numbers.latest_quarter_kpis.items[7]，as_of Q4 FY2026 公告（2026-07-28）對 Q1 FY2027（2026 年 9 月季）的指引）
  - 註記：未取得 Q1 FY27 共識
- `f_kpi8_guidance_q1_fy2027_non_g`（q1_business）｜Guidance — Q1 FY2027 non-GAAP operating margin（營收中點）＝50 %（約；non-GAAP opex 約 $300M）｜期間與口徑：Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）（numbers.latest_quarter_kpis.items[8]，as_of Q4 FY2026 公告（2026-07-28）對 Q1 FY2027 的指引）
  - 註記：未取得 Q1 FY27 共識
- `f_peer_stx_gross_margin_pct`（q2_moat）｜STX 毛利率＝45.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_stx_operating_margin_pct`（q2_moat）｜STX 營業利益率＝34.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mu_gross_margin_pct`（q2_moat）｜MU 毛利率＝72.57 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.gross_margin_pct，as_of TTM ending 2026-05-31（4季加總））
- `f_peer_000660_ks_gross_margin_pct`（q2_moat）｜000660.KS 毛利率＝76.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_gross_margin_pct`（q2_moat）｜005930.KS 毛利率＝57.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝35.78 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-09-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝55.37 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-09-19）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝78.29 USD/share｜期間與口徑：2026-09-19／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20260919.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-09-19）
- `f_kpi10_guidance_fy2027`（q1_business）｜Guidance — FY2027 全年營收成長（定性，無數字區間）＝> 34 %（管理層僅稱 FY27 營收成長將高於 FY26 的 34%；capex 維持 4–6% 營收目標區間）｜期間與口徑：Q4 FY2026 公告（2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：CEO／CFO prepared remarks（Koyfin 逐字稿 STX_Q4_2026_Earnings_Call_20260728.md）（numbers.latest_quarter_kpis.items[10]，as_of Q4 FY2026 公告（2026-07-28））
  - 註記：未取得
- `f_kpi5_free_cash_flow`（q1_business）｜Free cash flow＝1118 $M（FCF margin 約 31%；營運現金流 $1,305M − capex $187M）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q4 FY26 press release（表格對照 SEC 8-K 附件）；FY2026 全年 FCF $3,105M（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：未取得共識
- `f_kpi6_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝3.3 %（SBC $54M；占營收 1.5%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q4 FY26 press release non-GAAP 調節表（FY2026 全年 SBC $213M − 前三季 $159M＝Q4 $54M，與新聞稿單季數相符）（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：不適用
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝914.72 USD｜期間與口徑：2026-09-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-09-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.52 x｜期間與口徑：2026-09-19／分母＝FY1 EPS 35.78，分子＝快照價 877.33｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-09-19）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝65.9 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-09-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝17.07 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝17.25 x｜期間與口徑：2026-09-23（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-09-23（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-09-23（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝121.52 %｜期間與口徑：2026-09-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-09-23（RTH 收盤，UTC））
- `f_kpi4_non_gaap_diluted_eps`（q1_business）｜Non-GAAP diluted EPS＝5.71 $（GAAP $5.58；QoQ +39%，YoY +121%）｜期間與口徑：Q4 FY2026（季末 2026-07-03，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q4 FY26 press release；CFO prepared remarks（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-07-03，公告於 2026-07-28））
  - 註記：共識約 $5.09–5.10（媒體彙整兩個版本）；亦高於公司 Q4 指引上緣 $5.20（$5.00 ±$0.20）

### findings_digest 中方向為負或來源衝突的條目（25 條）
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Forbes（Tom Coughlin）標題主張：儲存與記憶體的價格飆升支撐 AI 需求，但『可能是暫時的』（僅據標題；內文未取得）。屬週期性論點，與『結構性缺貨』說法相反。
  - 來源：Forbes, Tom Coughlin, 'Storage And Memory Price Surges Supporting AI Demand Likely Temporary', https://www.forbes.com/sites/tomcoughlin/2025/10/10/storage-and-memory-price-surges-supporting-ai-demand-likely-temporary/（as_of 2025-10-10）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：2023-04-18 Seagate 與美國商務部工業安全局（BIS）達成和解：因 2020 年 8 月至 2021 年 9 月向被列入實體清單的華為出貨逾 740 萬顆硬碟，被處 3 億美元民事罰款；另有暫緩執行的拒絕出口令，在令發出滿五年且付款與稽核義務履行後豁免。
  - 來源：CNBC 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei' (2023-04-20); Paul, Weiss 'BIS Imposes $300 Million Penalty Against Seagate for Export Control Violations'; BIS order e2836.pdf（as_of 2023-04-20）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2026 10-K（會計年度止於 2026-07-03，簽署日 2026-08-04）前瞻聲明仍提到「按時支付與 BIS 和解協議的每季款項」的預期；風險因素寫明部分產品與服務受出口管制法規約束，法規變動或違反可能對業務、營運結果、財務狀況與現金流造成重大不利影響；製造據點含中國、馬來西亞、北愛爾蘭、新加坡、泰國與美國。10-K 法律程序段擷取內容僅見智慧財產權與環境事項，未見對 Seagate 的反壟斷或競爭主管機關調查。
  - 來源：Seagate Technology Holdings plc Form 10-K FY2026 (https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm)（as_of 2026-08-04）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Seagate FY2026 10-K risk factors state that changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on its business and results of operations; the 10-K also lists the impact of trade policy (including tariffs) and FX on the cost of producing its products and the effective price to customers as a factor.
  - 來源：Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm（as_of 2026-07-03）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Seagate FY2026 10-K states that some of its products and services are subject to export control laws, that changes to or violation of these laws could have a material and adverse effect on the business, and that if it were prohibited from selling to key customers for any reason, such as export regulations, revenues and results could be materially and adversely affected.
  - 來源：Seagate Technology Holdings plc Form 10-K, fiscal year ended 2026-07-03, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm（as_of 2026-07-03）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：In April 2023 the U.S. Commerce Department's BIS imposed a $300 million civil penalty on Seagate Technology LLC and Seagate Singapore for selling over 7.4 million HDDs to Huawei (added to the Entity List in May 2019) in violation of the Foreign Direct Product Rule; BIS also imposed a multi-year audit requirement and a five-year suspended Denial Order. This is the largest standalone administrative penalty in BIS history.
  - 來源：CNBC, 'Seagate hit with $300 million penalty for continuing $1 billion relationship with blacklisted firm Huawei, despite U.S. export controls', https://www.cnbc.com/2023/04/20/seagate-to-pay-300-million-penalty-over-billion-dollar-deal-with-huawei.html ; Orrick, 'Seagate Export Control Penalty Shows New, Aggressive China-Trade Enforcement'; Arnold & Porter Enforcement Edge blog (2023-04)（as_of 2023-04-20）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#5`（reg_tariff_export｜方向 -｜狀態 ok）：A Yahoo Finance article on Western Digital (HDD peer) states that the proposed tariffs focus on a wider set of chip-related products, including hardware used in data center servers and storage, and that this could influence WDC's component and system costs and where it sources and assembles drives for hyperscale and AI customers. The article is about WDC, not STX, and does not name Section 232 or Seagate.
  - 來源：Yahoo Finance, 'How Exposed Is Western Digital (WDC) To New Semiconductor Tariffs?', https://finance.yahoo.com/technology/articles/exposed-western-digital-wdc-semiconductor-021558493.html（as_of 2026-08-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Seagate 10-K risk-factor language: 'Shortages or delays in the receipt of, or cost increases in, critical components, equipment or raw materials necessary to manufacture our products, as well as reliance on single-source suppliers, have in the past and may in the future affect our production.' Also: 'Certain components and raw materials are available from a limited number of suppliers.'
  - 來源：Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm（as_of 2026-07-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Seagate 10-K states production requires 'commodities and specialty materials, including certain rare earth elements, precious metals and specialized alloys, which may be subject to supply constraints or price volatility.'
  - 來源：Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm（as_of 2026-07-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Seagate 10-K states: 'Changes in U.S. trade policy, including the imposition of sanctions or tariffs and the resulting consequences, may have a material and adverse impact on our business and results of operations.' It also says some products are subject to export control laws. The excerpt read has no explicit Taiwan-specific or Middle East/Iran language.
  - 來源：Seagate Technology Holdings plc Form 10-K FY2026, https://www.sec.gov/Archives/edgar/data/0001137789/000113778926000159/stx-20260703.htm（as_of 2026-07-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#5`（geo_supply_chain｜方向 -｜狀態 ok）：Third-party mapping (Gillware, estimate) says Japan's Nidec makes on the order of 80% of the world's HDD spindle motors. MinebeaMitsumi is a second source with Thailand manufacturing.
  - 來源：Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/（as_of 2026-07-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#6`（geo_supply_chain｜方向 -｜狀態 ok）：Third-party mapping (Gillware) says China accounted for roughly 60% of world mined rare-earth supply and around 90% of refining of magnet-grade material used in HDD magnets. Japan produces the finished magnets.
  - 來源：Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/（as_of 2026-07-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#7`（geo_supply_chain｜方向 -｜狀態 ok）：Third-party mapping (Gillware) says HDD controller silicon is designed by Broadcom and Marvell and manufactured by TSMC (Taiwan), with OSAT assembly in Taiwan and elsewhere in Asia. This is an industry-level map; it does not name Seagate's own controller vendors.
  - 來源：Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/（as_of 2026-07-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#8`（geo_supply_chain｜方向 -｜狀態 ok）：Third-party mapping (Gillware) says HDD final assembly is centered in a Thailand cluster (primary), with Malaysia and China also involved. It says the 2011 Thailand floods eliminated up to half of global HDD manufacturing capacity within weeks and roughly doubled drive prices.
  - 來源：Gillware, 'The 2026 Hard Drive Supply Chain, Mapped', https://www.gillware.com/articles/hard-drive-supply-chain/（as_of 2026-07-06）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：TrendForce 稱 AI 推論需求使 nearline HDD 交期由數週拉長到 52 週以上；高容量 QLC SSD 出貨 2026 年『可能爆發式成長』；與 nearline HDD 相比，QLC SSD 效能較高、功耗約低 30%。該文未給 QLC 出貨量或每 TB 成本的數字。
  - 來源：TrendForce Press Center, 'Soaring Inference AI Demand Triggers Severe Nearline HDD Shortages; QLC SSD Shipments Poised for Breakout in 2026' https://www.trendforce.com/presscenter/news/20250915-12714.html（as_of 2025-09-15）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：同一篇文章列出的風險：若需求或價格轉弱，Seagate 的負債與資本密集度是否可控；並提到謹慎的分析師擔心能源效率需求上升，可能限縮 Mozaic 4+ 的上行空間。文章未量化 SSD 替代幅度，也未寫 WD 的 HAMR 時程。
  - 來源：Yahoo Finance, 'Seagate (STX) Expands HAMR With Hyperscalers: Is Mozaic 4+ the Margin Story Investors Missed?' https://finance.yahoo.com/news/seagate-stx-expands-hamr-hyperscalers-043020641.html（as_of 2026-03-05）｜affects：decision_inputs.bear、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：Seagate 同意支付 1.75 億美元和解證券集體訴訟（每股約 1.03 美元）；原告指控公司隱瞞對中國客戶（Huawei）銷售規模且違反美國出口管制。集體期間 2020-09-14 至 2023-04-19，N.D. Cal. 受理；被告（Seagate、CEO Mosley、CFO Romano）否認指控。法院於 2026-07-07 初步核准和解，最終聽證會 2026-11-17，請求權申報截止 2026-10-19。
  - 來源：Seagate Securities Litigation 和解網站 https://seagatesecuritieslitigation.com/（金額、期間、聽證日、截止日）；初步核准日 2026-07-07 見 Kessler Topaz https://www.ktmc.com/new-cases/seagate-technology-holdings-plc/ 與 Levi & Korsinsky https://zlk.com/cases/seagate-technology-holdings-plc-class-action-lawsuit-stx 的搜尋摘要（該日期未在和解網站頁面正文中出現）（as_of 2026-07-07）｜affects：decision_inputs.bear、valuation、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2023-04-18 Seagate 與美國商務部 BIS 簽和解協議，處理對 Huawei 販售硬碟一案；公司同意向 BIS 支付 3 億美元，自 2023-10-31 起五年內每季分期 1,500 萬美元。截至 FY2026 Q2 10-Q（期末 2026-01-02），資產負債表列示應計餘額 6,000 萬與 1.05 億美元兩筆。
  - 來源：Seagate Technology Holdings plc Form 10-Q（期末 2026-01-02）https://www.sec.gov/Archives/edgar/data/1137789/000113778926000026/stx-20260102.htm，Legal Proceedings / Contingencies（as_of 2026-01-02）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2023（截至 2023-06）營收 $7.384B，FY2022 為 $11.661B；GAAP 毛利率 18.3%（FY2022 為 29.7%）、non-GAAP 毛利率 21.1%（FY2022 為 30.1%）；GAAP 淨損 $529M（FY2022 為淨利 $1.649B）；營運現金流 $942M（FY2022 為 $1.657B）。
  - 來源：Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx（as_of 2023-07-26）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2023 第四季（2023-06 季）營收 $1.602B，去年同期 $2.628B；GAAP 毛利率 19.0%（去年同期 28.9%）、non-GAAP 毛利率 19.5%（去年同期 29.3%）；GAAP 淨損 $92M。
  - 來源：Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx（as_of 2023-07-26）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：過去十二個月（至 FY2023 結束）產能閒置費用（扣除折舊攤銷後）合計 $171M，公司揭露原因含無錫廠疫情封控與生產計畫調整。
  - 來源：Seagate IR — Seagate Technology Reports Fiscal Fourth Quarter and Fiscal Year 2023 Financial Results, https://investors.seagate.com/news/news-details/2023/Seagate-Technology-Reports-Fiscal-Fourth-Quarter-and-Fiscal-Year-2023-Financial-Results/default.aspx（as_of 2023-07-26）｜affects：decision_inputs.bear、moat_trend
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：FY2023 第三季（2023-03 季）營收約 $1.9B、毛利率 17%，為搜尋摘要所見 FY2023 各季中最低的一季（搜尋摘要轉述 10-Q 與 Seagate IR 第三季新聞稿；未抓全文核對，as_of 取季末日）。
  - 來源：SEC Form 10-Q for quarter ended 2023-03-31, https://www.sec.gov/Archives/edgar/data/1137789/000113778923000029/stx-20230331.htm（as_of 2023-03-31）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#4`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Blocks and Files 報導：FY2023 營收較前一年下滑 37%，為 17 年來最低年度營收，也是 13 年以上來首次全年虧損；CEO Mosley 稱「a profound downturn in demand」，原因包含中國復甦不均、雲端庫存消化、企業支出謹慎；最大買家超大規模雲端業者的 nearline 硬碟採購大減。
  - 來源：Blocks and Files — Seagate cites 'profound downturn in demand' as revenues dip... and it won't get better soon, https://www.blocksandfiles.com/disk/2023/07/27/seagate-cites-profound-downturn-in-demand-as-revenues-dip-and-it-wont-get-better-soon/1613546（as_of 2023-07-27）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#5`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Tom Coughlin（Forbes）：2023 年第二季全產業硬碟出貨總容量（EB）較第一季下降約 19.3%；2023 全年出貨容量估約 875EB，較前一年下降約 29%（搜尋摘要彙整自 Coughlin 系列文章，全年數字對應文章為 2023-12-10 的 2024 年預測，未抓全文核對）。
  - 來源：Forbes / Tom Coughlin — C2Q 2023 Hard Disk Drive Industry Update, https://www.forbes.com/sites/tomcoughlin/2023/08/14/c2q-2023-hard-disk-drive-industry-update/ ；Digital Storage And Memory Projections For 2024, Part 1, https://www.forbes.com/sites/tomcoughlin/2023/12/10/digital-storage-and-memory-projections-for-2024-part-1/（as_of 2023-08-14）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Seagate 同意支付 1.75 億美元和解證券集體訴訟（每股約 1.03 美元）；集體期間 2020-09-14 至 2023-04-19，N.D. Cal. 受理；被告否認指控。法院於 2026-07-07 初步核准和解，最終聽證會 2026-11-17，請求權申報截止 2026-10-19。
  - 來源：Seagate Securities Litigation 和解網站 https://seagatesecuritieslitigation.com/（金額、期間、聽證日、截止日）；初步核准日 2026-07-07 見 Kessler Topaz https://www.ktmc.com/new-cases/seagate-technology-holdings-plc/ 搜尋摘要（as_of 2026-07-07）｜affects：decision_inputs.bear、valuation、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 15 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1620.0,"bear_5y_price":300.0,"p_bull_pct":30,"p_bear_pct":30,"upside_5y_pct":-21.8,"ev5y_pct":-5.8,"irr_base_pct":-4.8,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":35.78,"pe":25.57,"basis":"FY2027E 共識 non-GAAP 稀釋 EPS 的前瞻本益比；終端倍數同樣套在單一財年 non-GAAP EPS（FY2031E）上"},"eps":{"bull":[38.0,62.0,86.0,98.0,108.0],"base":[35.5,50.0,58.0,56.0,55.0],"bear":[34.0,40.0,30.0,22.0,25.0]},"pe":{"bull":15,"base":13,"bear":12},"p":{"bull":30,"base":40,"bear":30},"yield_pct":{"dividend":0.3,"net_buyback":0.2},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STX_Q3_2026_Earnings_Call_20260428.md
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季（FQ4）營收財測：34.5 億美元，上下 1 億美元。（原話："range of $3.45 billion, plus or minus $100 million"）
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季 non-GAAP EPS 財測：5 美元，上下 0.20 美元。（原話："Non-GAAP EPS is expected to be $5 plus or minus $0.20"）
- 2026-04-28｜CFO｜guidance：CFO 給 6 月季 non-GAAP 營業費用約 2.95 億美元（上一季實際 2.96 億）。（原話："operating expenses are expected to be approximately $295"）
- 2026-04-28｜CFO｜guidance：CFO 以營收財測中點計，6 月季 non-GAAP 營業利益率的口徑是「lower 40% range」，未給確切數字。（原話："in the lower 40% range"）
- 2026-04-28｜CFO｜guidance：CFO 預期自由現金流在 2026 日曆年剩餘季度持續改善。（原話："free cash flow generation to improve further"）
- 2026-04-28｜CFO｜guidance：CFO 預期 6 月季其他收支（其他收入與費用）與本季大致持平。（原話："other income and expense to remain relatively flat"）
- 2026-04-28｜CEO｜guidance：CEO 把年營收成長長期目標，從原本低至中十位數百分比，調高為至少 20%（未給明確期限，只說未來幾年）。（原話："target from the low to mid-teens to a minimum of 20%"）
- 2026-04-28｜CEO｜guidance：CEO 表示公司績效已超前一年前分析師日所訂的財務目標。（原話："driving performance ahead of the financial targets"）
- 2026-04-28｜CEO｜guidance：CEO 總結中把公司定位為進入「結構性成長期」，這是本次新增的敘事框架。（原話："Seagate is entering a period of structural growth"）
- 2026-04-28｜CFO｜guidance：CFO 稱每噸（每 TB）資料中心營收的年增中個位數趨勢，預期會延續。（原話："We expect this trend to continue"）
- 2026-04-28｜CFO｜commitment：CFO 在準備稿結尾表示有信心在 FY2027 持續季增營收並擴張利潤率。（原話："growth and margin expansion through fiscal 2027"）
- 2026-04-28｜CFO｜commitment：CFO 在問答中把同一承諾說成「有很好的機會」讓利潤與營收在 FY27 逐季增加，措辭比準備稿的 confident in delivering 略軟。（原話："increase our profit and our revenue sequentially"）
- 2026-04-28｜CEO｜commitment：CEO 重申資料中心 exabyte 供給成長目標為 20% 中段。（原話："supply data center exabyte growth in the mid-20%"）
- 2026-04-28｜CEO｜commitment：CEO 說 Mozaic 5（50TB）研發按計畫進行，客戶驗證出貨目標是 2027 日曆年末。（原話："qualification shipments targeted for late calendar 2027"）
- 2026-04-28｜CFO｜commitment：CFO 在回答 Krish 時再確認 50TB 第三代 HAMR 在下一個日曆年年底進入驗證。（原話："the end of next calendar year, we will be already in qual"）
- 2026-04-28｜CFO｜commitment：CFO 澄清先前的百分比口徑：目標是 nearline exabyte 中 70% 建在 HAMR 硬碟上。（原話："we will achieve 70% of exabyte, nearline"）
- 2026-04-28｜CFO｜commitment：CFO 講 70% 目標的時點時當場自我更正，從 calendar '27 改口為 fiscal '27。（原話："by the end of calendar '27, actually by fiscal '27, sorry"）
- 2026-04-28｜CEO｜commitment：CEO 準備稿說正在與雲端客戶敲定涵蓋到 FY2027 年底的 build-to-order 合約。（原話："finalizing build-to-order contracts with these customers"）
- 2026-04-28｜CFO｜commitment：CFO 在問答中用完成式，說 FY27 的 build-to-order 已經敲定（準備稿是進行式 finalizing）。（原話："now finalized our build-to-order for our fiscal '27"）
- 2026-04-28｜CFO｜margin：CFO 報 3 月季 non-GAAP 毛利率 47%，較上一季增加 480 個基點。（原話："47%, up 480 basis points sequentially"）
- 2026-04-28｜CFO｜margin：CFO 報 non-GAAP 營業利益率較上一季擴張 560 個基點，至 37.5%。（原話："operating margin by 560 basis"）
- 2026-04-28｜CFO｜margin：CFO 說毛利率改善來自長期定價策略加產品組合，兩者帶動資料中心每 TB 營收年增中個位數。（原話："Together, this drove a mid-single-digit increase"）
- 2026-04-28｜CFO｜margin：CFO 報 non-GAAP 營業費用 2.96 億美元，占營收 9.5%。（原話："at $296 million or 9.5% of revenue"）
- 2026-04-28｜CFO｜margin：CFO 說營收成長加費用紀律，讓長期營業利益率目標比原訂時程提早達成。（原話："earlier than originally planned"）
- 2026-04-28｜CFO｜margin：CFO 拆解過去幾季成本下降兩大來源是高容量組合與產線滿載，並說未來產能已滿，滿載這一項不再是成本下降來源。（原話："now we are full, so that part maybe will not"）
- 2026-04-28｜CFO｜margin：CFO 說未來成本下降的主要驅動力是每台硬碟 TB 數提高，同時不增加物料清單。（原話："not adding more bill of materials to the hard disk"）
- 2026-04-28｜CFO｜margin：CFO 澄清 FY27 營業費用「持平」是指金額持平，不是占營收比率持平。（原話："flat on a dollar basis, not as a percentage of revenue"）
- 2026-04-28｜CFO｜margin：CFO 說相較一年前的規劃，定價表現更好，是毛利率優於預期的原因之一。（原話："I say pricing was actually better"）
- 2026-04-28｜CFO｜margin：CFO 被問到增量毛利率能否維持 70% 以上時，只說看不出未來不能重複過去幾季的表現，隨即補上每季不同。（原話："I don't see a reason why we should not do the same"）
- 2026-04-28｜CFO｜margin：CFO 說定價策略沒有改變，已連續 12 季利潤成長，且 FY27 趨勢相同。（原話："there are no changes to our pricing strategy"）
- 2026-04-28｜CFO｜margin：CFO 被問到 FY27 底每 exabyte 價格年增幅度時，表示不對這麼遠的時點給指引。（原話："we probably don't guide so far out in time"）
- 2026-04-28｜CFO｜margin：CFO 說利潤改善的大部分來自定價，其餘來自產品組合與 40TB HAMR 硬碟帶來的成本下降。（原話："profitability improvement is coming from pricing"）
- 2026-04-28｜CEO｜margin：CEO 回答定價問題時說，公司透過多出貨幾顆硬碟來測試需求，看到的是市場價格。（原話："we're seeing what the market price, if you will, is"）
- 2026-04-28｜CEO｜margin：CEO 談 FY27 定價時說，最終價格由客戶（需求）決定，公司持續與客戶談預見性。（原話："they'll determine what the price is"）
- 2026-04-28｜CFO｜margin：CFO 報資料中心營收成長快於 exabyte 出貨量（營收季增 12%、年增 55%；exabyte 季增 6%、年增 47%）。（原話："Data center revenue increased even faster"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說 FY2026 資本支出預期落在占營收 4% 至 6% 的目標區間內，用於 HAMR 產品轉換與放量。（原話："2026 to be inside our target range of 4% to 6% of revenue"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報自由現金流 9.53 億美元，較上一季增 57%。（原話："$953 million, up 57% from the prior quarter"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報本季以股利與買回向股東回饋約 1.91 億美元。（原話："approximately $191 million to shareholders"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報本季以現金清償 6.41 億美元債務，其中含 6 億以上 2028 年到期可交換債。（原話："$641 million in debt, including over $600 million"）
- 2026-04-28｜CFO｜capital_allocation：CFO 報淨槓桿比率降至 0.7 倍，並預期隨獲利與現金增加持續下降。（原話："Net leverage ratio improved to 0.7x"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說 Fitch 最近把 Seagate 信用評等調升到投資等級。（原話："upgraded Seagate's credit to investment grade"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說仍有約 4 億美元可轉換債未處理，預計本季或下季處理。（原話："We still have about $400 million of the convertible"）
- 2026-04-28｜CFO｜capital_allocation：CFO 說少量還債之後，現金大部分會用於股票買回，且目前已在市場上買。（原話："majority will probably go to share buybacks"）
- 2026-04-28｜CEO｜capital_allocation：CEO 說下一步資金去向是回到先前的做法，也就是回饋股東。（原話："which is returning value to shareholders"）
- 2026-04-28｜CEO｜capital_allocation：CEO 回顧去年的資金重心在營運資金與供應鏈修復，之後才轉向還債與股東回饋。（原話："last year we were focused very much on working capital"）
- 2026-04-28｜CFO｜capital_allocation：CFO 被問到客戶預付款時說目前沒有把重心放在預付款，但也沒有排除未來實施。（原話："so far, we have not focused on that part"）
- 2026-04-28｜CEO｜capital_allocation：CEO 說若把人力從提升面密度轉去多做零件，未來幾年淨出貨的 exabyte 反而會更少，所以不以增加產能單位為路線。（原話："we would probably net-net fewer exabytes"）
- 2026-04-28｜CEO｜customer：CEO 說已有 2 家全球最大 CSP 通過 4TB 以上每碟片產品驗證。（原話："2 of the world's largest CSPs now qualified on our 4+"）
- 2026-04-28｜CFO｜customer：CFO 報 3 月季已對 75% 的主要全球雲端客戶出貨 Mozaic 硬碟並認列營收。（原話："75% of the leading global cloud customers"）
- 2026-04-28｜CFO｜customer：CFO 說剩下 2 家雲端客戶的驗證預計在本季（FQ4）完成。（原話："remaining 2 customers in the current quarter"）
- 2026-04-28｜CEO｜customer：CEO 說來自雲端客戶的營收已連續第 10 季成長。（原話："our 10th consecutive period of revenue growth"）
- 2026-04-28｜CEO｜customer：CEO 以剩餘履約義務（RPO）作為未來營收潛力代理指標，稱前三大 CSP 的 RPO 已近乎翻倍至 1.1 兆美元。（原話："nearly doubled their RPO to a staggering $1.1 trillion"）
- 2026-04-28｜CEO｜customer：CEO 說與幾乎所有大型雲端客戶簽有 exabyte 級供給協議，nearline 產能到 2027 日曆年幾乎全數分配完畢。（原話："capacity almost fully allocated through calendar 2027"）
- 2026-04-28｜CEO｜customer：CEO 說與客戶的策略規劃討論已延伸到 2028 日曆年及以後。（原話："planning discussions now reaching into calendar 2028"）
- 2026-04-28｜CEO｜customer：CEO 說開始看到主權（sovereign）與 neocloud 資料中心對企業級 nearline 硬碟與系統方案有興趣。（原話："interest from sovereign and neocloud data centers"）
- 2026-04-28｜CFO｜customer：CFO 說企業 OEM 資料中心市場營收季增明顯，原因是 AI 應用部署與混合／分層儲存架構需求回升。（原話："we saw a notable sequential revenue increase"）
- 2026-04-28｜CFO｜customer：CFO 說用戶端與消費市場，供給偏緊與 NAND 成本上升，抵銷了 3 月季的典型季節性需求走弱。（原話："tight supply and higher NAND cost offset the typical"）
- 2026-04-28｜CFO｜customer：CFO 被問到 FY27 產能有多少已鎖價時，只答 nearline 產能「絕大部分」已分配，沒有給比例。（原話："the vast majority of our nearline capacity is allocated"）
- 2026-04-28｜CEO｜product：CEO 說 Mozaic 4 單碟最高可達 44TB，較第一代 Mozaic 多 30% 以上容量。（原話："can deliver up to 44 terabytes per drive"）
- 2026-04-28｜CEO｜product：CEO 說 Mozaic 4 於 3 月下旬開始有營收出貨。（原話："revenue shipments for Mozaic 4 in late March"）
- 2026-04-28｜CEO｜product：CEO 預期到 2026 日曆年底，Mozaic 4 會占 HAMR exabyte 出貨的多數。（原話："HAMR exabyte shipments exiting calendar 2026"）
- 2026-04-28｜CEO｜product：CEO 說技術策略以面密度創新優先於增加出貨單位數。（原話："areal density innovation over increasing unit volumes"）
- 2026-04-28｜CEO｜product：CEO 說目前絕大多數 HAMR 供給都分配給雲端與超大規模客戶，並預期放量後才會把 4／5TB 每碟片技術用到較低容量產品。（原話："the vast majority of HAMR supply is allocated to cloud"）
- 2026-04-28｜CEO｜product：CEO 說公司刻意控制 Mozaic 4 的投入比重，因為其他產品家族仍對部分客戶重要且表現不差。（原話："We're not leaning too hard into the Mozaic 4"）
- 2026-04-28｜CEO｜product：CEO 回答用 HAMR 做 20TB 低容量款時說，Mozaic 4 高階需求太高，預期不會看到很多這類產品。（原話："I don't think you'll see very many of those"）
- 2026-04-28｜CFO｜product：CFO 說公共雲需求太強，沒有足夠產量再往低容量 4TB 每碟片策略延伸，可能較晚才處理。（原話："possibly, we will address it a bit later out in time"）
- 2026-04-28｜CEO｜product：CEO 談效能分層需求時說，過去出貨過數千萬 exabyte 級的堆疊式 actuator 設計，可以重新拿出來用。（原話："certainly pull those designs back down off the shelf"）
- 2026-04-28｜CEO｜product：CEO 回答 agentic AI 提問時說，部分 AI 應用屬於資料量很小的應用。（原話："are fairly small data applications"）
- 2026-04-28｜CEO｜product：CEO 說 agentic AI 帶來的儲存需求並非全部與大容量儲存相關，但已開始看到明顯增加。（原話："not entirely related to mass capacity storage"）
- 2026-04-28｜CEO｜product：CEO 回答 Tim Arcuri 時說，出貨顆數沒有成長，只有每顆平均磁頭數可能增加。（原話："The total number of units is not really increasing"）
- 2026-04-28｜CEO｜competition：CEO 談硬碟與 NAND 的成本差時說，因目前的經濟性，客戶正在回頭找硬碟。（原話："people are coming back to hard drives"）
- 2026-04-28｜CEO｜competition：CEO 認為資料中心儲存架構在未來很長一段時間內都很難改變。（原話："these architectures pretty sticky for a long, long time"）
- 2026-04-28｜CFO｜risk：CFO 說 HAMR 週期時間比 PMR 長，因此仍用一些 PMR 磁頭維持出貨顆數，否則顆數會下降。（原話："Otherwise, the units will actually go down"）
- 2026-04-28｜CFO｜risk：CFO 談中東衝突等地緣政治緊張時，表示目前預期不會對業務造成重大影響。（原話："do not currently expect material impacts"）

### STX_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜CFO｜guidance：CFO 說依現有 PO，整個 FY27 營收與獲利都會改善（原話："we see improvement also for the entire fiscal '27"）
- 2026-09-09｜CFO｜guidance：CFO 重述本財年每一季營收與獲利都會比前一季改善（原話："see an improvement in both revenue and profitability"）
- 2026-09-09｜CFO｜guidance：CFO 說 exabyte 目標是未來 2–3 年年複合成長至少 25%（原話："targeting that at least 25% CAGR in the next 2 or 3 years"）
- 2026-09-09｜CFO｜guidance：CFO 提到 9 月季財測給的是營收與獲利都大幅增加（原話："very significant increase in revenue and in profitability"）
- 2026-09-09｜CFO｜guidance：CFO 說本財年 OpEx 財測為每季約 3 億美元，大致持平（原話："OpEx fairly stable at around $300 million per quarter"）
- 2026-09-09｜CFO｜guidance：談完 OpEx 後，CFO 說未來 3–4 季看不到需要改變的理由（原話："next 3, 4 quarters, we don't see any reason for change"）
- 2026-09-09｜CFO｜guidance：CFO 說人力（headcount）會維持相當穩定（原話："we will be fairly stable in terms of headcount"）
- 2026-09-09｜CFO｜guidance：CFO 說供需缺口沒有縮小，反而略為擴大（原話："gap between supply/demand is not decreasing"）
- 2026-09-09｜CFO｜guidance：CFO 說需求成長速度比公司原先預期還快（原話："demand growing even faster than what we were thinking"）
- 2026-09-09｜CFO｜commitment：CFO 說手上有未來 4–5 季的採購訂單（PO）（原話："purchase orders in place for the next 4 or 5 quarters"）
- 2026-09-09｜CFO｜commitment：CFO 說已有涵蓋未來 2–3 年的長約（LTA）（原話："We have LTAs in place for the next 2, 3 years"）
- 2026-09-09｜CFO｜commitment：CFO 說長約配置不會超過確定能生產的量，彈性不大（原話："we don't allocate more than what we are sure we can produce"）
- 2026-09-09｜CFO｜commitment：CFO 回答分析師：長約條款沒有加入很多彈性（原話："No, not a lot of flexibility."）
- 2026-09-09｜CFO｜commitment：CFO 說 50TB 新一代硬碟約一年後開始認證（qual）（原話："we will start to qualify about in a year from now"）
- 2026-09-09｜CFO｜commitment：CFO 說第三代 HAMR 幾季後開始認證（原話："third-generation HAMR qual in just a few quarters from now"）
- 2026-09-09｜CFO｜commitment：CFO 說靠技術（單顆容量）成長，而非靠增加出貨顆數（原話："growing the content of the drive, not the units"）
- 2026-09-09｜CFO｜commitment：CFO 說 HAMR 讓公司不必增加顆數就能成長（原話："we can grow without the need to increase the units"）
- 2026-09-09｜CFO｜commitment：CFO 說擴產與零組件增加都放在 CapEx 佔營收 4%–6% 的區間內（原話："Everything in our CapEx range, so between 4% and 6%"）
- 2026-09-09｜CFO｜commitment：CFO 說 3–4 年後需要的容量會遠高於 50TB，公司只承諾做得到的量（原話："a capacity that is way higher than 50 terabytes"）
- 2026-09-09｜CFO｜margin：CFO 說漲價是每個客戶區段都有，不只企業 OEM（原話："it's in every segment"）
- 2026-09-09｜CFO｜margin：CFO 說調價方式不會過度激進，目的是讓逐季改善能持續很久（原話："we do this in a way that is not super aggressive"）
- 2026-09-09｜CFO｜margin：CFO 說前一季價格與成本表現都好，價格貢獻可能更大（原話："maybe even more on pricing than cost"）
- 2026-09-09｜CFO｜margin：CFO 說本季有一批高量新合約，帶來價格支撐（原話："we have a good level of new contracts with high volume"）
- 2026-09-09｜CFO｜margin：CFO 談價格空間：認為未來可得到與過去類似的結果（原話："no reason why we should not get a similar result"）
- 2026-09-09｜CFO｜margin：CFO 說 Seagate 佔客戶 CapEx 比重不大，漲價不會明顯影響客戶支出（原話："we are not a big part of our customer CapEx"）
- 2026-09-09｜CFO｜margin：CFO 總結各季雖有變數，但結果是營收與獲利都上升（原話："Revenue will go up and profitability will go up."）
- 2026-09-09｜CFO｜margin：CFO 說自製的磁頭與碟片，單位成本不隨容量變動（原話："the unit cost actually is not changing"）
- 2026-09-09｜CFO｜margin：CFO 說自製部分每 TB 成本降幅很好，但沒給數字（原話："a very good cost per terabyte decline on what we produce"）
- 2026-09-09｜CFO｜margin：CFO 說外購零組件的成本變化每年不同、公司較難控制（原話："it's less under our control"）
- 2026-09-09｜CFO｜margin：CFO 說換代轉換成本是正常現象，一直都有（原話："I would say it's normal for the business"）
- 2026-09-09｜CFO｜product：CFO 說 30TB 升到 40TB 容量增加 33%（原話："you increase 33% your capacity"）
- 2026-09-09｜CFO｜product：CFO 說 40TB 升到 50TB 再增加 25%（原話："Then going from 40 to 50 is another 25%."）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 只用在高容量端，2TB 到 28TB 基本上是 PMR（原話："Between 2 terabytes and 28 is basically PMR."）
- 2026-09-09｜CFO｜product：CFO 說 PMR 產品要加容量就得多加碟片與磁頭（原話："you need to have 1 more disk and 2 more heads"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 加碟片（10 片到 11 片）只增加約 10%，目前不划算（原話："If you go from 10 disks to 11 disks, you only gain 10%."）
- 2026-09-09｜CFO｜product：CFO 說第二代 HAMR 客戶認證進行得很快（原話："Second generation is going very, very fast."）
- 2026-09-09｜CFO｜product：CFO 說客戶現在把第二代 HAMR 當成已熟悉技術上的新產品（原話："it's just a new product on something that they already know"）
- 2026-09-09｜CFO｜product：CFO 說第一代 HAMR 認證較困難，客戶測試時間也較長（原話："the first-generation HAMR was a little bit more difficult"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 換代時 exabyte 出貨會有較大的季度波動，年複合仍約 25%（原話："a little bit more variability on exabyte volume"）
- 2026-09-09｜CFO｜product：CFO 說 HAMR 磁頭製程週期較長，需要多一點空間（原話："we need a little bit more space"）
- 2026-09-09｜CFO｜product：CFO 說顆數不變、exabyte 約增加 25%（原話："the same number of units, but about 25% more exabytes"）
- 2026-09-09｜CFO｜product：CFO 談 KV cache：只有部分層級與 NAND 有少量重疊，硬碟可以參與（原話："a little bit of overlap between NAND and our disk"）
- 2026-09-09｜CFO｜product：CFO 說參與 KV cache 不需要與快閃記憶體廠合作（原話："I don't think we need to partner with flash"）
- 2026-09-09｜CFO｜competition：CFO 說資料中心裡硬碟沒有替代品（原話："no replacement in data center for our disk storage"）
- 2026-09-09｜CFO｜competition：CFO 說公司想維持供需平衡，認為目前情況有助逐季改善（原話："we want to keep a good balance between supply and demand"）
- 2026-09-09｜CFO｜risk：被問到這次循環有何不同，CFO 承認現在不是循環的起點，已超過 3 年（原話："not for sure the beginning of the cycle"）
- 2026-09-09｜CFO｜risk：被問到未來 2–3 年是否需要消化已部署容量，CFO 說目前沒看到趨勢改變（原話："we don't see today any change in the trend"）
- 2026-09-09｜CFO｜risk：CFO 說有長約且客戶要求更多量，所以不認為是短期循環（原話："we feel comfortable that it's not a short-term cycle"）
- 2026-09-09｜CFO｜risk：CFO 說每一季受量、新合約、去年基期等多個變數影響，各季不同（原話："every quarter is different, there are a lot of variables"）
- 2026-09-09｜CFO｜risk：CFO 說外購零組件有的年度上升、有的下降，是好壞參半（原話："a mixed bag, some components are increasing"）
- 2026-09-09｜CFO｜customer：CFO 說公有雲買最高容量的硬碟（原話："Public clouds buy the highest-capacity drive."）
- 2026-09-09｜CFO｜customer：CFO 說企業 OEM（地端資料中心）需求又開始成長（原話："more on-prem data center demand, to start to grow again"）
- 2026-09-09｜CFO｜customer：CFO 說地端資料中心約 2 年後才會用到 40TB 硬碟（原話："on-prem data center will consume a 40-terabyte drive"）
- 2026-09-09｜CFO｜customer：CFO 說 40TB 產品還有其他客戶即將完成認證（原話："other customers that will be qualified fairly soon"）
- 2026-09-09｜CFO｜customer：CFO 說每次重談長約，客戶都要求更多量而不是更少（原話："our customers are asking for more volume, not less volume"）
- 2026-09-09｜CFO｜customer：CFO 說主權 AI 資料中心目前仍由同一批大型公有雲業者建置（原話："they're still built by the same big public cloud companies"）
- 2026-09-09｜CFO｜customer：CFO 說 neocloud 與 Seagate 客戶相同：Seagate 賣儲存、neocloud 賣算力（原話："We sell storage, they sell compute"）
- 2026-09-09｜CFO｜customer：CFO 說未來部分目前賣給公有雲的量會轉到 neocloud（原話："Tomorrow, some of that volume will go to the neoclouds."）
- 2026-09-09｜CFO｜customer：CFO 說量體變化不大，但對客戶分散度是好事（原話："it's good from a customer diversification"）
- 2026-09-09｜CFO｜customer：CFO 說最被低估的成長來源是所有和影像相關的應用（機器人、自駕等）（原話："everything that is based on video"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說債務處理接近完成（原話："in terms of debt, we are almost done"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說還剩一筆高利率票據，可能下一季處理（原話："one note with high interest rate that we want to address"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說債務處理完後，回到更多股票回購並維持股息（原話："so higher share buyback and still focusing on a good return"）
- 2026-09-09｜CFO｜capital_allocation：CFO 說前一季自由現金流為 11 億美元，高於 10 億（原話："was already above the $1 billion, was $1.1 billion"）
- 2026-09-09｜CFO｜capital_allocation：被問自由現金流率目標，CFO 說沒有公布目標（原話："We didn't share a target."）
- 2026-09-09｜CFO｜capital_allocation：CFO 說本季與下季持續回購，之後可能做得更多（原話："after that, we will probably do even more"）

### STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說依手上訂單，本財年每一季營收和毛利率都比前一季高（原句同時提 higher margin）。（原話："every quarter of this fiscal year having higher revenue"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說未來 4 到 5 季已有客戶訂單在手，依這些訂單營收上升、獲利改善。（原話："purchase orders in place for the next 4 or 5 quarters"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說近幾季增量毛利率遠高於先前的 50% 框架，落在 70% 以上。（原話："I would say, in the 70-plus percent"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說未來幾季用 70% 以上的增量毛利率看這門生意是合適的（回答分析師對新增量框架的提問）。（原話："So for the next few quarters, I think that is a good way"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說過去 3 年的定價策略加上技術帶來的 exabyte 成長，讓毛利率幾乎變成三倍。（原話："allow us to almost triple our gross margin"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說希捷的產品佔客戶資本支出的比重是低到中個位數。（原話："Now we are low to middle single digit of their CapEx."）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說需求比去年投資人日時看到的強很多。（原話："Demand is much, much stronger than what we were seeing"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說需求強讓公司能把價格調得比投資人日討論的還高一些，帶動毛利率、營業利益率與 EPS 更好。（原話："raise pricing a little bit more than what we were"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說自己認為未來數季業績會持續改善（未給數字）。（原話："results continue to improve in the next several quarters"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：CFO 說自投資人日以來情況持續轉好。（原話："the situation from our Investor Day has continued to improve"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說 40TB HAMR 硬碟已在賣給兩家最大的超大規模雲端客戶，另有幾家還在驗證。（原話："we're already selling to the 2 biggest hyperscalers"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說下一代 50TB 產品的量會落在 2027 曆年（原句：through the end of calendar year '27）。（原話："50 terabyte will be more calendar '27"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：分析師問 HAMR 出貨量交叉（超越 PMR）是否有變，CFO 答計畫穩固，12 月前 40TB 與整體 HAMR 都會到那個水準。（原話："I think by December, so just a few months from now"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說約兩年後，希捷資料中心產品有八到九成的量會走 HAMR。（原話："80%, 90% of the volume will be sold through HAMR"）
- 2026-09-10｜Gianluca Romano (CFO)｜competition：CFO 說傳統 PMR 技術追不上 HAMR（沒點名競爭對手，談的是技術路線）。（原話："no way that the PMR technology can keep up with HAMR"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 舉例：從 30TB 換到 40TB 硬碟，單顆內容量多 33%。（原話："a 40-terabyte drive, we can have 33% more content"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說 40TB 硬碟正在美國與亞洲的多家客戶驗證中。（原話："a good number of customers, both in U.S. and in Asia"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說 30TB HAMR 硬碟大約一年內就驗證完前 8 到 10 大客戶。（原話："we qualified the top 8, 10 customers in basically a year"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說所有大客戶都已經在買 HAMR。（原話："all the big customers are already buying HAMR, everyone"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說客戶每季買進的 HAMR 硬碟是數十萬顆等級。（原話："all buying hundreds of thousands of units every quarter"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 定調：HAMR 現在對希捷是產品開發，不再是技術開發（與客戶討論的重點已是單顆容量）。（原話："It's not anymore a real technology development"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說自製雷射搭配磁頭的成本，比外購雷射再組裝低很多。（原話："produce the laser together with the head is much lower"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說第二代 HAMR 起開始混用：部分產品用自家雷射，部分仍用外購雷射（第一代全用外購）。（原話："Some are still using external laser"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說未來自家雷射的占比會愈來愈高。（原話："more the mix will go into the internal laser"）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：分析師問需求過熱後客戶砍單的下行情境，CFO 答目前看不到這種情況。（原話："Today, we don't see that situation happening."）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：CFO 列舉客戶即使需求很高也可能放慢建資料中心的原因：電力限制、建照延誤、零組件缺料。（原話："a power constraint, can be a delay in building permit"）
- 2026-09-10｜Gianluca Romano (CFO)｜risk：CFO 說客戶若放慢建設，需求只是往後延，沒有消失。（原話："pushing that demand out in time is not going away"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說產業對資本支出與產能增加要保持紀律，希捷 2、3 年來一直如此。（原話："disciplined with CapEx and with capacity addition"）
- 2026-09-10｜Gianluca Romano (CFO)｜product：CFO 說成長來自技術升級（每顆內容更多），不是出貨顆數增加。（原話："growing because of technology, not because of more units"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 的數字口徑：這個產業賣的是 exabyte，不是顆數。（原話："this industry is selling exabytes, not units"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 的數字口徑：看 exabyte 成長時，他更看重絕對數字而不是百分比。（原話："I always look more at the absolute numbers and percentages"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 舉例：今年比 3 年前成長 25% 或 30%，換算成 exabyte 數量可能是 50% 以上，所以看營收要看賣出的 exabyte 與單價。（原話："that is maybe 50-plus percent if you look at the number"）
- 2026-09-10｜Gianluca Romano (CFO)｜guidance：分析師問長期 exabyte 成長目標是否仍是 20%，CFO 提到先前給過約 3、4 年的 mid-20% CAGR，並說每季每年都不同。（原話："We gave this mid-20% CAGR for a fairly long period of time"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：CFO 說公司有能力靠技術維持很好的 exabyte 年複合成長（未給數字）。（原話："grow through technology at a very good exabyte CAGR"）
- 2026-09-10｜Gianluca Romano (CFO)｜commitment：CFO 說目前沒有理由改變現行的技術加定價策略。（原話："we don't see any reason today to change it"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 說漲價是策略的一部分，對毛利率與營業利益率貢獻很大。（原話："huge contribution to our gross margin and operating margin"）
- 2026-09-10｜Gianluca Romano (CFO)｜margin：CFO 給定價策略有效的第一個原因：供需平衡和 4、5 年前不同。（原話："the supply-demand balance is different"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說客戶把資料存起來的成本，比日後重新運算那份資料低很多。（原話："the cost of storage is minimal comparing to recompute"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說資料中心占營收 80%（大容量硬碟），其餘 20% 是低容量的 edge（消費、用戶端、部分影像監控）。（原話："This is today 80% of our revenue."）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說 edge 低容量市場因為沒有長期訂單與大客戶，近幾季已調整定價策略。（原話："we have changed a little bit our pricing strategy there"）
- 2026-09-10｜Gianluca Romano (CFO)｜competition：CFO 說目前 NAND 價格偏高，讓低容量硬碟有機會漲價並維持出貨量（低容量段硬碟與 SSD 有重疊）。（原話："Today, the NAND price is fairly high"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說各個區隔的需求都大於供給，所以要配貨，優先給資料中心大客戶。（原話："demand is above supply in every segment today"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說從客戶資本支出看，AI 投資仍在前段階段。（原話："still being in the first part of the phase of AI investment"）
- 2026-09-10｜Gianluca Romano (CFO)｜customer：CFO 說近來除大型公有雲外，企業自建機房（on-prem）需求也有不錯成長，企業 OEM 通路也成長。（原話："a fairly good growth on enterprise OEM"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說本季後還剩一筆高利率票據想買回，可能下一季處理。（原話："still have one note that I would like to repurchase"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說 2027 曆年起庫藏股規模會更高（債務還清後自由現金流更多）。（原話："calendar year '27, I would say you will see a higher level"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說股利每年約 10、11 月與 CEO 內部檢討，這種強勁時期通常會加股利。（原話："we will probably increase the dividend"）
- 2026-09-10｜Gianluca Romano (CFO)｜capital_allocation：CFO 說股東回報中股利只是一部分，庫藏股占大得多。（原話："A much bigger part will be share buyback."）

### 問答異常語氣（迴避／改口／保留）
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Erik Woodring（Morgan Stanley）：agentic AI 具體如何帶動硬碟需求，並且是否改變對 nearline exabyte 20% 中段年複合成長率的看法？｜答法：CEO 只描述 agentic 工作流參照大型資料集並產生新資料，並加註部分應用資料量小、「not entirely related to mass capacity storage」，沒有回答 CAGR 是否調整。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Wamsi Mohan（BofA）：FY27 產能有多少比例已鎖價、多少仍浮動？｜答法：CFO 答的是產能「已分配」（vast majority、not 100%、very high percentage），沒有給鎖價比例，也沒有區分已分配與已鎖價。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Samik Chatterjee（JPMorgan）：新合約進入損益後，為何定價不會加速上升？｜答法：CEO 轉向談需求上升與提供客戶可預測性，CFO 重申定價策略不變、FY27 有機會逐季增加，兩人都沒有正面回答加速與否。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Mark Newman（Bernstein）：每 exabyte 價格季增中個位數，是新合約占比較高，還是新合約漲幅擴大？此幅度是否每季延續？｜答法：CFO 答「策略不變、每季不同、取決於新合約數與產品組合」，說未來 4 季趨勢相同且可能更久，沒有區分兩種原因，也沒有給幅度。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Jim Schneider（Goldman）：FY27 底的長期訂單，每 exabyte 價格年增是低、中還是高個位數？｜答法：CFO 明確表示不對這麼遠的時點給指引，只說每季會略好，利潤改善主要來自定價、組合與 40TB HAMR 成本下降；CEO 補充最終由需求決定價格。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Amit Daryanani（Evercore）：分析師日的 50% 增量毛利率已被 70% 以上超越，FY27 模型是否用 70% 增量毛利率當框架？｜答法：CEO 先請 CFO 談量化，CFO 沒給數字，只說過去執行優於預期、看不出未來不能重複，並加上「每季不同，let's see」。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Karl Ackerman（BNP Paribas）：HAMR 多快會超過總 exabyte 出貨的一半？｜答法：CFO 沒回答何時過半，改為重述並更正先前說過的百分比（70% nearline exabyte 建在 HAMR 上，講到一半把 calendar '27 改為 fiscal '27），CEO 補說產線相對滿載、不會過度押 Mozaic 4。
- STX_Q3_2026_Earnings_Call_20260428.md｜問：Ananda Baruah（Loop Capital）：Mozaic 4 是否為切入 20TB 低容量 HAMR 的機型，何時可能做？｜答法：與準備稿說預期把 4／5TB 每碟片用於較低容量產品相比，問答中 CEO 說不預期看到很多、CFO 說產量不夠並可能較晚才處理，時程未定。
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：第二代 HAMR 良率提升後，每 TB 成本下降幅度該怎麼看？｜答法：回答 'It's very good'，拆成自製（磁頭、碟片）與外購兩類，沒有給任何降幅數字；外購部分只說每年不同、較難控制
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：40TB 換到 50TB 時的製造無效率（送認證品不能認列營收等）該怎麼看？｜答法：回答換代成本是正常現象、一直都有，沒有量化；轉向說 exabyte 季度波動會變大
- STX_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：HDD 相對 NAND 還有多少價格彈性？｜答法：沒有給價格幅度或上限，回答改談供需缺口略增、調價不會過度激進，並說未來可得到與過去類似的結果
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：上一季 price per exabyte 年增 11%，這個數字能否當作本財年建模的參考、未來幾季定價成長節奏如何？｜答法：CFO 沒給任何數字或節奏，改談定價策略 3 年前改變、供需平衡不同、資料價值較高等原因。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：公司剛上調長期營收展望，這個目標能維持多久、可持續性如何？｜答法：CFO 沒給期間或數字，只說看不出趨勢會改變、未來數季業績會繼續改善。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：長期 exabyte 成長目標 20% 是否仍正確，還是可持續超越？｜答法：CFO 沒有確認或修改 20%，改說先前給的是約 3、4 年的 mid-20% CAGR，並強調每季每年不同、應看絕對數字。
- STX_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260910.md｜問：有沒有辦法用絕對 exabyte 數字來表達產業成長？｜答法：CFO 先答 No，只給一個百分比對絕對量的舉例，沒有提供絕對 exabyte 數字。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 4 |
| customer_concentration_credit | found | 2 | 4 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 8 | 4 |
| geo_supply_chain | found | 9 | 4 |
| end_markets | found | 6 | 6 |
| substitute_technology | found | 6 | 4 |
| channel_business_model_shift | found | 6 | 4 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 5 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 8 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 近線儲存需求為結構性而非週期性，且合約化程度足以把可預測期拉到 2028-2029"},{"id":"H2","text":"HAMR／Mosaic 的面密度領先，讓 STX 在機櫃數持平下持續擴 exabyte 並取得定價權"},{"id":"H3","text":"市場願意給這門「合約化的循環商品生意」高於歷史中樞的倍數（16-18x 前瞻以上）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國稀土出口管制打到硬碟音圈馬達的 NdFeB 永磁——含鏑／鋱重稀土的釹鐵硼永磁驅動硬碟讀寫臂，自 2025 年起納入中國非自動出口許可制，核准延遲普遍 60-120 天以上，ex-China 重稀土瓶頸預期延續至 2027；域外「0.1% 規則」暫緩期於 2026-11-10 屆滿，第三國產品只要含 0.1% 中國源稀土即受管。這是雙面刃：既支撐定價，也威脅交期與毛利。"},{"id":"R2","text":"供給端追上：WD HAMR 2027 量產 ＋ Toshiba 40TB 級 ＋ 新產能投產，使定價權見頂——WD HAMR 已在兩家超大規模客戶認證中、2027 年量產爬坡（36TB CMR／40TB SMR／44TB UltraSMR），12 碟平台 2028 年到 60TB；Toshiba 市佔穩定 17%，2026 年 4 月起出貨 M12（30-34TB）、2027 年瞄準 40TB 級。同時 hyperscaler 需求端若進入 AI capex 消化期，缺口收斂會更快。"},{"id":"R3","text":"QLC 固態硬碟總持有成本交叉 × STX 自身漲價的負回饋迴路——QLC 在熱／溫資料層已於總持有成本勝出，業界預期 QLC 位元產出 2027 年超越 TLC；Meta 目標 2026 年底至 2027 年初部署 10-12EB QLC flash（效果為「限制硬碟成長率、尚未逆轉需求」）。關鍵在於：業界目標定價 $25-30/TB（現行 $14.30-14.90/TB）會直接壓縮硬碟對 flash 的每 TB 價差，定價權主張越強，越可能加速溫資料層遷移。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","irr_base_pct":-3.5,"ev5y_pct":-6.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.1,"ev5y_pct":-6.3,"irr_base_pct":-3.5,"max_dd_pct":-75.0,"bull_5y_price":1200.0,"bear_5y_price":144.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","price_at_dd":747.3,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"STX","date":"2026-09-23","schema":"v15.2","contract":"v19","company_name":"Seagate Technology Holdings plc"},"oneliner":"硬碟缺貨讓毛利率連 13 季擴張、Q1 財測再拉高，但現價已付清共識到 FY2029 的單價漲勢，循環走到後段；等股價回到 $572–644，或 CY2028 長約確認單價續漲，再重跑研究","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STX_20260923/scenario.json","answers":{"q1_business":{"verdict":"賺雲端大客戶買大容量硬碟的錢，錢卡在每 EB 單價：出貨顆數不增，營收靠單碟容量和漲價","reasoning":"Q4 FY2026 營收 36.29 億美元，年增 48.5%。資料中心 29 億美元，占 81%；Edge IoT 6.97 億美元，占 19%。出貨 218 EB，其中資料中心 195 EB。non-GAAP 毛利率 52.7%、營業利益率 44.6%，兩者都是紀錄。每 EB 營收約 1,660 萬美元，季增 6.5%；每 EB 單價年增 10%，9 月季財測隱含約 20% 以上。公司策略是顆數持平、靠 HAMR 提高單碟容量，所以量的成長上限約每年 25%，超出的部分全看單價。產業時鐘在過熱段：大部分 nearline 產能已配置到 CY2028，毛利率連 13 季擴張，而新產能（STX 與 TDK 擴磁頭、WD HAMR）要到 2027–2028 才到。單點依賴有兩處：最大客戶約占營收 14%，資料中心以雲端大廠為主；上游主軸馬達約八成出自 Nidec，磁鐵用稀土的精煉約九成在中國。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_gross_margin","f_kpi2_non_gaap_operating_incom","f_kpi11_exabytes_shipped","f_kpi12_revenue_per_exabyte_asp","f_kpi13_price_per_exabyte_yoy","f_kpi15_nearline_exabyte_lta_bac","f_kpi7_guidance_q1_fy2027_reven","f_kpi8_guidance_q1_fy2027_non_g"],"verdict_values":{"revenue_quality":"高，但只高到 CY2027 年底：八成營收來自有長約與 build-to-order 的資料中心大客戶，CY2027 的規格與價格已入約；CY2028 只配置了量，價格還沒定","unit_econ_note":"每 EB 營收約 1,660 萬美元，季增 6.5%；顆數持平，每顆硬碟裡的碟片與磁頭數去年增加 15–20%（CFO 2026-07-28）","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"近七年有 GAAP 虧損年（FY2023），毛利率谷峰差超過 30 個百分點（FY2023 最差一季 17%，本季 52.7%），營收由每 EB 單價驅動；長約與顆數紀律讓波動變小，但沒有消失"},"industry":{"clock_phase":"III","sd_verdict_source":"量是結構性、價是週期性：資料留存與 AI 推論讓 EB 需求長期成長，長約把量鎖到 CY2028；但單價漲勢來自供需缺口，供給可逆性中等——WD HAMR 2027 量產，STX 與 TDK 的磁頭擴產 12–18 個月後到位","bargaining":{"up":"上游關鍵零件集中：主軸馬達約八成出自 Nidec，稀土精煉約九成在中國，控制晶片由台積電代工；磁頭與碟片自製，北愛爾蘭晶圓廠約供應全球三分之一磁頭（第三方估計）","down":"買方集中但目前弱勢：最大客戶約占營收 14%，資料中心占 81%；STX 產品只占客戶資本支出低到中個位數，缺貨時客戶願意付得比合約價還高","geo":"組裝與測試集中在泰國、馬來西亞、中國；2011 年泰國水災曾在幾週內讓全球硬碟產能少掉近半"},"profit_pool_dir":"利潤池正往硬碟廠移：CFO 說三年內毛利率幾乎變成三倍；但記憶體同業 TTM 毛利率 57–76%，仍高於 STX 的 45.6%","tam_table":[{"item":"2026 年全產業 HDD 營收","value":"上半年逾 150 億美元，全年可能超過 300 億（Coughlin，2026-08-09）"},{"item":"2026 年 Q2 全產業出貨","value":"504.3 EB，季增 5.6%；營收約 85 億美元，季增 14.9%"},{"item":"EB 份額（2025 全年）","value":"WDC 約 47%、STX 約 42%、Toshiba 約 11%（Coughlin 估計）"},{"item":"nearline 供給缺口（Morgan Stanley，經社群轉載）","value":"2026 年約 300 EB（10–15%），2027–28 年擴大到約 400 EB；供給年增 30–35%、需求年增 40–50%"}]}}},"q2_moat":{"verdict":"護城河方向持平：HAMR 領先是真的，但還沒變成份額，2027 年 WD 會追上來","reasoning":"機制是三家寡占，加上 HAMR 技術與自製磁頭、碟片、雷射的垂直整合。執行力給 8 分：40% HAMR 里程碑如期達成，Mozaic 3 在所有主要雲端認證，Mozaic 4 在最大兩家放量。定價能力給 7 分：三年內從價格接受者變成能定價，但這是缺貨撐起來的，CY2028 以後的價格沒有入約。合計落 B。方向判持平：份額沒動——2025 年 EB 份額 STX 約 42%、WD 約 47%，本季 STX 出貨 218 EB 對全產業 Q2 的 504.3 EB 約 43%；定價能力在擴大，但屬週期；執行力穩定。同業表沒有 WD，無法算 ROIC 差距；記憶體同業毛利率 57–76%，STX TTM 45.6%，說明它還不是最能定價的那一種。","fact_refs":["f_peer_stx_gross_margin_pct","f_peer_stx_operating_margin_pct","f_peer_mu_gross_margin_pct","f_peer_000660_ks_gross_margin_pct","f_peer_005930_ks_gross_margin_pct","f_kpi13_price_per_exabyte_yoy","f_kpi15_nearline_exabyte_lta_bac","f_kpi11_exabytes_shipped"],"verdict_values":{"moat":{"mechanism":"三家寡占＋顆數持平的供給紀律＋HAMR 單碟容量領先（40% nearline EB 已在 HAMR）＋磁頭、碟片、雷射自製；長約 2–3 年、少彈性","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"份額：2025 年 EB 份額 STX 約 42%、WD 約 47%，本季 STX 出貨對全產業 Q2 出貨約 43%，持平。定價能力擴大（每 EB 單價年增 10% 加速到約 20% 以上），但來自缺貨，不算護城河變寬。執行力穩定（HAMR 里程碑如期）。WD 40TB ePMR 與 2027 年 HAMR 會縮小容量差距","competitor_notes":[{"name":"WDC","strategy_note":"不在同業表內，但是最直接的對手：EB 份額約 47% 高於 STX；40TB ePMR 2026 下半年上市、HAMR 2027 量產，是 CY2028 單價紀律最大的變數"},{"name":"Toshiba","strategy_note":"份額約 11%，推 34TB SMR；TDK 加磁頭產能主要支援它，是第三家增量來源"},{"name":"MU","strategy_note":"記憶體同業，TTM 毛利率 72.6%，高 STX 約 27 個百分點；NAND 價格高是 STX 低容量段能漲價的原因，也是 QLC 替代的煞車"},{"name":"000660.KS","strategy_note":"TTM 毛利率 76.3%；與 STX 合寫 KV cache 分層儲存白皮書，屬互補，不是直接競爭"},{"name":"005930.KS","strategy_note":"TTM 毛利率 57.5%；NAND 端價格走向決定 QLC 對硬碟的替代速度"},{"name":"285A.T","strategy_note":"事實表缺營收，無法比較"}],"peer_na_reason":"同業表只有記憶體廠利潤率，沒有 WDC 與 Toshiba，無法計算對最強同業的 ROIC 差距","threats":[{"level":"🟡","text":"WD：40TB ePMR 2026 下半年上市、已在兩家大型雲端認證中；HAMR 2027 年認證並量產，2029 年 100TB。STX 的 HAMR 領先期大約只剩一到兩年，屬點對點競爭，但剛好落在 CY2028 定價的時間點","p":"60%","evidence_refs":["substitute_technology#4","channel_business_model_shift#5"]},{"level":"🟡","text":"QLC 大容量 SSD：TrendForce 說硬碟缺貨把部分需求推向 QLC，QLC 功耗約低 30%；另有分析師擔心能源效率需求限縮 Mozaic 4+ 的上檔。目前 NAND 價格偏高，CFO 說資料中心沒有替代品，先判點對點（溫資料層）。升級條件：NAND 價格回落、STX 同時繼續漲價，兩邊每 TB 價差一起收窄","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"level":"🟡","text":"Toshiba 與 TDK：Toshiba 推 34TB SMR，TDK 2026 年 4 月加磁頭產能，給第三家更多量","p":"30%","evidence_refs":["competitive_share_entrants#3","cyclical_supply_discipline_capacity#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未證：TTM 營業利益率 34.65%、Q4 44.6%，資本支出只占營收 4.7%，推定周轉不低；投入資本事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（雲端應用、AI 推論、影片）、決策者（雲端儲存架構）、付款者（雲端業者）三者一致，需求是真的。但延後購買的代價低：FY2023 雲端消化庫存時 nearline 採購大減、營收少 37%；CFO 2026-09-10 也承認電力、建照延誤會讓需求往後推"},{"item":"決策層級","level":"🟡","text":"客戶按儲存層級決定。冷資料層是在硬碟廠之間選：第二代 HAMR 認證已變快（30TB 約一年認證前 8–10 大客戶），WD 40TB 也在兩家大型雲端認證，換供應商的門檻在降。溫資料層是在硬碟與 QLC 之間選。短期黏著來自 2–3 年、少彈性的長約"},{"item":"價值鏈分配","level":"🟢","text":"STX 產品只占客戶資本支出低到中個位數，存資料比重算便宜得多（CFO 2026-09-10），客戶對漲價不敏感；供給端三家、顆數持平，磁頭碟片自製。風險在上游：主軸馬達約八成出自 Nidec，稀土精煉集中中國，可能分走漲價的好處"},{"item":"社會容忍度","level":"🟢","text":"B2B 賣給雲端大廠，沒有消費者或政治上的漲價天花板。政策風險在出口管制與關稅（2023 年被 BIS 罰 3 億美元並附五年暫緩拒絕出口令），不在價格容忍度"}],"roiic":"事實表未涵蓋（缺投入資本、折舊與營運資金變動）","reinvest_rate":"低：FY2026 資本支出 5.69 億美元、占營收 4.7%，同年自由現金流 31.05 億美元；扣除折舊後的淨再投資率事實表未涵蓋","endo_ceiling":25,"formula_note":"標準公式是增量 ROIC×再投資率，兩個輸入都缺。改用管理層在資本支出 4–6% 營收之內可達成的 EB 年增 mid-20%，當作量的內生上界（25%）。這家公司的成長大多來自單價與費用化的研發，不是資本再投資，所以超出上界的部分全數歸給單價"}}}},"q3_growth":{"verdict":"跑道中等：資料量長期成長有依據，但五年後沒有已證實的第二條曲線，EPS 成長主要靠單價","reasoning":"成長來源是量（EB 年增目標 mid-20%，靠單碟容量，不加顆數）加上價（每 EB 單價年增 10% 到 20% 以上），再加 CY2027 起加大的回購；沒有併購。共識 EPS 由 FY2026A 的 15.58 到 FY2029E 的 78.29，年複合約 71%。量的內生上界約 25%，缺口約 46 個百分點，歸因於單價帶動的毛利率擴張、還債後利息下降與回購，其中單價占大頭。實體 AI、KV cache 被管理層提為下一波需求，但 CEO 自己說還很早期、沒有量化，不算第二條曲線。衰退訊號十項亮一項（EPS 成長遠高於營收成長）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi10_guidance_fy2027","f_kpi11_exabytes_shipped","f_kpi13_price_per_exabyte_yoy"],"verdict_values":{"growth":{"driver_mix":"量（EB 年增約 25%，靠單碟容量）＋價（每 EB 單價年增 10% 到 20% 以上）＋回購（CY2027 起加大）；無併購","runway_years":"不適用滲透率算法（成熟產品）；以合約可見度計約 2–3 年（到 CY2028）","runway_post_y5":"🟡","endo_ceiling_basis":"量的內生上界約 25%（管理層 EB 年增 mid-20% 目標，在資本支出 4–6% 營收內完成）；共識 FY2026A→FY2029E EPS 年複合約 71%，缺口約 46 個百分點歸因於單價帶動的毛利率擴張、利息下降與回購，依賴單價不回頭","segments":[{"item":"資料中心","value":"Q4 FY2026 營收 29 億美元，年增 57%，占 81%；出貨 195 EB，年增 43%；雲端大廠為主，企業 OEM 連 5 季成長"},{"item":"Edge IoT","value":"6.97 億美元，年增 20%，占 19%；非 nearline 出貨 23 EB，年減 10%，營收成長來自缺貨漲價與 NAND 偏貴"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"連 13 季擴張"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"EB 份額約 42–43%，持平"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"漲價同時總出貨 EB 年增 34%"},{"signal":"EPS 年複合比營收年複合高 5 個百分點以上","lit":true,"note":"共識 FY2026A→FY2029E EPS 年複合約 71%，遠高於營收成長；差距靠單價與毛利率"},{"signal":"自由現金流÷淨利連 2 年低於 0.75","lit":false,"note":"全年淨利事實表未涵蓋；Q4 自由現金流利潤率約 31%，未見轉換問題"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"1.5%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"QLC 在溫資料層有壓力，未見 TAM 萎縮，列威脅觀察"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"相反，年度端點分位全在頂部"},{"signal":"維持性資本支出占自由現金流超過 60%","lit":false,"note":"全年資本支出 5.69 億對自由現金流 31.05 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"仍在投資 HAMR 製程設備"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置合理但回饋偏小：先還債到投資等級，CY2027 起才大量回購，而回購會落在循環高檔","reasoning":"Q4 自由現金流 11.18 億美元，利潤率約 31%；FY2026 全年 31.05 億美元。資本支出占營收 4.7%，維持 4–6% 區間。債務由年初約 50 億降到 36 億，9 月季末再降到約 24 億，淨槓桿 0.4 倍，剩一筆高利率票據。Q4 以股息加回購回饋約 2.83 億美元，相對市值不到 1%。SBC 占營收 1.5%，稀釋很低。主要風險是 CY2027 起加大的回購，會在倍數最高、循環最熱的時候買進。","fact_refs":["f_kpi5_free_cash_flow","f_kpi6_sbc_non_gaap","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年唯一收購是 2025 年的 Intevac（全現金每股 4 美元），金額事實表未涵蓋，遠小於市值 5%，不適用"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q4 股息加回購約 2.83 億美元，年化約 11 億；以判斷日股價乘約 2.31 億稀釋股數估市值，回饋殖利率不到 1%，不論 10 年期殖利率多少都過不了（10 年期殖利率事實表未涵蓋）"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 單季 5,400 萬美元，占營收 1.5%、占 non-GAAP 營業利益 3.3%；相對市值的年化稀釋遠低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；現金先還債，CY2027 起轉回購與加股息，沒有需要拆解的併購報酬"}}}},"q5_valuation":{"verdict":"現價要求共識一路兌現到 FY2029，也就是每 EB 單價再漲三年；我只給三成機率，所以過貴","reasoning":"現價 $914.72 是 FY2027E 共識 35.78 的 25.6 倍、FY2028E 55.37 的 16.5 倍、FY2029E 78.29 的 11.7 倍。對循環股來說，11.7 倍已接近高峰獲利常見的倍數，等於市場把共識算到 FY2029，還給了高峰倍數。要划算，得是 FY2029 之後單價還守得住，或 EPS 再超共識。賣方均價 $1,125 高於現價約 23%，但同期 FY2027 共識三個月內上修約 35%，目標價是跟著 EPS 走，不是獨立證據。PEG 約 0.36 看似便宜，但分母是高峰單價，不採用。股價營收比 17.07 倍、EV/營收 17.25 倍，年度端點分位都在最高。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027E、FY2028E 共識）對照循環位置；商品循環型本該用股價淨值比，但事實表未涵蓋","peers":{"expanded":false,"reason":"事實表同業只有利潤率、沒有倍數，也沒有 WDC；估值錨改用自身前瞻倍數與循環位置"},"fwd_pe":25.6,"peg":0.36,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"Base 五年價約 $715（FY2031E 55×13 倍），低於現價約 22%；機率加權的五年價也低於現價；本益比、股價營收比、EV/營收在年度端點裡都是最高（只有 3–4 個點，不是連續五年分位）；循環位置在晚段，所以判過貴","upside_short_pct":-18.0,"upside_mid_pct":-21.8,"denominator_disputed":true,"denominator_note":"FY2028E–FY2029E 共識 EPS 建立在每 EB 單價再漲兩到三年；用遠期本益比說便宜的論證不成立，估值改看 FY2027E（價格已入約）與情境機率"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把高峰單價當成新常態：遠期本益比看起來便宜，是因為分母假設單價再漲三年","reasoning":"三個反證視角寫在反證紀錄。陷阱風險中等：衰退訊號只亮一項，公司本身沒有問題，問題在估值用的分母。上一個高峰之後的 FY2023，營收一年少 37%、毛利率掉到 17–19%、全年虧損。這次有長約和顆數紀律，下行會比較淺，但不會沒有。股價 26 週已漲 121.5%。","fact_refs":["f_consensus_eps_fy3","f_pe_current","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰獲利陷阱（中等）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":35.78,"pe":25.57,"basis":"FY2027E 共識 non-GAAP 稀釋 EPS 的前瞻本益比；終端倍數同樣套在單一財年 non-GAAP EPS（FY2031E）上"},"eps":{"bull":[38.0,62.0,86.0,98.0,108.0],"base":[35.5,50.0,58.0,56.0,55.0],"bear":[34.0,40.0,30.0,22.0,25.0]},"pe":{"bull":15,"base":13,"bear":12},"p":{"bull":30,"base":40,"bear":30},"yield_pct":{"dividend":0.3,"net_buyback":0.2},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":3},"max_dd":{"lo":-75,"hi":-50,"basis":"下緣：Bear 路徑 EPS 由 FY2028 約 40 跌到 FY2030 約 22，倍數由現在前瞻約 25.6 倍壓到 11–12 倍，股價約 $240–265，距現價約 −71% 到 −74%；深度參照 FY2023（營收一年少 37%、毛利率 17–19%、全年虧損）。上緣：Base 路徑下市場提前交易循環轉向，FY2028E 約 50 只給 9 倍左右，約 −50%。股價歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"缺口延續到 2029：EB 年增約 25%，每 EB 單價再漲兩年，毛利率到六成五以上；WD HAMR 放量沒有打破紀律；市場改給結構性倍數 15 倍","base":"CY2027 價格已入約，FY2027 貼近共識；CY2028 起 WD HAMR 與磁頭擴產讓單價漲幅收斂、FY2030 起小幅回落，EPS 在 FY2029 見高約 58（低於共識 78.29）；倍數回到循環股常態 13 倍。同業現值倍數事實表未涵蓋，以自身 FY2029E 共識隱含 11.7 倍為對照。回購含在每股盈餘內；殖利率只知 Q4 股息加回購年化約 0.5%，拆分事實表未涵蓋","bear":"2028 年雲端消化庫存、供給追上、QLC 替代三件事疊在一起，重演 FY2023 型下行但較淺（長約有取消費）；EPS 在 FY2030 探底約 22，倍數 12 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023 營收由 116.61 億美元掉到 73.84 億（−37%），non-GAAP 毛利率 21.1%、最差一季 17%，全年 GAAP 虧損 5.29 億，閒置產能費用 1.71 億；起因是雲端消化庫存、nearline 採購大減，產業 EB 出貨全年少約 29%。Coughlin 認為這波漲價可能是暫時的","assumption":"長約與顆數紀律讓這次不一樣","consequence":"2028 年單價回頭加上雲端暫停採購，EPS 在 FY2030 探底約 22，倍數壓到 11–12 倍，股價約 $240–300，較現價少約七成","ruling":"部分採納。長約少彈性、有取消費，下行會比 2023 淺，所以 Bear 定在 FY2030 EPS 約 22，不是虧損；但長約只鎖量，CY2028 以後不鎖價，機率給 30%。這條和唯一致命點是同一條因果鏈，CY2028 定價是它第一個看得到的事件","watch":"資料中心營收季增率、CFO 對訂單遞延的說法、每 EB 單價年增","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","supply_demand_durability#3"],"fact_refs":["f_kpi13_price_per_exabyte_yoy","f_kpi15_nearline_exabyte_lta_bac"]},{"view":"論點成功但股東經濟變差","evidence":"需求照講的成長，但 WD 2027 年 HAMR 量產；STX 自己擴磁頭廠（報導稱近 3 倍，但面積數字是 1.1 萬到 1.9 萬平方呎，約 1.7 倍）；TDK 加磁頭產能。STX 漲價讓硬碟對 QLC 的每 TB 價差收窄，TrendForce 已看到缺貨把需求推向 QLC。上游主軸馬達約八成出自 Nidec，稀土精煉集中中國，漲價的好處可能被上游分走","assumption":"量成長時，單價與毛利率也守得住","consequence":"EB 照樣年增 20% 以上，但每 EB 單價轉跌、毛利率回到五成出頭，EPS 在 FY2029 見高約 58 後走平，低於共識 78.29","ruling":"採納，這就是 Base 情境：量說對了，價說錯了","watch":"CY2028 長約單價、WD HAMR 認證家數、管理層對外購零件成本的說法","evidence_refs":["substitute_technology#0","substitute_technology#3","substitute_technology#4","geo_supply_chain#5","geo_supply_chain#6","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"現價 $914.72 是 FY2027E 共識的 25.6 倍、FY2029E 的 11.7 倍；股價營收比 17.07 倍，本益比、股價營收比、EV/營收在年度端點裡都是最高；26 週漲 121.5%；賣方 25 家、88% 偏多","assumption":"共識 EPS 一路兌現到 FY2029，而且市場之後還願意給高於循環常態的倍數","consequence":"就算共識全中、FY2029 給 12 倍，股價也只到約 $940，三年幾乎沒有報酬；要賺錢得 EPS 再超共識","ruling":"採納：價格已付清到 FY2029 的共識。反駁面是 Q4 營收與 EPS 都超過自己的財測上緣（EPS 5.71 對上緣 5.20），再超共識不是沒可能，這部分放在 Bull 三成","watch":"股價對 FY2027E、FY2028E 的前瞻倍數；共識修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_ps_current","f_ps_percentile","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy3","f_kpi4_non_gaap_diluted_eps"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 747.3 → 本次 914.72（+22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=747.3","side_b":"本次 price_at_dd=914.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求是結構性還是週期性","cause":null,"prior_field":null,"side_a":"結構性，也是現在就買的最強論證：nearline 大部分已配置到 CY2028，客戶要把規劃延到 2029 以後（CEO 2026-07-28）；CFO 2026-09-09 說供需缺口沒縮反而略擴，每次重談長約客戶都要更多量；Morgan Stanley 估缺口 2027–28 年擴大到約 400 EB；顆數持平的紀律讓這次不像以前","side_b":"週期性：Coughlin 認為這波漲價可能是暫時的；FY2023 營收一年少 37%、毛利率跌到 17–19%、全年虧損，就發生在上一個高峰之後；CFO 2026-09-09 自己承認這已不是循環起點，走了三年以上","ruling":"方向相反，不可調和，裁決拆開量與價。量的部分採結構性：合約、客戶規劃期延長、資料留存需求都有來源。價的部分採週期性：CY2028 以後的價格沒有入約，WD HAMR 與新磁頭產能剛好在那時到位。所以 FY2027 可信，FY2029 共識不可信；量的結構性給 Bull 三成機率","evidence_level":"管理層說法＋第三方轉述（Morgan Stanley 經社群轉載、Coughlin 僅標題）＋公司歷史財報","settle_metric":"CY2028 長約的每 EB 單價年增率（2027 年 4 月與 7 月法說）","if_then":["若 2027 年中 CY2028 長約確認每 EB 單價續漲，且資料中心 EB 年增 ≥20%：Bull 機率升到 40%，股價 ≤$760 時建首倉 1.5%","若每 EB 單價年增連 2 季 ≤0：維持不持有；已持有者清倉","反向（價格先走、證據未到）：股價續漲而 CY2028 價格未公布，不追；股價跌到 $644 以下而毛利率仍季增，分批反買首倉 1.5%"],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#3","end_markets#3","end_markets#5","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#4"]},{"axis":"HAMR 進度說法前後","cause":null,"prior_field":null,"side_a":"2026-04-28 CFO：FY2027 年底 nearline EB 七成在 HAMR（講到一半把 calendar '27 改成 fiscal '27）；2026-09-10 CFO：12 月前會到位，兩年後資料中心八到九成走 HAMR","side_b":"2026-07-28 CEO 被問七成目標時說 PMR 推得比原先想的多一點，並刻意放慢 Mozaic 4；CFO 2026-09-09 承認換代時 EB 季度波動會變大","ruling":"可調和，是程度差異：40% 里程碑如期達成，多推 PMR 是為了在 HAMR 製程週期較長時維持顆數。但七成目標的緩衝變小，列為第三個假設的第一個驗證點","evidence_level":"法說與會議逐字稿","settle_metric":"2027 年 7 月法說的 HAMR 占 nearline EB 比例","if_then":["若 2027 年 7 月 HAMR 占比低於 60%：Bull 機率降到 20%","若 ≥70% 且 Mozaic 5 如期送認證：假設成立，但估值仍是約束，不建倉"],"evidence_refs":["substitute_technology#5","end_markets#3"]},{"axis":"管理層定價口徑對照實際","cause":null,"prior_field":null,"side_a":"2026-04-28 CFO：資料中心每 TB 營收年增中個位數，預期延續；不對 FY2027 底的價格給指引","side_b":"6 月季每 EB 單價年增 10%，9 月季財測隱含約 20% 以上（Morgan Stanley 分析師推算，CFO 認同缺口擴大）；2026-09-10 CFO 說增量毛利率七成以上","ruling":"可調和：管理層口徑一向保守，實際跑贏。但四場會議被問到價格幅度與持續期時全部迴避、不給數字，市場無法驗證 CY2028 價格，這正是本次把唯一致命點放在 CY2028 定價的原因","evidence_level":"法說逐字稿","settle_metric":"每季每 EB 單價年增","if_then":["若 Q1 FY2027 每 EB 單價年增低於 15%：財測隱含的加速沒發生，Bull 機率降到 20%"],"evidence_refs":["end_markets#2","capital_markets_pricing#4"]},{"axis":"共識上修幅度的口徑","cause":null,"prior_field":null,"side_a":"事實表的 FY1 共識三個月上修 140.3%（14.89 到 35.78）","side_b":"24/7 Wall St. 同期 FY2027 共識由 26.58 上修到 35.78，約 +34.6%","ruling":"採 B 側：14.89 是財年換季前的 FY2026 估計（FY2026 實際 15.58），140% 是換年造成的，不是上修。同年度真實上修約 35%，仍然很強，但不要拿 140% 當動能證據","evidence_level":"兩個資料源對照","settle_metric":"下一次 Koyfin 快照同財年比較","if_then":["若下一次快照顯示 FY2027E 同財年再上修 10% 以上：Base 的 FY2027 上調到共識"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"結構轉好：三家供給、顆數持平、合約化（長約 2–3 年、少彈性、特定情況有取消費）","side_b":"競爭惡化在路上：WD 40TB ePMR 2026 下半年、HAMR 2027 量產，STX 與 TDK 擴磁頭產能；其他結構變數是 QLC 替代與出口管制、關稅","ruling":"雙向拉鋸：結構轉好目前佔上風（毛利率連 13 季擴張），競爭惡化要到 2027–2028 才到，替代技術與出口管制是尾端風險","evidence_level":"公司 10-K、同業新聞稿、第三方報導","settle_metric":"CY2028 長約單價與 WD HAMR 認證家數","if_then":["若 WD HAMR 在 2027 年底前於 2 家以上大型雲端量產：裁決改為競爭惡化中，已持有者減碼一半"],"evidence_refs":["channel_business_model_shift#1","channel_business_model_shift#3","substitute_technology#4","cyclical_supply_discipline_capacity#0","substitute_technology#0","reg_tariff_export#2"]},{"axis":"前份漂移：未變欄位","cause":"價格變動","prior_field":["dca_verdict","dca_role","signal","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-29，股價 $747.3）：觀望、訊號 B、陷阱風險中等、護城河持平、五年後跑道中等、循環商品型","side_b":"本次（股價 $914.72）：以上判斷不變","ruling":"股價漲約 22%，FY2027 EPS 基數只從指引隱含約 34 升到共識 35.78（約 +5%）。Q4 超標與 Q1 財測是真的好消息，但已被價格吃掉，所以裁決輸入與商業判斷都不變","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"前份漂移：情境價格與報酬","cause":"新證據","prior_field":["bull_5y_price","bear_5y_price","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份：Bull 五年價 $1,200、Bear $144、報酬不對稱 1.1、五年期望報酬 −6.3%、Base 年化 −3.5%","side_b":"本次：Bull 約 $1,620（FY2031E 108×15 倍）、Base 約 $715（55×13 倍）、Bear 約 $300（25×12 倍）；不對稱、期望報酬與年化由程式重算","ruling":"Q4 EPS 5.71 超過財測上緣 5.20，Q1 FY2027 財測 7.30，加上 CY2027 規格與價格已入約，三條路徑整體上移。Bear 底部抬高，是因為 FY2027 幾乎沒有下行空間（CFO 說手上有 4–5 季訂單）","evidence_level":"公司財報與財測","settle_metric":null,"if_then":[],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#4","end_markets#0"]},{"axis":"前份漂移：機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 30%、Bear 25%；最大回撤單點 −75%","side_b":"本次：Bull 30%、Base 40%、Bear 30%；最大回撤改為 −50% 到 −75% 的區間","ruling":"共識 EPS 三年年複合約 71%，遠超量的內生上界約 25%，Bear 機率不低於 30%；回撤改用區間，把 Base 下市場提前殺倍數的情況也算進來","evidence_level":"情境樹規則","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論：偏貴","side_b":"本次估值結論：過貴","ruling":"前瞻本益比由約 22 倍（$747.3÷約 34）升到約 25.6 倍；Base 五年價約 $715 低於現價，機率加權也低於現價","evidence_level":"事實表價格與共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：中循環","side_b":"本次：晚循環","ruling":"三件事改變：毛利率從 47% 升到 52.7%，9 月季財測隱含再升；每 EB 單價年增由 10% 加速到約 20% 以上；新產能開始宣布（STX 擴磁頭廠、TDK 加產能，12–18 個月後到位）。CFO 2026-09-09 也承認已不是循環起點。商品循環六訊號中毛利率與量價關係偏賣，供給紀律與庫存中性，情緒未到狂熱（賣方均價仍高於現價），股價淨值比事實表未涵蓋；多數決落在晚段","evidence_level":"財報＋法說＋第三方產能報導","settle_metric":null,"if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","end_markets#2","capital_markets_pricing#0"]},{"axis":"前份漂移：重新評估價位","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"$505-630（16-18x FY2027 指引隱含 EPS ~$34，即前份 $400-500 門檻按 EPS 基數 +26% 平移）；或循環位置由中轉早","side_b":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","ruling":"倍數法不變（FY2027E 的 16–18 倍），EPS 基數由指引隱含約 34 換成共識 35.78，區間上移到 $572–644。拿掉「循環位置由中轉早」，因為現在已是晚循環；改成單一價格約束，觸發後先重跑研究，不直接建倉","evidence_level":"事實表共識","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"CY2028 年度 build-to-order 合約的新約每 EB 單價年增率轉負（預計 2027 年第二到第三季談定）","ruling":"前份把風險拆成三條並列，沒有指出哪一條數學上最敏感。共識 FY2026A→FY2029E EPS 年複合 71% 裡，約六成五靠單價，所以 Single Thing 定在 CY2028 定價；發生即清倉","evidence_level":"情境樹敏感度","settle_metric":"CY2028 新約每 EB 單價年增率","if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標（空白）","side_b":"每 EB 單價年增連 2 季 ≤0（清倉）；non-GAAP 毛利率連 2 季季減且低於 52%（減碼一半）；資料中心 EB 年增連 2 季低於 15%（減碼一半）；WD HAMR 在 2027 年底前於 2 家以上大型雲端量產（減碼一半）","ruling":"前份只有進場價，沒有持有後的退出線；本次補上四條，各自對應情境樹的 Bear 路徑","evidence_level":"情境樹規則","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q1 FY2027 財報：毛利率是否照承諾逐季上升","type":"假設驗證","maps_to":"H2","metric":"non-GAAP 毛利率（季）","threshold":"低於 Q4 的 52.7%（季減）","action":"第二個假設削弱，Bull 機率降到 20%；未持有者不動作","source_freq":"每季財報新聞稿","date":"2026-10"},{"n":2,"text":"股價回到 FY2027E 共識的 16–18 倍","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤$644（35.78×18）","action":"重跑完整研究；通過後建首倉 1.5%","source_freq":"每日收盤","date":null},{"n":3,"text":"CY2028 長約定價","type":"Single Thing","maps_to":"H2","metric":"新長約每 EB 單價年增率","threshold":"≤0%","action":"移出觀察名單；已持有者清倉","source_freq":"2027 年 4 月與 7 月法說","date":"2027-07"},{"n":4,"text":"HAMR 七成目標","type":"假設驗證","maps_to":"H3","metric":"HAMR 占 nearline EB 比例","threshold":"2027 年 6 月底 ≥70%；低於 60% 即削弱","action":"低於 60%：Bull 機率降到 20%","source_freq":"每季法說","date":"2027-07"},{"n":5,"text":"WD HAMR 在大型雲端量產","type":"風險","maps_to":"R1","metric":"WD HAMR 完成認證並量產的大型雲端家數","threshold":"≥2 家，且早於 Mozaic 5 送認證","action":"已持有者減碼一半；未持有者 Bear 機率升到 40%","source_freq":"WD 季度法說與新聞稿","date":"2027-06","evidence_refs":["substitute_technology#4"]},{"n":6,"text":"供應鏈或出口管制卡住出貨","type":"風險","maps_to":"R3","metric":"單季營收對財測下緣","threshold":"低於下緣，且公司把原因歸給零件、稀土、出口管制或關稅","action":"已持有者減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#8","reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","major_events#1"]},{"n":7,"text":"雲端消化庫存","type":"風險","maps_to":"R4","metric":"資料中心營收季增率；CFO 對訂單的說法","threshold":"季減，或提到訂單遞延","action":"已持有者清倉；未持有者等循環位置轉回早段","source_freq":"每季財報與法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5"]},{"n":8,"text":"證券集體訴訟和解最終聽證","type":"風險","maps_to":"R3","metric":"法院是否最終核准 1.75 億美元和解","threshold":"未核准","action":"核准則結案、不動作；未核准則把超出 1.75 億美元的求償列進 Bear 情境","source_freq":"和解網站、8-K","date":"2026-11-17","evidence_refs":["lawsuit_class_action#0","major_events#0"]},{"n":9,"text":"下次複審","type":"複審日期","maps_to":null,"metric":"Q1 FY2027 財報與 Q2 財測","threshold":"財報公布後一週內","action":"更新情境路徑與機率","source_freq":"每季","date":"2026-10"}],"kill_metrics":[{"metric":"新長約每 EB 單價年增率","bear_threshold":"連 2 季 ≤0%（清倉）","window":"2026Q4–2028Q2","source":"每季法說 Q&A（分析師轉述、CFO 確認）","last_status":"ok"},{"metric":"non-GAAP 毛利率","bear_threshold":"連 2 季季減且低於 52%（減碼一半）","window":"FY2027–FY2028","source":"公司財報新聞稿","last_status":"ok"},{"metric":"資料中心 EB 出貨年增率","bear_threshold":"連 2 季低於 15%（減碼一半）","window":"FY2027–FY2028","source":"CFO 法說準備稿","last_status":"ok"},{"metric":"WD HAMR 量產的大型雲端家數","bear_threshold":"2027 年底前 ≥2 家（減碼一半）","window":"2027","source":"WD 新聞稿與法說","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價回到 $572–644（FY2027E 共識 35.78 的 16–18 倍）即重跑研究；此價位之前不建倉","exec_line":"不建倉、不追價。約束只有一個：價格已付清共識到 FY2029 的單價漲勢。股價回到 $572–644 重跑研究；若 2027 年中 CY2028 長約確認單價續漲，股價 ≤$760 也重跑。","holding_cap":"目前 0%；日後進場上限 3%"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方均價 $1,125 等於 FY2028E 約 20 倍、FY2029E 約 14 倍，隱含每 EB 單價到 CY2029 仍在漲；但 CY2028 價格尚未入約，WD HAMR 2027 量產、磁頭擴產 12–18 個月後到位，單價漲勢在 FY2029 前收斂的機率被低估","momentum_overheated":false,"cycle_gates_pass":false,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方均價 $1,125 等於 FY2028E 約 20 倍、FY2029E 約 14 倍，隱含每 EB 單價到 CY2029 仍在漲；但 CY2028 價格尚未入約，WD HAMR 2027 量產、磁頭擴產 12–18 個月後到位，單價漲勢在 FY2029 前收斂的機率被低估"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='→', week26=121.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心 EB 需求維持結構性成長，長約配置持續往後滾到 CY2029","2y":null,"5y":"FY2031 前資料中心 EB 年增不低於 20%","10y":null,"threshold":"資料中心 EB 出貨年增 ≥20%，且管理層每季仍說 nearline 大部分已配置到 18 個月以後","source":"每季法說 CFO 準備稿的資料中心 EB 與年增；10-Q","drift_rule":"資料中心 EB 年增連 4 季低於 19%（偏離 5%）削弱；連 6 季低於 18%（偏離 10%）反轉"},{"id":"H2","text":"CY2027 已入約的價格加上供需缺口，讓毛利率在 FY2027 逐季上升、FY2028 守住 55% 以上","2y":"FY2028 全年 non-GAAP 毛利率不低於 55%","5y":null,"10y":null,"threshold":"FY2027 各季 non-GAAP 毛利率逐季上升（管理層承諾）；FY2028 不低於 55%；每 EB 單價年增大於 0","source":"每季財報新聞稿的 non-GAAP 毛利率；法說 Q&A 的每 EB 單價年增（分析師轉述、CFO 確認）","drift_rule":"FY2027 任一季毛利率季減即削弱；FY2028 連 2 季低於 52.25% 削弱、連 3 季低於 49.5% 反轉"},{"id":"H3","text":"HAMR 領先換成每 TB 成本優勢，而且領先期撐到 WD HAMR 放量之後","2y":null,"5y":"Mozaic 5、6 持續領先 WD 同代產品至少一年","10y":null,"threshold":"2027 年 6 月底 nearline EB 七成在 HAMR；Mozaic 5 在 2027 年底前送客戶認證","source":"每季法說的 HAMR 占比與里程碑；WD 新聞稿與法說的 HAMR 認證進度","drift_rule":"里程碑延後 1 季削弱；延後 2 季以上，或 WD HAMR 在 Mozaic 5 送認證前已在兩家大型雲端量產，反轉"}],"R":[{"id":"R1","text":"供給追上、單價見頂：WD 40TB ePMR 2026 下半年上市、HAMR 2027 量產；STX 擴磁頭廠、TDK 加磁頭產能，12–18 個月後陸續到位。CY2028 長約定價時缺口可能收斂，重演上一個高峰後的下行","h_ref":"H2","clock":"🔥","threshold":"每 EB 單價年增連 2 季 ≤0，或毛利率連 2 季季減","evidence_refs":["supply_demand_durability#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","substitute_technology#4","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1"]},{"id":"R2","text":"QLC 替代加上漲價的反作用：STX 越漲價，硬碟對 QLC 的每 TB 價差越窄；等 NAND 價格回落，兩邊一起收窄，溫資料層加速轉向快閃","h_ref":"H1","clock":"🐢","threshold":"資料中心 EB 年增連 2 季低於 15%，且管理層或客戶提到溫資料層改用快閃","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"id":"R3","text":"供應鏈與出口管制：主軸馬達約八成出自 Nidec，稀土精煉約九成在中國，組裝集中泰國，控制晶片靠台積電；10-K 列出關稅、出口管制可能造成重大不利影響。2023 年因對華為出貨被 BIS 罰 3 億美元，仍在分季付款，附五年暫緩拒絕出口令；另有 1.75 億美元證券集體訴訟和解待最終核准","h_ref":"H1","clock":"⚡","threshold":"單季營收低於財測下緣，且公司把原因歸給零件、稀土、出口管制或關稅","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#5","geo_supply_chain#6","geo_supply_chain#7","geo_supply_chain#8","reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#5","regulatory_antitrust#1","regulatory_antitrust#2","major_events#1"]},{"id":"R4","text":"雲端暫停採購：FY2023 雲端消化庫存時 nearline 採購大減；最大客戶約占營收 14%，一家放慢就看得見。CFO 說電力、建照延誤會讓需求往後推","h_ref":"H1","clock":"🔥","threshold":"資料中心營收季減，或 CFO 提到訂單遞延","evidence_refs":["cyclical_prior_downcycle_behavior#4","cyclical_prior_downcycle_behavior#5","customer_concentration_credit#0"]}],"single_thing":{"description":"CY2028 年度 build-to-order 合約（預計 2027 年第二到第三季談定）的新約每 EB 單價年增率轉負","why_fatal":"共識 FY2026A→FY2029E EPS 年複合約 71%，量的內生上界約 25%，約六成五的成長靠單價。單價轉負，毛利率從高峰回落，EPS 改走 Bear 路徑，倍數也從前瞻約 25 倍掉到循環常態","if_happens":"未持有者移出觀察名單、不等回檔買；已持有者清倉。Bear 機率由 30% 升到 45%","how_monitor":"2027 年 4 月與 7 月法說對新長約定價的說法；每季每 EB 單價年增（分析師 Q&A 轉述、CFO 確認）；WD 同期的定價說法","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.52,"peg_fy2":0.3,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":15.58,"FY2027E":35.78,"FY2028E":55.37,"FY2029E":78.29},"fy_end_month":6,"eps_basis":"non-GAAP 稀釋 EPS；財年止於最接近 6 月 30 日的週五（FY2026 止於 2026-07-03）；共識取 Koyfin 2026-09-19 快照，家數事實表未涵蓋"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報與 Q2 財測","impact":"高","watch":"毛利率是否季增、每 EB 單價年增是否約 20% 以上"},{"date":"2026-11-17","date_precision":null,"type":"other","event":"證券集體訴訟 1.75 億美元和解最終聽證","impact":"低","watch":"法院是否核准"},{"date":"2026-11","date_precision":"month","type":"other","event":"年度股息檢討（CFO 說強勁時期通常會加）","impact":"低","watch":"加幅與回購節奏"},{"date":"2026-12","date_precision":"month","type":"product","event":"Mozaic 4 占 HAMR EB 過半的里程碑","impact":"中","watch":"2027 年 1 月法說是否確認達成"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"WD HAMR 客戶認證與量產","impact":"高","watch":"大型雲端認證家數"},{"date":"2027-07","date_precision":"quarter","type":"guidance","event":"CY2028 長約定價談定","impact":"高","watch":"新約每 EB 單價年增是否轉負"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"Mozaic 5（50TB）送客戶認證","impact":"中","watch":"是否如期"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
