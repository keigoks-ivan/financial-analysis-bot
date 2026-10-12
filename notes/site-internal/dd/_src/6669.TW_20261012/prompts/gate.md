你是 DD 管線 v20 的判斷層閘（gate），標的 6669.TW（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（28 條）
- `f_kpi0_ifrs`（q1_business）｜合併營收（IFRS）＝278.153 十億 NT$｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿 wiwynn.com/news/wiwynn-reports-second-quarter-2026-financial-results（YoY +26.0%）；QoQ +0.59% 為上半年 554.660 − Q2 278.153 = Q1 276.507 推算（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無營收共識
- `f_kpi1`（q1_business）｜毛利率＝9.3 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；公司歸因＝記憶體代採購模式移出營收與成本＋新產品導入帶來較高 NRE 收入（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無毛利率共識
- `f_kpi2_ifrs_non_gaap`（q1_business）｜營業利益率（IFRS，緯穎不揭露 Non-GAAP）＝7.3 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；新聞稿未列營業利益金額（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：查無營益率共識
- `f_kpi3_pat_eps`（q1_business）｜稅後淨利（PAT）／基本 EPS＝14.969 十億 NT$（EPS NT$80.43）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）；PAT 年增 23.5%，PAT margin 5.4%；Q2 2025 EPS NT$65.23（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-07））
  - 註記：凱基事前預估 EPS 82.01 元（來源：KGI 報告 2026-07-28，實際略低於該預估）；非全市場共識
- `f_kpi4`（q1_business）｜管理層指引（下一季／全年）＝無量化指引｜期間與口徑：Q2 2026（公告於 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：緯穎 IR 新聞稿（同上）：僅表示對 AI 與資料中心市場長期成長樂觀，未給營收／利益率區間；並提及 AI 產品組合變化與零組件成本上升，正與客戶調整商業模式（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（公告於 2026-08-07））
  - 註記：不適用
- `f_kpi5`（q1_business）｜下半年資本支出預算＝942 百萬 US$｜期間與口徑：董事會 2026-08-07 核准（2026 下半年）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：緯穎 IR 新聞稿（同上）：主要用於電力基礎設施、設備、土地與廠房；同時核准首次國內無擔保可轉債上限 NT$150 億與 US$15 億聯貸（numbers.latest_quarter_kpis.items[5]，as_of 董事會 2026-08-07 核准（2026 下半年））
  - 註記：不適用
- `f_peer_6669_tw_gross_margin_pct`（q2_moat）｜6669.TW 毛利率＝8.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6669_tw_operating_margin_pct`（q2_moat）｜6669.TW 營業利益率＝6.62 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6669_tw_fcf_margin_pct`（q2_moat）｜6669.TW FCF 利潤率＝-5.84 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6669.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2382_tw_gross_margin_pct`（q2_moat）｜2382.TW 毛利率＝5.54 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2382.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2382_tw_operating_margin_pct`（q2_moat）｜2382.TW 營業利益率＝3.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2382.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3231_tw_gross_margin_pct`（q2_moat）｜3231.TW 毛利率＝5.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3231.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3231_tw_operating_margin_pct`（q2_moat）｜3231.TW 營業利益率＝3.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3231.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_smci_gross_margin_pct`（q2_moat）｜SMCI 毛利率＝10.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SMCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_smci_operating_margin_pct`（q2_moat）｜SMCI 營業利益率＝7.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SMCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝120.95 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝179.98 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝226.58 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝23.2 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝2275.0 TWD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.128 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝18.52 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 120.95，分子＝快照價 2240.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.14 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.21 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝91.56 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Q1 2026 營收 NT$276.5B（YoY +62%），毛利率 7.6%；與鴻海、廣達、英業達等 ODM 同樣出現營收增速高於毛利增速
  - 來源：Borecraft：AI server ODMs are running into awkward math（as_of 2026-05-01）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：Quartr Q1 2026 摘要指客戶集中度與訴訟為風險；以美國為主要市場
  - 來源：Quartr Wiwynn (6669) Q2 2026 earnings summary（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：CMoney 研究筆記稱緯穎營收 Meta 占 52%、Microsoft 占 34%、其他 14%（合計兩大客戶 86%）；為 2024 年資料，非 2026 年揭露，as_of 為約略年份
  - 來源：CMoney 研究筆記 note-detail nid=782415（經搜尋摘要轉引）（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：Quartr 2026 Q1 摘要將客戶集中與訴訟列為風險，未給占比
  - 來源：Quartr, Wiwynn (6669) Q2 2026 earnings summary（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：Goldman估計2027年需約4,000億美元投資級債券發行支應建置，且五大hyperscaler每年需約3,000億美元AI相關營收才能打平基礎設施投資（融資風險面）。
  - 來源：roic.ai: Goldman Sachs sees AI capex at 12 trillion by 2027 fueling debt financed buildout（as_of 2026-09-25）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：緯穎產能分布：墨西哥占總產能 70%、馬來西亞 20%、歐洲 10%；德州第二棟廠明年量產後，美國產能預計占 20%。
  - 來源：Taipei Times, 2026-09-18 Wiwynn Texas plant report（as_of 2026-09-18）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年報導：墨西哥產出因 USMCA 待遇避開部分關稅；有客戶要求停止自墨西哥出貨、改由捷克或馬來西亞工廠供應（摘要轉述，未取得原文）。
  - 來源：Taipei Times / Taiwan News 2025 coverage (search summary)（as_of 2025-03-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Q1 2026 毛利率 7.6%（Q4 2025 為 7.2%）；GPU與DRAM價格推升營收但毛利未同步；4月起部分客戶改由雲端客戶直購記憶體、記憶體不計入營收，4月營收月減16%；Q1 78%銷售來自美洲；ODM-direct 約占 Q1 2026 伺服器營收 50.2%（IDC）；緯穎在台灣五大AI伺服器ODM中Q1營收排第四
  - 來源：Borecraft / Digitimes 2026-06-15 (secondary)（as_of 2026-06-15）｜affects：decision_inputs.bear、moat_trend、valuation
