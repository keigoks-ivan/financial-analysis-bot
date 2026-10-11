你是 DD 管線 v20 的判斷層閘（gate），標的 6805.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（29 條）
- `f_kpi0_ifrs`（q1_business）｜營收（IFRS 合併）＝3739.7 NT$ 百萬｜期間與口徑：Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt＋CNA 2026-08-04（季減 10.61%、年增 42.75%）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi1`（q1_business）｜毛利率＝34.05 %｜期間與口徑：Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：CNA 2026-08-04；yfinance 毛利 NT$1,273.2 百萬交叉驗證（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi2_ifrs_non_gaap_gaap`（q1_business）｜營業利益（IFRS，台股無 Non-GAAP 口徑，GAAP 即報表值）＝1040.3 NT$ 百萬｜期間與口徑：Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（上半年累計 NT$2,164 百萬與 Q1 1,123.3＋Q2 1,040.3 吻合）（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi3`（q1_business）｜營業利益率＝27.82 %｜期間與口徑：Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：營業利益 ÷ 營收（yfinance 數字計算）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi4_eps`（q1_business）｜稅後純益／EPS＝12.39 NT$/股（純益 NT$849 百萬）｜期間與口徑：Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：CNA 2026-08-04（純益季減 7.42%、年增約 1.57 倍；yfinance diluted EPS 12.37）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi7`（q1_business）｜管理層指引（無數字區間）＝定性：下半年優於上半年；Q3 起多項 AI 伺服器滑軌新專案（NVIDIA／ASIC，含 AWS Trillium）量產；全年毛利率隨伺服器占比續升、費用率下降 定性｜期間與口徑：Q2 2026 法說（媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：CNA 2026-08-04；富果研究 https://blog.fugle.tw/post/earnings-call-6805-2026-08-04（AI 摘要，待原始簡報核對）（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026 法說（媒體報導日 2026-08-04））
  - 註記：查無
- `f_kpi8`（q1_business）｜產能（滑軌／快接頭）＝滑軌 35 萬組/月；QD 快接頭 300 萬件/月（近滿載）；Q3 稼動率預期大升 組或件/月｜期間與口徑：Q2 2026 法說（媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：富果研究 2026-08-04 法說摘要（AI 摘要，待原始簡報核對）（numbers.latest_quarter_kpis.items[8]，as_of Q2 2026 法說（媒體報導日 2026-08-04））
  - 註記：不適用
- `f_kpi9`（q1_business）｜營收結構（上半年）＝伺服器 55.7%（去年同期 19.2%）／折疊機 38%（71%）／筆電 5.6%（8.9%） %｜期間與口徑：2026 上半年（媒體報導日 2026-08-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：CNA 2026-08-04；富果研究 2026-08-04（numbers.latest_quarter_kpis.items[9]，as_of 2026 上半年（媒體報導日 2026-08-04））
  - 註記：不適用
- `f_peer_6805_tw_gross_margin_pct`（q2_moat）｜6805.TW 毛利率＝30.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6805.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6805_tw_operating_margin_pct`（q2_moat）｜6805.TW 營業利益率＝24.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6805.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6805_tw_fcf_margin_pct`（q2_moat）｜6805.TW FCF 利潤率＝25.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6805.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_gross_margin_pct`（q2_moat）｜3017.TW 毛利率＝28.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_gross_margin_pct`（q2_moat）｜3324.TWO 毛利率＝27.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_gross_margin_pct`（q2_moat）｜3653.TW 毛利率＝42.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8996_tw_gross_margin_pct`（q2_moat）｜8996.TW 毛利率＝27.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8996.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流−資本支出）＝1561.7 NT$ 百萬｜期間與口徑：Q2 2026（季末 2026-06-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營業現金流 1,583.7、資本支出 21.9；上半年 FCF 1,994 與法說摘要吻合）（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30））
  - 註記：查無
- `f_kpi6_sbc`（q4_capital）｜SBC 占營收＝0.0 %｜期間與口徑：Q2 2026（季末 2026-06-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow SBC=0（Q1 僅 NT$2.5 百萬，可忽略）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.527 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝9.93 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝10.51 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝2370.0 USD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝50.73 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝29.71 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.49｜期間與口徑：2026-10-08（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝1717.33 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w250`（q5_valuation）｜250 週均線＝731.59 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）

### findings_digest 中方向為負或來源衝突的條目（4 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：蘋果折疊iPhone鉸鏈供應鏈報導顯示供應商為新日興與Amphenol（美商安菲諾），新日興為主供；富世達未列於該報導的蘋果鉸鏈供應商名單。
  - 來源：經濟日報／聯合新聞網 money.udn.com 與供應鏈報導（搜尋摘要）（as_of 2026-03-06）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：2026Q1折疊手機占營收降至37.7%（去年同期73.5%），公司表示未承接華為Pure S系列鉸鏈訂單；伺服器產品占比升至56.4%成最大營收來源。
  - 來源：富果投研 法說會整理（2026-05-05）／ctee 報導（as_of 2026-05-05）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：富世達鉸鏈占營收約85%，為陸系品牌高階折疊機供應關鍵；3月營收受陸系客戶折疊新機訂單帶動。報導未揭露個別客戶名稱或占比。
  - 來源：Yahoo奇摩股市《陸系訂單旺 富世達、兆利寫最強Q1》（as_of 2025-04-10）｜affects：decision_inputs.bear、thesis.R
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：大和列出下行風險含主要客戶市占率、摺疊手機滲透率不如預期
  - 來源：經濟日報／大和報告（as_of 2026-08-05）｜affects：decision_inputs.bear、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":4816,"bear_5y_price":840,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":11.4,"ev5y_pct":11.6,"irr_base_pct":2.2,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":46.72,"pe":50.73,"basis":"TTM 至 2026-06-30 稀釋 EPS（股價 2,370 元÷trailing 本益比 50.73 倍回推），終端倍數同為 trailing 口徑"},"eps":{"bull":[70,112,138,158,172],"base":[66,90,106,114,120],"bear":[60,70,58,52,56]},"pe":{"bull":28,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.527,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 3 | 3 |
