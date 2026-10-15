你是 DD 管線 v20 的判斷層閘（gate），標的 3665.TW（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_ifrs`（q1_business）｜營收（IFRS 合併）＝232.81 億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw/articles/1343453844（轉載鉅亨網）；Quartr 交叉一致；非公司 IR 原稿（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-21））
  - 註記：查無
- `f_kpi1`（q1_business）｜毛利率＝30.73 %｜期間與口徑：Q2 2026（公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw/articles/1343453844；Quartr（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（公告於 2026-08-21））
  - 註記：查無
- `f_kpi2_ifrs_gaap`（q1_business）｜營業利益率（IFRS，等同 GAAP）＝17.22 %｜期間與口徑：Q2 2026（公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw/articles/1343453844；Quartr（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（公告於 2026-08-21））
  - 註記：查無
- `f_kpi3_ifrs`（q1_business）｜營業利益（IFRS）＝40.1 億 TWD｜期間與口徑：Q2 2026（公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Quartr 頁面列 NT$4.01B；與營收×營益率推算一致（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（公告於 2026-08-21））
  - 註記：查無
- `f_kpi4_eps`（q1_business）｜稅後純益（歸屬母公司）／EPS＝15.28 TWD/股（純益 29.82 億，QoQ +31.13%，YoY +47.29%）｜期間與口徑：Q2 2026（公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw/articles/1343453844；Quartr（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（公告於 2026-08-21））
  - 註記：查無
- `f_kpi5`（q1_business）｜管理層展望（無數字指引）＝定性｜期間與口徑：Q2 2026（公告於 2026-08-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Quartr 摘要、uanalyze；非公司原稿（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（公告於 2026-08-21））
  - 註記：無數字區間可比
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-25 date｜期間與口徑：2026-08-25／距今 34 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-25）
- `f_peer_3665_tw_gross_margin_pct`（q2_moat）｜3665.TW 毛利率＝31.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3665.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3665_tw_operating_margin_pct`（q2_moat）｜3665.TW 營業利益率＝17.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3665.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3665_tw_fcf_margin_pct`（q2_moat）｜3665.TW FCF 利潤率＝5.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3665.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_aph_gross_margin_pct`（q2_moat）｜APH 毛利率＝37.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APH.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aph_operating_margin_pct`（q2_moat）｜APH 營業利益率＝26.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APH.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aph_fcf_margin_pct`（q2_moat）｜APH FCF 利潤率＝17.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APH.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tel_gross_margin_pct`（q2_moat）｜TEL 毛利率＝36.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TEL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tel_operating_margin_pct`（q2_moat）｜TEL 營業利益率＝20.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TEL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tel_fcf_margin_pct`（q2_moat）｜TEL FCF 利潤率＝17.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TEL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3023_tw_gross_margin_pct`（q2_moat）｜3023.TW 毛利率＝24.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3023.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3023_tw_operating_margin_pct`（q2_moat）｜3023.TW 營業利益率＝10.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3023.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3023_tw_fcf_margin_pct`（q2_moat）｜3023.TW FCF 利潤率＝4.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3023.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝69.25 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝127.97 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝164.67 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.655 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝2355.0 TWD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝43.31 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.58 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.56 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝34.08 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 69.25，分子＝快照價 2360.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝6.77 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.54｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：2025年初農曆年前，傳出大客戶Credo引進第二個AEC供應商，貿聯股價一度跌停；董事長梁華哲稱雙方合作六年、貿聯仍是Credo獨家供應商（搜尋摘要轉述，未逐字取得）。
  - 來源：工商時報／經濟日報等報導（ctee 20250220700247-439901）（as_of 2025-02-20）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：2025年12月報導：市場再傳AEC大客戶Credo引進第二供應商，壓抑貿聯股價；未見公司或Credo正式確認，亦無第二供應商出貨規模資料。
  - 來源：中時 wantrich 20251205900555-420101（as_of 2025-12-05）｜affects：decision_inputs.bear、thesis.R
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：2026年1月報導：輝達CES表示Rubin伺服器將採「無線纜」設計，線束大廠貿聯首當其衝（潛在設計面衝擊，非確認輝達自製線束）。
  - 來源：中時 wantrich 20260114900129-420101（as_of 2026-01-14）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：CRU 預期銅雙絞線（twinax）成長延續到本十年末，但 2020 年代後期至 2030 年代初隨光學替代擴大而放緩
  - 來源：CRU Group, The outlook of copper based data cables in AI data centres（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Gartner（2026 年 2 月）預期 CPO 約三年內成為主流，銅在 224Gbps/lane 遇到極限，買方焦點轉向 scale-up 互連
  - 來源：Gartner Insights Abstract（as_of 2026-02-01）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：歐系外資報告指貿聯擬發行 GDR 與 ECB，預估稀釋每股盈餘約 6%~7%（摘要轉述，無逐字原文）。
  - 來源：工商時報 wantrich 外資報導（as_of 2026-07-09）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":6860,"bear_5y_price":1344,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":64.4,"ev5y_pct":63.9,"irr_base_pct":10.5,"asym_ratio":3.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":69.25,"pe":34.01,"basis":"FY2026E 共識 EPS（Fwd 口徑）；終端倍數同樣乘在終端年度 EPS"},"eps":{"bull":[125,160,192,220,245],"base":[105,128,148,163,176],"bear":[78,72,80,88,96]},"pe":{"bull":28,"base":22,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.655,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 3665.TW_Q1_2026_Earnings_Call_20260512.md
