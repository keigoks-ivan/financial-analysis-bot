你是 DD 管線 v20 的判斷層閘（gate），標的 8996.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝2305.2 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無共識資料（8996.TW 不在 EPS 快照）
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益／利益率＝296.6 百萬TWD（利益率 12.87%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無共識資料
- `f_kpi2`（q1_business）｜毛利率＝26.0 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無共識資料
- `f_kpi6`（q1_business）｜管理層指引＝定性：散熱業務 Q2 受 AI 伺服器新舊平台交替、客戶拉貨遞延；預期 Q3 重返成長，無數值區間｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：媒體轉述公司說法（moneyweekly／winvest 彙整），未見 IR 原文（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-14 date｜期間與口徑：2026-08-14／距今 41 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-14）
- `f_peer_8996_tw_gross_margin_pct`（q2_moat）｜8996.TW 毛利率＝27.03 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8996.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8996_tw_operating_margin_pct`（q2_moat）｜8996.TW 營業利益率＝16.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8996.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8996_tw_fcf_margin_pct`（q2_moat）｜8996.TW FCF 利潤率＝6.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8996.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_operating_margin_pct`（q2_moat）｜3017.TW 營業利益率＝23.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_fcf_margin_pct`（q2_moat）｜3017.TW FCF 利潤率＝24.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_gross_margin_pct`（q2_moat）｜3324.TWO 毛利率＝27.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_operating_margin_pct`（q2_moat）｜3324.TWO 營業利益率＝15.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3324_two_fcf_margin_pct`（q2_moat）｜3324.TWO FCF 利潤率＝-13.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3324.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_gross_margin_pct`（q2_moat）｜3653.TW 毛利率＝42.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3653_tw_operating_margin_pct`（q2_moat）｜3653.TW 營業利益率＝33.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3653.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6230_tw_operating_margin_pct`（q2_moat）｜6230.TW 營業利益率＝-0.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6230.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.74 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝40.85 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝74.35 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流−資本支出）＝-125.6 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核；OCF 406.9 百萬、Capex 532.6 百萬（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無共識資料
- `f_kpi3_eps`（q4_capital）｜稅後淨利／稀釋 EPS＝200.8 百萬TWD（EPS 2.16 元）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：無共識資料
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝0.7 %（SBC 2.08 百萬）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／quarterly_cashflow（TWD，源自公司合併財報）；公司 IR 新聞稿／MOPS 原文未取得，待複核（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-14））
  - 註記：不適用
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.266 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1710.0 TWD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝115.31 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝16.22 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝16.21 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝82.45 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 20.74，分子＝快照價 1710.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝69.31 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（6 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：高力以往資料中心液冷營收主要集中單一美系大型伺服器品牌廠（客戶集中）
  - 來源：經濟日報 money.udn.com《兩大產品傳捷報 法人調升高力目標價逾60%》（as_of 2026-06-22）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：高力燃料電池業務主力客戶為美國 Bloom Energy，Bloom 擴產計畫被視為燃料電池業務成長關鍵；報導未揭露具體客戶占比百分比。
  - 來源：財訊/今周刊類報導 moneyweekly（高力 8996 燃料電池、液冷散熱）（as_of 2026-04-09）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：Bloom Energy 2026-07-08 遭 Hunterbrook Media 發布針對會計與供應鏈的批評報告，公司否認；7 月底股價因分析師降評單日跌約 18%。未見信評機構（Moody's/S&P/Fitch）調整。
  - 來源：boerse-express Hunterbrook 報導；MarketBeat 2026-07-29（as_of 2026-07-29）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：主要客戶 Bloom Energy 與甲骨文等完成大型合約，報導稱目前擴出的產能全數被訂走（客戶集中於燃料電池單一客戶）。
  - 來源：財經媒體報導（搜尋摘要，未逐字取得）（as_of 2026-05-30）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：浸沒式冷卻（單相／兩相）被列為主要替代路徑之一，但供應商（如 CAREL）定位為與直接液冷互補，並非取代；浸沒單相仍需熱交換器排熱。
  - 來源：Introl blog《Cooling Distribution Units: Liquid Cooling Infrastructure for AI Data Centers》；CAREL data centre liquid cooling systems（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：另一篇財經週刊（Money Weekly）引法人預期2026 EPS約17.05元，與上述25.00元不一致，且提示本益比逾85倍與客戶集中風險（未取得該篇原文逐字，僅搜尋摘要轉述）。
  - 來源：Money Weekly 搜尋結果摘要（as_of 2026-06-30）｜affects：valuation、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3450.0,"bear_5y_price":540.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-6.4,"ev5y_pct":2.0,"irr_base_pct":-1.3,"asym_ratio":1.2,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":20.74,"pe":82.45,"basis":"FY2026E 共識 EPS（前瞻一年口徑）；終端倍數同樣套在終端年 EPS 上"},"eps":{"bull":[21.0,41.0,74.0,95.0,115.0],"base":[19.5,31.0,44.0,55.0,64.0],"bear":[17.0,20.0,24.0,27.0,30.0]},"pe":{"bull":30,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.266,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | none | 0 | 3 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 7 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | none | 0 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）（沿用 8996.TW_20261011，0d）：高力熱處理 8996 antitrust OR regulation OR 公平會 2026；Kaori Heat Treatment 8996 regulatory scrutiny plate heat exchanger 2026