| customer_concentration_credit | found | 1 | 4 |
| supply_demand_durability | found | 5 | 2 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | none | 0 | 3 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | none | 0 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：6805.TW 富世達 antitrust OR regulation OR regulatory scrutiny 2026；富世達 6805 公平會 OR 反壟斷 OR 調查 OR 法規 2026
- **reg_tariff_export**（none）：6805.TW 富世達 tariff section 232 2026；富世達 6805 關稅 出口管制 2026；Fositek hinge tariff OR export control OR China 2026 富世達 關稅 影響
- **major_events**（none）：6805.TW 富世達 acquisition merger 2025 2026；6805.TW class action lawsuit securities fraud 訴訟；6805.TW clinical trial FDA approval 2025 2026；6805 台股 product recall warning letter 召回；6805.TW SEC investigation restatement 重編 調查

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"6805.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"富世達"},"oneliner":"富世達把鉸鏈工藝移植到 AI 伺服器滑軌與液冷快接頭，上半年伺服器已占營收 55.7%，2027 年產能倍增；但現價為 trailing 本益比 50.73 倍、約 FY2026 共識 EPS 的 36 倍，已貼近賣方平均目標價，Base 五年報酬約一成，等回落再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6805.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 伺服器機櫃與折疊機品牌的精密機構件錢：滑軌、液冷快接頭與鉸鏈按件出貨，利潤卡在平台換代時能否被選進供應商名單、以及產能能否及時到位；伺服器已占上半年營收 55.7%，成為主引擎。","reasoning":"營收分部（2026 上半年）：伺服器（滑軌＋液冷快接頭）55.7%、折疊機鉸鏈 38%、筆電 5.6%，去年同期分別為 19.2%、71%、8.9%。以上半年營收 79.24 億元（年增 62.64%）回推去年同期約 48.72 億元，伺服器營收約 44.1 億元、約為去年同期 9.4 億元的 4.7 倍；折疊機約 30.1 億元，對去年同期約 34.6 億元年減約 13%。最新一季（Q2 2026）營收 37.40 億元、季減 10.61%，毛利率 34.05%、營業利益率 27.82%，EPS 12.39 元；營收下滑時毛利率仍季增 1.74 個百分點，說明伺服器組合在拉高毛利。錢卡在兩個節點：一是 NVIDIA 與 ASIC 平台換代時能否入選，二是產能能否到位（滑軌 35 萬組／月、快接頭 300 萬件／月且近滿載）。產業時鐘判 II（擴張）：快接頭近滿載、第三季起多項新專案投產、2027 年產能規劃倍增，依據是供需而非股價。單點依賴：集中度沒有消失，只是由陸系折疊機品牌換到 AWS 與 NVIDIA 主導的平台；法人估第三季伺服器占比升至 8 成以上，單一平台落選的衝擊因此放大。管理層指引只有定性（下半年營收與毛利率優於上半年、費用率下降），沒有數字區間；最新一季逐字稿未收錄，無法對照管理層前後說法。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_non_gaap_gaap","f_kpi3","f_kpi4_eps","f_kpi7","f_kpi8","f_kpi9"],"verdict_values":{"revenue_quality":"按件出貨的專案型收入，能見度約一個平台世代；沒有經常性收入，伺服器線跟著雲端資本支出走，折疊機線跟著品牌新機週期走。","unit_econ_note":"Q2 毛利率 34.05%、營業利益率 27.82%，高於 2025 年全年的 26.34% 與 20.23%；單價與出貨量的拆分事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 資本支出與折疊機新機兩個產品週期疊加的精密機構件廠，擴產期毛利率與營業槓桿同步放大"},"industry":{"clock_phase":"II","sd_verdict_source":"供需持久性判為週期性：需求是雲端資本支出的衍生需求，供給端公司自身 2027 年產能倍增、滑軌三強同步擴產，供給可逆性高；依據為 2026 年 8 月法說產能規劃與滑軌擴產報導。","bargaining":{"up":"上游原物料與加工環節的議價事實表未涵蓋。","down":"下游是 NVIDIA 主導的 GPU／ASIC 平台與雲端業者，平台定案權在客戶手上，買方集中度高。","geo":"以中國生產為主，越南廠擴產滑軌與快接頭，目的之一是降低單一地區依賴。"},"profit_pool_dir":"利潤池由消費性折疊機轉向 AI 伺服器機構件，伺服器占比一年內由 19.2% 升至 55.7%。","tam_table":[{"item":"折疊機出貨（2025）","value":"約 1,830 萬支，占手機市場 1.6%"},{"item":"折疊機成長（Counterpoint，2026-09）","value":"全球累計出貨 2026 年底破 1 億支，2027 年出貨年增 37%，預期蘋果 2026 年占 25%"},{"item":"蘋果折疊 iPhone","value":"IDC 預估 2027 年逾 1,700 萬支；Mizuho 稱鉸鏈與面板設計未定，上市可能延至 2027；公司未列鉸鏈供應商"},{"item":"AI 伺服器滑軌與液冷快接頭的 TAM、滲透率與利潤池占比","value":"事實表未涵蓋；滑軌台灣三強為川湖、南俊、富世達，無權威市占統計"}]}}},"q2_moat":{"verdict":"護城河方向不變（→）、等級 C：伺服器線的平台導入在擴大，折疊機在最大客戶與蘋果的份額在縮，滑軌只排第三；毛利率走高主要來自產品組合與快接頭供給吃緊，不是定價權。","reasoning":"機制：把折疊機鉸鏈的精密機構件工藝延伸到伺服器滑軌與液冷快接頭，靠平台認證與越南自動化產能卡位。對同業的 ROIC 利差無法計算（投入資本事實表未涵蓋），改看份額方向與利潤率：TTM 毛利率 30.38%、營業利益率 24.27%，毛利率高於 3017、3324、8996，低於 3653；FCF 利潤率 25.6% 為同業對照中最高。份額方向分兩邊：伺服器線擴大（AWS 第二季起出貨、NVIDIA／ASIC 多項滑軌專案第三季起投產）；折疊機線縮減（華為 Pure S 未承接、蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭，上半年折疊機營收估年減約 13%）。領先玩家在最大客戶的份額下滑，方向不能判擴大，兩邊相抵判 →。評分：執行力 7，一年內把伺服器占比由 19.2% 拉到 55.7%、滑軌產能由 7～8 萬套擴到 35 萬套，扣分在折疊機丟掉華為 Pure S；定價力 5，滑軌排第三、折疊機份額流失、快接頭毛利靠近滿載的供給吃緊撐住。合併約 6，等級 C。架構替代：浸沒式液冷建置成本高數倍、機構需重新設計，部分品牌廠偏好水循環，現有證據不支持列為架構替代；折疊機摺痕改善轉向 UTG 與面板堆疊的材料協同設計，不是替換鉸鏈本身。","fact_refs":["f_peer_6805_tw_gross_margin_pct","f_peer_6805_tw_operating_margin_pct","f_peer_6805_tw_fcf_margin_pct","f_peer_3017_tw_gross_margin_pct","f_peer_3324_two_gross_margin_pct","f_peer_3653_tw_gross_margin_pct","f_peer_8996_tw_gross_margin_pct","f_kpi1","f_kpi5"],"verdict_values":{"moat":{"mechanism":"精密機構件工藝由鉸鏈延伸到伺服器滑軌與液冷快接頭，加上每一代平台的認證資格與越南自動化產能；轉換成本只存在於單一平台生命週期內。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：AWS 第二季起出貨、多項 NVIDIA／ASIC 滑軌專案第三季起投產、伺服器占比一年由 19.2% 升至 55.7%。定價面縮減：折疊機最大客戶的 Pure S 專案未承接、蘋果鉸鏈名單未列、滑軌僅排第三。最大客戶份額下滑，方向不能判擴大，兩邊相抵判 →。","competitor_notes":[{"name":"川湖","strategy_note":"伺服器滑軌龍頭，規模與客戶廣度都在富世達之上；富世達的滑軌份額要從它與南俊手上搶。"},{"name":"南俊","strategy_note":"滑軌第二，規模大於富世達；同樣在擴產，是 2027 年後滑軌報價壓力的來源之一。"},{"name":"新日興","strategy_note":"蘋果折疊 iPhone 鉸鏈主供，折疊機最大增量被它拿走，富世達未列入名單。"},{"name":"Amphenol（安菲諾）","strategy_note":"蘋果折疊機鉸鏈的另一競爭者，連接器大廠的資本與客戶關係都比富世達深。"},{"name":"3017.TW","strategy_note":"毛利率與營業利益率和富世達相近，同屬吃液冷順風的台廠；對照表只能比利潤率，無法比快接頭份額。"},{"name":"3324.TWO","strategy_note":"毛利率接近但自由現金流為負，擴產吃現金；富世達的現金轉換明顯較好。"},{"name":"3653.TW","strategy_note":"毛利率與營業利益率都高於富世達，是液冷相關零組件裡定價力較強的參照。"},{"name":"8996.TW","strategy_note":"營業利益率與自由現金流利潤率都低於富世達，規模化的散熱方案未轉成更高獲利。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用份額方向與利潤率對照。","threats":[{"level":"🟡","text":"折疊機鉸鏈份額被新日興與 Amphenol 分走：華為 Pure S 未承接、蘋果折疊 iPhone 鉸鏈名單未列，折疊機最大增量不在手上。","p":0.5,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"伺服器滑軌排第三，川湖與南俊同步擴產，2027 年後滑軌報價可能下修。","p":0.35,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"液冷快接頭目前近滿載、毛利靠供給吃緊；公司自身 2027 年產能倍增，若其他液冷零組件廠跟進，單價與毛利率回落（快接頭市占統計事實表未涵蓋）。","p":0.4,"evidence_refs":["supply_demand_durability#0"]}],"roic_durability":{"quadrant":"高營業利益率（TTM 24.27%）×周轉率不明（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心機櫃，決策者是 GPU／ASIC 平台與伺服器設計團隊，付款者是雲端業者與代工廠，三者都成立；液冷機櫃一定要用滑軌與快接頭，屬需要而非想要。但這是雲端資本支出的衍生需求，急迫性高不等於持久，2028 年後的需求事實表未涵蓋。"},{"item":"決策層級","level":"🟡","text":"替代性在平台世代這個最小單位決定：每一代 NVIDIA／ASIC 平台都要重新驗證，AWS 第二季才開始出貨，其他 ASIC 客戶仍在驗證。滑軌有三家台廠可選，客戶多源採購，轉換成本只在單一平台生命週期內有效。"},{"item":"價值鏈分配","level":"🟡","text":"價值大部分落在 GPU 與 ASIC 端，滑軌與快接頭占機櫃成本的比例事實表未涵蓋；買方高度集中，客戶握有定案權。目前 34% 的毛利率靠快接頭近滿載的供給吃緊，產能倍增後分配可能回到買方。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的機構件，沒有消費者或政策對價格的容忍上限，也不依賴監管授權；外部約束主要是地緣，越南擴產用來降低中國單一地區依賴，關稅與出口管制未見相關報導。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋（Q2 資本支出僅 0.22 億元、營業現金流 15.84 億元，淨再投資接近零，公式不適用）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；投入資本、折舊與營運資金變動事實表未涵蓋，無法計算。可觀察的代理：TTM 自由現金流利潤率 25.6% 高於營業利益率 24.27%，成長目前由內部現金支應。"}}}},"q3_growth":{"verdict":"五年後的跑道判黃燈（🟡）：折疊機滲透率只有 1.6%，但公司不在蘋果鉸鏈名單；伺服器線靠 2027 年產能倍增撐到 2028 年，之後看雲端資本支出，第二條曲線（CPO 產品）只有法人說法。","reasoning":"成長來源是量與組合：AI 伺服器滑軌與快接頭出貨放量、產能擴張，毛利率隨伺服器占比上升；沒有併購，也沒有回購。三年共識 EPS 成長率無法計算：只有 FY2026 共識中位數 66.17 元（FactSet 9 家，2026-07 報導），FY2027／FY2028 共識事實表未涵蓋。Base 路徑 FY2025A 30.98 元→FY2028E 106 元，年化約 50.7%，主要來自 2026 至 2027 年的放量；FY2026E→FY2029E 年化約 20%。內生天花板缺投入資本資料無法量化，缺口無法計算，但成長可歸因於產能擴張的量與組合，不靠收購或回購；長期信心上限取中。跑道：折疊機滲透率 1.6% 很低，但最大增量（蘋果）不在手上、華為 Pure S 未承接；伺服器線滲透率事實表未涵蓋，管理層稱 2027 年成長最高的是快接頭，其次滑軌與手機；法人提到 CPO 產品 2027 年貢獻營收，未見規模數字，不算已證實的第二條曲線。衰退信號亮 2 個：折疊機核心份額縮減、EPS 成長顯著高於營收成長，長期成長性判黃燈。","fact_refs":["f_kpi9","f_kpi8","f_kpi7","f_kpi0_ifrs"],"verdict_values":{"growth":{"driver_mix":"量為主（伺服器滑軌與快接頭出貨、產能擴張），組合為輔（伺服器占比拉高毛利率）；無併購、無回購。","runway_years":"事實表未涵蓋（液冷與滑軌滲透率無資料，無法換算）","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法計算：增量 ROIC 與再投資率所需的投入資本、折舊、營運資金事實表未涵蓋。代理證據顯示成長由內部現金支應（Q2 營業現金流 15.84 億元、資本支出 0.22 億元），Base 路徑 FY2025A→FY2028E EPS 年化約 50.7% 主要來自產能擴張的量與組合；是否超過天花板無法裁定。","segments":[{"item":"伺服器（滑軌＋液冷快接頭）","value":"上半年占 55.7%（去年同期 19.2%），營收約為去年同期的 4.7 倍；法人估第三季占比升至 8 成以上"},{"item":"折疊機鉸鏈","value":"上半年占 38%（去年同期 71%），營收估年減約 13%"},{"item":"筆電","value":"上半年占 5.6%（去年同期 8.9%）"}],"decay_signals":[{"item":"核心市占近 12 個月縮減","lit":true,"note":"折疊機：華為 Pure S 未承接、蘋果鉸鏈名單未列，上半年折疊機營收估年減約 13%"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"2025 年 EPS 年增約 73%（30.98 元對 17.89 元），營收年增 51.62%，差逾 5 個百分點，屬擴產期營業槓桿"},{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 毛利率 34.05%，高於 2025 年全年 26.34%"},{"item":"自由現金流÷淨利＜0.75 連 2 年","lit":false,"note":"2024 年約 0.70、2025 年約 0.77，未連兩年；Q2 2026 約 1.84"},{"item":"SBC 占營收＞5% 且逐年上升","lit":false,"note":"約 0%"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置以自有現金擴產，不靠併購也沒有股權稀釋，現金轉換好；但回購與現金去向事實表未涵蓋，可見的股東回報只有約 0.5% 的股息。","reasoning":"自由現金流÷淨利：2022 年約 3.9（22.08 億元÷5.64 億元）、2023 年約 1.62、2024 年約 0.70（擴產期）、2025 年約 0.77（16.42 億元÷21.25 億元），Q2 2026 約 1.84（15.62 億元÷8.49 億元）。SBC 占營收約 0%，稀釋 EPS 12.37 元對基本 12.39 元，稀釋可忽略。EV/S 9.93 倍低於 P/S 10.51 倍，表示帳上為淨現金。營運槓桿為正：2025 年營業利益年增約 109%，高於營收年增 51.62%。近三年現金去向四分、債務結構與回購均價事實表未涵蓋；事件掃描未見併購。","fact_refs":["f_kpi5","f_kpi6_sbc","f_dividend_yield_ttm","f_ev_s_current","f_ps_current","f_peer_6805_tw_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事件掃描未見併購紀錄，成長來自自有產能擴張"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購紀錄事實表未涵蓋；可見的股東回報只有股息，殖利率 0.527%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收約 0%（Q2 2026），Q1 僅約 250 萬元；稀釋 EPS 12.37 元對基本 12.39 元"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能擴張而非併購，股東回報可見部分只有股息（殖利率約 0.5%），近三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2030E EPS 約 173 元、且屆時仍給 22 倍，才換得到一成年化報酬，等同 Bull 路徑；我信成長、不信倍數撐得住，結論是偏貴、等價格。","reasoning":"trailing 本益比 50.73 倍、P/S 10.51 倍、EV/S 9.93 倍，都在可得 4 個年度端點的最高位置；前瞻本益比約 35.8 倍（2,370 元÷FY2026 共識 66.17 元）。賣方：8 位分析師全為買進，平均目標價兩份快照約 2,391 元與 2,594 元，FactSet 目標價 2,600 元，現價只差約 9.7%。Base 五年終值約 2,640 元（120 元×22 倍），比現價高約 11.4%，年化不到 3%；反推一成年化報酬需要約 3,817 元，以 22 倍計要 FY2030E EPS 約 173 元。PEG 以 FY2026E→FY2029E 年化約 20% 計約 1.8；若用 FY2025A 低基期算三年成長會壓到約 0.7，那是週期高成長期的假便宜，不採用。26 週漲 29.71%，RSI 54.49 未過熱，股價在 52 週均線 1,717 元之上約 38%。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14","f_ma_w52"],"verdict_values":{"valuation":{"basis":"trailing 本益比與 FY2026 共識前瞻本益比為主尺，PEG 輔助；循環屬性以獲利正常化後的終端倍數校驗。","peers":{"expanded":false,"reason":"同業本益比與目標價事實表未涵蓋，同業對照只有利潤率，無法當倍數錨；終端倍數改以成長降至 5～10% 的零組件廠倍數區間定錨，並標資料缺口。"},"fwd_pe":35.8,"peg":1.8,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"三個倍數都在可得 4 個年度端點的最高（非連續五年序列，五年分位事實表未涵蓋）；前瞻本益比約 35.8 倍、PEG 約 1.8；現價距共識目標價約 +9.7%，Base 五年終值約 +11.4%。成長真實但價格已大致反映，判偏貴；未到最貴一級，是因為動能未過熱、且 8 月法說後法人調升獲利預估。","upside_short_pct":9.7,"upside_mid_pct":11.4,"denominator_disputed":false,"denominator_note":"分母為 TTM 與 FY2026 共識 EPS，屬擴產期高成長獲利、非一次性；但以 FY2025A 低基期算成長會讓 PEG 失真，本結論以 FY2026E→FY2029E 成長率為準。"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：一是 2027 年產能倍增撞上同業同步擴產與資本支出消化，毛利率回落、倍數從 50 倍級收縮；二是低估 AI 平台導入的黏著度，伺服器成長一路延續到 2029 年，現價其實不貴。","reasoning":"陷阱判斷依據見反證紀錄：衰退信號亮 2 個（折疊機核心份額縮減、EPS 成長顯著高於營收成長），判黃燈，屬週期高點的獲利放大，不是價值陷阱。產業態勢三軸：競爭面惡化（折疊機鉸鏈份額被新日興與 Amphenol 分走，滑軌三強同步擴產）；結構面轉好（液冷滲透推升快接頭近滿載，伺服器占比一年升到近 3 倍）；其他結構變數以客戶結構為主（集中度由陸系品牌換到 AI 平台），裁決為雙向拉鋸。成長熄火壓力測試：Base 到 FY2028E 106 元後，若 FY2029 成長降到 15%／10%／5%，給 20／15／11 倍，價格約 2,440／1,750／1,220 元，對現價 +3%／−26%／−48%，三種只過一種。最大回撤：純倍數收縮回 28 倍即跌約 45%，Bear 路徑谷底可到約 −70%。事件面：併購、訴訟、召回、監管調查均未見。","fact_refs":["f_pe_current","f_week26_return_pct","f_ma_w52","f_ma_w250","f_kpi9"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點的獲利放大，非價值陷阱；風險在倍數收縮與折疊機份額流失"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":46.72,"pe":50.73,"basis":"TTM 至 2026-06-30 稀釋 EPS（股價 2,370 元÷trailing 本益比 50.73 倍回推），終端倍數同為 trailing 口徑"},"eps":{"bull":[70,112,138,158,172],"base":[66,90,106,114,120],"bear":[60,70,58,52,56]},"pe":{"bull":28,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.53,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-72,"hi":-45,"basis":"上緣 −45%：TTM EPS 46.72 元不變、本益比由 50.7 倍收縮到 28 倍（約 1,308 元）；下緣 −72%：Bear 路徑 FY2029E 谷底 52 元遇 13～14 倍，價格約 680～730 元，較現價跌 69～71%，再留少量超跌空間；Bear 終點約 −65%（56 元×15 倍）落在範圍內。","trigger_time":null},"basis":{"bull":"AI 機櫃換代續選中、AWS 與第二家 ASIC 客戶放量、CPO 產品 2027 年起貢獻，2027 年產能倍增滿載、毛利率維持 33% 以上；終端 28 倍為高成長延續下的零組件倍數，遠低於現值 50.7 倍。","base":"2026 年 EPS 66 元貼近共識，2027 年產能倍增帶來約 36% 成長，2028 年起放緩到個位數、毛利率回到 30% 左右；終端 22 倍以成長降至 5～10% 的零組件廠倍數定錨（同業現值倍數事實表未涵蓋）。","bear":"2027 年後雲端資本支出消化、滑軌與快接頭同業產能倍增壓價、折疊機份額續失，EPS 2029 年回落至 52 元；終端 15 倍取成長熄火降至 10% 的倍數。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"公司 2027 年滑軌與快接頭產能要比現在倍增，滑軌三強同時擴產（富世達由 7～8 萬套擴至 35 萬套）；需求全部來自雲端資本支出；大和點名主要客戶市占率不如預期是下行風險。","assumption":"雲端資本支出 2028 年仍成長，新增產能被吸收、報價守住。","consequence":"若 2028 年進入消化期，滑軌與快接頭報價下修，EPS 由 2027 年高點回落到 50～60 元、本益比收縮到 14～15 倍，五年後股價約 780～900 元，較現價虧六成以上。","ruling":"採納：Bear 機率給 30%，這是五年虧損過半最可能的路徑。與唯一致命事件部分重疊——致命事件是平台落選（離散），本條是整體報價下行（連續），兩者分開監測。","watch":"月營收年增率、單季毛利率、同業擴產公告","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#3","channel_business_model_shift#2"],"fact_refs":["f_kpi8","f_kpi1"]},{"view":"論點失敗","evidence":"2026 第一季未承接華為 Pure S 鉸鏈；蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭；2025 年 4 月時鉸鏈占營收約 85%、高度依賴陸系品牌。","assumption":"華為三摺與左右摺新機能補回 Pure S 的缺口，折疊機維持現金流業務。","consequence":"折疊機營收年減擴大，伺服器以外沒有第二支腳，伺服器一旦換代失利就沒有緩衝。","ruling":"部分採納：上半年折疊機營收估年減約 13%，已計入 Base；蘋果名單未列，折疊機不再算成長來源。","watch":"每季折疊機營收年增率","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_concentration_credit#0"],"fact_refs":["f_kpi9"]},{"view":"論點成功但股東經濟變差","evidence":"2024 年擴產期自由現金流只有淨利的 70%（8.57 億元÷12.27 億元），2025 年 77%；股息殖利率 0.527%，回購紀錄事實表未涵蓋。","assumption":"產能倍增不需要大額資本支出，成長紅利會以現金回到股東手上。","consequence":"若越南廠與 2027 年倍增轉為重資本，或客戶要求降價換量，EPS 成長了，但每股自由現金流與股東回報不成比例。","ruling":"暫不採納：Q2 營業現金流 15.84 億元、資本支出 0.22 億元，TTM 自由現金流利潤率高於營業利益率，目前沒有重資本跡象；保留監測。","watch":"自由現金流÷淨利連兩年低於 0.75；資本支出占營收比","evidence_refs":[],"fact_refs":["f_kpi5","f_peer_6805_tw_fcf_margin_pct","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"trailing 本益比 50.73 倍、P/S 10.51 倍、EV/S 9.93 倍都在可得 4 個年度端點的最高；現價 2,370 元已落在賣方平均目標價約 2,391～2,594 元附近，FactSet 目標價 2,600 元只剩約 10%；FY2026 EPS 共識中位數由 66.52 元微降至 66.17 元。","assumption":"市場會一直用高成長年度的倍數評價，2027 年後倍數不回落。","consequence":"Base 路徑五年後約 2,640 元，只比現價高約 11%；要拿到一成年化報酬需要 FY2030E EPS 約 173 元，等同 Bull 路徑。","ruling":"採納：這是不追價的主因，也是唯一的約束條件。","watch":"股價相對 52 週均線 1,717 元的距離；FY2027 共識 EPS 上修幅度","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_price_at_dd","f_ma_w52"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2370.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2370.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"折疊機份額：公司說法對上客戶專案落選","cause":null,"prior_field":null,"side_a":"公司稱在中系與美系客戶皆為折疊機軸承主要供應商，訂單占比超過五成（2026-03）。","side_b":"2026 第一季未承接華為 Pure S 鉸鏈；蘋果折疊 iPhone 鉸鏈由新日興主供、Amphenol 競爭，未列富世達；上半年折疊機營收估年減約 13%（79.24 億元×38% 對上回推去年同期 48.72 億元×71%）。","ruling":"可調和，屬程度差異：既有中系客戶仍是主要供應商，但份額在流失，最大增量不在手上。採 B 側作為定價依據，折疊機視為逐年縮小的現金流業務，不計入成長。","evidence_level":"法說摘要與媒體供應鏈報導，非公司正式揭露","settle_metric":"每季法說營收結構中的折疊機營收年增率","if_then":["若 2026 下半年華為三摺與左右摺新機帶動折疊機營收年增轉正，則把折疊機由衰退改為不變並上調 Base FY2027E","若蘋果折疊機量產後折疊機營收仍連 2 季年減超過 25%，則下修 Base 並停止任何加碼"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"客戶集中度：降低還是換對象","cause":null,"prior_field":null,"side_a":"2025 年 4 月報導鉸鏈占營收約 85%，為陸系品牌高階折疊機的關鍵供應商。","side_b":"2026 上半年伺服器占 55.7%，法人估第三季伺服器占比升至 8 成以上；AWS 第二季起出貨，其他 ASIC 客戶仍在驗證。","ruling":"可調和：舊數字已過時，但集中度沒有下降，只是從陸系手機品牌換到少數 AI 平台；風險性質由消費週期換成雲端資本支出週期與平台換代。","evidence_level":"媒體報導與法人說法","settle_metric":"AWS 以外 ASIC 客戶的量產時點；伺服器營收占比","if_then":["若 2027 年底前至少一家 AWS 以外的 ASIC 客戶量產，則把集中度風險由中期降為長期","若伺服器占比逾 8 成而第二家雲端客戶到 2027 年底仍未量產，則 Bear 機率由 30% 上調至 35%"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#0","end_markets#4"]},{"axis":"賣方全面看多對上本研究不追價","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：8 位分析師全為買進、FactSet 目標價 2,600 元；第三季伺服器占比衝上 8 成以上，第三、四季營收預期季增雙位數；2027 年產能倍增、AWS 自 2027 第一季放量、CPO 產品 2027 年貢獻營收；26 週漲 29.71% 但 RSI 只有 54.49，沒有過熱。","side_b":"現價 2,370 元已在平均目標價約 2,391～2,594 元附近，trailing 本益比 50.73 倍為可得年度端點最高；FY2026 EPS 共識中位數由 66.52 元微降至 66.17 元；Base 路徑五年報酬約 11%。","ruling":"不可調和（行動方向相反），採 B 側。依據：分歧在框架層，賣方以短期目標價對高成長年度獲利給高倍數，本研究以五年終值計入同業同步倍增產能後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。執行：不追價，等價格回落或等 2027 年共識上修。","evidence_level":"賣方共識快照（日期不明確）與年度端點估值","settle_metric":"股價對 52 週均線的距離；FY2027 共識 EPS","if_then":["若股價回落至 1,700 元附近（約 52 週均線）且最近一季毛利率≥30%，則重跑研究後分批建立首倉","若股價續漲但 2027 年新平台與 AWS 放量的營收證據未到，則不追","反向：若 2027 年共識 EPS 上修使現價前瞻本益比降到 25 倍以下且毛利率≥33%，則不等回落，改以現價分批建立首倉"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"股價回落至 1,700 元附近且最近一季毛利率仍在 30% 以上，重跑研究後分批建立首倉","type":"估值rearm","maps_to":null,"metric":"股價；單季毛利率","threshold":"股價≤1,700 元且毛利率≥30%","action":"重跑研究後分批建立首倉","source_freq":"每日股價／每季財報","date":null},{"n":2,"text":"2026 第三季財報驗證下半年轉強","type":"假設驗證","maps_to":"H1","metric":"第三季營收季增率、毛利率","threshold":"營收季增≥10% 且毛利率≥33%","action":"未達則下修 Base FY2026E 至 60 元並把進場價下移","source_freq":"季報","date":"2026-11"},{"n":3,"text":"2027 上半年產能倍增轉成營收","type":"假設驗證","maps_to":"H2","metric":"2027 上半年營收年增率；伺服器占比","threshold":"營收年增≥30% 且伺服器占比≥70%","action":"達標則上調 Base FY2027E 並重估進場價；未達則維持觀望","source_freq":"月營收／法說","date":"2027-08"},{"n":4,"text":"折疊機份額流失擴大","type":"風險","maps_to":"R2","metric":"折疊機營收年增率","threshold":"連 2 季≤−25%","action":"下修 Base FY2027E 約 5%，停止任何加碼","source_freq":"每季法說營收結構","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"n":5,"text":"資本支出消化與同業擴產壓縮毛利","type":"風險","maps_to":"R3","metric":"單季毛利率；月營收年增率","threshold":"毛利率連 2 季＜30%，或月營收年增轉負連 3 個月","action":"取消進場價、改以 Bear 路徑重估；若已持有則減碼一半","source_freq":"季報／月營收","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":6,"text":"2027 年主力 AI 機櫃平台換代時未獲選為滑軌或快接頭主要供應商","type":"Single Thing","maps_to":"Single Thing","metric":"新平台量產供應商名單；伺服器營收年增率","threshold":"法說或供應鏈報導確認落選，或伺服器營收年增轉負","action":"清倉；未持有則停止追蹤","source_freq":"法說／供應鏈報導","date":"2027-06"},{"n":7,"text":"2026 年報與 2027 年法說後全面複審","type":"複審日期","maps_to":null,"metric":"FY2026 實際 EPS 對 Base 66 元","threshold":"偏離≥10%","action":"重跑完整研究","source_freq":"年報","date":"2027-03"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連 2 季＜30%","window":"2026Q3–2027Q4","source":"公司季報","last_status":"ok"},{"metric":"折疊機營收年增率","bear_threshold":"連 2 季≤−25%","window":"2026Q3–2027Q4","source":"每季法說營收結構","last_status":"warning"},{"metric":"月營收年增率","bear_threshold":"轉負連 3 個月","window":"2026-10 至 2027-12","source":"公開資訊觀測站月營收","last_status":"unknown"},{"metric":"伺服器產品營收占比","bear_threshold":"回落至 50% 以下","window":"2027 全年","source":"法說營收結構","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤1,700 元（約 52 週均線）且最近一季毛利率≥30%；或 2027 共識 EPS 上修使前瞻本益比≤25 倍","exec_line":"不追價；觸發重啟條件後先重跑研究，再分批建立首倉；主力平台落選則停止追蹤。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方以短期目標價對高成長年度獲利給高倍數，未計入 2027 年同業同步倍增產能與 2028 年資本支出消化後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回落至 1,700 元附近（約 52 週均線）且最近一季毛利率維持 30% 以上；或 2027 年共識 EPS 上修，使同價位前瞻本益比降到 25 倍以下。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方以短期目標價對高成長年度獲利給高倍數，未計入 2027 年同業同步倍增產能與 2028 年資本支出消化後的倍數回落；現價要 Bull 路徑才換得到一成年化報酬。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=29.71, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 伺服器滑軌與液冷快接頭撐起 2026 下半年：營收與毛利率高於上半年，全年 EPS 接近共識。","2y":"2026 下半年營收高於上半年 79.24 億元，全年 EPS≥60 元","5y":null,"10y":null,"threshold":"下半年營收＞79.24 億元；第三、四季毛利率≥33%；FY2026 EPS≥60 元（共識 66.17 元）","source":"公司季報與法說；FactSet 共識","drift_rule":"以 TTM 營收與毛利率對 Base 路徑的偏離計：連 2 季偏離≥5% 視為削弱，連 3 季≥10% 視為反轉。"},{"id":"H2","text":"2027 年產能倍增能轉成營收：AWS 自 2027 第一季增溫，驗證中的 ASIC 客戶至少一家量產。","2y":"2027 年營收年增≥30%，伺服器占比≥70%","5y":null,"10y":null,"threshold":"2027 年營收年增≥30%；伺服器占比≥70%；2027 年底前 AWS 以外至少一家 ASIC 客戶量產","source":"月營收、法說營收結構與客戶驗證進度","drift_rule":"連 2 季營收偏離 Base 路徑≥5% 視為削弱，連 3 季≥10% 視為反轉。"},{"id":"H3","text":"同業擴產後毛利率仍守在 30% 以上，代表賺到的是工藝與認證，不只是供給吃緊。","2y":null,"5y":"2027–2030 年度毛利率≥30%、營業利益率≥22%","10y":null,"threshold":"年度毛利率≥30%（TTM 30.38%）；營業利益率≥22%（TTM 24.27%）","source":"年報與季報","drift_rule":"連 4 季偏離門檻≥5% 視為削弱，連 6 季≥10% 視為反轉。"}],"R":[{"id":"R1","text":"新專案量產遞延：第三季起投產的 NVIDIA／ASIC 滑軌專案延後，下半年轉強落空。","h_ref":"H1","clock":"⚡","threshold":"第三季營收季增＜10% 或毛利率＜33%","evidence_refs":["end_markets#2"]},{"id":"R2","text":"折疊機鉸鏈份額持續流失：華為 Pure S 未承接、蘋果鉸鏈名單未列，加上大和點名的主要客戶市占率與折疊機滲透率不如預期。","h_ref":"H1","clock":"🔥","threshold":"折疊機營收連 2 季年減≥25%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"id":"R3","text":"2028 年起雲端資本支出消化，滑軌與快接頭同業同步倍增產能，報價與毛利率下行。","h_ref":"H3","clock":"🐢","threshold":"年度毛利率＜28%，或月營收年增轉負連 3 個月","evidence_refs":["supply_demand_durability#3","competitive_share_entrants#3"]},{"id":"R4","text":"集中度只是換了對象：由陸系折疊機品牌（2025 年鉸鏈占營收約 85%）換成 AWS 與 NVIDIA 平台，單一平台換代落選的衝擊放大。","h_ref":"H2","clock":"🔥","threshold":"伺服器占比回落至 50% 以下，或 2027 年底前 AWS 以外 ASIC 客戶仍未量產","evidence_refs":["customer_concentration_credit#0","customer_second_source#0"]}],"single_thing":{"description":"2027 年主力 AI 機櫃平台（NVIDIA 下一代與 AWS ASIC 機櫃）換代時，公司未獲選為滑軌或液冷快接頭主要供應商。","why_fatal":"法人估第三季伺服器已占營收 8 成以上，2027 年產能倍增以新平台放量為前提；落選會讓 FY2027E EPS 由 Base 90 元落到 70 元以下，倍數同時由成長股收縮到零組件循環股，是股價對單一事件最大的敏感項。","if_happens":"清倉；未持有則停止追蹤並取消進場價。","how_monitor":"每季法說的新平台量產時程與客戶驗證進度、月營收年增率、越南廠稼動率、供應鏈報導的平台供應商名單。","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":30.98,"FY2026E":66.17,"FY2027E":null,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（新台幣）；FY2026E 為 FactSet 共識中位數（9 家，2026-07 報導）；FY2027E／FY2028E 共識事實表未涵蓋。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 第三季財報與法說：驗證伺服器占比升至 8 成以上與毛利率","impact":"高","watch":"營收季增率是否≥10%、毛利率是否≥33%"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"蘋果折疊機上市時點（Counterpoint 預期 2026 年，Mizuho 稱可能延至 2027）","impact":"中","watch":"公司是否打入鉸鏈或周邊機構件供應鏈；折疊機營收年增率"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"AWS 滑軌出貨自 2027 第一季增溫（法人預估）","impact":"高","watch":"月營收年增率；AWS 以外 ASIC 客戶的驗證進度"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"2027 年滑軌與液冷快接頭產能較現在倍增","impact":"中","watch":"稼動率與毛利率是否同步維持"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