- 2026-05-12｜Mike Wang｜guidance：主持人聲明本場不提供前瞻性量化評論（原話："there will be no forward-looking quantitative comments"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 將毛利/營運槓桿壓力歸因於世代轉換：舊品下滑、新世代爬坡初期、產能利用率與產品組合尚未到位（原話："our legacy solution are declining as expected, while next-generation programs are still in early stage of ramp"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 列出重疊期的三項壓力來源：舊品價格正常化、新案爬坡低效率、多世代並行的營運複雜度（原話："legacy pricing normalization, early-stage ramp inefficiency for newer programs and elevated operational complexity"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 稱目前毛利狀況屬轉換與重疊階段，並非長期軌跡改變（原話："the current margin profile is best understood as part of the transition and overlap phases"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 稱長期營運槓桿不變但逐季未必線性，並提到本季營業利益層級顯示費用控管（原話："it still show that we have strong OpEx discipline"）
- 2026-05-12｜Charles Tsai (CFO)｜margin：CFO 描述新平台初期的成本結構：量小、前期工程與營運成本高（原話："newer platform typically begin with lower initial volume and higher upfront engineering and operational costs"）
- 2026-05-12｜Charles Tsai (CFO)｜risk：銅與 PVC 原料成本持續上升，引發部分供應鏈的價格討論，公司選擇性調價（原話："We are selectively adjusting pricing where appropriate while continuing to support customer ramp requirements."）
- 2026-05-12｜Charles Tsai (CFO)｜risk：供應鏈緩衝庫存與急單減少，部署時程差異在近期更為明顯（原話："which means timing difference are more visible in the near term"）
- 2026-05-12｜Charles Tsai (CFO)｜risk：擴產與營運整備可能暫時影響近期效率（原話："this effort may temporarily impact near-term efficiency"）
- 2026-05-12｜Charles Tsai (CFO)｜competition：家電業務在部分品類因產業產能過剩與客戶競爭而仍具競爭性壓力（原話："electrical appliances remain competitive across selected product categories due to industry overcapacity"）
- 2026-05-12｜Charles Tsai (CFO)｜customer：工業與車用狀況逐步改善，來自特定客戶活動與試產案（原話："industrial and automotive conditions continue improving gradually"）
- 2026-05-12｜Charles Tsai (CFO)｜customer：半導體設備端近期投資節奏較為溫和，但能見度仍屬健康（原話："a more measured near-term investment cadence in certain areas of semiconductor ecosystem"）
- 2026-05-12｜Florian Hettich (COO)｜risk：COO 稱檳城的主要挑戰在營運擴張與勞動力能力培養，而非需求（原話："our primary challenge remains operational scaling and labor capability development rather than demand generation"）
- 2026-05-12｜Florian Hettich (COO)｜product：COO 稱 AI 基礎設施趨向機櫃層級設計（原話："One of the clearest shifts is that AI infrastructure is becoming rack-centric."）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜product：HPC 布局涵蓋銅互連、光連接與電源傳輸三層（原話："copper interconnect, optical connectivity and power delivery"）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜competition：董事長稱公司策略不依賴單一架構結果，多種電源／光／互連路線將並存多年（原話："our strategy is not dependent on any single architecture outcome"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜product：CEO 說明鑫福盛（XFS）自 1 月初併入，Q1 反映與 2025 大致一致的基線（原話："we consolidated the business starting early January"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜product：CEO 指出 4 月活動明顯回升，但仍定性為早期階段（原話："particularly into April, is a meaningful pickup in activities"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜commitment：CEO 表示需再觀察數季穩定表現才對 XFS 軌跡下結論（原話："we would prefer to see a few more quarters of consistency before drawing firm conclusions on the trajectory"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：XFS 近期營收貢獻取決於客戶部署步調與時程（原話："near-term revenue contribution will still depend on the pace and timing of customer deployments"）
- 2026-05-12｜Florian Hettich (COO)｜competition：COO 回應銅 vs 光：不視為二元取代，兩者並存（原話："we do not view this as a binary transition where one technology is just replaced by another"）
- 2026-05-12｜Charles Tsai (CFO)｜capital_allocation：CFO 說明資本支出採能見度驅動、紀律式節奏，擴產地點含 Batam、Tainan、Penang、Johor、Vietnam（原話："disciplined and visibility driven rather than speculating"）
- 2026-05-12｜Charles Tsai (CFO)｜commitment：CFO 稱投資步調對應客戶專案能見度與營運成熟度，而非短期需求波動（原話："pacing investment alongside customer program visibility and operational maturity"）
- 2026-05-12｜Hwa-Tse Liang (Chairman)｜capital_allocation：董事長稱長期併購策略不變，採能力導向、選擇性，並維持估值與整合紀律（原話："long-term M&A strategy remains the same, unchanged"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜commitment：CEO 稱目標不在單純加快成長，而是建立可跨週期擴展的長期能力（原話："our objective is not simply to grow faster"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：CEO 稱處於 AI 基礎設施投資週期的非常早期階段；季度部署時程仍會變動（原話："we are, again, in a very early stage of the AI total development investment cycle"）
- 2026-05-12｜Chien-Hua Teng (CEO)｜guidance：CEO 稱季度部署時程仍可能因客戶排程而變動，但整體建置呈多年累積性質（原話："quarterly deployment timing can still vary depending on customer schedules"）
- 2026-05-12｜Florian Hettich (COO)｜product：COO 稱電壓提升由物理與效率驅動，客戶仍在評估不同 HVDC 與機櫃配電方案，預期多路徑並存（原話："we are therefore, expect multiple pathways to coexist"）