- `ems_utilization_capex_cycle#0`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：Amazon 與緯穎於 2026-09-09 表示德州 Socorro 伺服器製造據點投資額已超過 US$1.6 billion（2025-06 首次揭露為 US$152 million）；報導未說明 Amazon 是否共同出資。
  - 來源：CTOL, Wiwynn's $1.6B Texas Expansion: Amazon Gets the Capacity, Wiwynn Takes the Risk（as_of 2026-09-09）｜affects：thesis.R、decision_inputs.bear、valuation
- `ems_roic_asset_turnover_benchmark#0`（ems_roic_asset_turnover_benchmark｜方向 -｜狀態 ok）：Wiwynn 2026Q1末存貨約NT$229.2B（較上季+68%），應收約NT$91.8B；存貨堆高拉長現金循環（僅事實，未見官方CCC數字）
  - 來源：Wiwynn 26Q1 investor conference presentation (2026-05-07)（as_of 2026-05-07）｜affects：decision_inputs.bear、valuation
- `ems_roic_asset_turnover_benchmark#1`（ems_roic_asset_turnover_benchmark｜方向 -｜狀態 ok）：StockAnalysis資產負債表：2026/3/31總資產約NT$432.6B（FY2025末NT$338.2B），存貨約NT$229B（前期NT$136B），應付帳款NT$152.6B
  - 來源：StockAnalysis Wiwynn balance sheet（as_of 2026-03-31）｜affects：decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":5520,"bear_5y_price":1125,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":34.3,"ev5y_pct":35.9,"irr_base_pct":6.1,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":120.95,"pe":18.81,"basis":"FY1（2026 年）Koyfin 共識 EPS，與判斷日股價同一每股口徑；終端倍數同樣套用在終端年當年 EPS"},"eps":{"bull":[195,250,285,315,345],"base":[172,200,205,220,235],"bear":[150,120,105,115,125]},"pe":{"bull":16,"base":13,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.128,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 4 | 3 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | found | 2 | 4 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | none | 0 | 5 |