- **reg_tariff_export**（none）（沿用 8996.TW_20261011，0d）：高力熱處理 8996 關稅 出口 2026；Kaori Heat Treatment 8996 tariff section 232 plate heat exchanger 2026；高力 8996 板式熱交換器 美國關稅 中國 出口 營收占比
- **major_events**（none）（沿用 8996.TW_20261011，0d）：8996.TW 高力熱處理 併購 收購 2025 2026；8996 高力熱處理 訴訟 集體訴訟 證券；8996 高力 Kaori Heat Treatment product recall warning letter；8996 高力 金管會 調查 重編 財報 檢調

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"8996.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"高力"},"oneliner":"高力把熱交換器做進 AI 液冷與 Bloom 燃料電池，前八月營收年增 115%；但兩條成長線各綁一家主力客戶，現價已是 2026 年共識 EPS 的 82 倍，基準情境五年報酬接近零，等價格回落再看。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 伺服器液冷與 Bloom 燃料電池擴產的錢，錢卡在熱交換器製造與平台認證這一節；兩條成長線各綁一家主力客戶，議價權在買方","reasoning":"高力賣熱交換器與熱管理元件，營收分三塊：AI 資料中心液冷（法人估 2026 年占營收 51%，主要出給單一美系伺服器品牌，板換 2026 下半年起出貨美系雲端服務商）、Bloom Energy 燃料電池熱元件、傳統板式熱交換器（前八月年增約 19%）。2026 Q2 營收 23.05 億元、毛利率 26.0%、營益率 12.87%。上半年營收 57.28 億元減去 Q2，推得 Q1 約 34.2 億元，Q2 季減約 33%，原因是 AI 伺服器新舊平台交替、客戶遞延拉貨；7–8 月合計約 21.3 億元，月均回到 10 億元以上，約為 2025 年月均的兩倍。錢卡在製造與認證這一節：熱交換器是 CDU 與燃料電池熱箱的核心元件，但下游兩家主力客戶規模遠大於高力。產業處於擴張期，依據是訂單被客戶追著跑、公司正把產能擴到目前的 3～6 倍，不是股價。供需判斷：需求屬結構性（AI 機櫃功率走向單櫃 600kW～1MW、液冷成為基線），但供給可逆性高，本廠 2027–2028 年大量開出產能，一旦客戶放緩，過剩會先打在零組件價格上。單點依賴：液冷靠一家伺服器品牌、燃料電池靠 Bloom，這是集中度風險，不是護城河證據；兩家各自的營收占比事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2","f_kpi6","f_earnings_recency"],"verdict_values":{"revenue_quality":"成長集中在液冷與燃料電池熱元件（前八月合計年增 158%），傳統板式熱交換器年增約 19%；營收跟著客戶平台節奏走，2026 Q2 季減約 33%，訂單能見度約二至三個月","unit_econ_note":"2026 Q2 毛利率 26.0%、營益率 12.87%，低於 TTM 的 27.03%、16.3%；營收下滑季營業槓桿反向。單價與出貨量拆分事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 資本支出與單一燃料電池客戶擴產驅動的零組件供應商；2024 年營收年減 7.45%、2026 Q2 季減約 33%，需求隨客戶資本支出斷層"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求、供給可逆性高：液冷與燃料電池訂單被客戶追著跑、擴出產能已被訂走（2026-05 股東會與媒體轉述）；但本廠 2027–2028 年產能擴到 3～6 倍，供給可在兩年內追上需求，同業擴產規模事實表未涵蓋","bargaining":{"up":"上游供應商結構事實表未涵蓋","down":"買方高度集中：液冷主要出給單一美系伺服器品牌、燃料電池主力客戶為 Bloom Energy，客戶規模遠大於高力，議價權在下游","geo":"擴產在台灣（橋頭、中壢），泰國廠考慮租廠生產燃料電池散熱產品、啟動時間未定"},"profit_pool_dir":"液冷與燃料電池熱管理利潤池在擴大；高力在池中的份額方向事實表未涵蓋","tam_table":[{"item":"資料中心 CDU 市場規模","value":"約 10.5 億美元（2025）→ 77.4 億美元（2032），年化 33.0%；另一份液對液 CDU 預測年化 19.2%（付費市調摘要，口徑不一）"},{"item":"CDU 製造營收","value":"約 1.5 億美元（2023）→ 約 10 億美元（2027），Omdia 經 Upsite 引述"},{"item":"CDU 前三大廠合計市占","value":"46%（2025）"},{"item":"燃料電池主力客戶產能","value":"Bloom Energy 2026 年產能由 1GW 擴至 2GW"},{"item":"板式熱交換器專屬 TAM 與高力滲透率","value":"事實表未涵蓋"},{"item":"營業利益池占比（5 年前→現）","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行面擴大（新增美系雲端服務商客戶、延伸 Manifold 與系統 ODM），定價面縮減（毛利率三年下滑），等級 C","reasoning":"機制是真空焊接板式熱交換器的製程與平台認證：元件進入 CDU 與燃料電池熱箱後，客戶換供應商要重新驗證，但認證以平台為單位、每代重新選料，切換成本中等。同業投入資本與 ROIC 事實表未涵蓋，改用 TTM 利潤率當可比軸：高力營益率 16.3%，低於 3017.TW 的 23.56% 與 3653.TW 的 33.06%，略高於 3324.TWO 的 15.3%；FCF 利潤率 6.98%，遠低於 3017.TW 的 24.1%。高力有生意，但看不到超額定價權。執行面在擴大：板換切入美系雲端服務商、拓展 Manifold 與系統 ODM。定價面在縮減：毛利率 2024 年 29.85%、2025 年 27.34%、2026 Q2 26.0%，擴出產能已被訂走卻沒換來毛利率上升，價值仍在往買方流。兩向相抵判穩定，執行 7、定價 5。報酬持續期：歷史增量報酬高（代理估算約 68%），但 2026 年起擴產 42.5 億元並私募，新產能的增量報酬尚未驗證，決策層級與價值鏈分配兩點偏黃。","fact_refs":["f_peer_8996_tw_gross_margin_pct","f_peer_8996_tw_operating_margin_pct","f_peer_8996_tw_fcf_margin_pct","f_peer_3017_tw_operating_margin_pct","f_peer_3017_tw_fcf_margin_pct","f_peer_3324_two_gross_margin_pct","f_peer_3324_two_operating_margin_pct","f_peer_3324_two_fcf_margin_pct","f_peer_3653_tw_gross_margin_pct","f_peer_3653_tw_operating_margin_pct","f_peer_6230_tw_operating_margin_pct","f_kpi2"],"verdict_values":{"moat":{"mechanism":"真空焊接板式熱交換器的製程與平台認證：元件進入 CDU 與燃料電池熱箱後，客戶換供應商需重新驗證；認證以平台為單位、每代重新選料，客戶也有多家認證政策，切換成本中等","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：板換切入美系雲端服務商、2026 下半年出貨，並拓展 Manifold 與系統 ODM。定價面縮減：毛利率 2024 年 29.85% → 2025 年 27.34% → 2026 Q2 26.0%，TTM 營益率 16.3% 低於 3017.TW 的 23.56% 與 3653.TW 的 33.06%。兩向相抵，合併為穩定","competitor_notes":[{"name":"3017.TW","strategy_note":"TTM 營益率 23.56%、FCF 利潤率 24.1%，獲利與現金轉換都比高力高一截，是定價力的上緣參考"},{"name":"3324.TWO","strategy_note":"毛利率 27.85% 與高力相近，但 FCF 利潤率 −13.66%，同樣處在重資本投入期"},{"name":"3653.TW","strategy_note":"毛利率 42.63%、營益率 33.06%，高出高力 15pp 以上，屬不同定價層級，只作利潤率天花板對照"},{"name":"6230.TW","strategy_note":"營益率 −0.88%，同組中後段玩家賺不到錢，客戶位置決定利潤"}],"spread_notes":null,"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，改用 TTM 營益率與 FCF 利潤率作可比軸；只有單期數字，無法判斷差距在擴大或收窄","threats":[{"level":"🟡","text":"浸沒式冷卻是另一條散熱路徑，但供應商定位為與直接液冷互補，單相浸沒仍需熱交換器排熱，屬點對點威脅","p":"15%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"客戶多家認證：Bloom 對單一來源零件採多家資格認證的一般政策，伺服器端每代平台重新選料，高力新產能開出前客戶可能先分單","p":"30%","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（營益率 16.3%；投入資本與周轉率事實表未涵蓋，當期 ROIC 無法計算；依 2026 Q2 資本支出 5.33 億元大於營業現金流 4.07 億元推判周轉率走低）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（資料中心）、決策者（伺服器品牌與雲端服務商）、付款者（雲端服務商）三角色都成立；AI 機櫃功率走向單櫃 600kW～1MW（Kyber 2027），液冷已是基線，屬需要不是想要。燃料電池端 Bloom 產能由 1GW 擴至 2GW"},{"item":"決策層級","level":"🟡","text":"替代性的最小單位是單一 AI 平台的 CDU 設計導入，每代平台重新選料；2026 Q2 平台交替即出現拉貨遞延。Bloom 10-Q 載明對單一來源零件採多家資格認證，換供應商的代價在重新認證週期，不在技術門檻"},{"item":"價值鏈分配","level":"🟡","text":"熱交換器是 CDU 與燃料電池熱箱的核心元件，但採購金額占系統比重事實表未涵蓋；買方集中在兩家，擴出產能已被訂走、議價權短期應偏賣方，毛利率卻由 2024 年 29.85% 降到 2026 Q2 的 26.0%，價值仍在往買方流"},{"item":"社會容忍度","level":"🟢","text":"工業零組件，非民生必需品，不依賴監管授權，沒有社會定價天花板"}],"roiic":68,"reinvest_rate":58,"endo_ceiling":40,"formula_note":"代理估算（投入資本事實表未涵蓋，以淨利代替稅後營業利益，資料取自年度財報歷史 2022–2025）：再投資＝淨利−自由現金流（即資本支出−折舊＋營運資金增加）。2022–2024 年累計再投資約 7.75 億元，淨利 2022→2025 年增加約 5.29 億元，增量報酬約 68%（改用 2023–2025 年再投資 5.55 億元算為 95%，取低者）。再投資率：2022–2025 年累計再投資 13.31 億元÷累計淨利 23.00 億元≈58%。內生成長上界≈68%×58%≈40%/年。2026 Q2 再投資率約 163%（淨利 2.01 億元、自由現金流 −1.26 億元），加上 42.5 億元擴產，超出部分靠私募與外部資金，新產能的增量報酬尚未驗證"}}}},"q3_growth":{"verdict":"成長年限中（🟡）：液冷在新建 AI 機櫃已成基線、燃料電池是第二曲線但綁單一客戶；共識三年 EPS 年化約 103%，遠超內生上界約 40%，缺口靠外部資本擴產與新產能全數填滿","reasoning":"成長幾乎全靠量：液冷與燃料電池前八月合計年增 158%，價格貢獻事實表未涵蓋；無併購、無回購，另有私募稀釋。共識 EPS 由 2025 年 8.93 元到 2028 年 74.35 元，三年年化約 103%；內生上界約 40%，缺口約 63pp。缺口不能歸因於利潤率擴張（毛利率在降）、淨回購或收購；唯一指得出的來源是私募與舉債支應的外部資本擴產，其餘無法歸因，依賴 re-rate 與新產能全數填滿，長期信心上限為中。成長年限：液冷在新建 AI 機櫃已是基線，整體資料中心滲透率事實表未涵蓋，無法推算年限；CDU 市場預測 2025–2032 年年化 19.2%～33.0%，分歧大。燃料電池雖是第二條曲線，但已在現有成長基數內、又綁單一客戶 Bloom，撐不起五年後仍寬的判斷，故判中。衰退信號亮 2 個：自由現金流對淨利低於 0.75、EPS 成長高於營收成長逾 5pp；毛利率年減序列不完整，列觀察。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi4","f_kpi2"],"verdict_values":{"growth":{"driver_mix":"量為主：液冷與燃料電池出貨量隨兩家主力客戶擴產放大（前八月合計年增 158%），價格貢獻事實表未涵蓋；無併購、無回購，私募 9,000 張帶來約 9.7% 稀釋","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"引報酬持續期檢核：增量報酬約 68%×再投資率約 58%≈40%/年；共識 FY2025A→FY2028E EPS 年化約 103%（8.93→74.35 元），缺口約 63pp，無法歸因於利潤率、回購或收購","segments":[{"item":"液冷散熱（資料中心）","value":"法人估營收占比 2026/2027/2028 年 51%/49%/46%；客戶集中於單一美系伺服器品牌，板換 2026 下半年起出貨美系雲端服務商"},{"item":"燃料電池熱元件","value":"主力客戶 Bloom Energy（產能 1GW→2GW）；與液冷合計前八月年增 158%；占比事實表未涵蓋"},{"item":"板式熱交換器（傳統本業）","value":"前八月年增約 19%（公司公告口徑 18.73%）"},{"item":"分部毛利率","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"自由現金流對淨利低於 0.75 連 2 年","lit":true,"evidence":"2025 年 0.33（自由現金流 2.74 億元÷淨利 8.30 億元），2026 Q2 自由現金流 −1.26 億元，擴產期第二年大概率延續；屬成長型資本支出，非維持性"},{"signal":"EPS 年化成長高於營收年化成長逾 5pp","lit":true,"evidence":"2022–2025 年 EPS 年化約 38.4%、營收約 32.3%，差 6.1pp，來源是營益率由 12.31% 升到 15.87%，不是回購"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"年度毛利率 2024 年 29.85% → 2025 年 27.34%，2026 Q2 26.0%；季度年比序列事實表未涵蓋，暫不計入但列觀察"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置可評的只有股權激勵稀釋一項且通過；無回購、無併購，擴產改用私募股權籌資，價值取決於新產能的增量報酬","reasoning":"現金轉換弱：自由現金流對淨利 2023 年 0.57、2024 年 1.42、2025 年 0.33；2026 Q2 營業現金流 4.07 億元、資本支出 5.33 億元，自由現金流 −1.26 億元。SBC 2.08 百萬元，占營業利益 0.7%、占營收約 0.09%。現金去向以擴產資本支出為主，配息殖利率 0.27%，無回購、無併購；三年現金去向四分事實表未涵蓋。股數由 2022 年約 8,930 萬股增至 2026 Q2 約 9,300 萬股（淨利÷EPS 推算），年化約 1.2%；股東會已通過私募 9,000 張，約為現有股數 9.7%，用於擴產與營運資金。營運槓桿：2025 年營收年增 64.37%、營業利益年增約 61.9%，差 2.5pp，未到壓縮警示。私募稀釋屬一次性籌資，好壞要看 2027–2028 年新產能能否賺回增量報酬，現在無法評分。","fact_refs":["f_kpi3_eps","f_kpi4","f_kpi5_sbc","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購紀錄，重大事件搜尋亦無併購"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無回購；反向以私募 9,000 張籌資"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 2.08 百萬元，占營業利益 0.7%；2022 至 2026 Q2 股數年化增約 1.2%；私募 9,000 張約 9.7% 屬一次性籌資，另於增量報酬檢視"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長由自建擴產帶動而非併購；無回購、配息殖利率 0.27%，三年現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求三年 EPS 年化約 100%、營收放大到 2025 年的 7～8 倍，且五年後市場仍給 25 倍以上；我不信全部兌現，價格已預付共識路徑","reasoning":"現價 1,710 元＝2026 年共識 EPS 20.74 元的 82.45 倍、2027 年共識 40.85 元的 41.9 倍、2028 年共識 74.35 元的 23 倍；trailing 本益比 115.31 倍、P/S 16.22 倍、EV/S 16.21 倍，都在近四個年度端點的最高位，且已高於 8 月法人目標價 1,320 元。基準情境（2030 年 EPS 64 元、終端 25 倍）五年價格約 1,600 元，略低於現價；牛市 3,450 元、熊市 540 元，三情境機率加權五年合計報酬約 +2%。以共識算的 PEG 約 0.80 看似便宜，但分母本身是爭點，便宜論證不成立。循環型理應以 P/B 為主尺，淨值資料事實表未涵蓋；同業倍數也未涵蓋，終端倍數無法對同業現值校準，屬資料缺口。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Fwd P/E（2026 年共識 EPS 20.74 元）對照 2027–2028 年共識；循環型理應用 P/B，淨值資料事實表未涵蓋","tier":"AI 散熱高成長同組（3017.TW、3324.TWO、3653.TW、6230.TW）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 Fwd P/E，無法做倍數對照；終端倍數的同業現值校準屬資料缺口"},"fwd_pe":82.45,"peg":0.8,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"trailing 115.31 倍、Fwd 82.45 倍，四個年度端點分位皆為 100（只有四點，非五年口徑，五年分位資料缺口）；基準五年報酬 −6%、三情境加權五年合計約 +2%、牛熊不對稱比約 1.2；PEG 0.80 建立在爭議分母上不採用。估值判紅","upside_short_pct":-9.9,"upside_mid_pct":4.8,"denominator_disputed":true,"denominator_note":"2026 年 EPS 預估從 17.05 到 25.00 元分歧；2028 年共識 74.35 元換成淨利約 76 億元（私募後約 1.02 億股），淨利率 15% 也需營收約 500 億元，是 2025 年的 7～8 倍。便宜的 PEG 全靠這個分母，視為爭點。12 個月：2027 年秋以 2028 年基準 EPS 44 元×35 倍＝1,540 元；三年：2029 年秋以 2030 年基準 EPS 64 元×28 倍＝1,792 元"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩家主力客戶同時放緩、擴產與私募稀釋讓每股盈餘落後營收、以及市場已提前定價 2028 年三處；路徑屬深回撤型","reasoning":"三個看錯方向：一是 Bloom 與單一美系伺服器品牌任一放緩，3～6 倍新產能閒置；二是訂單如期但擴產折舊與私募稀釋讓每股盈餘落後營收；三是現價已預付共識三年路徑。歷史最大回撤事實表未涵蓋；2024 年營收年減 7.45%、2026 Q2 營收季減約 33%，證明需求會斷層。最大回撤範圍 −50%～−75%：下緣對應熊市終點 540 元（−68%）再加路徑超跌，上緣對應 2027 年 EPS 降到共識七成約 29 元、倍數壓到 30 倍（約 860 元）。論點本身未破，不因波動砍倉，但首倉要小。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi4","f_pe_current","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長兌現風險：價格已預付三年高成長，兩家主力客戶任一放緩即落空"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":20.74,"pe":82.45,"basis":"FY2026E 共識 EPS（前瞻一年口徑）；終端倍數同樣套在終端年 EPS 上"},"eps":{"bull":[21.0,41.0,74.0,95.0,115.0],"base":[19.5,31.0,44.0,55.0,64.0],"bear":[17.0,20.0,24.0,27.0,30.0]},"pe":{"bull":30,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.27,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-75,"hi":-50,"basis":"歷史最大回撤事實表未涵蓋。下緣 −75%：熊市終點 540 元（−68%）再加路徑超跌；上緣 −50%：2027 年 EPS 降到共識七成約 29 元、倍數由 82 倍壓到 30 倍，約 860 元。依據：2024 年營收年減 7.45%、2026 Q2 營收季減約 33%，需求會斷層；現價倍數在近四個年度端點最高位，下跌時盈餘與倍數雙殺","trigger_time":null},"basis":{"bull":"共識路徑兌現並延續：中壢 2028 年 6 倍產能填滿、板換打進美系雲端服務商、Bloom 2GW 如期；2030 年 EPS 115 元，終端 30 倍對應 2030 年後年增約 20%","base":"營收 2027 年約 +70%、2028 年 +40%，之後降到 15～25%；淨利率約 15%～16%；股數含私募約 1.02 億股；EPS 為共識的六到八成。終端 25 倍對應 2030 年後年增約 15%；同業 Fwd P/E 事實表未涵蓋，無法對同業現值校準","bear":"Bloom 放緩或最大液冷客戶分單，新產能利用率不足：2027 年 EPS 僅年增約 18%、之後年增 10～20%；終端 18 倍＝成長熄火降至約 10% 的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"液冷營收集中在單一美系伺服器品牌、燃料電池主力客戶為 Bloom；Bloom 7 月遭放空報告質疑會計與供應鏈、因降評單日跌約 18%；報導稱擴出產能全數被 Bloom 等客戶訂走","assumption":"兩家主力客戶在 2027–2028 年持續放大訂單，填滿 3～6 倍新產能","consequence":"任一家放緩，新產能閒置、折舊壓低獲利率，2030 年 EPS 停在 30 元附近，倍數壓到 18 倍，股價較現價跌六到七成","ruling":"採納，列為熊市情境、機率 30%。與唯一致命點部分重疊：唯一致命點只看液冷主力客戶轉單，這條另加 Bloom 放緩，兩者合起來構成熊市","watch":"熱能產品月營收年增率、Bloom 季報產能目標與全年財測","evidence_refs":["competitive_share_entrants#1","customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"],"fact_refs":["f_kpi0_gaap","f_kpi6"]},{"view":"論點成功但股東經濟變差","evidence":"擴產投入 42.5 億元、私募 9,000 張（約現有股數 9.7%）；2026 Q2 自由現金流 −1.26 億元、毛利率 26.0% 低於 TTM 27.03%、營益率 12.87% 低於 TTM 16.3%","assumption":"營收如期放大，每股盈餘同步放大","consequence":"營收成長但股數增加、新產能爬坡期毛利率下滑，每股盈餘成長落後營收，自由現金流連兩年為負","ruling":"部分採納：基準情境已用私募後約 1.02 億股、淨利率約 15% 計算，EPS 比共識低兩到四成；若毛利率跌破 25% 連 2 季，終端倍數再降到 20 倍","watch":"單季毛利率、年度自由現金流、私募定價與實際發行股數","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"],"fact_refs":["f_kpi2","f_kpi1_gaap","f_kpi4","f_peer_8996_tw_gross_margin_pct","f_peer_8996_tw_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"現價 1,710 元＝2026 年共識 EPS 的 82.45 倍、trailing 115.31 倍、P/S 16.22 倍，皆為近四個年度端點最高；26 週漲 69.31%；另一份法人預估 2026 年 EPS 僅 17.05 元，與 25.00 元的說法差距大，並提示本益比逾 85 倍與客戶集中","assumption":"共識 2028 年 EPS 74.35 元兌現，且高成長放緩後市場仍給高倍數","consequence":"共識 2028 年 EPS 等於要營收放大到 2025 年的 7～8 倍；只兌現七成（約 52 元）、給 30 倍，價格約 1,560 元，仍低於現價","ruling":"採納，這是觀望的主因：基準情境五年價格約 1,600 元，三情境加權五年合計報酬約 +2%","watch":"FY2027 共識 EPS 是否守在 35 元以上、2027 上半年季營收能否站上 45 億元","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_ps_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1710.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1710.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單能見度 vs 客戶集中","cause":null,"prior_field":null,"side_a":"燃料電池訂單能見度拉長到 2028 年、擴出產能全數被訂走、在手訂單成長優於原先預期（公司與券商報告）","side_b":"能見度集中在 Bloom 與單一美系伺服器品牌兩家；Bloom 7 月遭放空報告、單日跌約 18%；2026 Q2 已因平台交替出現拉貨遞延、營收季減約 33%","ruling":"可調和，屬程度差異：能見度是真的，但只來自兩家客戶，轉成營收的時點與規模風險高，所以基準情境比共識保守","evidence_level":"公司說法經媒體轉述＋客戶 10-Q 與市場報導，未見公司 IR 原文","settle_metric":"2026 Q3、Q4 單季營收與毛利率；Bloom 季報產能進度","if_then":["若 2026 Q4 單季營收 ≥33 億元且毛利率 ≥26%，則維持基準路徑、牛市機率上調 5pp，仍等價格","若 Bloom 下修財測或延後 2GW 目標，則 2027 年基準 EPS 下修到 25 元、熊市機率提到 40%"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2","supply_demand_durability#2"]},{"axis":"估值：共識 PEG 便宜 vs 基準五年持平","cause":null,"prior_field":null,"side_a":"以共識算，2028 年本益比只有 23 倍、PEG 約 0.8；法人 6 月目標價上調逾六成、8 月目標價 1,320 元","side_b":"共識 2028 年 EPS 74.35 元換成淨利約 76 億元（私募後約 1.02 億股），淨利率拉到 15% 也要營收約 500 億元，是 2025 年 65.8 億元的 7～8 倍；需新產能近乎零閒置且毛利率不降；現價已越過 8 月目標價","ruling":"不可調和，選後者。依據是營收倍數的算術：中壢 2028 年產能也只到目前 6 倍、橋頭 2028 年才完工，共識要求產能幾乎全滿。基準 EPS 用共識的六到八成，五年價格約 1,600 元，略低於現價。執行：觀望不追","evidence_level":"賣方共識快照＋公司擴產規劃（股東會轉述）","settle_metric":"2027 上半年季營收與毛利率、FY2027 共識 EPS 走向","if_then":["若 2027 上半年任一季營收站上 45 億元且毛利率 ≥26%，則基準 EPS 上調至共識的 85% 並重跑研究，在現價附近以 ≤3% 小倉位起步","若股價續漲而 2026 Q4 營收未達 33 億元，則不追","若股價跌到 1,000 元以下且熱能產品月營收年增仍為正，則分批反買，首筆 ≤3%"],"evidence_refs":["capital_markets_pricing#2","supply_demand_durability#1","supply_demand_durability#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"7–8 月營收合計約 21.3 億元，月均約為 2025 年的兩倍；液冷與燃料電池前八月年增 158%、訂單被客戶追著跑；板換 2026 下半年起出貨美系雲端服務商、中壢 2027 年產能 3 倍；AI 機櫃 2027 年走向單櫃 600kW 以上。若共識兌現，2028 年本益比只剩 23 倍","side_b":"這些都已寫進 2026–2028 年共識，現價高於 8 月法人目標價；買進是在賭共識再上修，而上修取決於兩家客戶","ruling":"反駁。觀望的約束是價格：論點本身成立，但現價已預付共識路徑，三情境加權五年合計報酬約 +2%，卻要承擔 −50%～−75% 的最大回撤","evidence_level":"公司營收公告＋媒體轉述","settle_metric":"股價與熱能產品月營收年增","if_then":["若股價 ≤1,000 元且熱能產品月營收年增為正，則重跑研究、首倉 ≤3%","若 FY2028 共識 EPS 再上修 20% 以上且 2027 上半年季營收站上 45 億元，則重跑研究；證據到位前不追"],"evidence_refs":["end_markets#0","end_markets#1","supply_demand_durability#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"需求結構轉好：液冷成為 AI 基礎設施基線、CDU 市場預測年化 19%～33%、現行 CDU 仍以板式熱交換器為核心元件、Bloom 產能 1GW→2GW","side_b":"客戶結構偏負：成長集中在兩家客戶；液冷商模往 Manifold 與系統 ODM 延伸，利潤率可能被稀釋；競爭份額資料事實表未涵蓋","ruling":"雙向拉鋸：需求結構轉好、客戶結構集中；競爭是否惡化沒有份額證據可判","evidence_level":"市調摘要＋產品規格書＋媒體報導","settle_metric":"年報主要客戶占比、分部毛利率","if_then":["若 2027 年報最大單一客戶占比降到 40% 以下，則客戶結構改判轉好，執行分維持 7","若最大客戶占比上升或 Bloom 占比揭露超過 40%，則熊市機率提到 35%"],"evidence_refs":["substitute_technology#0","end_markets#6","channel_business_model_shift#0"]},{"axis":"2026 年 EPS 預估分歧","cause":null,"prior_field":null,"side_a":"共識快照 20.74 元、9 月法人預估 21.00 元","side_b":"6 月另一份法人預估 25.00 元、Money Weekly 引述 17.05 元，最高最低相差約 1.47 倍","ruling":"可調和：分歧未到 2.5 倍，不因此下調倉位上限，但預估品質低；基準起點取 19.5 元（偏共識下緣），因 2026 Q2 營益率 12.87% 低於 TTM、上半年已有一季落空","evidence_level":"媒體轉述法人預估＋共識快照","settle_metric":"2026 全年 EPS（2027 年 3 月年報）","if_then":["若 2026 年 EPS ≥21 元，則基準起點上調","若 2026 年 EPS 低於 18 元，則 2027 年基準 EPS 下修到 27 元"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","end_markets#4"]}],"triggers":[{"n":1,"text":"2026 全年營收未達 110 億元，下修基準 EPS 路徑 15%","type":"假設驗證","maps_to":"H1","metric":"2026 全年營收","threshold":"≥110 億元","action":"未達則下修基準情境並重估","source_freq":"月營收（每月）","date":"2027-01-10"},{"n":2,"text":"單季毛利率跌破 25% 連 2 季，擴產稀釋獲利率","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"<25% 連 2 季","action":"不追；基準終端倍數由 25 倍降到 20 倍","source_freq":"季報（每季）","date":null},{"n":3,"text":"Bloom Energy 下修全年財測或延後 2GW 產能目標","type":"風險","maps_to":"R1","metric":"Bloom 年度產能目標與全年財測","threshold":"2GW 延後或財測下修","action":"熊市機率由 30% 提到 40%；若持有則減碼一半","source_freq":"Bloom 季報（每季）","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"]},{"n":4,"text":"單季營收季減超過 20% 連 2 季，平台交替遞延變成常態","type":"風險","maps_to":"R2","metric":"單季營收季增率","threshold":"<−20% 連 2 季","action":"若持有則減碼一半；未持有則延後重跑研究","source_freq":"季報（每季）","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":5,"text":"最大液冷客戶下一代平台轉單，或熱能產品月營收連 3 個月年減","type":"Single Thing","maps_to":"Single Thing","metric":"熱能產品月營收年增率／主要客戶變動","threshold":"連 3 個月 <0%，或公司證實主要客戶轉單","action":"若持有則清倉；未持有則移出名單","source_freq":"月營收（每月）、法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"FY2027 共識 EPS 跌破 35 元，共識路徑開始鬆動","type":"風險","maps_to":"R4","metric":"FY2027 共識 EPS","threshold":"<35 元","action":"不追；熊市機率提到 40%","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#2"]},{"n":7,"text":"股價回到 1,000 元以下且熱能產品月營收年增仍為正","type":"估值rearm","maps_to":"rearm_trigger","metric":"股價／熱能產品月營收年增","threshold":"≤1,000 元且年增 >0%","action":"重跑研究，首倉 ≤3%","source_freq":"每日股價、每月營收","date":null},{"n":8,"text":"2026 Q3 財報複審：平台交替後是否重返成長","type":"複審日期","maps_to":"H1","metric":"2026 Q3 單季營收與毛利率","threshold":"營收 ≥30 億元、毛利率 ≥26%","action":"重估基準 EPS 路徑","source_freq":"季報","date":"2026-11-15"}],"kill_metrics":[{"metric":"熱能產品（液冷＋燃料電池）月營收年增率","bear_threshold":"連續 3 個月 <0%","window":"2026-10 至 2027-12，每月","source":"公司月營收公告（公開資訊觀測站）","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"<25% 連 2 季","window":"2026 Q3 至 2027 Q4","source":"公司季報","last_status":"ok"},{"metric":"Bloom Energy 年度產能目標","bear_threshold":"2GW 目標延後或全年財測下修","window":"2026 Q4 至 2027 Q4","source":"Bloom Energy 10-Q／季報","last_status":"warning"},{"metric":"年度自由現金流與營益率","bear_threshold":"2027 年自由現金流為負且營益率 <14%","window":"FY2027","source":"公司年報","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤1,000 元（三情境加權五年年化約 12%）且熱能產品月營收年增仍為正；兩者同時成立才重跑研究","exec_line":"觀望不追。約束是價格：現價已預付共識路徑。重啟條件成立後重跑研究，首倉 ≤3%；Bloom 下修擴產或最大液冷客戶轉單則移出名單","holding_cap":"首倉 ≤3%；最大回撤範圍 −50%～−75%，客戶集中未解前總倉位不超過 5%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"共識 2028 年 EPS 74.35 元等於要求營收放大到 2025 年的 7～8 倍、新產能近乎零閒置且毛利率不降；市場把兩家主力客戶的擴產計畫當成確定營收","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤1,000 元且熱能產品月營收年增仍為正"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"requires_critic":[],"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=共識 2028 年 EPS 74.35 元等於要求營收放大到 2025 年的 7～8 倍、新產能近乎零閒置且毛利率不降；市場把兩家主力客戶的擴產計畫當成確定營收"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=69.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}]},"thesis":{"H":[{"id":"H1","text":"液冷與燃料電池（熱能產品）維持高速成長，帶動 2026 年營收站上 110 億元、2027 年再年增五成以上","2y":"2026 年營收 ≥110 億元；2027 年營收 ≥165 億元","5y":null,"10y":null,"threshold":"2026 全年營收 ≥110 億元、2027 年營收年增 ≥50%","source":"公司每月營收公告、季報","drift_rule":"兩年期：TTM 營收連 2 季低於門檻路徑 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H2","text":"擴產期間獲利率守得住：3～6 倍新產能爬坡時，毛利率不跌破 26%、營益率維持 15% 以上","2y":null,"5y":"2027–2030 年度毛利率 ≥26%、營益率 ≥15%","10y":null,"threshold":"年度毛利率 ≥26%、營益率 ≥15%（2025 年為 27.34%、15.87%）","source":"季報、年報","drift_rule":"五年期：TTM 營益率連 4 季低於門檻 5% 以上為削弱，連 6 季低於 10% 以上為反轉"},{"id":"H3","text":"客戶基礎分散：板換打進美系雲端服務商後，液冷不再只靠單一伺服器品牌，燃料電池以外出現第二個大客戶","2y":null,"5y":"2028 年年報最大單一客戶占營收 ≤40%","10y":null,"threshold":"年報揭露的最大單一客戶占比 ≤40%（現值事實表未涵蓋）","source":"年報主要客戶揭露、公司法說","drift_rule":"五年期：連兩份年報最大客戶占比上升為削弱，連三份上升為反轉"}],"R":[{"id":"R1","text":"燃料電池主力客戶 Bloom Energy 放緩擴產，或因會計爭議影響融資與訂單，燃料電池營收出現斷層","h_ref":"H1","clock":"🔥","threshold":"Bloom 下修全年財測或延後 2GW 產能目標；高力熱能產品月營收連 3 個月年減","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"]},{"id":"R2","text":"最大液冷客戶在 AI 平台交替時拉貨遞延（2026 Q2 已出現），或下一代平台分單給他廠","h_ref":"H3","clock":"⚡","threshold":"單季營收季減超過 20% 連 2 季（2026 Q2 約季減 33%）","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"擴產 42.5 億元加私募 9,000 張（約 9.7% 稀釋）後，新產能利用率不足，增量報酬掉到資金成本附近","h_ref":"H2","clock":"🐢","threshold":"2027 年自由現金流為負且營益率 <14%","evidence_refs":["supply_demand_durability#1"]},{"id":"R4","text":"賣方預估品質低，2026 年 EPS 預估從 17.05 到 25.00 元，共識三年路徑可能大幅下修","h_ref":"H1","clock":"⚡","threshold":"FY2027 共識 EPS 跌破 35 元","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"最大液冷客戶（單一美系伺服器品牌）在下一代 AI 平台把熱交換器改由他廠供應或自製","why_fatal":"法人估液冷占 2026 年營收約 51%，且集中在這家客戶；失去一代平台等於營收砍掉近半、新產能閒置，2027–2028 年共識 EPS 全面失效","if_happens":"若持有則清倉；未持有則移出名單，基準 EPS 路徑改用熊市情境","how_monitor":"熱能產品月營收年增率、季報毛利率、公司法說與年報主要客戶揭露；板換對美系雲端服務商的出貨能否補位","probability":"15%～20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":41.86,"peg_fy2":0.51,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":8.93,"FY2026E":20.74,"FY2027E":40.85,"FY2028E":74.35},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（新台幣）；共識為 Koyfin 快照，美元依 2026-10-09 匯率 31.912 換算"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 Q3 財報：平台交替後首季，檢驗是否重返成長","impact":"高","watch":"單季營收 ≥30 億元、毛利率維持 26% 以上"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"Bloom Energy 第三季財報與 2GW 產能進度","impact":"高","watch":"全年財測是否維持、產能擴張是否延後"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"板式熱交換器對美系雲端服務商開始出貨","impact":"中","watch":"板換月營收年增是否由約 19% 加速"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"橋頭廠部分投產、中壢廠產能達目前三倍","impact":"高","watch":"新產能開出後毛利率是否守住 26%"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