### 問答異常語氣（迴避／改口／保留）
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：毛利低於預期的具體原因與復原路徑（Morgan Stanley、BofA 等）｜答法：管理層以世代轉換／產業結構論述作答，未給出毛利數字、各項壓力的量化拆解或復原時點；僅稱「隨新案放量自然抵銷」
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：光學／XFS 的商機與放量軌跡｜答法：未給 XFS 營收或放量數字；稱 Q1 為與 2025 一致的基線、4 月回升，並表示需數季一致表現才下結論
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：營運槓桿與長期獲利力（含工程密集度與光學投資）｜答法：僅稱長期槓桿「intact」、路徑逐季不線性，未給時點或幅度
- 3665.TW_Q1_2026_Earnings_Call_20260512.md｜問：CapEx 與製造擴張規模；HPC 能見度；48/54V 與 800V HVDC 母排 ASP 差距｜答法：CapEx 與能見度問題未給金額或訂單量；ASP 提升幅度的提問未被直接回答，改談物理與架構

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | found | 4 | 3 |
| customer_concentration_credit | none | 0 | 3 |
| supply_demand_durability | found | 5 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | none | 0 | 2 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_concentration_credit**（none）：貿聯-KY 3665 前十大客戶 營收比重 客戶集中度 2026；BizLink Holding top customer revenue concentration annual report 2026；貿聯-KY 客戶 Credo 占營收 比重 大客戶
- **regulatory_antitrust**（none）：貿聯-KY BizLink antitrust OR monopoly investigation 2026；BizLink regulation OR regulatory scrutiny cable connector AI server 2026；BizLink 貿聯 DOJ OR FTC OR EU competition 2026
- **geo_supply_chain**（none）：貿聯-KY BizLink manufacturing locations geopolitical risk 2026；BizLink supply chain concentration copper cable assembly Mexico Vietnam China tariff 2026
- **channel_business_model_shift**（none）：貿聯-KY BizLink 3665 business model transition 2026；BizLink distribution channel shift go-to-market change 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3665.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"貿聯-KY（BizLink）"},"oneliner":"AI 資料中心銅纜、電源與光纖互連的製造商，前 9 月營收年增四成、Q2 獲利創單季新高；共識 2027 年 EPS 年增 85% 偏樂觀，銅被光替代、客戶二供與增資稀釋是三大折價，基準情境五年年化約一成。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3665.TW_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 資料中心（銅纜、AEC、電源母排、光纖組件）與半導體設備、工業客戶的互連與子系統製造錢；錢卡在 NVIDIA 平台規格與 Credo AEC 方案這一節點，貿聯是被指定、每一代都要重新認證的工程製造方。","reasoning":"Q2 2026 營收 232.81 億元（年增 37%、季增 12%），毛利率 30.73%、營益率 17.22%、EPS 15.28 元創單季新高，Q1 毛利率 28.77% 的轉換期壓力已回穩；管理層不給數字指引。營收結構：HPC 相關占比由 2024 年約 18% 升到 2025 年約 35%，外資估 Interplex 併入後 2026、2027 年達 53%、75%（分析估計，口徑不一）；半導體設備端財務長稱訂單能見度到 2027 下半年；工業與車用逐步回升。單點依賴：Credo 的 AEC 據報由貿聯獨家或主要供應，2025 年兩度傳出二供，屬集中度風險，不當護城河證據；前大客戶營收占比事實表未涵蓋。供需持久性：AI 部署需求屬結構性，但管理層兩場法說都說投資週期會有消化期，產品層屬週期性將反轉的類型。產業態勢：競爭惡化中（大廠擴展 AI 互連與電源、客戶二供）與結構轉好中（電力與互連需求、半導體設備子系統）同時存在，屬雙向拉鋸。四項外部依賴逐項檢查：（一）客戶集中度與信用：付款端是少數超大規模雲端，規格由 NVIDIA 決定、AEC 方案由 Credo 決定，HPC 占比外資估 2026 年 53%、2027 年 75%，集中度高且還在上升；前大客戶營收占比、應收帳款天數與客戶信用條件事實表皆未涵蓋，所以只能定性判為高、不給量化分數，以 Credo 二供消息與月營收年增率作監測點。（二）監管與反壟斷：產品不是受監管品項，沒有授權依賴；美國 301 關稅屬總體背景、未點名公司；直接涉及公司的反壟斷或出口管制事件事實表未見，判低。（三）地緣與供應鏈：擴產分散在巴淡、台南、檳城、柔佛、越南，降低單一國家關稅風險；原料端銅與 PVC 漲價只能選擇性轉嫁（2026-05-12 財務長），屬毛利風險而非斷料風險；關鍵零組件是否單一來源事實表未涵蓋。（四）通路與商業模式轉移：由線纜組件往電源母排、光學（XFS）與機構件（Interplex）子系統延伸，是每櫃內容價值擴大，不是通路改變；真正的風險在 NVIDIA 平台設計改動（CES 2026 稱 Rubin 伺服器採無線纜設計）把內容價值移出公司產品範圍，已列入風險項追蹤。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_gaap","f_kpi3_ifrs","f_kpi4_eps","f_kpi5","f_earnings_recency"],"verdict_values":{"revenue_quality":"以專案出貨為主，非經常性合約；隨平台世代換代，季度波動受客戶部署時點影響（管理層自述）","unit_econ_note":"每櫃內容價值隨功率密度與傳輸速度上升而增加；新平台初期量小、前期工程成本高，放量後才有效率（2026-05-12 財務長 Charles Tsai）","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"AI 平台世代驅動的互連製造，三年毛利率上升，成長部分靠併購與外部股本"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構持久（AI 部署由算力延伸到電力、網路、散熱與機構），但產品層週期性將反轉：管理層自述會有加速與消化期，銅纜段本十年末後面臨光學替代（CRU）","bargaining":{"up":"銅與 PVC 原料漲價，公司只能選擇性轉嫁（2026-05-12 財務長）","down":"NVIDIA 定平台規格、Credo 定 AEC 方案、超大規模雲端付款，議價權在客戶端；Credo 兩度傳出引進二供","geo":"擴產地點分散於巴淡、台南、檳城、柔佛、越南；美國 301 關稅屬總體背景、未點名公司"},"profit_pool_dir":"AI 機櫃互連與電源利潤池擴大，但向光學與 800V HVDC 遷移；銅雙絞線段本十年末後放緩","tam_table":{"expanded":false,"reason":"事實表未收高速銅纜、AEC、HVDC 母排與光纖組件的 TAM、滲透率與段別成長資料，只有 CRU 的定性判斷，無法建表；以 HPC 營收占比與替代技術時點代替"}}}},"q2_moat":{"verdict":"護城河方向持平：多世代認證累積的工程與量產能力在擴大，但客戶二供與銅被光替代讓定價力沒有變強。","reasoning":"機制：高速銅與電源產品歷經多代開發與認證，董事長稱既有供應商帶著認證紀錄、客戶關係與量產經驗進入下一代，後進者要追趕；財務長稱部分工程已延伸到 N+2 平台。執行面擴大：毛利率由 FY2022 25.65% 升到 FY2025 31.73%，營益率 10.46% 升到 17.52%（年度財報）。定價面持平：TTM 營益率 17.44% 仍低於 APH 26.77%、TEL 20.49%，FCF 率 5.38% 對兩者約 17%，差距大；原料漲價只能選擇性轉嫁；Credo 二供傳聞代表最大 AEC 客戶並非鎖死。同業 ROIC spread 事實表未涵蓋，以利潤率代替。評分：執行 8、定價 6。","fact_refs":["f_peer_3665_tw_gross_margin_pct","f_peer_3665_tw_operating_margin_pct","f_peer_3665_tw_fcf_margin_pct","f_peer_aph_gross_margin_pct","f_peer_aph_operating_margin_pct","f_peer_aph_fcf_margin_pct","f_peer_tel_gross_margin_pct","f_peer_tel_operating_margin_pct","f_peer_tel_fcf_margin_pct","f_peer_3023_tw_gross_margin_pct","f_peer_3023_tw_operating_margin_pct","f_peer_3023_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"多世代平台認證累積的高速銅、電源與系統整合工程能力，加上早期參與客戶下一代平台開發；轉換成本來自重新認證週期","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大（毛利率三年由 25.65% 升到 31.73%、營益率 10.46% 升到 17.52%，Q2 2026 回到 30.73%／17.22%）；定價面持平（營益率仍低於 APH、TEL，FCF 率差距約 12pp，Credo 二供傳聞兩度出現、原料成本只能選擇性轉嫁），合起來判持平","competitor_notes":[{"name":"APH","strategy_note":"毛利率 37.6%、營益率 26.8%、FCF 率 17.3% 全面高於貿聯，是高速銅與電源互連最強對手，規模與現金流能在價格與產能上施壓"},{"name":"TEL","strategy_note":"營益率 20.5%、FCF 率 17.2%；供應鏈報告稱其 GB300 銅背板份額低於預期的 30%，大廠在這個細分並未壓倒性勝出"},{"name":"3023.TW","strategy_note":"毛利率 24.4%、營益率 10.6%，台系線束同業的獲利結構明顯較低，貿聯的溢價來自 HPC 與高速產品組合"}],"spread_notes":null,"peer_na_reason":"事實表未收同業 ROIC 與投入資本，只能用毛利率、營益率、FCF 率代替 spread","threats":[{"level":"🟡","text":"Credo 兩度傳出引進第二家 AEC 供應商，未見正式確認與出貨規模；屬點對點份額威脅","p":35,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"level":"🔴","text":"NVIDIA 平台設計改變線纜內容：CES 2026 稱 Rubin 伺服器採無線纜設計，背板份額每代重分","p":25,"evidence_refs":["customer_second_source#2"]},{"level":"🔴","text":"光學／CPO 在 scale-up 取代銅：CRU 預期 2020 年代後期放緩、Gartner 預期約三年內成主流；公司有 XFS 光學可部分接住，所以列生態攻擊而非全面架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"大廠跨入資料、電源、光學的完整產品線，董事長 2026-08-21 承認競爭者正在擴大組合","p":40,"evidence_refs":[]}],"roic_durability":{"quadrant":"未定：事實表未收投入資本；營益率 17.4% 屬中高，FCF 率 5.4% 顯示營運資金與資本支出占用偏重","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 機櫃）、決策者（NVIDIA 定規格、Credo 定 AEC 方案）、付款者（超大規模雲端）三環都成立；9 月營收年增 39.2%。風險在部署時點而非需求本身，管理層 2026-08-21 自己說會有消化期"},{"item":"決策層級","level":"🟡","text":"替代性的最小單位是每一代平台的重新認證；董事長稱多代認證讓既有供應商帶著資歷進下一代，但 Credo 兩度傳出引進二供，每代認證都是重新競爭的窗口"},{"item":"價值鏈分配","level":"🟡","text":"規格與晶片價值在 NVIDIA 與 Credo，貿聯拿製造與工程段；營益率低於 APH、TEL，銅與 PVC 漲價只能選擇性轉嫁（2026-05-12 財務長），價值鏈位置偏中段"},{"item":"社會容忍度","level":"🟢","text":"產品非民生必需品、無監管授權依賴；美國 301 關稅與產能過剩關稅屬總體背景、未點名公司，產能已分散到東南亞與台灣"}],"roiic":"事實表未涵蓋（缺投入資本與併購前後資產負債表）","reinvest_rate":"事實表未涵蓋（缺折舊攤銷與營運資金變動；收購 Interplex 企業價值 8.5 億美元，XFS 金額未列）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入皆缺，不推估上界數字。判定共識超出內生能力的依據不是算式，而是資金來源檢驗：共識三年 EPS 年化約 52.6%，同期內部現金只有 TTM FCF 率 5.4%（FCF／淨利 FY2025 約 0.54），擴張資金實際來自 GDR／ECB 增資（估每股盈餘稀釋 6%～7%）與 8.5 億美元現金收購 Interplex；若內部現金足以支撐，就不需要外部股本。可能看錯之處：外部募資也可能是趁高估值籌碼，而非內部資金不足。此判定屬定性、信心中，待投入資本揭露後改以算式重驗。"}}}},"q3_growth":{"verdict":"五年後跑道中等：AI 互連與半導體設備仍在擴張，HVDC 電源與光學是有來源的下一段，但銅纜段本十年末放緩、光學份額尚未證實。","reasoning":"成長組成：量為主（AI 機櫃出貨、半導體設備子系統）＋併購（XFS 2026 年 1 月、Interplex 2026 年 9 月）＋產品組合帶動毛利；無回購，反向有增資稀釋。共識三年 EPS：FY2025A 46.33 元→FY2028E 164.67 元，年化約 52.6%，前段集中在 FY2027（69.25→127.97，年增 85%）。缺口歸因：內生上界因投入資本缺資料無法計算；可歸因部分＝營益率擴張（FY2025 17.52%，Q2 2026 17.22%）與 Interplex 併入（過去 12 個月營收約 3.92 億美元，依 2026-10-09 匯率 31.912 約 125 億元，約占 2026 年營收一成三）；其餘無法歸因，信心上限中。跑道：滲透率事實表未涵蓋；永豐估 CPO 與 800V HVDC 在 2027～2028 年全面放量，為有來源的下一段，但 CEO 稱 XFS 需再看數季才下結論，所以跑道給中等而非寬。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi0_ifrs","f_kpi4_eps"],"verdict_values":{"growth":{"driver_mix":"量（AI 機櫃互連、半導體設備子系統）為主，併購（XFS、Interplex）次之，產品組合帶動毛利；股本增加抵銷部分每股成長","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與再投資率事實表未涵蓋，無法算內生上界；成長資金來自 GDR／ECB 增資與 8.5 億美元現金收購，而非內部現金（TTM FCF 率 5.4%），判定共識三年 EPS 年化約 53% 超出內生能力","segments":[{"item":"HPC 相關營收占比 2024","value":"約 18%（分析估計）"},{"item":"HPC 相關營收占比 2025","value":"約 35%（分析估計）"},{"item":"HPC 營收占比 2026E／2027E","value":"53%／75%（外資估，含 Interplex）"},{"item":"HPC 相關營收年增 2026E／2027E","value":"91%／40%（永豐投顧估）"},{"item":"半導體設備","value":"訂單能見度到 2027 下半年，客戶討論延伸到 2028（2026-08-21 財務長）"},{"item":"工業與車用","value":"逐步回升、各市場速度不一（管理層定性）"}],"decay_signals":["亮：EPS 成長遠高於營收成長，2025 年 EPS 年增約 96%、營收年增 31.7%，共識三年 EPS 年化約 53% 也高於營收成長","亮：替代技術壓縮銅纜 TAM，CRU 與 Gartner 都預期光學在 2020 年代後期擴大替代","半亮：FCF／淨利 FY2024 約 0.78、FY2025 約 0.54，TTM FCF 率 5.4%，尚未連 2 年低於 0.75","未亮：毛利率 Q2 回升到 30.73%，連 2 季年減無資料可證","未亮：核心份額縮減無確認數據，二供僅傳聞"]}}},"q4_capital":{"verdict":"資本配置偏弱：成長靠增資與現金收購撐，FCF 轉換率低，併購報酬尚無數字可驗證。","reasoning":"FCF／淨利：FY2022 約 0.14、FY2023 約 1.82、FY2024 約 0.78、FY2025 約 0.54（年度財報推算），TTM FCF 率 5.38%，遠低於 APH、TEL 約 17%。股東回報：trailing 殖利率 0.655%，回購紀錄事實表未涵蓋。2026 年以 GDR＋ECB 募資，歐系外資估每股盈餘稀釋約 6%～7%；以現金收購 Interplex（企業價值 8.5 億美元＋最高 5,000 萬美元或有價金），XFS 2026 年 1 月併入。管理層強調不為高需求預期擴產、報酬門檻不降，有機資本支出確實節制，但資金來源已轉向外部股本。營運槓桿：Q2 2026 營收年增 37%、淨利年增 47%，未見壓縮。SBC 數字事實表未涵蓋。","fact_refs":["f_peer_3665_tw_fcf_margin_pct","f_dividend_yield_ttm","f_kpi4_eps"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"事實表未涵蓋：XFS 與 Interplex 併入後的獲利與投入資本未揭露，Interplex 2026-09 才交割"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無回購可評，近期反向以 GDR 與 ECB 增資"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"GDR＋ECB 估每股盈餘稀釋 6%～7%（2026-07 歐系外資），遠高於每年 1.5% 上限"}]},"governance":{"capital_returns":[{"item":"股息","value":"trailing 12 個月殖利率 0.655%"},{"item":"回購","value":"事實表未涵蓋，無可引紀錄"},{"item":"增資","value":"GDR＋ECB，估每股盈餘稀釋 6%～7%（2026-07）"},{"item":"併購","value":"Interplex Datacom 企業價值 8.5 億美元現金（2026-09 交割，日期待核）；XFS 2026 年 1 月併入"},{"item":"自由現金流／淨利","value":"FY2024 約 0.78、FY2025 約 0.54"}]}}},"q5_valuation":{"verdict":"現價要求 2026～2027 年 EPS 照共識跳升、且銅背板在 2028 年前不被光學取代才算便宜；我信營收成長，不信共識 FY2027 EPS 年增 85%，以自己的基準估算只算合理。","reasoning":"現價 2,355 元，Fwd 本益比 34 倍（FY2026 共識 69.25 元），FY2027 共識 127.97 元下約 18.4 倍；共識三年 EPS 年化約 52.6%，PEG 約 0.65。但便宜論證建立在 FY2027 共識上：營收年增約四成＋Interplex 約一成三，扣掉 6%～7% 稀釋，要 EPS 年增 85% 需淨利率大幅跳升，法說沒有這樣的指引，所以本報告基準 FY2027 EPS 取 105 元，對應約 22 倍。trailing 本益比 43.3 倍、P/S 5.6 倍都在近四個年度端點的最高（只有四點，不是五年分位）。賣方 14 位全數買進、平均目標價約 3,203 元，現價低於最低目標價 2,450 元，市場本身已在打折。同業倍數事實表未涵蓋，終端倍數以自身現值與成長降速推，不跨同業錨定。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Fwd 本益比（FY2026 共識與本報告 FY2027 基準）為主，PEG 僅供對照","tier":"台系 AI 互連組件製造","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，未收同業倍數，無法建立同級倍數錨；終端倍數改以自身現值 34 倍與成長降速推導"},"fwd_pe":34.08,"peg":0.65,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價 2,355 元；Fwd 34 倍、以基準 FY2027 EPS 105 元計約 22 倍；PEG 0.65 建立在有爭議的共識分母上不採用；trailing 本益比在近四個年度端點最高（樣本不足五年，不填五年分位）；基準五年終端約 3,870 元、年化約一成→估值中性","upside_short_pct":11,"upside_mid_pct":38,"denominator_disputed":true,"denominator_note":"便宜論證（PEG 0.65、FY2027 本益比約 18 倍）依賴 FY2027 共識 EPS 年增 85%；營收成長、Interplex 規模與 6%～7% 稀釋推不出這個數字，共識另為美元快照換算，可能含口徑問題。本報告改用基準 105 元，短期以 FY2027 基準×25 倍、三年以 FY2029 基準 148 元×22 倍估算"}}},"q6_how_wrong":{"verdict":"價值陷阱風險中等：成長是真的，但每股經濟與現金轉換待驗，替代技術在後段等著。","reasoning":"依據見反證紀錄。衰退信號兩個亮、一個半亮：EPS 成長遠高於營收成長、替代技術壓縮銅纜市場、FCF／淨利 FY2025 約 0.54。股價 26 週只漲 6.77%、RSI 54.5，沒有動能過熱；歷史最大回撤事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_pe_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長真實，現金轉換與每股經濟待驗"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":69.25,"pe":34.01,"basis":"FY2026E 共識 EPS（Fwd 口徑）；終端倍數同樣乘在終端年度 EPS"},"eps":{"bull":[125,160,192,220,245],"base":[105,128,148,163,176],"bear":[78,72,80,88,96]},"pe":{"bull":28,"base":22,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.655,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-40,"basis":"事實表未收歷史最大回撤；以 Bear 終點跌幅約 −43%（96 元×14 倍）為下緣參照，再加上消化期估值與獲利同步下修：Bear 谷底 EPS 72 元×14 倍約 1,010 元，約 −57%；2025 年 Credo 二供傳聞曾讓股價跌停，顯示事件型下跌很快→範圍 −60%～−40%","trigger_time":null},"basis":{"bull":"AI 機櫃互連、800V HVDC 電源與 XFS 光學同時放量，Interplex 帶入機構件，FY2027 EPS 125 元接近共識但不追平，之後年增 12%～28%","base":"FY2027 EPS 105 元（營收約四成成長＋Interplex，扣 GDR／ECB 稀釋 6%～7%），之後成長率逐年降到約 8%；終端 22 倍反映成長降速","bear":"2027～2028 年 AI 資本支出消化＋Credo 二供分量＋scale-up 局部改光，EPS 回落到 70 多元再緩步回升，終點仍低於 FY2027 共識；本益比降到成長熄火的 14 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Credo 兩度傳出引進 AEC 二供；Rubin 伺服器採無線纜設計；CRU、Gartner 預期光學在 2020 年代後期取代銅；管理層兩場法說都提醒會有消化期","assumption":"AI 互連需求與貿聯份額在 2027～2028 年同時延續","consequence":"消化期遇上二供分量與局部改光，EPS 回落到 70 多元、本益比降到 14 倍，股價約 −43%～−57%","ruling":"採納，作為 Bear 情境 30% 機率；與唯一致命點部分重疊（架構改光），本條另補客戶二供與消化期兩個獨立來源","watch":"月營收年增率、Credo 對供應商的說法、NVIDIA 下一代平台 BOM","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#2","substitute_technology#0","substitute_technology#2"],"fact_refs":["f_kpi0_ifrs"]},{"view":"論點成功但股東經濟變差","evidence":"GDR＋ECB 估每股盈餘稀釋 6%～7%；以現金 8.5 億美元收購 Interplex；FCF／淨利 FY2025 約 0.54，TTM FCF 率 5.4%，APH、TEL 約 17%","assumption":"營收成長能完整轉成每股盈餘與自由現金流","consequence":"營收照預期成長，但股本擴大、併購報酬不明、現金被營運資金吃掉，每股價值成長落後營收","ruling":"採納，基準 FY2027 EPS 取 105 元而非共識 127.97 元，資本配置不給好評","watch":"Interplex 併入後營益率、季 EPS 年增與營收年增差、年度 FCF 率","evidence_refs":["major_events#2"],"fact_refs":["f_peer_3665_tw_fcf_margin_pct","f_peer_aph_fcf_margin_pct","f_peer_tel_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"trailing 本益比 43.3 倍、P/S 5.6 倍都在近四個年度端點最高；14 位分析師全數買進","assumption":"市場已把共識 FY2027 的爆發式成長全部計價","consequence":"若共識下修，倍數與 EPS 同時下修","ruling":"部分反駁：現價低於全部分析師最低目標價 2,450 元，26 週只漲 6.77%，以基準 105 元計約 22 倍，市場已對共識打折；但不足以稱便宜，估值判中性","watch":"共識 FY2027 EPS 修正方向、Q3 與 Q4 季 EPS","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2355.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2355.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率復原（管理層承諾對照）","cause":null,"prior_field":null,"side_a":"2026-05-12 法說，財務長 Charles Tsai 把 Q1 毛利率 28.77% 歸因於世代轉換、舊品價格正常化與新案爬坡，稱非長期軌跡改變","side_b":"Q2 毛利率回升到 30.73%、營益率 17.22%；但 2026-08-21 財務長要大家不要把毛利當成每季直線向上建模","ruling":"可調和：承諾已兌現一季，管理層同時降低續升預期；基準不假設毛利率超過 FY2025 的 31.73%","evidence_level":"實現數字＋管理層原話","settle_metric":"Q3 與 Q4 2026 季毛利率","if_then":["若 Q3、Q4 毛利率皆 ≥31%→基準 FY2027 EPS 上修至 115 元並可加碼","若任一季毛利率 <28.5%→停止加碼，連 2 季則減碼"],"evidence_refs":[]},{"axis":"Credo AEC 份額","cause":null,"prior_field":null,"side_a":"2025-02 與 2025-12 兩度傳出 Credo 引進第二家 AEC 供應商，股價一度跌停；公司與 Credo 皆未正式確認，也無出貨規模","side_b":"2026 年中歐系外資稱貿聯仍是 Credo AEC 與 ALC 主要供應商；9 月營收年增 39.2%、前 9 月年增 39.9%","ruling":"不可調和（份額方向相反），裁定採 B 側：營收加速是較硬的數據，傳聞無出貨規模；但二供傳聞本身代表議價權非獨家，定價面不給加分","evidence_level":"實現營收＋外資轉述 vs 媒體傳聞","settle_metric":"月營收年增率與 Credo 季報對供應商的說法","if_then":["若公司或 Credo 確認二供出貨且月營收年增連 2 月 <15%→減碼至半倉","若到 2027 年 6 月仍無二供出貨證據且月營收年增 ≥25%→維持點狀威脅判斷，可加碼至原定上限"],"evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#3"]},{"axis":"銅與光的替代時點","cause":null,"prior_field":null,"side_a":"CRU 預期銅雙絞線成長延續到本十年末後隨光學替代放緩；Gartner（2026-02）預期 CPO 約三年內成主流，銅在 224Gbps 遇到極限","side_b":"大摩分析 Rubin NVLink 背板仍用約 5,184 條被動銅纜；NVIDIA 稱 CPO 交換器 2026 下半年才小量部署、雲端 2026～2028 仍以可插拔為主；公司已有 448Gbps 銅纜與 XFS 光學","ruling":"不可調和在時點：2028 年前採 B 側（直接平台證據較多），2028 年後採 A 側風險，放入長期風險與 Bear 30%；公司光學能否接住尚無營收數字（CEO 2026-05-12 稱需再看數季）","evidence_level":"產業研究機構 vs 平台 BOM 分析與公司產品","settle_metric":"NVIDIA 下一代機櫃 scale-up 互連架構發表","if_then":["若 NVIDIA 正式宣布下一代 scale-up 背板改光學→減碼至半倉並重跑研究","若 Kyber 確認延至 2028 下半年且沿用銅背板→上修基準 FY2029～FY2030 EPS，維持持有"],"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","supply_demand_durability#3","supply_demand_durability#4","competitive_share_entrants#2"]},{"axis":"共識 FY2027 EPS 可達性","cause":null,"prior_field":null,"side_a":"賣方共識 FY2027 EPS 127.97 元，較 FY2026 的 69.25 元年增 85%；14 位分析師全數買進，平均目標價約 3,203 元","side_b":"營收成長約四成＋Interplex 約一成三，且 GDR／ECB 稀釋每股盈餘 6%～7%；要 EPS 年增 85% 需淨利率大幅跳升，法說無此指引","ruling":"不可調和，採 B 側：基準 FY2027 EPS 105 元，便宜論證不採用；現價已低於最低目標價，市場本身也在打折","evidence_level":"共識快照 vs 實現營收與稀釋估計","settle_metric":"Q4 2026 季 EPS（2027 年 3 月公布）","if_then":["若 Q4 2026 季 EPS ≥22 元且毛利率 ≥31%→基準上修至共識並加碼","若 Q3 2026 季 EPS <16 元→基準下修至 95 元並停止加碼"],"evidence_refs":["major_events#2","capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"資本紀律說法對照實際資金來源","cause":null,"prior_field":null,"side_a":"管理層兩場法說都強調不為高需求預期擴產、資本支出看能見度、資金變多不降低報酬門檻","side_b":"2026 年以 GDR＋ECB 募資並以現金 8.5 億美元收購 Interplex；TTM FCF 率 5.4% 遠低於 APH、TEL","ruling":"可調和（程度差異）：有機擴產確實節制，但成長資金已轉向外部股本；Interplex 報酬要等併入後四季才能驗證，在那之前資本配置不給好評","evidence_level":"管理層原話 vs 已公告交易與現金流","settle_metric":"Interplex 併入後四季合併營益率與 FCF 率","if_then":["若併入後四季營益率 ≥17% 且 FCF 率回到 ≥7%→資本配置上調一級","若併入後兩季合併營益率 <15%→減碼至七成"],"evidence_refs":["major_events#0","major_events#1","ma_merger#0","ma_merger#1","major_events#2"]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：營收前 9 月年增四成、Q2 獲利創新高、半導體設備能見度到 2027 下半年；股價半年只漲 6.8%、低於全部分析師最低目標價，FY2027 只做到基準 105 元也只有 22 倍","side_b":"現在就賣：共識把 2027 年 EPS 估到年增 85% 本身就是下修風險，trailing 本益比在近四年端點最高，管理層連兩季提醒消化期，二供與銅被光替代都落在 2027～2028 年","ruling":"兩邊都成立：基準五年年化約一成，不追高也不放空，依觸發器分批","evidence_level":"實現數字＋共識＋管理層原話","settle_metric":"Q4 2026 季 EPS 與月營收年增率","if_then":["若股價回到 2,000 元以下且月營收年增仍 ≥25%→分批反買","若股價高於 3,360 元而基準 EPS 未上修→減碼三分之一"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸惡化中：大廠擴展 AI 互連、電源與光學產品線，Credo 傳二供","side_b":"結構軸轉好中：AI 部署延伸到電力與互連，800V HVDC 與半導體設備子系統擴大；替代技術軸在 2028 年後成形；關稅屬背景未點名公司","ruling":"雙向拉鋸：2028 年前結構轉好的力量大於競爭惡化，2028 年後替代技術主導","evidence_level":"管理層原話＋外資估計＋產業研究","settle_metric":"HPC 營收占比與月營收年增率","if_then":["若 2027 年 HPC 占比 <60%→下修跑道判斷並停止加碼","若 HPC 占比 ≥70% 且營益率 ≥17%→維持持有並可加碼"],"evidence_refs":["end_markets#1","end_markets#2","reg_tariff_export#0","reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"月營收累計年增率跌破 25%，連 2 個月","type":"假設驗證","maps_to":"H1","metric":"月營收累計年增率","threshold":"<25% 連 2 個月","action":"停止加碼","source_freq":"公司月營收公告，每月","date":null,"evidence_refs":[]},{"n":2,"text":"季毛利率 <28.5% 或季營益率 <15%，連 2 季","type":"假設驗證","maps_to":"H2","metric":"季毛利率／季營益率","threshold":"毛利率 <28.5% 或營益率 <15% 連 2 季","action":"減碼","source_freq":"季報，每季","date":null,"evidence_refs":[]},{"n":3,"text":"公司或 Credo 確認二供出貨，且月營收年增連 2 月 <15%","type":"風險","maps_to":"R1","metric":"二供確認＋月營收年增率","threshold":"確認二供且月營收年增 <15% 連 2 月","action":"減碼至半倉","source_freq":"重大訊息、Credo 季報、月營收","date":null,"evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"n":4,"text":"NVIDIA 正式宣布下一代機櫃 scale-up 背板改光學","type":"Single Thing","maps_to":"Single Thing","metric":"NVIDIA 平台架構發表","threshold":"官方宣布背板改 CPO／NPO","action":"減碼至半倉並重跑研究","source_freq":"GTC（每年 3 月）、Computex（6 月）、供應鏈 BOM 報告","date":"2027-03","evidence_refs":["substitute_technology#2","customer_second_source#2"]},{"n":5,"text":"Interplex 併入後兩季合併營益率 <15%，或季 EPS 年增落後營收年增超過 10pp","type":"風險","maps_to":"R4","metric":"合併營益率／EPS 與營收年增差","threshold":"營益率 <15% 或落差 >10pp，連 2 季","action":"減碼","source_freq":"季報，每季","date":"2027-05","evidence_refs":["major_events#2"]},{"n":6,"text":"月營收年增連 3 個月 <10%，消化期確認","type":"風險","maps_to":"R5","metric":"單月營收年增率","threshold":"<10% 連 3 個月","action":"減碼","source_freq":"公司月營收公告，每月","date":null,"evidence_refs":[]},{"n":7,"text":"股價回到 2,000 元以下且月營收累計年增仍 ≥25%","type":"估值rearm","maps_to":"估值","metric":"股價＋月營收累計年增率","threshold":"≤2,000 元且年增 ≥25%","action":"分批反買","source_freq":"每日股價、每月營收","date":null,"evidence_refs":[]},{"n":8,"text":"股價高於 3,360 元（基準 FY2027 EPS 的 32 倍）而基準 EPS 未上修","type":"減碼","maps_to":"估值","metric":"股價對基準 FY2027 EPS 倍數","threshold":">32 倍","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"Q4 2026 財報與首個完整 Interplex 併表季後複審","type":"複審日期","maps_to":"H1/H2/R4","metric":"季 EPS、毛利率","threshold":"Q4 季 EPS ≥22 元上修基準；<16 元下修","action":"重跑研究","source_freq":"季報","date":"2027-03","evidence_refs":[]}],"kill_metrics":[{"metric":"月營收累計年增率","bear_threshold":"連 3 個月 <10%","window":"2026-11 至 2027-12","source":"公司月營收公告（公開資訊觀測站）","last_status":"ok"},{"metric":"季營益率","bear_threshold":"<13% 連 2 季","window":"2026Q4 至 2027Q4","source":"公司季報","last_status":"ok"},{"metric":"年度自由現金流／淨利","bear_threshold":"FY2027 <0.5","window":"FY2027 年報","source":"年報現金流量表","last_status":"warning"},{"metric":"NVIDIA 下一代機櫃 scale-up 互連材質","bear_threshold":"官方宣布背板改光學","window":"2027-03 至 2028-06","source":"NVIDIA GTC／Computex 發表、供應鏈 BOM 報告","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價 ≤2,000 元且月營收累計年增 ≥25%，或 Q4 2026 季 EPS ≥22 元證實共識","exec_line":"不追高；現價可依基準年化約一成持有，股價回到 2,000 元以下且成長未破才分批加碼；二供確認或背板改光學即減碼至半倉；路徑回撤可能達 −60%，論點完整時不因波動砍倉，需有深回撤心理準備"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 2,000 元以下，且月營收累計年增率仍 ≥25%（與加碼觸發器第 7 條相同）"},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=6.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"AI 機櫃互連與電源需求讓營收維持三成以上成長，2027 年併入 Interplex 後更高","2y":"2027 全年營收年增 ≥30%（含 Interplex）","5y":null,"10y":null,"threshold":"月營收累計年增率 ≥25%；2027 全年 ≥30%","source":"公司每月營收公告、季報","drift_rule":"2 年期：TTM 營收成長偏離門檻連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H2","text":"毛利率與營益率在世代轉換與併購整合期間守住 Q2 2026 水準，規模放大讓每股獲利跟上營收","2y":"2027 年季毛利率維持 ≥28.5%、季營益率 ≥15%","5y":null,"10y":null,"threshold":"季毛利率 ≥28.5% 且季營益率 ≥15%","source":"季報、法說會","drift_rule":"2 年期：連 2 季偏離 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H3","text":"銅、電源、光學三條線並行，讓公司在銅被光替代的轉換中保住每櫃內容價值","2y":null,"5y":"HPC 營收占比 2027 年 ≥60%，2028 年起光學與電源成長抵銷銅纜放緩","10y":null,"threshold":"HPC 營收占比 2027 年 ≥60%；光學（XFS）營收有季度揭露且年增為正","source":"法說會、外資報告、年報產品別營收","drift_rule":"5 年期：連 4 季偏離 ≥5% 為削弱、連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"Credo 的 AEC 二供分走份額","h_ref":"H1","clock":"⚡","threshold":"公司或 Credo 確認二供出貨，且月營收年增連 2 月 <15%","evidence_refs":["customer_second_source#0","customer_second_source#1"]},{"id":"R2","text":"NVIDIA 平台設計減少線纜內容（運算托盤無線纜化、背板份額重分）","h_ref":"H3","clock":"🔥","threshold":"下一代平台每櫃銅纜條數較 GB300 世代減少 ≥30%（供應鏈 BOM）","evidence_refs":["customer_second_source#2"]},{"id":"R3","text":"光學／CPO 在 scale-up 取代銅，公司光學份額接不住","h_ref":"H3","clock":"🐢","threshold":"CPO 在 scale-up 量產部署，且公司 HPC 營收年增連 4 季 <10%","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R4","text":"增資稀釋與 Interplex 整合拉低每股獲利","h_ref":"H2","clock":"🔥","threshold":"併入後兩季合併營益率 <15%，或季 EPS 年增落後營收年增 >10pp","evidence_refs":["major_events#2"]},{"id":"R5","text":"AI 資本支出進入消化期，客戶部署時點延後（管理層 2026-08-21 自述會發生）","h_ref":"H1","clock":"⚡","threshold":"單月營收年增連 3 個月 <10%","evidence_refs":[]}],"single_thing":{"description":"NVIDIA 正式宣布下一代機櫃（Rubin Ultra／Kyber）的 scale-up 背板改用光學（CPO／NPO），不再用被動銅纜","why_fatal":"銅背板與 AEC 是 HPC 營收中份額最穩、毛利最好的一塊，外資估 HPC 占比 2027 年達 75%；背板一改光，公司從主要供應商變成光學後進者，FY2028 起 EPS 路徑整段下移，終端倍數同步壓縮，是情境樹裡敏感度最大的單一變數","if_happens":"減碼至半倉並重跑研究；只有在 XFS 拿到同代光學背板訂單證據時才回補","how_monitor":"NVIDIA GTC（每年 3 月）與 Computex（6 月）發表、供應鏈 BOM 報告、公司法說對銅背板世代的說法","probability":"約 20%（12～24 個月）：Rubin 背板仍用約 5,184 條銅纜、NVIDIA 稱 2026～2028 雲端仍以可插拔光模組為主；但 Gartner 預期 CPO 約三年內成主流，Kyber 若延後反而延長銅的壽命"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.4,"peg_fy2":0.64,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":46.33,"FY2026E":69.25,"FY2027E":127.97,"FY2028E":164.67},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS；共識為 Koyfin 美元快照依 2026-10-09 匯率 31.912 換算新台幣"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說，首次反映 GDR 稀釋與 Interplex 一週併表","impact":"高","watch":"毛利率是否 ≥30%、季 EPS 是否 ≥16 元"},{"date":"2026-11","date_precision":"month","type":"other","event":"10 月營收，首個完整併入 Interplex 的月份","impact":"中","watch":"月營收年增率與 Interplex 貢獻規模"},{"date":"2027-03","date_precision":"month","type":"product","event":"NVIDIA GTC 2027，下一代機櫃 scale-up 互連架構","impact":"高","watch":"背板是否仍用銅纜、CPO 部署時程"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"Q4 2026 財報，檢驗共識 FY2027 EPS 可達性","impact":"高","watch":"季 EPS 是否 ≥22 元、FCF 率"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