| ems_utilization_capex_cycle | found | 2 | 3 |
| ems_roic_asset_turnover_benchmark | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：6669.TW Wiwynn antitrust OR monopoly investigation 2026；Wiwynn regulation OR regulatory scrutiny Computer Hardware 2026；6669.TW Wiwynn DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）：Wiwynn product substitute technology threat 2026；Wiwynn AI server rack ASIC custom silicon liquid cooling competition ODM direct 2026
- **major_events**（none）：6669.TW Wiwynn acquisition merger 2025 2026；6669.TW Wiwynn class action lawsuit securities fraud；6669.TW Wiwynn clinical trial FDA approval 2025 2026；6669.TW Wiwynn product launch recall warning letter；6669.TW Wiwynn SEC investigation restatement

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"6669.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"緯穎科技 Wiwynn"},"oneliner":"緯穎是直供 hyperscaler 的 ASIC 機櫃龍頭 ODM，營業利益率高於台系同業；但前兩大客戶占營收八成以上、自由現金流連年為負，倍數也在自身高檔、循環偏晚段。結論是不追，等股價回落或擴張轉成現金再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺的是 hyperscaler 自建 AI 與通用伺服器的機櫃設計整合費，錢卡在兩個節點：客戶的 capex 決策，以及上游 GPU、ASIC、記憶體的供應。","reasoning":"最新一季（2026 年第二季）營收 2,781.53 億元，年增 26.0%；毛利率 9.3%，營業利益率 7.3%，稅後淨利 149.69 億元。公司沒有給量化財測。營收結構方面，2025 年 AI 伺服器與通用伺服器各占約一半，AI 伺服器裡 ASIC 約占九成；管理層預期 2026 年 AI 占比過半。Q2 的年增率看起來放緩，有一部分是會計口徑造成：4 月起部分客戶的記憶體改由緯穎代採購，金額不再計入營收與成本。單點依賴是本案的核心風險而不是護城河。2024 年資料顯示 Meta 占 52%、Microsoft 占 34%，合計 86%；另有外資估計 AWS 相關 ASIC 份額約七成。產業時鐘判在擴張期（II）：TrendForce 估 2026 年 AI 伺服器出貨年增逾 28%，北美前五大 CSP capex 年增約 40%，記憶體與 CoWoS 都仍供不應求。供需持久度屬週期性，供不應求可延續到 2027 下半年至 2028 上半年；Goldman 預估 2028 年 capex 成長放緩到 12%，之後有反轉風險。","fact_refs":["f_kpi0_ifrs","f_kpi1","f_kpi2_ifrs_non_gaap","f_kpi3_pat_eps","f_kpi4","f_kpi5"],"verdict_values":{"revenue_quality":"營收裡有大量零組件轉嫁（GPU、記憶體），成長率會被零組件價格放大。4 月起部分記憶體改為代採購、不入帳，營收增速因此被壓低，毛利率百分比則被抬高；Q2 的 NRE 收入屬新產品導入的一次性項目。","unit_econ_note":"每座機櫃賺的是整合、測試與交付費，加上專案 NRE；毛利率長期落在 8%–10% 之間，獲利靠出貨量和營運資金周轉，不靠單價。","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"直供 hyperscaler 的機櫃級 ODM：毛利率個位數，營運資金與產能都吃資本，營收跟著少數客戶的 capex 週期走"},"industry":{"clock_phase":"II","sd_verdict_source":"屬週期性。TrendForce 估記憶體 2027 下半年才緩解；Goldman 估供需最早 2027 下半年平衡，2028 年 capex 成長放緩到 12%；Morgan Stanley 估 2028 年 capex 上看 1.4 兆美元。","bargaining":{"up":"上游 GPU、記憶體、先進封裝都是賣方市場，緯穎是價格接受者，只能與客戶協商成本轉嫁","down":"客戶是少數 hyperscaler，2024 年前兩大客戶合計 86%，議價權在客戶手上","geo":"產能墨西哥七成、馬來西亞兩成、歐洲一成；德州第二棟廠 2027 年量產後，美國產能約占兩成"},"profit_pool_dir":"利潤池往晶片、記憶體與封裝端集中。客戶透過直購與代採購把帳面營收移出 ODM，整合費比重小，資本負擔卻往 ODM 移。","tam_table":{"expanded":false,"reason":"事實表只有產業層級的出貨量與 capex 數字，沒有緯穎可服務市場規模與份額的五年序列，無法組出五年前到現在的對照表；份額證據只有單一客戶的外資推估"}}}},"q2_moat":{"verdict":"護城河方向持平，等級 C。執行力領先台系同業，定價權有限，價值鏈分配正往客戶端移動。","reasoning":"機制：緯穎直接替 hyperscaler 設計並整合 ASIC 機櫃，電力容量已鎖到 2028 年，在客戶下一代平台的導入速度有優勢。可證方向用利潤率差距衡量：近十二個月營業利益率 6.62%，對廣達 3.34%、緯創 3.8% 高約 3 個百分點；毛利率 8.2%，對兩家的 5.54%、5.85% 也較高；只略低於 SMCI 的 7.09%。不給向上的理由：自身營業利益率由 2024 年 7.8% 降到 6.62%，ROCE 由五年前 38% 降到 23%（2024 年資料）。不給向下的理由：最大客戶份額沒有下滑的來源證據，外資仍估 AWS 相關份額約七成。子評分：執行力 7、定價權 5。當期 ROIC 事實表未涵蓋（缺廠房設備與投入資本口徑）。產業態勢判為雙向拉鋸：競爭面，台系 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大 AI 伺服器 ODM 裡排第四；結構面，供不應求延續到 2027 下半年；其他結構變數是客戶改直購記憶體，以及德州據點擴大投資由緯穎承擔。","fact_refs":["f_peer_6669_tw_gross_margin_pct","f_peer_6669_tw_operating_margin_pct","f_peer_6669_tw_fcf_margin_pct","f_peer_2382_tw_gross_margin_pct","f_peer_2382_tw_operating_margin_pct","f_peer_3231_tw_gross_margin_pct","f_peer_3231_tw_operating_margin_pct","f_peer_smci_gross_margin_pct","f_peer_smci_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"直供 hyperscaler 的 ASIC 機櫃設計與整合能力，加上提前鎖定的高功率廠房電力容量；換供應商要多走一個平台世代的驗證","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"對台系同業的營業利益率差距約 3 個百分點仍在，但自身營益率由 2024 年 7.8% 降到 6.62%，ROCE 也由 38% 降到 23%；最大客戶份額沒有下滑的來源證據。執行力判穩定，定價權判穩定偏弱，合判持平","competitor_notes":[{"name":"2382.TW 廣達","strategy_note":"營業利益率 3.34%，約為緯穎一半，靠 GPU 機櫃規模取勝，利潤結構較薄"},{"name":"3231.TW 緯創","strategy_note":"營業利益率 3.8%，自由現金流率 −8.93% 比緯穎更吃資本；外資提到它可能是緯穎的組裝備援"},{"name":"SMCI","strategy_note":"毛利率 10.82%、營益率 7.09% 略高於緯穎，但自由現金流率 −17.85% 最差；走品牌與通路，不是直供 ODM"}],"spread_notes":{"operating_margin":"對廣達約 +3.3 個百分點、對緯創約 +2.8 個百分點、對 SMCI 約 −0.5 個百分點；ROIC 差距事實表未涵蓋"},"peer_na_reason":null,"threats":[{"level":"🔴","text":"客戶把價值鏈往自己拉：部分記憶體改為客戶直購；德州據點投資放大到 16 億美元以上，報導未說明 Amazon 是否出資，ODM 只拿整合費卻要扛資本風險","p":35,"evidence_refs":["ems_utilization_capex_cycle#0","end_markets#4"]},{"level":"🟡","text":"同業擠壓：台系 AI 伺服器 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大裡排第四，廣達、鴻海的 GPU 機櫃規模更大","p":40,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"大客戶第二供應來源：日系外資提到緯創可能作為 L10 配額備援，目前不是明確的第二供應商認定","p":25,"evidence_refs":["customer_second_source#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是 hyperscaler 本身，三個角色一致。需求急迫，但急迫不等於持久：Goldman 估 2027 年五大 capex 約 1.2 兆美元、2028 年成長放緩到 12%，而且每年要約 3,000 億美元 AI 營收才能打平"},{"item":"決策層級","level":"🟡","text":"替代性要在每一代機櫃專案的主供決定上衡量，不是看市場上有幾家 ODM。每代平台都要重新認證，客戶有能力切換，換供應商的代價是一個平台週期的驗證時間。讀數：外資估 AWS 相關份額約七成；續約率與合約年限事實表未涵蓋"},{"item":"價值鏈分配","level":"🔴","text":"整條鏈的利潤集中在晶片、記憶體與先進封裝，ODM 毛利率在 8% 上下。客戶自 2026 年 4 月起把部分記憶體改為直購，德州據點投資卻由緯穎承擔。讀數：近十二個月毛利率 8.2%、自由現金流率 −5.84%"},{"item":"社會容忍度","level":"🟡","text":"伺服器整合價格沒有民生敏感度，社會不會限制定價；風險在政策面。美國 232 條款對先進晶片衍生品課 25%（美國資料中心用途可豁免），鋁鋼銅關稅擴大，墨西哥產出又依賴 USMCA 待遇"}],"roiic":"約 24%，且在下滑。2024→2025 年淨利增加 283 億元，對應前一年再投資 479 億元約 59%、當年再投資 657 億元約 43%；以 2026 年共識淨利 667.97 億元計，增量淨利 157 億 ÷ 2025 年再投資 657 億 ≈ 24%","reinvest_rate":"2025 年約 128%（再投資 657 億 ÷ 淨利 511 億），2024 年約 210%；再投資以淨利減自由現金流計，用淨利代替稅後營業利益","endo_ceiling":24,"formula_note":"內生成長上限 = 增量報酬約 24% × 再投資率（封頂 100%）≈ 24%。超過 100% 的再投資靠可轉債與聯貸支應，不算內生"}}}},"q3_growth":{"verdict":"Y5 之後的成長跑道屬中等：ODM 直供模式已占伺服器營收約一半，看不到 AI 機櫃以外的第二條曲線。","reasoning":"成長來源以量為主：機櫃出貨量，加上 GPU、ASIC 內容增加帶動的單機價值；價格面多半是零組件轉嫁，不是議價。共識 EPS 三年路徑為 FY2026 120.95、FY2027 179.98、FY2028 226.58 元。基期取判斷日股價 2,275 元 ÷ trailing 本益比 23.2 ≈ 98.06 元，三年 CAGR 約 32.2%。內生天花板約 24%，缺口約 8 個百分點，無法歸因於利潤率擴張、淨回購或收購，實際是靠可轉債與聯貸撐起超過內生資金的再投資，屬依賴re-rate，長期信心上限為中。跑道方面，IDC 估 ODM 直供已占 Q1 伺服器營收約 50.2%，落在 35%–70% 區間；AMD Helios 是新客戶，不是新曲線，所以判中等，約五年。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_price_at_dd","f_kpi0_ifrs","f_peer_6669_tw_fcf_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（機櫃出貨與單機內容），價多為零組件轉嫁；無併購、無回購","runway_years":5,"runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 24% × 再投資率封頂 100%；共識三年 CAGR 約 32.2% 超出天花板約 8 個百分點，靠外部融資補足","segments":[{"item":"AI 伺服器","value":"2025 年約占營收一半，其中 ASIC 約九成；管理層預期 2026 年過半"},{"item":"通用伺服器","value":"2025 年約占一半；Nomura 預期 2026 年出貨年增 20%–30%，管理層稱各季出貨年增"}],"decay_signals":["自由現金流對淨利連兩年低於 0.75：2024、2025 年自由現金流都是負值（亮燈）","毛利率年度下滑：2024 年 10.37% 降到 2025 年 8.25%；季度年比連兩季的資料事實表未涵蓋（半亮）","其餘八類事實表未見亮燈：核心市占、提價後銷量、EPS 與營收增速差、員工股票酬勞、TAM 被替代、產業倍數下移、維護性資本支出、停止投資，均無資料或不成立"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：擴張速度超過內生現金，靠可轉債與聯貸支應。","reasoning":"自由現金流轉換率為負：2024 年自由現金流 −251 億元、淨利 228 億元；2025 年自由現金流 −146 億元、淨利 511 億元；近十二個月自由現金流率 −5.84%。2026 下半年資本支出預算 9.42 億美元，用於電力、設備、土地與廠房；同時核准上限 150 億元國內無擔保可轉債與 15 億美元聯貸。股息殖利率 2.13%。三項計分：近年沒有重大收購，收購報酬不適用；回購紀錄事實表未涵蓋，而且籌資方向與回購相反；員工酬勞股數事實表未涵蓋，可轉債將來有稀釋。現金去向四分與債務到期結構事實表未涵蓋。流動比率約 1.32 倍，短期償債沒有壓力。","fact_refs":["f_kpi5","f_peer_6669_tw_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事件軸查無重大收購"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄；公司正以可轉債與聯貸籌資，方向與回購相反"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"員工酬勞股數事實表未涵蓋；上限 150 億元可轉債若轉換會有稀釋，但市值與轉換價未列，無法精算"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；事實表只有股息殖利率 2.13%，沒有股息與回購的歷年明細，無法展開"}}}},"q5_valuation":{"verdict":"現價要成立，需要 2027 年 EPS 照共識成長約 49%、2028 年再成長約 26%，而且市場仍給 12 倍以上。前半段我信，後半段不信。","reasoning":"同一每股口徑下，前瞻本益比 FY2026 為 18.5 倍、FY2027 為 12.6 倍，PEG 約 0.58（18.52 ÷ 三年 CAGR 32.2）。若共識兌現，這個價位不算貴。不過 trailing 本益比 23.2 倍、市銷率 1.14、EV/S 1.21，三者都在自身四個年度端點的最高位；26 週已漲 91.56%。真正的五年分位事實表未涵蓋。上檔推算如下。短期：2027 年基本情境 EPS 172 元 × 14 倍 = 2,408 元，約 +5.8%。五年：2031 年基本情境 EPS 235 元 × 13 倍 = 3,055 元，約 +34.3%，年化約 6% 加股息。外資目標價 6,600–7,568 元是另一套每股口徑，不能直接拿來和現價比較。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_week26_return_pct","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3"],"verdict_values":{"valuation":{"basis":"前瞻本益比（Koyfin FY1 共識，與判斷日股價同口徑），輔以 PEG","tier":null,"peers":{"expanded":false,"reason":"事實表只有同業的利潤率，沒有同業本益比，無法組成同層級的倍數對照"},"fwd_pe":18.52,"peg":0.58,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 18.5 倍與 12.6 倍、PEG 0.58，若共識兌現不算貴；但 trailing 各倍數都在自身四個年度端點的最高位，獲利處在客戶 capex 高峰，每股口徑也有爭議，便宜的論證不成立，結論是合理偏滿。五年分位事實表未涵蓋，四個年度端點中位於最高","upside_short_pct":5.8,"upside_mid_pct":34.3,"denominator_disputed":true,"denominator_note":"分母有兩層爭議。第一是每股口徑：公司新聞稿 Q2 EPS 80.43 元、FactSet 2026 EPS 348.72 元，與判斷日股價 2,275 元、Koyfin FY1 120.95 元相差約 2.9 倍；本判斷只用後者這一套。第二是 2026–2027 年 EPS 落在 hyperscaler capex 高峰，高峰獲利配上低倍數不等於便宜"}}},"q6_how_wrong":{"verdict":"最可能看錯在 2028 年：客戶 capex 放緩時，現在堆起來的存貨、德州廠與可轉債會同時變成負擔。","reasoning":"空頭路徑寫在反證紀錄的論點失敗那一條。最大回撤推算：過去四年唯一的下行年是 2023 年，營收年減 17.4%；空頭情境 2029 年 EPS 105 元 × 9 倍 = 945 元，較現價約 −58%；26 週漲 91.56% 若回吐一半，約 −24%。歷史最大回撤序列事實表未涵蓋。價值陷阱判黃燈：自由現金流連兩年為負屬亮燈，毛利率年度下滑為半亮。","fact_refs":["f_week26_return_pct","f_peer_6669_tw_fcf_margin_pct","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"高成長但現金轉換為負的循環高點"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":120.95,"pe":18.81,"basis":"FY1（2026 年）Koyfin 共識 EPS，與判斷日股價同一每股口徑；終端倍數同樣套用在終端年當年 EPS"},"eps":{"bull":[195,250,285,315,345],"base":[172,200,205,220,235],"bear":[150,120,105,115,125]},"pe":{"bull":16,"base":13,"bear":9},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.13,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-60,"hi":-40,"basis":"下緣：空頭情境 2029 年 EPS 105 元 × 9 倍 = 945 元，約 −58%，取 −60%。上緣：大客戶 capex 只放緩、不削減，倍數由 18.8 倍收斂到 12 倍左右，約 −40%。另有參照：2023 年營收年減 17.4%，26 週漲幅回吐一半約 −24%","trigger_time":null},"basis":{"bull":"AWS 份額維持約七成、AMD Helios 拿到三到四成，2028 年 capex 上看 1.4 兆美元；2027 年 EPS 195 元略高於共識，之後年增率逐步放緩到約一成","base":"2027 年扣掉可轉債利息與稀釋後略低於共識（172 元）；2028 年 capex 成長放緩到 12%，EPS 200 元低於共識 226.58；2029 年消化期持平，之後年增 6%–7%。終端 13 倍對照本身現值前瞻 18.8 倍與 12.6 倍，同業倍數事實表未涵蓋","bear":"2028 年起客戶 capex 進入消化期，毛利率回到 7% 以下，EPS 由 2027 年 150 元降到 2029 年 105 元，之後緩步回到 125 元；成長熄火情境下倍數壓到 9 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Goldman 估五大 hyperscaler 每年需約 3,000 億美元 AI 營收才能打平，2027 年要靠約 4,000 億美元投資級債支應建置，2028 年 capex 成長放緩到 12%","assumption":"客戶 capex 到 2028 年後仍維持高檔","consequence":"2028–2029 年 EPS 回落到 105–120 元、倍數壓到 9 倍，股價約 945–1,080 元，五年虧損過半","ruling":"採納，作為空頭情境主軸，機率 30%。這條與唯一致命點（大客戶轉單）是不同事件，分開計算","watch":"hyperscaler 次年 capex 指引、投資級債發行量、月營收年增率","evidence_refs":["supply_demand_durability#5"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"德州據點投資由 1.52 億美元放大到 16 億美元以上，報導未說明 Amazon 是否出資；Q1 存貨約 2,292 億元，季增 68%；總資產由 3,382 億增到 4,326 億元；自由現金流 2024、2025 年與近十二個月都是負的；董事會核准 150 億元可轉債與 15 億美元聯貸","assumption":"營收成長會帶來對應的現金","consequence":"EPS 成長，但每股自由現金流與資本報酬下滑，可轉債稀釋吃掉部分 EPS 成長","ruling":"採納，這是本次不追的主因之一，用第三條假設（2028 年自由現金流率轉正）驗證","watch":"營業現金流、存貨季增率對營收季增率、可轉債轉換價","evidence_refs":["ems_utilization_capex_cycle#0","ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"],"fact_refs":["f_peer_6669_tw_fcf_margin_pct","f_kpi5"]},{"view":"價格已反映太多","evidence":"26 週漲 91.56%；trailing 本益比 23.2 倍、市銷率 1.14、EV/S 1.21，三者都在自身四個年度端點的最高位","assumption":"高峰獲利的倍數不會收斂","consequence":"就算 2027 年 EPS 達標，倍數從 18.8 倍收斂到 13 倍也會吃掉大部分報酬","ruling":"部分採納。2027 年前瞻 12.6 倍不算貴，但基本情境已假設倍數收斂，五年約 +34%、年化約 6% 加股息，不足以補償循環風險","watch":"股價對 2027 年共識 EPS 的倍數","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 2275.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=2275.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"每股口徑","cause":null,"prior_field":null,"side_a":"公司新聞稿 Q2 EPS 80.43 元、FactSet 2026 EPS 中位數 348.72 元、外資目標價 6,600–7,568 元","side_b":"判斷日股價 2,275 元、Koyfin FY1 共識 120.95 元、trailing 本益比 23.2 倍、股息殖利率 2.13%，兩套每股數字相差約 2.9 倍","ruling":"可調和，屬口徑差異。估值與情境全程只用判斷日股價這一套；外資目標價與新聞稿每股數字不拿來和現價比較","evidence_level":"多源交叉，口徑差異的成因事實表未涵蓋","settle_metric":"公司公告的流通股數或面額變更","if_then":["若查明為股數變動，將外資目標價除以同一比例後再比較","若查明 Koyfin 共識換算有誤，重跑情境樹"],"evidence_refs":[]},{"axis":"毛利率方向","cause":null,"prior_field":null,"side_a":"Q2 毛利率升到 9.3%，公司歸因於記憶體改代採購與新產品 NRE 收入","side_b":"Q1 為 7.6%；台系 ODM 營收增速普遍高於毛利增速，緯穎 Q1 營收在五大裡排第四","ruling":"可調和，屬程度差異。管理層歸因不採信也不否定：代採購只是把營收移出、讓百分比變好看，NRE 屬一次性。標為未證、監測；若 2027 年第一季前連兩季毛利率低於 8%，視為歸因證偽","evidence_level":"公司新聞稿與二手產業報導","settle_metric":"季毛利率與毛利金額年增率","if_then":["若連兩季毛利率低於 8%，下修營益率假設並取消進場條件","若毛利金額年增率連兩季高於營收年增率，承認利潤率改善屬結構性"],"evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"axis":"需求持久度與融資","cause":null,"prior_field":null,"side_a":"記憶體、CoWoS 到 2027 年都供不應求，2027 年五大 capex 約 1.2 兆美元","side_b":"Goldman 估 2027 年要靠約 4,000 億美元債券支應，2028 年成長放緩到 12%","ruling":"可調和，屬時間差。2027 年以前需求有支撐，風險集中在 2028 年，所以基本情境 2029 年 EPS 持平","evidence_level":"賣方研究，多家一致","settle_metric":"五大 hyperscaler 2028 年 capex 指引","if_then":["若 2028 年 capex 指引年增仍高於 20%，空頭機率下修到 25%","若任一家年減逾 10%，取消進場條件"],"evidence_refs":["supply_demand_durability#5"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"2027 年前瞻本益比 12.6 倍、PEG 約 0.58；高盛估 AWS 相關份額約七成，AMD Helios 機櫃可拿三到四成；電力容量已鎖到 2028 年；分析師共識 2027 年營收約 2.1 兆元","side_b":"循環偏晚段，trailing 倍數在自身最高；自由現金流為負，擴張靠外部融資；前兩大客戶占 86%","ruling":"不可調和（買與不買方向相反），選 B 側：不追。依據是增量報酬已由 43%–59% 降到約 24%，新投入資本的報酬在下滑，而 2028 年 capex 成長預估只剩 12%","evidence_level":"財報推算加賣方研究","settle_metric":"股價對 2027 年共識 EPS 的倍數、2027 年共識修正、季營業現金流","if_then":["若股價續漲，但第三季毛利率與存貨沒有改善，則不追","若股價回落到 1,800 元以下，且 2027 年共識 EPS 未下修逾一成，重跑研究後分批反買","若連兩季營業現金流轉正、存貨增速低於營收增速，代表不追的判斷錯了：即使價格未回落，也在 2027 年第二季財報後重跑研究，考慮分批建立","若任一大客戶下修次年 capex 逾一成，取消進場條件，改為迴避"],"evidence_refs":["ems_utilization_capex_cycle#0"]}],"triggers":[{"n":1,"text":"2027 年 EPS 共識守住","type":"假設驗證","maps_to":"H1","metric":"FY2027 共識 EPS","threshold":"較 179.98 元下修逾 10%（低於 162 元）","action":"撤回進場條件，改為迴避並重跑研究","source_freq":"Koyfin 共識快照，每月","date":null},{"n":2,"text":"毛利率被擠壓","type":"風險","maps_to":"R1","metric":"季毛利率","threshold":"低於 7.0%，連兩季","action":"不建倉；已持有則減碼一半","source_freq":"公司季報，每季","date":null,"evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"n":3,"text":"存貨堆積領先營收","type":"風險","maps_to":"R5","metric":"存貨季增率減營收季增率","threshold":"高於 10 個百分點，連兩季","action":"停止加碼；已持有則減碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]},{"n":4,"text":"大客戶下一代專案主供轉給其他 ODM","type":"Single Thing","maps_to":"single_thing","metric":"單一客戶份額或月營收","threshold":"任一大客戶份額掉到三成以下，或月營收連兩月年減","action":"清倉並重跑研究","source_freq":"外資報告、月營收，每月","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":5,"text":"客戶 capex 轉向","type":"風險","maps_to":"R3","metric":"Meta、Microsoft、Amazon 次年 capex 指引","threshold":"任一家年減逾 10%","action":"不追；已持有則減碼","source_freq":"客戶季報，每季","date":null,"evidence_refs":["supply_demand_durability#5"]},{"n":6,"text":"墨西哥產能與關稅","type":"風險","maps_to":"R4","metric":"USMCA 待遇與客戶出貨地要求","threshold":"USMCA 待遇取消，或客戶再次要求停止自墨西哥出貨","action":"停止加碼並重估毛利率","source_freq":"政策公告與公司說明，事件型","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"n":7,"text":"價格回落到可進場區","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2027 共識 EPS","threshold":"股價 1,800 元以下，且 FY2027 共識 EPS 不低於 162 元","action":"重跑研究後小部位分兩批建立","source_freq":"每日股價、每月共識","date":null},{"n":8,"text":"擴張轉成現金","type":"假設驗證","maps_to":"H3","metric":"年度自由現金流率","threshold":"2028 年全年 ≥ +2%","action":"未達則不升級持有","source_freq":"公司年報，每年","date":null},{"n":9,"text":"第三季財報複審","type":"複審日期","maps_to":"H2","metric":"毛利率、存貨、營業現金流","threshold":"毛利率 ≥ 8% 且存貨增速不高於營收增速","action":"未達則維持不追","source_freq":"公司季報","date":"2026-11-15"}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"低於 7.0% 連兩季","window":"2026 年第三季到 2027 年第二季","source":"緯穎季度財報新聞稿","last_status":"ok"},{"metric":"存貨季增率減營收季增率","bear_threshold":"高於 10 個百分點，連兩季","window":"每季滾動","source":"緯穎法說簡報與資產負債表","last_status":"warning"},{"metric":"FY2027 共識 EPS","bear_threshold":"較 179.98 元下修逾 10%","window":"至 2027 年底","source":"Koyfin 共識快照","last_status":"unknown"},{"metric":"大客戶次年 capex 指引","bear_threshold":"Meta、Microsoft、Amazon 任一家年減逾 10%","window":"2027–2028 年","source":"各客戶季度財報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","exec_line":"兩條件同時成立才重跑研究，研究通過後首筆小部位、分兩批進場；期間任一大客戶下修 capex 逾一成即取消","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不追，等股價回落到 1,800 元以下，且 2027 年共識 EPS 未下修超過一成","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=91.56, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 機櫃出貨與 ASIC 份額撐住，2027 年 EPS 達到共識附近","2y":"FY2027 EPS 不低於 162 元（共識 179.98 元下修一成以內）","5y":null,"10y":null,"threshold":"FY2027 共識或實際 EPS ≥ 162 元","source":"公司季度財報新聞稿、Koyfin 共識月快照","drift_rule":"近十二個月 EPS 落後基本情境路徑連 2 季 ≥ 5% 為削弱，連 3 季 ≥ 10% 為反轉"},{"id":"H2","text":"營業利益率持續高於台系同業：近十二個月 6.62%，對廣達 3.34%、緯創 3.8%","2y":null,"5y":"營業利益率 ≥ 5.5%，且對廣達、緯創的差距 ≥ 2 個百分點","10y":null,"threshold":"營益率 ≥ 5.5% 且同業差距 ≥ 2 個百分點","source":"各公司季報","drift_rule":"差距低於 2 個百分點連 4 季為削弱，連 6 季為反轉"},{"id":"H3","text":"擴張轉成現金：自由現金流率由近十二個月 −5.84% 轉正","2y":null,"5y":"2028 年全年自由現金流率 ≥ +2%","10y":null,"threshold":"年度自由現金流率 ≥ +2%","source":"公司年報與季度現金流量表","drift_rule":"近十二個月自由現金流率連 4 季低於 0% 為削弱，連 6 季為反轉"}],"R":[{"id":"R1","text":"毛利率被零組件成本與同業擠壓；Q2 的 9.3% 含一次性 NRE 與代採購的會計效果","h_ref":"H2","clock":"⚡","threshold":"季毛利率低於 7.0%，連兩季","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"id":"R2","text":"客戶集中：2024 年 Meta 占 52%、Microsoft 占 34%，合計 86%；另有財報摘要把客戶集中與訴訟列為風險，訴訟內容事實表未涵蓋","h_ref":"H1","clock":"🔥","threshold":"任一大客戶下一代專案改由其他 ODM 主供","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"id":"R3","text":"hyperscaler capex 2028 年放緩，融資壓力浮現","h_ref":"H1","clock":"🔥","threshold":"Meta、Microsoft、Amazon 任一家次年 capex 指引年減逾 10%","evidence_refs":["supply_demand_durability#5"]},{"id":"R4","text":"產能七成集中在墨西哥，關稅待遇與客戶出貨地要求可能改變","h_ref":"H2","clock":"🐢","threshold":"USMCA 待遇取消，或客戶再次要求停止自墨西哥出貨","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R5","text":"資本風險轉到緯穎：德州據點投資放大到 16 億美元以上，Q1 存貨季增 68%，總資產由 3,382 億增到 4,326 億元","h_ref":"H3","clock":"🔥","threshold":"存貨季增率比營收季增率高 10 個百分點以上，連兩季","evidence_refs":["ems_utilization_capex_cycle#0","ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]}],"single_thing":{"description":"Meta、Microsoft 或 AWS 任一家，在下一代 AI 機櫃專案把主供改給其他 ODM，緯穎份額掉到三成以下","why_fatal":"前兩大客戶 2024 年合計占營收 86%。一家主供專案轉走，等於三到五成營收消失，而德州廠折舊與利息照算；對 EPS 的衝擊大於任何利潤率或關稅情境","if_happens":"不建倉；已持有則清倉並重跑研究","how_monitor":"季報的客戶占比、外資對 AWS 份額的追蹤（高盛估 2026 年約七成）、月營收連兩月年減","probability":"約 15%（12–24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.64,"peg_fy2":0.39,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":98.06,"FY2026E":120.95,"FY2027E":179.98,"FY2028E":226.58},"fy_end_month":12,"eps_basis":"Koyfin 共識（美元依 2026-10-09 匯率 31.912 換成台幣），與判斷日股價同一口徑。基期 98.06 元由判斷日股價 2,275 元 ÷ trailing 本益比 23.2 反推，屬近十二個月口徑，代用 FY2025 實際值；公司年報稀釋 EPS 265.54 元是另一套每股口徑，不混用"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"2026 年第三季財報","impact":"高","watch":"毛利率是否守在 8% 以上、存貨是否續增、營業現金流"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"Meta、Microsoft、Amazon 公布 2027 年 capex 指引","impact":"高","watch":"是否仍高於 2026 年"},{"date":"2027","date_precision":null,"type":"capacity","event":"德州第二棟廠量產，美國產能占比升到約兩成","impact":"中","watch":"折舊增加對毛利率的影響"},{"date":null,"date_precision":null,"type":"other","event":"上限 150 億元國內可轉債發行與 15 億美元聯貸動用","impact":"中","watch":"轉換價與稀釋幅度"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
