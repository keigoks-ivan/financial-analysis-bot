你是 DD 管線 v20 的判斷層閘（gate），標的 3189.TW（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝12496.25 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）；H1 累計 23,601,219 仟元（MOPS，經 Q1+Q2 加總核對相符）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無單季共識
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝26.1 %｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝1670.31 百萬 TWD（利益率 13.4%）｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）；H1 營業利益 2,569,277 仟元（MOPS）（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi6`（q1_business）｜管理層指引（間接，非公司官方數字）＝Q3/Q4 ABF 與 BT 載板均價各季增約 8%；高盛預期 Q3/Q4 營收各季增約 10%、Q3 毛利率 27–29%｜期間與口徑：Q2 2026 法說後（2026-08）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：高盛引述法說內容（媒體轉載 money.udn.com／wantrich.chinatimes.com），未取得公司法說簡報原文（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 法說後（2026-08））
  - 註記：另一法人預估 Q3 營收 QoQ +12.4%、毛利率 27.3%
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-06 date｜期間與口徑：2026-08-06／距今 47 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-06）
- `f_peer_3189_tw_gross_margin_pct`（q2_moat）｜3189.TW 毛利率＝23.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3189_tw_operating_margin_pct`（q2_moat）｜3189.TW 營業利益率＝10.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3189_tw_fcf_margin_pct`（q2_moat）｜3189.TW FCF 利潤率＝7.37 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_gross_margin_pct`（q2_moat）｜3037.TW 毛利率＝19.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_operating_margin_pct`（q2_moat）｜3037.TW 營業利益率＝10.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_fcf_margin_pct`（q2_moat）｜3037.TW FCF 利潤率＝-0.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8046_tw_gross_margin_pct`（q2_moat）｜8046.TW 毛利率＝16.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_8046_tw_operating_margin_pct`（q2_moat）｜8046.TW 營業利益率＝12.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_8046_tw_fcf_margin_pct`（q2_moat）｜8046.TW FCF 利潤率＝7.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝11.26 TWD/share｜期間與口徑：2026-10-12／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-12）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝28.11 TWD/share｜期間與口徑：2026-10-12／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-12）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝53080.62 TWD m｜期間與口徑：2026-10-12／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝78875.57 TWD m｜期間與口徑：2026-10-12／yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_eps`（q4_capital）｜歸屬淨利／稀釋 EPS＝2.56 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（Win 投資快訊記 2.57）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi4_ocf_capex`（q4_capital）｜自由現金流（OCF−Capex）＝315.26 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：不適用
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝1.2 %｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（SBC 20.17 百萬）；僅供參考，Q1 同欄 455 百萬疑含員工酬勞/分類差異，跨季不可比（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-8457.2 TWD m｜期間與口徑：2026-10-12／yfinance 最新一季：總債務 9687.77、現金 18144.97（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝526.91 m shares｜期間與口徑：2026-10-12／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.143 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1060.0 TWD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝182.76 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝18.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝18.1 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝12.48 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.29 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝10.36 x｜期間與口徑：2026-10-12／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝550067.79 TWD m｜期間與口徑：2026-10-12／市值 558524.99 ＋ 淨負債 -8457.2｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝189.72 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝66.15｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：競爭對手欣興在美系 AI ASIC 載板市占據報導超過 70%，Nvidia Blackwell 相關載板市占超過 30%；Ibiden 被視為欣興在高階 ABF 主要對手
  - 來源：經濟日報 money.udn.com（欣興 ASIC 市占）；工商時報 wantrich 2026-06-25（as_of 2026-06-25）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：T-Glass 缺料是景碩目前最大營運限制，估計每月 10%~15% 營收受限；Nittobo 獨供 T-glass 預計 2027 年第 3 季才有擴產
  - 來源：景碩 3189 載板需求 搜尋結果（聯合報系／券商整理）（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：凱基估 2025–28 年全球主要 ABF 載板廠資本支出比上一輪高 51%；景碩 235 億元投資自 2027 年起折舊壓力受關注
  - 來源：KGI PCB sector report 2026-07-20 / 景碩 3189 搜尋結果（as_of 2026-07-20）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：味之素 ABF 增層膜是許多載板廠指定的唯一供應商，市占九成以上；ABF 約占載板原物料成本 25%–30%（產業層面，非景碩專屬揭露）。as_of 為約略值，原文日期未確認。
  - 來源：udn 經濟日報，ABF 載板三雄漲勢吸睛 法人解析成本漲為何帶動股價?（引國泰期貨）（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：玻璃核心基板量產時點說法不一：一份分析報告基準情境為 2030 年量產；2026 年 6 月文章估 2027 年底起大規模導入；GlaSSEM（Samsung Electro-Mechanics 與 Sumitomo Chemical 合資）目標 2027 下半年供貨
  - 來源：AAIG Substack: Glass Core Substrate Sector Research; atlaspcb.com glass core substrate news 2026（as_of 2026-06-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：景碩宣布約196億元專案資本支出（另有報導稱235億元），分三年執行，用於楊梅/幼獅廠新廠房擴 ABF；ABF月產能由約4,000萬顆增至5,000萬顆，新增產能2027年陸續開出；高盛稱目標2029年底前月產能翻倍至8,000萬顆。公司表示196億為專案額度，實際支出視客戶需求彈性調整。
  - 來源：搜尋摘要彙整（含 udn、uanalyze、ctee 報導）；各則確切發布日未能逐一確認（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：同業南電宣布2026年資本支出超過新台幣100億元，聚焦AI/HPC先進載板（二手轉述自 Atlas PCB 引 Taiwan News，2026年5月股東會，未經原始來源查證）。
  - 來源：Atlas PCB news: Nan Ya PCB AI substrate expansion 2026（as_of 2026-05-31）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Counterpoint（2023年7月）：Unimicron、景碩、南電2023Q1表現差，景氣下行比預期更糟，載板谷底可能落在2023Q2或Q3。
  - 來源：Counterpoint Research, ABF substrate demand likely recover H2 2023, BT substrate demand remain weak（as_of 2023-07-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：DigiTimes（2023年11月）：全球IC載板市場2023年預估下滑約30%，ABF需求未如預期回升。
  - 來源：DigiTimes 2023-11-21（as_of 2023-11-21）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：優分析：景碩2023年前三季每股虧損0.7元；2023Q4因子公司晶碩支撐而提早走出谷底；ABF載板Q4營收季增約3成、毛利率由10~15%升至25%（單一來源）。
  - 來源：優分析 uanalyze（as_of 2024-04-01）｜affects：decision_inputs.bear、thesis.R、moat_trend

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1550,"bear_5y_price":180,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-45.3,"ev5y_pct":-40.2,"irr_base_pct":-11.4,"asym_ratio":0.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":11.26,"pe":94.14,"basis":"起點用 FY2026 共識 EPS（FY1）；終端倍數同樣套在預估年度 EPS 上，口徑一致"},"eps":{"bull":[32,42,52,58,62],"base":[26,32,30,27,29],"bear":[20,15,7,6,10]},"pe":{"bull":25,"base":20,"bear":18},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.143,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":2},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | none | 0 | 3 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | none | 0 | 3 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：景碩 3189 最大客戶 第二供應商 ABF載板 2026；Kinsus Interconnect Technology largest customer second-source OR in-house 2026
- **customer_concentration_credit**（none）：景碩 3189 前幾大客戶 營收比重 客戶集中 2026；Kinsus Interconnect Technology customer concentration top customers revenue share 2026；景碩 客戶 NVIDIA 博通 高通 Apple 占比 法說會 2026 載板
- **regulatory_antitrust**（none）：3189.TW Kinsus Interconnect Technology antitrust OR monopoly investigation 2026；Kinsus Interconnect Technology regulation OR regulatory scrutiny Semiconductor Equipment & Materials 2026；3189.TW Kinsus Interconnect Technology DOJ OR FTC OR EU competition 2026
- **channel_business_model_shift**（none）：Kinsus Interconnect Technology 景碩 business model channel shift 2026；景碩 3189 ABF載板 客戶 直接供應 商業模式 2026
- **major_events**（none）：景碩 3189 併購 合併 收購 2026；3189.TW Kinsus Interconnect Technology class action lawsuit securities fraud；景碩 3189 訴訟 裁罰 金管會 重大訊息 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3189.TW","date":"2026-10-12","schema":"v15.0","contract":"v19","company_name":"景碩"},"oneliner":"景碩吃到 ABF 載板缺貨漲價，但 FY2027 共識 EPS 28.11 元已近上輪高峰兩倍，股價仍要 37.7 倍。高峰盈餘配上成長股倍數，2027 年起新產能潮是主要風險，等回檔再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261012/scenario.json","answers":{"q1_business":{"verdict":"賺的是 AI 伺服器 CPU／GPU 與一般運算晶片的載板錢。錢卡在上游兩個獨供節點：T-glass 玻纖布與 ABF 增層膜。產業正處在缺貨漲價的過熱段。","reasoning":"Q2 2026 合併營收 12,496 百萬元，毛利率 26.1%，營益率 13.4%。載板營收 10,382 百萬元，約占合併 83%；其餘約 2,114 百萬元的內容事實表未涵蓋。上半年營收年增 29.8%，Q2 創新高。成長來自三個來源：一是 AI 高層數 ABF，法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%，ABF 稼動率由 86% 升到 95%；二是全產業缺貨帶動報價，法人估 Q3、Q4 均價各季增約 8%；三是稼動率回升。手機與 PC 需求仍弱。AI 相關營收 2026 年約一成，2027 年預期一成五到兩成，所以八成以上營收仍跟著載板週期走。錢卡在上游：T-glass 由 Nittobo 獨供，2027 年第三季才擴產，每月壓住 10%～15% 營收；ABF 膜由味之素供應九成以上。供需持久性判為週期性將反轉：缺口預估 2027～2028 年擴大，但全球載板廠 2025～28 年資本支出比上一輪高 51%，綠地產能 2027 年起開出。產業時鐘判在過熱段，依據是稼動率接近滿載、部分現貨價漲逾三成、各家同步擴產、壓膜機交期排到 2031 年。客戶與分部占比事實表未涵蓋，單一客戶依賴程度無法量化。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi6","f_earnings_recency"],"verdict_values":{"revenue_quality":"營收由報價與稼動率雙升推動，不是長約鎖量。AI 占比僅約一成，其餘隨載板週期漲跌。","unit_econ_note":"毛利改善的原因說法分歧：公司歸因稼動率，法人歸因報價。單價與量的拆分事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY2022→FY2023 營收減 36.8%，EPS 由 14.57 元掉到 0.10 元，再回升到 FY2025 的 3.37 元。走勢由產能建設週期與報價驅動。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。缺口估計 2027～2028 年擴大，但全球載板廠 2025～28 年資本支出比上一輪高 51%，綠地產能 2027 年起開出，T-glass 2027 年第三季擴產。各家缺口預估差距大，2028 年從 16% 到 51% 都有。","bargaining":{"up":"上游 T-glass（Nittobo 獨供）與 ABF 膜（味之素市占九成以上）議價力強，景碩是價格接受者。","down":"缺貨期間景碩對客戶的議價轉強，證據有兩項：長約客戶同意額外產能付款，擴產設備由客戶出資。這個判斷只適用於缺貨期。客戶集中度、前幾大客戶的營收占比與信用狀況，以及客戶的第二供應來源與轉單成本，事實表都查無資料，所以這裡不對客戶集中度下結論。單一客戶風險列為資料缺口，待年報主要客戶揭露後補判。間接線索只有一項：美系 AI CPU 客戶對景碩的供貨率由一成升到五成，代表該客戶同時有其他供應商，份額可以在供應商之間移動；但其他供應商是誰、份額多少，事實表未涵蓋。","geo":"生產據點在台灣、中國蘇州與美國；美國 232 半導體關稅是否涵蓋載板未確認。"},"profit_pool_dir":"利潤池目前流向載板環節（報價上漲、部分現貨漲逾三成）。2027 年後上游獨供材料與新一輪擴產會把利潤收回。","tam_table":{"expanded":false,"reason":"事實表未涵蓋載板市場規模與滲透率。AI GPU 份額兩成只是公司目標，沒有第三方份額序列可建表。"}}}},"q2_moat":{"verdict":"護城河方向持平（→）。執行面在 AI CPU 客戶拿到份額，但定價力來自全產業缺貨，不是景碩獨有。","reasoning":"同業 TTM 比較：景碩毛利率 23.3%，高於欣興 19.9% 與南電 16.0%；營益率 10.1%，與欣興 10.2% 相當、低於南電 12.3%；FCF 利潤率 7.4%，欣興 −0.4%、南電 7.7%。毛利率領先但營益率沒有領先，多出來的毛利被研發（占營收 5.6%）與費用吃掉，看不出結構性成本優勢。與同業的 ROIC 差距無法計算，因為投入資本事實表未涵蓋。執行面往上：AI CPU 客戶供貨率由一成升到五成；公司目標拿下 Vera CPU 載板全部份額、AI GPU 份額升到兩成，但都尚未實現。定價面穩定：漲價來自全產業 T-glass 缺料，欣興與南電同樣受惠。欣興在美系 AI ASIC 載板份額逾七成、Blackwell 相關逾三成，高階 AI 客戶的主供仍是欣興與 Ibiden。產業態勢是雙向拉鋸：競爭面各家同步擴產，南電 2026 年資本支出逾 100 億元；結構面缺貨延續到 2027 年；替代技術面，玻璃核心基板最快 2027 下半年導入，但目前的設計仍保留 ABF 增層。","fact_refs":["f_peer_3189_tw_gross_margin_pct","f_peer_3189_tw_operating_margin_pct","f_peer_3189_tw_fcf_margin_pct","f_peer_3037_tw_gross_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_3037_tw_fcf_margin_pct","f_peer_8046_tw_gross_margin_pct","f_peer_8046_tw_operating_margin_pct","f_peer_8046_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"護城河靠高層數 ABF 的製程良率與客戶認證週期，加上缺貨期的產能可得性。產能這項優勢會隨 2027 年後新產能開出而消退。","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：AI CPU 客戶供貨率由 10% 升到 50%。定價力穩定但屬全產業共享；營益率與欣興相當、低於南電，同業利潤率差距沒有擴大。","competitor_notes":[{"name":"欣興（3037.TW）","strategy_note":"美系 AI ASIC 與 Blackwell 載板主供，擴產最積極，TTM FCF 已轉負，是景碩在高階 AI 客戶的主要對手。"},{"name":"南電（8046.TW）","strategy_note":"營益率 12.3% 為三家最高，2026 年資本支出逾 100 億元，聚焦 AI／HPC 先進載板，屬同步擴產的供給壓力。"},{"name":"Ibiden（4062.T）","strategy_note":"高階 ABF 老牌主力，FY2027 起陸續新增量產產能。事實表缺營收與利潤率，無法比較。"}],"peer_na_reason":"Ibiden 營收欄缺失且只有兩季資料，無法計算利潤率。","threats":[{"level":"🟡","text":"欣興在美系 AI ASIC 載板份額逾七成、Blackwell 逾三成，景碩在 GPU 端份額目標兩成尚未實現，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"玻璃核心基板最快 2027 下半年導入（GlaSSEM 目標供貨），但 Intel 的設計保留 ABF 增層，只取代核心層，目前不算整體替代。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"ABF 增層膜由味之素供應九成以上，約占載板原料成本 25%～30%；材料漲價或配額會直接吃掉載板的漲價空間。","p":"30%","evidence_refs":["geo_supply_chain#1"]}],"roic_durability":{"quadrant":"低利益率×低周轉（TTM 營益率 10.1%；周轉率事實表未涵蓋，依載板重資產特性暫判）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"AI 伺服器 CPU／GPU 封裝必須用 ABF，屬於需要而非想要；但手機與 PC 端需求仍弱，非 AI 部分可延後採購，整體需求基礎只有部分是剛性。"},{"item":"決策層級","level":"🟡","text":"客戶在單一封裝料號層級認證，重新認證有成本；但同一客戶同時用欣興、Ibiden、南電多源供應，料號層級可以調整份額，景碩的供貨率由一成升到五成就是例證。"},{"item":"價值鏈分配","level":"🔴","text":"上游 T-glass（Nittobo）與 ABF 膜（味之素）都是獨供或近獨供，下游是強勢晶片商；載板環節只有在缺貨期才多拿到利潤，上輪下行時 FY2023 前三季虧損。"},{"item":"社會容忍度","level":"🟢","text":"B2B 零件，不依賴監管授權，不涉民生定價。美國 232 關稅是否涵蓋載板未確認，屬政策觀察項，不構成價格天花板。"}],"roiic":"事實表未涵蓋（投入資本與折舊未收）","reinvest_rate":"粗估 4.1～4.9 倍，屬總資本支出口徑：三年擴產專案 196～235 億元，年均 65～78 億元，除以 FY2025 淨利 15.96 億元。折舊事實表未涵蓋，淨再投資率無法計算；方向上遠高於 100%。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。再投資率粗估＝（196～235 億元÷3）÷15.96 億元＝4.1～4.9 倍；這是未扣折舊的總資本支出口徑，也無法拆出客戶出資的設備金額，實際淨再投資率會較低。增量 ROIC 缺投入資本，無法計算，所以內生上界不給數字。共識成長主要來自利潤率回升，不是再投資複利。"}}}},"q3_growth":{"verdict":"成長跑道評為中等（🟡）。AI 載板是第二曲線的雛形，但占營收只有一到兩成，份額目標也還沒有外部證據證實。","reasoning":"成長由量與價共同推動，沒有併購或回購。量：ABF 月產能 4,000 萬顆，2027 年增到 5,000 萬顆，2029 年底目標 8,000 萬顆，擴產設備由客戶出資。價：法人估 Q3、Q4 報價各季約增 8%。共識 EPS 從 FY2025A 3.37 元到 FY2027E 28.11 元，兩年年化約 189%；同期營收由 39,351 百萬元到 78,876 百萬元，年化約 42%。EPS 成長比營收快約 147pp，差距幾乎全部來自利潤率由谷底回升，屬循環修復，無法歸因到再投資報酬，所以這段成長依賴估值重估。FY2028E 共識事實表未涵蓋，三年 CAGR 無法計算。滲透率事實表未涵蓋，跑道年數不給。衰退訊號亮一個：EPS 成長大幅高於營收成長。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6"],"verdict_values":{"growth":{"driver_mix":"量（產能 4,000→5,000 萬顆，2029 年目標 8,000 萬顆）加上價（Q3、Q4 報價各季約 +8%）；沒有併購、沒有回購。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界的輸入事實表未涵蓋。共識 FY2025A→FY2027E EPS 年化約 189%，營收年化約 42%，缺口來自利潤率回升與報價，屬循環修復而非再投資複利，判為超出內生上界。","segments":{"expanded":false,"reason":"ABF 與 BT 的分部營收與毛利事實表未涵蓋。載板營收占 Q2 合併約 83%，其餘約 2,114 百萬元的內容未揭露，無法建表。"},"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"Q1 2026 21.2%→Q2 26.1%，季比上升；季度年比資料事實表未涵蓋"},{"signal":"核心市占縮減","lit":false,"note":"AI CPU 客戶供貨率上升；整體份額序列事實表未涵蓋"},{"signal":"提價後銷量下滑","lit":false,"note":"稼動率由 86% 升到 95%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2025A→FY2027E EPS 年化約 189%，營收約 42%"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"note":"FY2024 為負、FY2025 約 1.07，只有一年未達"},{"signal":"SBC／營收逾 5% 且上升","lit":false,"note":"Q2 SBC 僅占營業利益 1.2%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"玻璃核心最快 2027 下半年導入，列入觀察"},{"signal":"產業倍數近三年系統性下移","lit":false,"note":"P/S、EV/S 在自身年度端點最高"},{"signal":"維持性資本支出占 FCF 逾六成","lit":false,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"正在大幅擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本幾乎全部投入擴產，現金回饋股東極低。擴產設備由客戶出資，降低了自有資本的風險，但廠房與折舊仍由景碩承擔。","reasoning":"FCF 轉換率：FY2022 −1,217 百萬元對淨利 6,977 百萬元；FY2023 −4,105 對 48；FY2024 −2,900 對 49；FY2025 才轉正，1,711 對 1,596，約 1.07 倍。TTM FCF 利潤率 7.4%，Q2 FCF 315 百萬元。SBC 很低：Q2 為 20.2 百萬元，占營業利益 1.2%（Q1 同欄口徑不同，跨季不可比）。現金去向以擴產為主：三年專案 196～235 億元，對照目前淨現金 8,457 百萬元，需要靠營運現金或舉債支應；股息殖利率 0.14%，回購事實表未涵蓋。股數存在疑點：目前流通股數 526.91 百萬股，但 FY2025 淨利除以 EPS 約 473 百萬股，可能有增資稀釋，也可能只是口徑差異，事實表未涵蓋原因。","fact_refs":["f_kpi3_eps","f_kpi4_ocf_capex","f_kpi5_sbc","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年沒有併購事件（事實表併購軸查無資料）"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購；股息殖利率 0.14%"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 占營業利益 1.2%，但流通股 526.91 百萬股與 FY2025 淨利除以 EPS 推得的約 473 百萬股不一致，淨稀釋率無法確認"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；回購與近三年現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 FY2027 共識 EPS 28.11 元（上輪 2022 年高峰 14.57 元的近兩倍）兌現，還要在 2028 年後的新產能潮中守住。前半段我信一半，後半段不信。","reasoning":"現價 1,060 元，對 FY2026 共識 EPS 11.26 元是 94.1 倍，對 FY2027 共識 28.11 元是 37.7 倍，trailing 182.8 倍。P/S 12.5 倍、EV/S 12.3 倍，都在四個年度端點的最高點；前瞻 EV/S 10.4 倍。賣方平均目標價約 868～892 元（7 月資料、偏舊），FactSet 6 月是 620 元，現價高於兩者。共識 EPS 從 6 月的 9.33 元上修到 11.26 元，所以目標價落後並不等於賣方看空，但現價已走在賣方前面。trailing 本益比分位 18.1 看似便宜，是因為 2023～2024 年 EPS 只有約 0.10 元，把歷史本益比撐得極高，不能拿來說便宜。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027 共識 EPS），輔以 P/S、EV/S 自身區間","tier":"台系 ABF 載板三家（欣興、南電、景碩）同級","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或 EV/S，無法建倍數對照"},"fwd_pe":94.14,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"94.1 倍 FY1、37.7 倍 FY2 共識本益比，配上 P/S 與 EV/S 都在自身最高點，又是循環高峰盈餘，所以判為昂貴。PEG 不計算：基期 FY2025A 3.37 元是谷底回升，成長率被基期放大；FY2028E 共識也缺。五年分位不給：只有四個年度端點。短期上檔用賣方平均目標價中點 880 元，880÷1,060−1＝−17.0%。中期上檔用基準情境 FY2028E EPS 32 元乘終端 20 倍，得 640 元，640÷1,060−1＝−39.6%。","upside_short_pct":-17.0,"upside_mid_pct":-39.6,"denominator_disputed":true,"denominator_note":"估值分母 FY2027 共識 EPS 28.11 元是缺貨高峰的盈餘，是否能持續正是核心爭點；任何以 37.7 倍說便宜的論證都不成立。"}}},"q6_how_wrong":{"verdict":"我最可能看錯的地方：AI 封裝需求讓這輪缺貨比 2021～2022 年那輪長得多，2028 年缺口真的擴大到三到五成，FY2028 EPS 衝過 40 元，37.7 倍就變成約 26 倍。","reasoning":"高盛估 2028 年缺口 51%，大摩估 46%；擴產設備由客戶出資，代表客戶願意承擔產能風險；公司目標拿下 Vera CPU 載板全部份額、GPU 份額兩成。若這三件都成立，盈餘高峰會延到 2029 年後，我的基準情境就太悲觀。反方向的證據：另一家外資估 2028 年缺口只有 16%，全產業資本支出比上一輪高 51%，上輪 EPS 從 14.57 元掉到 0.10 元。股價 26 週已漲 189.7%，RSI 66.2，還沒到過熱線，但價格已經走在證據前面。陷阱評為中度：主要不是價值陷阱，而是高峰盈餘陷阱，倍數建立在景氣高點的盈餘上。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_eps_fy2","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰盈餘陷阱：倍數建立在景氣高點盈餘上"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":11.26,"pe":94.14,"basis":"起點用 FY2026 共識 EPS（FY1）；終端倍數同樣套在預估年度 EPS 上，口徑一致"},"eps":{"bull":[32,42,52,58,62],"base":[26,32,30,27,29],"bear":[20,15,7,6,10]},"pe":{"bull":25,"base":20,"bear":18},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.143,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":2},"max_dd":{"lo":-88,"hi":-55,"basis":"上輪下行時 FY2022→FY2023 營收減 36.8%，EPS 由 14.57 元掉到 0.10 元。股價 26 週漲 189.7%，回到半年前約 366 元就是 −65%。Bear 終點約 −83%，作為下緣的參考；上緣 −55% 對應盈餘只回落到基準情境水準時的倍數收縮。","trigger_time":null},"basis":{"bull":"AI 份額目標實現（Vera CPU 全拿、GPU 兩成），2029 年產能翻倍且由客戶出資，缺口延到 2028 年後，維持成長股倍數","base":"缺貨撐到 2027 年，FY2027 因 T-glass 受限略低於共識；2028 年後新產能開出，報價回落，利潤率回到中段，倍數收斂到循環股的 20 倍","bear":"2027 下半年 T-glass 解除加上各家新產能同時開出，報價轉跌，重演 2023 年的下行，EPS 回到個位數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上輪 FY2022→FY2023 營收減 36.8%，EPS 由 14.57 元掉到 0.10 元，2023 年前三季虧損；2023 年全球 IC 載板市場預估下滑約 30%。本輪全產業資本支出比上一輪高 51%，景碩自己就有 196～235 億元擴產。","assumption":"這輪 AI 需求能吸收 2027～2029 年的新產能，不重演 2023 年","consequence":"若報價在 2027 下半年轉跌，EPS 可能回到個位數；股價以循環股倍數計，有八成以上的下行空間","ruling":"採納。Bear 機率設 35%，高於一般水準，依據是本輪擴產規模比上一輪更大。","watch":"ABF 報價季變動、月營收年增率、季毛利率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","supply_demand_durability#5","cyclical_supply_discipline_capacity#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"三年擴產 196～235 億元，2027 年起折舊進來；ABF 膜由味之素近獨供，約占載板原料成本 25%～30%；流通股數 526.91 百萬股，高於 FY2025 淨利除以 EPS 推得的約 473 百萬股。","assumption":"AI 需求成立時，營收成長能轉成每股盈餘成長","consequence":"即使營收翻倍，折舊、材料漲價與可能的股本稀釋會讓 ROIC 低於帳面成長的暗示，每股價值成長慢於營收","ruling":"部分採納。設備由客戶出資，降低了資本風險；但股數疑點未解，列為資料缺口，下季財報核對。","watch":"季營益率、季報股本變動、材料成本占比","evidence_refs":["supply_demand_durability#5","geo_supply_chain#1"],"fact_refs":["f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價 1,060 元是 FY2026 共識的 94.1 倍、FY2027 共識的 37.7 倍；P/S、EV/S 在自身最高點；現價高於賣方平均目標價約 868～892 元；26 週漲 189.7%。","assumption":"市場給循環高峰盈餘成長股的倍數","consequence":"即使 FY2027 共識兌現，倍數收斂到 20 倍也只值約 560 元","ruling":"採納。現在就買的最強論證是：高盛估 2028 年缺口 51%，若 FY2028 EPS 達 40 元，現價只有 26.5 倍。但這個 EPS 沒有共識數字支持（FY2028E 共識缺），屬於未證實的推論。","watch":"FY2027 共識 EPS 修正方向、FY2028 共識是否出現且高於 FY2027","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_consensus_eps_fy2","f_ps_percentile","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1060.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1060.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率口徑","cause":null,"prior_field":null,"side_a":"MOPS 來源的季報：Q2 2026 合併毛利率 26.1%，營益率 13.4%，上半年數字與公告核對相符","side_b":"Quartr 簡報摘要：Q2 合併毛利率 12.7%，載板毛利率約 14%～15%","ruling":"採用 26.1%。若載板毛利率只有 14.5%，非載板部分要約 83% 的毛利率才能湊出 26.1%，不合理；Quartr 的數字較可能是營益率或其他口徑標錯。","evidence_level":"一手季報對二手摘要","settle_metric":"Q3 2026 季報的分部毛利揭露","if_then":["若 Q3 季報顯示載板毛利率低於 15%，H2 改用載板口徑重設門檻，基準 EPS 路徑下修兩成","若 Q3 合併毛利率落在 27%～29%，維持 26.1% 口徑"],"evidence_refs":["competitive_share_entrants#4","reg_tariff_export#1"]},{"axis":"缺貨持續期對新產能潮","cause":null,"prior_field":null,"side_a":"缺口延續擴大：高盛估 2026 下半年、2027、2028 年分別為 14%、34%、51%；凱基估 2027～28 年 22%、29%；壓膜機交期排到 2031 年","side_b":"供給追上：全球資本支出比上一輪高 51%，綠地產能 2027 年起開出，南電資本支出逾 100 億元，景碩自己擴產兩成五，另一家外資估 2028 年缺口只有 16%","ruling":"兩邊可以調和，關鍵在時間先後。2027 年缺貨的證據較強，採 A 側；2028 年後各家預估差三倍，不採信高峰延續，基準情境讓盈餘在 2028 年見頂。依據：上輪也是在擴產高峰後一年內反轉。","evidence_level":"多家券商估計，二手轉述為主","settle_metric":"ABF 報價季變動、景碩稼動率","if_then":["若 2027 年第三季 T-glass 擴產後報價仍季增且稼動率 ≥90%，Bull 機率由 20% 升到 30%，股價在 600 元以下開始分批反買","若 2027 年任一季報價季減，視為 Single Thing 發生，已持有者清倉"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","end_markets#5"]},{"axis":"毛利改善來源","cause":null,"prior_field":null,"side_a":"公司說法：毛利改善主要來自稼動率提升，而非漲價","side_b":"法人估計：ABF 與 BT 報價 Q2 再漲約 5%，Q3、Q4 各季約 8%，部分現貨漲逾三成","ruling":"程度差異，可以調和。稼動率已到 95%，接下來的毛利只剩報價這條路，所以報價是未來的關鍵變數。","evidence_level":"公司口徑對法人估計","settle_metric":"Q3 毛利率是否落在 27%～29%","if_then":["若 Q3 毛利率低於 26%，報價論點證偽，停止加碼且不建立"],"evidence_refs":["end_markets#4","cyclical_inventory_price_position#0"]}],"triggers":[{"n":1,"text":"股價回到約 600 元以下，且 FY2027 共識 EPS 未下修逾一成：重跑判斷，首筆不超過 2%","type":"估值rearm","maps_to":"action_conditions.rearm_trigger","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤600 元且共識 ≥25.3 元","action":"分批反買","source_freq":"每日股價；共識每月","date":null},{"n":2,"text":"2027 年 AI 相關營收占比達 15% 以上，份額論點成立","type":"假設驗證","maps_to":"H1","metric":"AI 相關營收占比","threshold":"≥15%（低於 12% 視為未實現）","action":"不追","source_freq":"每季法說","date":"2027-Q4"},{"n":3,"text":"T-glass 擴產延後到 2027 年第三季之後，或營收受限比率升破 15%","type":"風險","maps_to":"R1","metric":"Nittobo 擴產時程、公司揭露的營收受限比率","threshold":"延後或受限比率 >15%","action":"停止加碼","source_freq":"每季法說與供應鏈報導","date":"2027-Q3","evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"ABF 載板報價出現本輪首次季減","type":"Single Thing","maps_to":"thesis.single_thing","metric":"ABF 報價季變動","threshold":"任一季季減","action":"清倉","source_freq":"每季法說與法人報價調查","date":null},{"n":5,"text":"新產能開出後稼動率跌破 85%，或季毛利率連兩季低於 24.7%","type":"減碼","maps_to":"R2","metric":"稼動率、季毛利率","threshold":"稼動率 <85% 或毛利率連兩季 <24.7%","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"n":6,"text":"主要 GPU 或 CPU 客戶宣布量產封裝改用不含 ABF 增層的玻璃核心設計","type":"風險","maps_to":"R4","metric":"客戶封裝設計公告","threshold":"任一主要客戶宣布量產","action":"減碼","source_freq":"產業新聞與客戶發表會","date":"2027-Q3","evidence_refs":["substitute_technology#1"]},{"n":7,"text":"Q3 2026 財報：核對毛利率口徑、股本變動與 Q3 毛利率是否在 27%～29%","type":"複審日期","maps_to":"H2","metric":"Q3 合併毛利率、季報股本","threshold":"毛利率 ≥26%","action":"不追","source_freq":"季報","date":"2026-11"}],"kill_metrics":[{"metric":"合併季毛利率","bear_threshold":"連兩季低於 22%","window":"2026Q3～2027Q4","source":"MOPS 季報","last_status":"ok"},{"metric":"ABF 載板報價季變動","bear_threshold":"本輪首次季減","window":"2026Q4～2027Q4","source":"公司法說與法人報價調查","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"由 28.11 元下修逾 15%（低於 23.9 元）","window":"未來 12 個月","source":"yfinance 分析師共識","last_status":"unknown"},{"metric":"月營收年增率","bear_threshold":"連三個月低於 10%","window":"未來 12 個月","source":"MOPS 月營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","exec_line":"不追。觸發重啟條件後重跑判斷，首筆不超過 2%；加碼要等 Q3 2026 毛利率 ≥27% 確認。","holding_cap":"≤3%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把缺貨期的報價漲幅當成 AI 結構性成長來定價。但 AI 相關營收 2026 年只占約一成、2027 年預期一成五到兩成，其餘八成以上仍隨載板週期漲跌；而 2025～28 年全產業資本支出比上一輪高 51%。","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 600 元以下（FY2027 共識 EPS 的 21 倍）且共識未下修逾一成；或 FY2028 共識出現且不低於 FY2027。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把缺貨期的報價漲幅當成 AI 結構性成長來定價。但 AI 相關營收 2026 年只占約一成、2027 年預期一成五到兩成，其餘八成以上仍隨載板週期漲跌；而 2025～28 年全產業資本支出比上一輪高 51%。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=189.72, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"AI 載板份額實現：AI 相關營收占比由 2026 年約一成升到 2027 年一成五以上","2y":"2027 年全年 AI 相關營收占比 ≥15%","5y":null,"10y":null,"threshold":"2027 年 AI 相關營收占比 ≥15%；低於 12% 視為未實現","source":"公司每季法說與年報","drift_rule":"連兩季法說占比低於 12% 為削弱；連三季低於 10% 為反轉"},{"id":"H2","text":"缺貨帶動的報價撐住毛利率","2y":"2027 年各季合併毛利率 ≥26%","5y":null,"10y":null,"threshold":"季毛利率 ≥26%（Q2 2026 為 26.1%）","source":"MOPS 季報","drift_rule":"連兩季低於 24.7%（偏離 5%）為削弱；連三季低於 23.4%（偏離 10%）為反轉"},{"id":"H3","text":"新增產能在折舊進來後仍賺得到合理報酬","2y":null,"5y":"2027 年起月產能由 4,000 萬顆增到 5,000 萬顆後，2028～2030 年營益率仍 ≥15%、稼動率 ≥85%","10y":null,"threshold":"年度營益率 ≥15%（FY2025 為 6.8%，Q2 2026 為 13.4%）","source":"年報與法說揭露的稼動率","drift_rule":"連四季 TTM 營益率低於 14.25% 為削弱；連六季低於 13.5% 為反轉"}],"R":[{"id":"R1","text":"T-glass 缺料延續，壓住每月 10%～15% 營收；Nittobo 獨供，2027 年第三季才擴產","h_ref":"H2","clock":"⚡","threshold":"擴產延後到 2027 年第三季之後，或受限比率升破 15%","evidence_refs":["supply_demand_durability#2"]},{"id":"R2","text":"全產業擴產潮：資本支出比上一輪高 51%，景碩 196～235 億元、南電逾 100 億元，2027～2029 年新產能陸續開出","h_ref":"H3","clock":"🔥","threshold":"新產能開出後報價季減，或稼動率跌破 85%","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"高階 AI 客戶主供仍是欣興（ASIC 逾七成、Blackwell 逾三成）與 Ibiden，景碩的 GPU 份額目標可能落空","h_ref":"H1","clock":"🔥","threshold":"AI CPU 客戶供貨率由五成回落到三成以下，或 2027 年底 GPU 份額仍低於一成","evidence_refs":["competitive_share_entrants#2"]},{"id":"R4","text":"玻璃核心基板最快 2027 下半年導入，若演進到取代 ABF 增層，會壓縮載板的價值","h_ref":"H1","clock":"🐢","threshold":"主要客戶宣布量產封裝不含 ABF 增層","evidence_refs":["substitute_technology#1"]},{"id":"R5","text":"ABF 膜由味之素近獨供，材料漲價或配額會吃掉載板的漲價空間","h_ref":"H2","clock":"🐢","threshold":"季毛利率因材料成本降 2pp 以上","evidence_refs":["geo_supply_chain#1"]},{"id":"R6","text":"重演上輪下行：2023 年全球載板市場約減三成，景碩前三季虧損","h_ref":"H2","clock":"🔥","threshold":"月營收連三個月年減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]}],"single_thing":{"description":"ABF 載板報價出現本輪首次季減","why_fatal":"FY2027 共識 EPS 28.11 元建立在報價每季上漲的前提上；稼動率已到 95%，報價是剩下唯一的毛利來源。上輪 2022→2023 年營收減 36.8%，EPS 由 14.57 元掉到 0.10 元。","if_happens":"已持有者清倉、未持有者不建立；改用下行的 Bear 路徑重新估值","how_monitor":"每季法說與法人報價調查、MOPS 月營收、季毛利率","probability":"12～24 個月內約 30%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":37.71,"peg_fy2":0.25,"stress":{"pass":null,"total":null},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-10-12）"},"eps_meta":{"base_eps_path":{"FY2025A":3.37,"FY2026E":11.26,"FY2027E":28.11,"FY2028E":null},"fy_end_month":12,"eps_basis":"TWD 稀釋 EPS（GAAP）；FY2026E、FY2027E 為 yfinance 分析師平均；FY2028E 共識事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 財報與法說","impact":"高","watch":"合併毛利率是否落在 27%～29%、分部毛利口徑、股本變動"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Nittobo T-glass 擴產出貨","impact":"高","watch":"缺料解除後報價是否仍季增"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"景碩與欣興新產能陸續開出（景碩月產能增到 5,000 萬顆）","impact":"高","watch":"稼動率是否守住 85%"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"GlaSSEM 玻璃核心基板目標供貨","impact":"中","watch":"主要客戶量產設計是否仍保留 ABF 增層"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
