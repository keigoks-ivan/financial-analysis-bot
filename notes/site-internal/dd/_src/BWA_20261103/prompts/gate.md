你是 DD 管線 v20 的判斷層閘（gate），標的 BWA（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定；來源 gate_contract §⑤／critic-gates ⑤ 同日改成同一條規則（核心軸 none 🔴、非核心 🟡）；重新濃縮時以本卡 ⑤ 為準 -->

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

⑤ 覆蓋面掃描——**燈號由程式判定**（核心軸 none→🔴；只有非核心軸 none→🟡；全 found／not_applicable→🟢），bundle 附程式結果，你回的 ⑤ 燈號會被覆寫。你只評論：facts.json 點名 status="none"／"not_applicable" 的軸，查詢是否切題（不以查詢次數計）、判斷有沒有交代缺口對結論的影響；不得因缺軸自行升 🔴。

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤（燈號由程式判定，你只評論）。
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

### 判斷檔 `fact_refs` 引到的事實（48 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝3487 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（2026-10-29）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未能以一手來源驗證；二手來源稱營收低於共識（約 $3.56–3.58B，未驗證）
- `f_kpi1_adjusted_operating_incom`（q1_business）｜Adjusted operating income / margin＝10.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未驗證
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝8.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：n/a
- `f_kpi4_adjusted_diluted_eps`（q1_business）｜Adjusted diluted EPS＝1.39 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：財報前共識約 $1.24（二手來源，7 位分析師，未以一手驗證）
- `f_kpi5_fy2026_guidance`（q1_business）｜FY2026 guidance（管理層指引）＝營收 $14.0–14.2B；調整後營業利益率 10.7–10.9%；調整後 EPS $5.20–5.35；GAAP EPS $4.65–4.84；營運現金流 $1.6–1.7B；FCF $0.9–1.1B mixed｜期間與口徑：Q3 2026（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-10-29））
  - 註記：調整後 EPS 指引上調自 $5.05–5.30；上調原因為庫藏股與較低有效稅率；FCF 指引不變；營收區間自 $14.0–14.3B 收窄；假設電池事業銷售約減 $250m、匯率約增 $250m
- `f_peer_bwa_gross_margin_pct`（q2_moat）｜BWA 毛利率＝19.8 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_rsi14`（q5_valuation）｜RSI(14)＝27.7｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝48.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_peer_bwa_operating_margin_pct`（q2_moat）｜BWA 營業利益率＝10.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bwa_fcf_margin_pct`（q2_moat）｜BWA FCF 利潤率＝9.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BWA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_gross_margin_pct`（q2_moat）｜APTV 毛利率＝19.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_operating_margin_pct`（q2_moat）｜APTV 營業利益率＝9.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aptv_fcf_margin_pct`（q2_moat）｜APTV FCF 利潤率＝3.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.APTV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_gross_margin_pct`（q2_moat）｜LEA 毛利率＝6.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_operating_margin_pct`（q2_moat）｜LEA 營業利益率＝3.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_fcf_margin_pct`（q2_moat）｜LEA FCF 利潤率＝3.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_gross_margin_pct`（q2_moat）｜MGA 毛利率＝14.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_operating_margin_pct`（q2_moat）｜MGA 營業利益率＝5.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_fcf_margin_pct`（q2_moat）｜MGA FCF 利潤率＝7.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.26 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.9 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝6.66 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝14099.0 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝14675.45 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.17 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（5.91 → 5.9）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.45 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（6.63 → 6.66）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝195 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 borgwarner.com Q3 2026 press release（營運現金流 $320m）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1616.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 3199.0、現金 1583.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝200.81 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝12096.49 USD m｜期間與口徑：2026-11-03／市值 10480.49 ＋ 淨負債 1616.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.303 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝52.2 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝9.92 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.26，分子＝快照價 52.19｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝22.11 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝48.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.74 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.85 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝71.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝71.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝0.86 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.54 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 5.18 → 5.26（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.96 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（5.21 → 5.26）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-6.77 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 51.94 / W52 57.39 / W104 45.78 / W250 39.13 / W250 13週斜率 0.64%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝57.39 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝45.78 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝39.13 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.64 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K風險因素：中國本土OEM擴大市占並增加自製原由Tier 1供應之零件；多家主要OEM表示將內製部分零件
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：競爭對手包含主要 OEM 客戶的垂直整合單位；多家主要 OEM 客戶已表明有意將公司生產的部分零組件自製（insource），OEM 已選擇且可能再選擇自製取代現有供應。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：Volkswagen 占營收 13%（2024 年 10%、2023 年 11%），Ford 12%（13%、14%）；無其他單一客戶超過 10%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1. Business（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因子：前十大客戶占 2025 年營收 71%，供貨合約多為需求合約，失去主要客戶或其車款大幅減產會對業務造成不成比例的重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A. Risk Factors（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：Volkswagen 集團評等頁：Moody's 2025-03 由 A3 降至 Baa1，之後展望轉負；S&P BBB+ 展望負面。
  - 來源：Volkswagen Group Annual Report 2025 - Ratings（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Ken Research（2026年1月）稱汽車供應商產業面臨獲利結構性重置而非週期性放緩，快速擴產與中國供應商積極定價壓低全球價格底部
  - 來源：Ken Research - Automotive Suppliers Profitability Reset Global（as_of 2026-01-15）｜affects：moat_trend、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 關稅對成本與營收的影響：客戶回收關稅使銷售增加約 $80M；關稅費用使銷貨成本年增約 $108M。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-11）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：2025 年美國對歐盟、加拿大、墨西哥、中國等課徵關稅，已推高原料與零件成本，並引發中國等報復性關稅；USMCA 2026 年待更新，中國供應鏈整合帶來特有風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：BorgWarner 10-Q（2026 Q2）稱已收到約 $35M IEEPA 關稅退款，但因金額與時點不確定未認列退款應收；2025 年對 EU、加拿大、墨西哥、中國進口加徵關稅推高原料與零組件成本。
  - 來源：BorgWarner 10-Q 2026-06-30 (SEC)（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 Turbos & Thermal Technologies 銷售 $1,372M，較去年同期 $1,437M 下滑；分部調整後營業利益率 14.7%（去年 15.2%）
  - 來源：BorgWarner 10-Q (period 2026-09-30), SEC（as_of 2026-10-29）｜affects：moat_trend、valuation
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Pitchgrade 研究文章指燃燒相關產品（如渦輪增壓器）替代風險最高，且 OEM 垂直整合（如 Tesla 自製馬達與逆變器）為成長中威脅（二手意見）。
  - 來源：Pitchgrade：borgwarner ai margin pressure（as_of 2026-02-15）｜affects：moat_trend、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：BWA 調整後月價自2008年5月約$18.67跌至2009年1月約$6.18，2009年12月回到約$12.16（約8個月跌約67%，約11個月後回升近一倍）
  - 來源：digrin BWA Price History（as_of 2026-01-01）｜affects：valuation、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2009年Q2 BWA 排除一次性項目營業利益僅$0.8M（占銷售0.1%），去年同期為8.2%；銷售$916.2M，年減39.6%
  - 來源：BorgWarner Q2 2009 results (SEC EX-99.1 / AftermarketNews)（as_of 2009-07-30）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2020 COVID：H1銷售$3,705M年減28%；Q2 Adjusted EBIT $28M（去年同期$249M）；Drivetrain Q2 Adjusted EBIT margin 0.2%（去年10.2%）；全年毛利率18.8% vs 2019年20.7%
  - 來源：BorgWarner 10-Q Q2 2020 / 10-K FY2020（as_of 2021-02-17）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2008-09產業：輕型車產量2009年約降40%至約800萬輛；零組件出貨2008年-14%、2009年再-24%；北美產量2012年回到約1,600萬輛（V型）
  - 來源：US Dept of Commerce Auto Parts Industry report 2012 / industry reviews（as_of 2012-01-01）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":114.4,"bear_5y_price":32.2,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":37.0,"ev5y_pct":30.9,"irr_base_pct":6.5,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":5.26,"pe":9.92,"basis":"FY2026E 共識調整後 EPS 5.26（Koyfin 2026-10-31），股價 $52.2，對應 9.92 倍；終端倍數同樣乘當年度調整後 EPS，口徑一致"},"eps":{"bull":[5.33,6.05,6.95,7.9,8.8],"base":[5.27,5.75,6.3,6.75,7.15],"bear":[5.2,4.4,3.9,4.1,4.3]},"pe":{"bull":13,"base":10,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.303,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BWA_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Craig Aaron｜guidance：CFO 說明全年銷售、調整後營業利益率與自由現金流財測維持不變。（原話："adjusted operating margin and free cash flow guidance"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年調整後 EPS 財測上調為 $5.05 至 $5.30（原為 $5 至 $5.20）。（原話："$5.05 to $5.30 per diluted share"）
- 2026-08-05｜CFO Craig Aaron｜guidance：2026 全年銷售財測區間 $14.0B 至 $14.3B，維持不變。（原話："sales in the range of $14.0 billion to $14.3 billion"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年調整後營業利益率財測 10.7% 至 10.9%。（原話："range of 10.7% to 10.9% compared to our 2025"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年有機銷售變動財測為下滑 3.5% 至下滑 1.5%，與先前展望一致。（原話："sales change to be down 3.5% to down 1.5% year-over-year"）
- 2026-08-05｜CFO Craig Aaron｜guidance：全年自由現金流財測 $900M 至 $1.1B，維持不變。（原話："range of $900 million to $1.1 billion"）
- 2026-08-05｜CFO Craig Aaron｜risk：電池業務因北美缺乏誘因與歐洲需求偏弱而下滑，估計拖累全年銷售成長約 170 bp。（原話："this decline to represent roughly a 170 basis point"）
- 2026-08-05｜CFO Craig Aaron｜margin：利潤率財測低端所隱含的全年 decremental conversion 假設。（原話："a full year decremental conversion in the low double digits"）
- 2026-08-05｜CFO Craig Aaron｜margin：利潤率財測高端的假設：以進一步成本控制大致抵銷有機銷售下滑。（原話："At the high end, our outlook assumes we largely offset"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率年增 100bp 的拆解：基礎業務 60bp。（原話："60 basis points came from strong performance"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率拆解：BES 重組與退出充電業務貢獻 20bp。（原話："We had 20 basis points of enhancement through BES"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 利潤率拆解：成本控制貢獻最後 20bp。（原話："And the final 20 basis points came from"）
- 2026-08-05｜VP IR Patrick Nolan｜margin：管理層對 incremental margin 的定義（有機調整後營業利益變動除以有機銷售變動）。（原話："Our incremental margin is defined as the organic change in"）
- 2026-08-05｜VP IR Patrick Nolan｜margin：管理層對 market 的定義：依地理曝險加權的輕型車產量變動。（原話："that means the change in light vehicle"）
- 2026-08-05｜CFO Craig Aaron｜margin：Q2 有機銷售增加 $18M（0.5%），略優於輕型車產量下滑。（原話："organic sales increase of $18 million, 0.5%"）
- 2026-08-05｜CFO Craig Aaron｜margin：CFO 說明排除充電業務退出與匯率後的 Q2 營業利益變動口徑。（原話："Excluding this benefit and FX impacts"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年銷售橋接：較低營收下的 decremental 約中段十幾 %。（原話："On those lower revenues, we're decrementing at"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年利潤率：不含工業 R&D 增加為 10.8%。（原話："our margin would be at 10.8%"）
- 2026-08-05｜CFO Craig Aaron｜margin：下半年利潤率：含工業 R&D 中點為 10.6%。（原話："industrial R&D at the midpoint, we're at 10.6%"）
- 2026-08-05｜CFO Craig Aaron｜commitment：下半年工業 R&D 增加 $10M 至 $15M，同時維持全年利潤率財測。（原話："investing an incremental $10 million to $15 million"）
- 2026-08-05｜CFO Craig Aaron｜commitment：管理層承諾在增加 R&D 的同時維持全年利潤率財測。（原話："while maintaining our full year margin guidance"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 回答增加的 R&D 是否持續時表示開發開始後會有一定程度的持續支出。（原話："you can expect to have some level of"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：董事會將庫藏股授權增加 $1B。（原話："approved a $1 billion increase to our current share"）
- 2026-08-05｜CFO Craig Aaron｜capital_allocation：合併原授權剩餘 $350M 後，可回購總額達 $1.35B，約市值 10% 以上。（原話："$1.35 billion of the company's outstanding shares"）
- 2026-08-05｜CFO Craig Aaron｜capital_allocation：過去四季回購約 $650M，原授權剩餘 $350M。（原話："$650 million and leaves $350 million remaining"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：CEO 表示將優先進行有機投資（R&D 與 CapEx）。（原話："we will always prioritize these organic investments"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：M&A 維持三項準則（核心競爭力、近期增益、不多付）。（原話："we're sticking to the 3 criteria"）
- 2026-08-05｜CEO Joseph Fadool｜capital_allocation：CEO 表示 M&A 門檻已經提高。（原話："we've really raised the hurdle in terms of any decision"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機測試已達 CARB 等級排放標準。（原話："we have achieved CARB-level emission standards"）
- 2026-08-05｜CEO Joseph Fadool｜product：UL 零組件認證預計 9 月開始。（原話："certification is expected to start in September"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機組裝廠設備預計第三季開始安裝。（原話："capital equipment installation to begin in the third quarter"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：電池儲能系統預計 2027 年量產就緒。（原話："we expect to be production ready in 2027"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 表示預期今年會有部分電池儲能訂單。（原話："We do expect to see some battery awards this year"）
- 2026-08-05｜CEO Joseph Fadool｜product：微電網逆變器已有四家客戶取得樣品。（原話："Four customers now have BorgWarner samples"）
- 2026-08-05｜CEO Joseph Fadool｜guidance：渦輪發電機產能：宣布安裝 2 吉瓦產能。（原話："we're installing 2 gigawatts of capacity"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 對明年約 $300M 工業營收表示有信心。（原話："which we're very comfortable with next year"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：渦輪發電機產能是否追加，管理層預計下半年做決定，尚未定案。（原話："So no decisions made yet"）
- 2026-08-05｜CEO Joseph Fadool｜product：渦輪發電機使用情境與早先預期相反：近 12 個月轉為以主電源（prime）為主。（原話："that's flopped, and we see more of them in prime use"）
- 2026-08-05｜CEO Joseph Fadool｜customer：針對 Koch 可能出售 Edged 股權的報導，管理層表示協議中無控制權變更觸發條款。（原話："nothing in our agreement that triggers change in control"）
- 2026-08-05｜CEO Joseph Fadool｜risk：對 Endeavour 夥伴 Koch 的新聞，管理層認為不會實質改變雙方關係。（原話："we don't think it materially changes anything"）
- 2026-08-05｜CEO Joseph Fadool｜competition：VCT 在中國取得 1.5L 渦輪汽油引擎新案，取代原有供應商。（原話："replacing the previous incumbent supplier"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 預期新訂單將支持 2027 年 outgrowth 的改善。（原話："improvement in our objective in outgrowth across portfolio in 2027"）
- 2026-08-05｜CEO Joseph Fadool｜competition：CEO 公開表示對目前 outgrowth 表現不滿意，並稱因此調整了策略。（原話："Craig and I are not pleased with the current outgrowth"）
- 2026-08-05｜CEO Joseph Fadool｜commitment：CEO 表示預期這些訂單會改善公司 outgrowth。（原話："we're clearly expecting that they're going to improve the outgrowth"）
- 2026-08-05｜CEO Joseph Fadool｜customer：中國占全球銷售約 20%。（原話："China is about 20% of BorgWarner's global sales"）
- 2026-08-05｜CEO Joseph Fadool｜risk：管理層對中國產量的預期區間：下滑 4% 至 7%。（原話："China, likely to be down 4% to 7%"）

### 問答異常語氣（迴避／改口／保留）
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Spak：EBIT 較預期高近 $40M、R&D 只增 $10–15M，其餘 $25–30M 是否為較高成本？｜答法：CFO 未直接回答差額去向，改談上下半年營收橋接與利潤率（10.8% vs 10.6%）。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Picariello：BES 上半年虧損僅 $4M，遠優於 mid-teens decremental，下半年如何橋接？｜答法：CFO 以重組與充電業務退出帶過，未解釋差距，僅重申下半年管理在 mid-teens decremental。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Percoco：渦輪發電機訂單到交貨是否少於 6 個月？｜答法：CEO 表示未揭露交期且不打算談，改稱目前重點在 2026 年的產品上線。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Perry：電力產品營收可擴大到多少、EBIT 貢獻如何估算？｜答法：CEO 只重申明年 $300M，未給 EBIT 或營收對產能比，稱可能未來再分享。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：McNally：電池儲能典型合約規模有無經驗法則？｜答法：CEO 稱沒有經驗法則、每案客製，僅說任何超大規模客戶訂單都會相當可觀，不給數字。
- BWA_Q2_2026_Earnings_Call_20260805.md｜問：Rosner：逆變器的產能與投資規模？｜答法：CEO 表示未宣布產能計畫，待年底報價後再評估，2027 年才可能分享。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 3 | 0 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 2 | 3 |
| cyclical_inventory_price_position | found | 1 | 5 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B｜衛星候選｜等 W52 拉回 $46-50 後分批進場；近 4 月 +60% 短期 stretched，估值燈 🟡 不急建倉","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"eProducts 達成 25% revenue mix（2027 target）+ margin ≥ 8%","columns":{"2Y 驗證":"FY 27 eProducts revenue ≥ $4.3B + OPM ≥ 8%","5Y 驗證":"FY 30 eProducts revenue ≥ $6B + OPM ≥ 10%","10Y 驗證":"2035 eProducts ≥ 40% mix + OPM 等同集團","數字門檻":"FY 27 eProducts $4.3B（公司公開 target）+ implied margin ≥ 8%","信息來源":"公司 2025 投資人日 + Capital Markets Day 2024-06","漂移觸發":"連 2 季 eProducts revenue YoY &lt; +15% → 削弱（2Y 假設）"}},{"id":"H2","text":"Adj OPM 結構維持 10-11% mid-cycle","columns":{"2Y 驗證":"FY 26 Adj OPM 10.7-10.9% （公司 guidance）","5Y 驗證":"5Y 平均 Adj OPM ≥ 10.5%","10Y 驗證":"無 mean reversion 至 9% 以下","數字門檻":"FY 26 ≥ 10.7% / FY 27 ≥ 10.7% / FY 28 ≥ 11%","信息來源":"2026-02 公司 guidance","漂移觸發":"連 4 季 OPM &lt; 9.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Data Center turbine generator scale up + free option value 兌現","columns":{"2Y 驗證":"2027 Y1 訂單 ≥ $300M + 2 GW capacity 達標","5Y 驗證":"FY 30 Data Center revenue ≥ $1B（mix &gt; 5%）","10Y 驗證":"2035 Data Center 為第三大業務線（mix ≥ 10%）","數字門檻":"Y1 $300M（公司公開）/ Y3 $800M / Y5 $1.5B","信息來源":"2026-02-11 BWA press release","漂移觸發":"連 2 季訂單 announcements &lt; $50M → 削弱（2Y）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"eProducts margin 永遠卡 6-7%（vs 集團 10.7%）","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 Adj OPM + 業務段 margin disclosure","警戒閾值":"連 4 季 集團 OPM &lt; 9.5%"}},{"id":"R2","text":"Vitesco-Schaeffler 合併 + 中國 EV 本土化 pricing war","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"eProducts 季度 ASP/W trend + 中國 OEM 自製率","警戒閾值":"跨 2 個年度 eProducts revenue YoY 連續 &lt; +10%"}},{"id":"R3","text":"ICE turbo 加速結構下行（BEV 強滲透）","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Air Management 業務 organic + BEV 滲透率","警戒閾值":"連 4 季 Air Management organic &lt; -7%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":65.82,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BWA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"BorgWarner Inc."},"oneliner":"BWA 前瞻本益比 9.9 倍、自由現金流殖利率約 9.5%，但利潤率在近年高點、2027 年車市有逆風；等 2027 年 2 月指引證明有機營收不落後市場、調整後 EPS 中點 ≥$5.75 再分批，渦輪發電機當期權看，不算進基礎","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BWA_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺 OEM 車款平台合約的錢：把渦輪、可變正時（VCT）、分動箱、電機、逆變器、引擎控制模組等動力系統零件，按車型生命週期直接賣給 OEM。錢卡在 OEM 排產量與年度議價兩個節點；近兩年獲利成長靠成本控制與回購，不靠量。","reasoning":"最新一季（Q3 2026）營收 $3,487M，年減約 2.9%，有機年減 3.1%。剔除電池事業後有機年減 1.6%，大致等於輕型車產量跌幅。調整後營業利益率 10.9%（去年同期 10.7%），GAAP 營業利益率 8.7%；TTM 毛利率 19.8%。調整後 EPS $1.39，年增 12%，增幅來自稅率與過去四季約 $725M 回購（約市值 6%），不是營運量能。分部：渦輪與熱管理 $1,372M（約 39%，利潤率 14.7%）；PowerDrive 季營收約 $700M 以上，季虧約 $5M；eProduct 合計約 $708M（20%）；其餘分部事實表未涵蓋。輕型車占營收 80% 以上。收錢方式依 10-K：年度合約或長期供貨協議，按 OEM 排產出貨，量隨車市走。單點依賴：Volkswagen 13%、Ford 12%，前十大客戶 71%，這是集中度風險，不是護城河證據；中國約占 20%（CEO 2026-08-05）。產業時鐘在收縮段：2026 年加權終端市場 −1~−2%、中國 −6~−8%，CFO 點名 2027 年有利率與購車負擔逆風。供需上，量是週期性、會反轉，燃油零件組合則是結構性萎縮。產業態勢判為雙向拉鋸：競爭端，中國 OEM 自製與供應商利潤率重置在惡化；結構端，電動化（Q3 輕型車 eProduct 年增 33%）與資料中心電力在打開新利潤池；其他結構變數（關稅、USMCA 續約）偏負。循環位置判中段：需求量未見向上拐點；倍數在自身 4 個年度端點的中位到偏高；情緒超賣（RSI 27.7），賣方目標價高於股價約五成。訊號互相矛盾，不給循環進場姿態。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi4_adjusted_diluted_eps","f_kpi5_fy2026_guidance","f_peer_bwa_gross_margin_pct","f_earnings_recency","f_rsi14","f_pe_percentile","f_ps_percentile"],"verdict_values":{"revenue_quality":"以 OEM 車款生命週期合約為主，量跟 OEM 排產走，議價權在客戶端。2025 年自由現金流 $1,208M，遠高於 GAAP 淨利 $277M，帳面盈餘被非現金項目壓低，現金品質比損益表好。","unit_econ_note":"Q3 剔除匯率後營收少 $112M，調整後營業利益只少 $6M，遞減率約 5%，遠優於 Q4 指引的中十幾 %。PowerDrive 本季增量轉換約每美元 0.24 美元（CFO 2026-10-29）。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"車用 Tier 1 動力系統零件，營收隨全球輕型車產量走：2009 年 Q2 營收年減 39.6%，2020 年上半年年減 28%。不屬商品子型（近年無虧損年、毛利率擺動小、不是報價型產品），屬需求量循環。"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉（量）：2026 年加權終端市場 −1~−2%（2026-10-29 法說），BCG 2026 年 3 月估至 2027 年供應商年成長約 2–3%。燃油零件組合另屬結構性萎縮：渦輪與熱管理分部 Q3 營收年減約 4.5%。","bargaining":{"up":"電子料成本上升，CFO 2026-10-29 說今年吸收得了、明年再看；碳化矽沿用車用供應商","down":"前十大客戶 71%，合約多為依排產的需求合約；2025 年關稅成本約 $108M，只向客戶回收約 $80M","geo":"中國約 20%（CEO 2026-08-05），其中約 75% 為中國本土 OEM（高盛轉述，二手）；美國以外約 84%（二手）；USMCA 2026 年待續約"},"profit_pool_dir":"利潤池由燃油動力系統往混動、純電的電機與電力電子移動，中國本土 OEM 同時把部分零件收回自製；車用以外，資料中心電力是新池，尚未有公司營收。","tam_table":{"expanded":false,"reason":"利潤池遷移（燃油→電動化、車用→資料中心電力）確實存在，但事實表沒有 TAM、滲透率或利潤池占比數字。Base 情境不靠新品類 TAM，只用公司給的 2027 年渦輪發電機約 $300M 目標，並在情境裡打折。"}}}},"q2_moat":{"verdict":"→：執行力擴大、定價力縮減，份額大致跟著市場走。機制是車款平台設計導入，加上跨燃油、混動、純電的成本規模，不是定價權，評 C。","reasoning":"事實表沒有同業 ROIC，可證方向改用同業利潤率差代理。BWA TTM 營業利益率 10.2%，高於 APTV 9.75%、MGA 5.48%、LEA 3.67%；FCF 利潤率 9.16%，對三家的 3.65%、7.52%、3.58% 優勢更大。同業資料截至 2026-06-30，BWA 截至 2026-09-30，期間差一季；而且只有單一期間，價差是擴大還是收窄無法判斷。自身 GAAP 營業利益率 2022–2025 由 8.57% 升到 9.24%，TTM 10.2%，方向往上。執行力 8 分：2026 年產量下滑，仍把調整後營業利益率守在 10.7–10.9%；新案不斷，包括中國 VCT 取代既有供應商（CEO 2026-08-05）、全球動力系統大廠的三件渦輪 conquest 案、中國鋁線電機首案（2026-10-29）。定價力 4 分：2025 年關稅只轉嫁約七成；CFO 說電子料通膨今年吸收、明年再看；前十大客戶占 71%。份額方面，2026 前三季輕型車營收大致與加權市場同步；CEO 2026-08-05 說對目前超越市場的幅度不滿意，Q3 仍未見超越，所以不標往上。最大威脅是 OEM 自製（10-K 風險因素），屬生態層級。燃油車萎縮方面，公司自己也賣替代產品，算產品層級替代，不算整體架構出局。","fact_refs":["f_peer_bwa_gross_margin_pct","f_peer_bwa_operating_margin_pct","f_peer_bwa_fcf_margin_pct","f_peer_aptv_gross_margin_pct","f_peer_aptv_operating_margin_pct","f_peer_aptv_fcf_margin_pct","f_peer_lea_gross_margin_pct","f_peer_lea_operating_margin_pct","f_peer_lea_fcf_margin_pct","f_peer_mga_gross_margin_pct","f_peer_mga_operating_margin_pct","f_peer_mga_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"車款平台設計導入綁住整個車型生命週期（例如新 ECU 合約延到 2034 年），加上燃油、混動、純電三種架構都有產品與成本規模。換供應商的時點在新平台招標，轉換成本只在平台期間有效。","execution":8,"pricing":4,"grade":"C","trend":"→","trend_evidence":"執行力擴大：產量下滑中，調整後營業利益率由 2025 年 10.7% 擴到指引 10.7–10.9%；Q3 剔除匯率營收少 $112M，營業利益只少 $6M。定價力縮減：2025 年關稅成本約 $108M，只回收約 $80M；電子料通膨。份額穩定：前三季輕型車營收與加權市場同步，沒有縮減也沒有超越。兩個方向互相抵銷，判穩定。","competitor_notes":[{"name":"APTV","strategy_note":"毛利率 19.63% 與 BWA 相當，營益率 9.75% 略低，但 FCF 利潤率只有 3.65%，BWA 現金轉換明顯較好；同業期間截至 2026-06-30，差一季"},{"name":"LEA","strategy_note":"毛利率 6.86%、營益率 3.67%、FCF 利潤率 3.58%，三項都遠低於 BWA，顯示 Tier 1 之間利潤池位置差距大"},{"name":"MGA","strategy_note":"Magna Powertrain 是 10-K 點名的非 OEM 主要對手；Magna 營益率 5.48%、FCF 利潤率 7.52%，BWA 營益率高約 4.7pp"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率差代理，且只有單一期間","threats":[{"level":"🔴","text":"OEM 垂直整合：10-K 稱多家主要 OEM 表明要自製部分零件，中國本土 OEM 擴大市占，並把原由 Tier 1 供應的零件收回自製。這是生態層級的攻擊。","p":"35%","evidence_refs":["customer_second_source#0","competitive_share_entrants#1","substitute_technology#1"]},{"level":"🟡","text":"燃油車結構萎縮壓縮渦輪與熱管理分部：Q3 分部營收 $1,372M（去年 $1,437M），利潤率 14.7%（去年 15.2%）。公司 eProduct 同期成長 33%，屬產品層級替代、可部分對沖，所以不列為架構替代；代價是組合轉換期間利潤率被稀釋。","p":"40%","evidence_refs":["end_markets#0","substitute_technology#1"]},{"level":"🟡","text":"供應商利潤率結構重置與中國供應商低價（Ken Research 二手意見）。BWA 2026 年利潤率仍在擴張，尚未反映在財報上，但屬破壞性競爭，機率取下限 30%。","p":"30%","evidence_refs":["supply_demand_durability#1"]}],"roic_durability":{"quadrant":"無法定象限：事實表未涵蓋投入資本與周轉率。營業利益率在同業屬高檔，但絕對值約 10%，暫視為中等利益率，周轉率待補","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是駕駛，決策者是 OEM 工程與採購，付款者是 OEM，三個角色都成立；不論燃油、混動、純電，每台車都要動力系統零件，需求是必要而非想要。但量隨車市：2026 年加權市場 −1~−2%、中國 −6~−8%，CFO 預告 2027 年有利率與購車負擔逆風。延後買車的代價低，急迫性不等於持久性。"},{"item":"決策層級","level":"🟡","text":"替代性要看平台招標這一層。設計導入後，供貨綁住整個車型生命週期，平台期間轉換成本高；但每個新平台都重新報價。BWA 自己在中國以 VCT 取代既有供應商、拿下渦輪 conquest 案，可見招標點換供應商是常態；10-K 也稱多家 OEM 表明要自製部分零件。"},{"item":"價值鏈分配","level":"🔴","text":"議價權在 OEM：前十大客戶占 71%，合約多為依排產的需求合約；2025 年關稅成本 $108M，只回收 $80M；Ken Research 稱供應商利潤率是結構性重置（二手）。BWA 營益率高於同業，靠的是成本執行，不是分到更大的利潤池。"},{"item":"社會容忍度","level":"🟢","text":"單一零件占整車成本低，沒有價格管制，也沒有社會對漲價的反彈問題。政策風險在別處：2025 年關稅、USMCA 2026 年待續約、電池事業因北美缺乏補貼而衰退。美國限制外國電網設備的行政命令若落實，反而有利於美國製造的微電網逆變器（CEO 2026-10-29）。"}],"roiic":"事實表未涵蓋（缺投入資本）","reinvest_rate":"事實表未涵蓋（缺資本支出、折舊、營運資金變動）","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率 × 投入資本周轉率；內生成長率＝增量 ROIC × 再投資率。事實表只有 TTM 營業利益率 10.2%，沒有投入資本、資本支出、折舊、營運資金，三項都無法計算，列為資料缺口。代理讀數：2022→2025 年營收增 $1,681M，GAAP 營業利益增約 $240M（增量利潤率約 14%），但缺投入資本，無法換算成報酬率"}}}},"q3_growth":{"verdict":"🟡：核心車市飽和，營收四年持平；五年後的跑道靠 eProduct 占比提升，以及尚未驗證的資料中心電力。共識 EPS 年增約 10.5%，一半以上靠回購。","reasoning":"營收 2022–2025 年依序為 $12,635M、$14,198M、$14,086M、$14,316M，2026 年指引 $14.0–14.2B，四年幾乎沒長；共識營收 FY2027 為 $14,675M（+4.1%）。共識調整後 EPS 路徑：FY2025A 約 4.93（由 2026-10-29 CFO「指引中點約較 2025 年增 7%」回推）→ FY2026E 5.26 → FY2027E 5.90 → FY2028E 6.66，三年年複合約 10.5%，比營收成長高 6pp 以上。成長拆解：量約 0～+4%；價為負（議價與關稅轉嫁不足）；併購為零；回購每年約減股 4–5%（過去四季約市值 6%）。內生上界無法計算（缺投入資本、資本支出、折舊），改用營收年增約 4% 當量能代理，缺口約 6pp。缺口歸因：淨回購約 4–5pp；利潤率擴張約 1–2pp，包括成本控制、稅率，以及渦輪發電機 2027 年約 $300M、以中十幾 % 增量轉換，約貢獻每股 $0.17（以 25% 稅率、約 1.95 億股粗估）。缺口可歸因，不靠倍數重新評價。跑道：核心車用是成熟市場，滲透率概念不適用；eProduct 占營收由前九月 18% 升到 Q3 20%，PowerDrive 2026 年預期成長約 20%。第二條曲線（渦輪發電機、電池儲能、微電網逆變器）有廠房完工、UL 認證、7 家客戶取得樣品等具體進度，但沒有已揭露的終端客戶合約，算不上已證實的下一條曲線，所以給中而不給寬。衰退信號亮兩項：EPS 成長高於營收成長逾 5pp，以及燃油零件被替代技術壓縮。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_fy2026_guidance","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量：輕型車與市場同步（2026 年加權 −1~−2%），2027 年起有新案與渦輪發電機約 $300M；價：議價與關稅轉嫁不足，為負；併購：零；回購：過去四季約市值 6%，2026 年約七成自由現金流回饋股東；利潤率：成本控制與稅率","runway_years":"核心車用是成熟市場，滲透率年數不適用；eProduct 占營收 Q3 為 20%，事實表沒有歷年占比序列，無法推算到 30% 需要幾年","runway_post_y5":"🟡","endo_ceiling_basis":"無法計算：事實表沒有投入資本、資本支出、折舊與營運資金，增量 ROIC 與再投資率都是缺口。以營收年增約 4%（共識 FY2027）當內生量能代理，共識 EPS 三年年複合約 10.5%，超出代理值約 6pp；缺口可歸因於淨回購約 4–5pp 與利潤率擴張","segments":[{"item":"渦輪與熱管理（Q3 2026）","value":"營收 $1,372M（去年同期 $1,437M），分部調整後營業利益率 14.7%（去年 15.2%）；來源 10-Q 2026-09-30"},{"item":"PowerDrive（Q3 2026）","value":"季營收約 $700M 以上，EBIT 虧損約 $5M，季增約 20%；CFO 預期 2026 全年成長約 20%，目標增量轉換中十幾 %"},{"item":"eProduct 合計","value":"Q3 約 $708M，占營收 20%；前九月約 $1,968M，占 18%；Q3 輕型車 eProduct $630M，年增 33%，主要來自歐洲"},{"item":"電池儲能系統事業","value":"Q3 營收年減 $54M，全年拖累營收成長約 170bp；分部營收與利潤事實表未涵蓋"},{"item":"其餘分部","value":"事實表未涵蓋"},{"item":"資料中心與工業（2027 年起）","value":"渦輪發電機 2027 年營收目標約 $300M，首年增量轉換中十幾 %；電池儲能 2027 年量產就緒；微電網逆變器樣品已送 7 家客戶，UL 認證預計 2027 年初完成"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"季度毛利率事實表未涵蓋；年度依序 18.09%、18.8%、18.68%，TTM 19.8%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"前三季輕型車營收大致與加權市場同步，未見縮減，也未見超越"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"事實表未涵蓋"},{"signal":"EPS 成長顯著高於營收成長（差逾 5pp）","lit":true,"note":"共識 EPS 三年年複合約 10.5%，共識營收 FY2027 只增 4.1%"},{"signal":"自由現金流／淨利連 2 年低於 0.75","lit":false,"note":"2024 年約 2.2 倍、2025 年約 4.4 倍"},{"signal":"SBC／營收逾 5% 且上升","lit":false,"note":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"渦輪與熱管理分部 Q3 營收年減約 4.5%；電池事業因補貼缺口衰退"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流逾 60%","lit":false,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"營收四年持平，但仍在投資渦輪發電機廠與 2GW 產能"}],"trap_rating":"🟡（衰退信號亮 2 項）"}}},"q4_capital":{"verdict":"資本配置以回購為主，紀律尚可：2026 年約七成自由現金流回饋股東，買回價位約 10 倍本益比。併購報酬與 SBC 事實表未涵蓋。","reasoning":"現金轉換：2025 年自由現金流 $1,208M，對 GAAP 淨利 $277M 約 4.4 倍；2024 年 $729M 對 $338M 約 2.2 倍。GAAP 淨利被非現金項目壓低，現金面比帳面好。2026 年指引自由現金流 $0.9–1.1B、營運現金流 $1.6–1.7B。現金去向：股東回饋 2026 年預計逾 $700M（Q3 回購 $175M、股息 $35M，Q4 回購同規模），約占自由現金流七成。Q3 另做了債務收購（CFO 稱可增厚 EPS），淨槓桿 1.5 倍，目標 2.0 倍。資本支出投向北卡羅來納的渦輪發電機組裝廠與 2GW 產能，產能是否擴充尚未決定。近 12 個月沒有併購類 8-K；CEO 稱併購範圍已擴大到車用以外，但維持三條準則。回購報酬：以判斷日股價 $52.2 與 FY2026 共識 EPS 5.26 計，盈餘收益率約 10.1%；以前份判斷日 $65.82 的高位計也約 8.0%。自由現金流指引中點 $1.0B 對市值約 $10.48B，約 9.5%。10 年期公債殖利率事實表未涵蓋，只要低於約 6%，回購就過關。目前淨負債 $1,616M。SBC 占營收比、歷史併購的已實現報酬，事實表都未涵蓋。","fact_refs":["f_kpi3_free_cash_flow","f_kpi5_fy2026_guidance","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_dividend_yield_ttm","f_price_at_dd","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購類重大項目；歷史併購的已實現報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"現價回購的盈餘收益率約 10.1%（5.26 ÷ 52.2），以 $65.82 高位計約 8.0%；過去四季回購約 $725M、約市值 6%。10 年期殖利率事實表未涵蓋，低於約 6% 即過"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 事實表未涵蓋；回購使淨股數下降，但毛稀釋率無法驗證"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：近 12 個月沒有併購類 8-K，EPS 成長來源是回購與利潤率；回購與股息已寫在回購項，不另展開"}}}},"q5_valuation":{"verdict":"現價只要求 EPS 維持在 2026 年的水準：以 10 倍終端倍數回推，$52.2 對應長期 EPS 約 $5.2，等於零成長。回購帶來的每年約 4–5% 成長我信；2027 年車市與高檔利潤率一定撐得住，我不信。結論是合理價，不是便宜價。","reasoning":"前瞻本益比 9.92 倍（FY2026 共識 5.26），以 FY2027 計 8.85 倍。Trailing GAAP 本益比 22.1 倍被減損等項目扭曲，不採用。PEG 0.94（9.92 ÷ 三年 EPS 年複合 10.5%）。歷史位置只有 4 個年度端點可用：本益比在 48 分位；股價營收比 0.74 倍在最高點；EV/S 0.85 倍在 71 分位。營收端並不便宜，而且這不能當五年分位用。分母檢查：調整後 EPS 2026 年指引 $5.20–5.35，GAAP $4.65–4.84，差約一成；以 GAAP 中點計前瞻本益比約 11 倍，結論不變。自由現金流佐證調整後盈餘有現金支撐，分母不構成爭點。賣方平均目標價約 $78.6（MarketBeat 2026-10-10），隱含約 13 倍 FY2027 EPS，需要倍數重新評價，本次 Base 不採用。上行空間：一年以 Base FY2027 EPS 5.75 × 10 倍＝$57.5（+10.2%）；五年以 Base FY2030 EPS 7.15 × 10 倍＝$71.5（+37.0%）。同業前瞻倍數事實表未涵蓋，終端倍數只能對照自身現值 9.9 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_kpi5_fy2026_guidance"],"verdict_values":{"valuation":{"basis":"前瞻本益比（調整後 EPS）","tier":"車用 Tier 1 動力系統零件","peers":{"expanded":false,"reason":"事實表同業對照只有毛利率、營益率與 FCF 利潤率，沒有同業前瞻本益比或 EV 倍數，無法做倍數對照；終端倍數以自身現值與 4 個年度端點為錨"},"fwd_pe":9.92,"peg":0.94,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 9.9 倍、PEG 0.94 指向便宜，但有三點抵銷。第一，股價營收比 0.74 倍在近 4 個年度端點的最高點，EV/S 在 71 分位，營收端並不便宜。第二，調整後營業利益率在近年高點，循環股的低本益比可能落在高峰盈餘上。第三，以 Base 路徑與 10 倍終端倍數，五年年化約 7–9%（含股息），落在弱與中的交界。綜合判合理，不到便宜。五年分位：事實表只有 4 個年度端點，依規不外推，留空。","upside_short_pct":10.2,"upside_mid_pct":37.0,"denominator_disputed":false,"denominator_note":"調整後 EPS 2026 年指引 $5.20–5.35，GAAP $4.65–4.84，差約一成；以 GAAP 中點 4.75 計前瞻本益比約 11 倍，結論不變。2025 年 GAAP EPS 1.28 被非現金項目壓低，但同年自由現金流 $1.21B，調整後盈餘有現金支撐"}}},"q6_how_wrong":{"verdict":"🟡：最可能看錯的地方，是把循環高點的利潤率當成常態。2009 年與 2020 年都證明，量一掉，利潤會很快蒸發。","reasoning":"最強的三個反駁如下。一是循環：2008-05 到 2009-01 股價約 −67%，2009 年 Q2 調整後營業利益率只剩 0.1%；2020 年 Q2 調整後 EBIT $28M，去年同期 $249M。現在調整後營業利益率在近年高點，低本益比可能正是對高峰盈餘的折價。二是結構：燃油零件萎縮與 OEM 自製同時發生，渦輪與熱管理分部 Q3 營收年減約 4.5%、利潤率降 50bp，PowerDrive 仍小虧，組合轉換期間整體利潤率會被稀釋。三是揭露落差：渦輪發電機的設備安裝，2026-08-05 說第三季開始，2026-10-29 改為 12 月安裝、年底試產；交期、EBIT、合約規模在 8 月法說都沒有回答。壓力測試 5 項過 3 項。過關的三項：關稅（2025 年淨成本約 $28M，利潤率仍擴張）；中國產量 −6~−8%（2026 年利潤率仍擴張）；VW 降評（BWA 對其營收占比反而由 10% 升到 13%）。不過的兩項：車市衰退（量 −10%、遞減率約 18%，EPS 約 −18~−20%）；燃油零件萎縮只能算部分通過，計為不過。動能：股價 $51.94，低於 52 週均線 $57.39、高於 104 週均線 $45.78，RSI 27.7 超賣，26 週報酬 −6.77%，不是追高情境。","fact_refs":["f_price_at_dd","f_rsi14","f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_kpi1_adjusted_operating_incom"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率高檔的循環股：低本益比可能是對高峰盈餘的折價"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":5.26,"pe":9.92,"basis":"FY2026E 共識調整後 EPS 5.26（Koyfin 2026-10-31），股價 $52.2，對應 9.92 倍；終端倍數同樣乘當年度調整後 EPS，口徑一致"},"eps":{"bull":[5.33,6.05,6.95,7.9,8.8],"base":[5.27,5.75,6.3,6.75,7.15],"bear":[5.2,4.4,3.9,4.1,4.3]},"pe":{"bull":13,"base":10,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.3,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":4},"max_dd":{"lo":-55,"hi":-35,"basis":"歷史：2008-05 到 2009-01 調整後股價約 −67%（8 個月）；2020 年上半年營收年減 28%，Q2 調整後 EBIT 只剩 $28M；本輪自 2026-05 的 $65.82 已跌 21%。推導：若 2027 年車市衰退，EPS 落到約 $3.9–4.4，倍數壓到 7–7.5 倍，股價約 $27–33（−37%～−48%）；再加上情緒超跌的空間，下緣取 −55%。不照搬 2009 年 −67%，因為目前淨槓桿約 1.5 倍，2025 年自由現金流 $1.21B，但這只能降低幅度，不能排除深跌。","trigger_time":null},"basis":{"bull":"車市 2028 年回升，PowerDrive 轉盈；渦輪發電機 2029 年營收破 $1B，利潤率中高十幾 %。資料中心業務占比提高，帶動倍數重新評價到 13 倍，仍低於賣方平均目標價隱含的倍數。","base":"車市 2027 年持平小降、2028 年起溫和回升；渦輪發電機 2027 年約 $300M，但時程打折；EPS 路徑已含每年約 4–5% 的回購減股，所以淨回購殖利率填 0，避免重複計算。終端 10 倍約等於現值 9.9 倍，不靠倍數擴張。","bear":"2027–2028 年車市衰退式下滑（加權產量年減約 8–10%），燃油零件萎縮與中國 OEM 自製同時加速；遞減率約 18–20%，回購放緩，渦輪發電機延後。終端 7.5 倍取成長熄火到約 5% 時的循環股低檔倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2008-05 到 2009-01 股價約 −67%；2009 年 Q2 營收年減 39.6%、調整後營業利益率 0.1%；2020 年上半年營收年減 28%、Q2 調整後 EBIT $28M；2008–09 年產業零件出貨連兩年 −14%、−24%","assumption":"2027–2028 年加權車市不出現年減 8% 以上的衰退，Q4 指引的中十幾 % 遞減率在更大跌幅下仍然成立","consequence":"EPS 落到約 $3.9–4.4、倍數壓到 7–7.5 倍，股價約 $27–33（−37%～−48%），這是五年後虧損接近五成最可能的故事","ruling":"採納：Bear 機率給 30%，最大回撤給 −35%～−55%。不照搬 2009 年 −67%，因為目前淨槓桿約 1.5 倍、2025 年自由現金流 $1.21B，但這只能降低幅度。這條與唯一致命點部分重疊：致命點是這個故事最早可觀察到的結果（2027 年 EPS 指引），已補進觸發器","watch":"季度有機營收年增率對公司口徑的加權輕型車市場；連 2 季年減逾 5% 即減碼","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"],"fact_refs":["f_net_debt_m","f_kpi3_free_cash_flow"]},{"view":"論點失敗","evidence":"渦輪與熱管理分部 Q3 營收 $1,372M（去年 $1,437M），利潤率 14.7%（去年 15.2%）；10-K 稱多家主要 OEM 表明要自製部分零件，中國本土 OEM 擴大自製；Ken Research 稱供應商利潤率結構重置；Pitchgrade 指渦輪的替代風險最高（二手）","assumption":"燃油零件萎縮的速度，慢於 eProduct 轉盈的速度，組合轉換期間整體利潤率不被稀釋","consequence":"高利潤的燃油零件每年縮 5% 以上，低利潤的 PowerDrive 補不上，調整後營業利益率回到 9% 附近，EPS 年增歸零","ruling":"部分採納：列為長期風險並設分部門檻。不據此把護城河方向標為往下，因為公司整體有機營收仍與市場同步；本季也在中國拿到鋁線電機首案與三件電機案，在歐洲與南美拿到渦輪 conquest 案","watch":"渦輪與熱管理分部的有機營收年增率與利潤率；PowerDrive 分部損益","evidence_refs":["end_markets#0","competitive_share_entrants#1","customer_second_source#0","substitute_technology#1","supply_demand_durability#1"],"fact_refs":["f_kpi1_adjusted_operating_incom"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 2026-10-29 稱併購『已打開視野』，車用內外都在看；渦輪發電機產能是否擴充尚未決定；逆變器的產能投資規模，8 月法說不願回答。VW 評等降到 Baa1、S&P 展望負面；VW 占營收 13%、Ford 12%，前十大 71%","assumption":"資料中心業務成功後，公司仍把約七成自由現金流回饋股東，不用高價併購或大額資本支出換成長；主要客戶的財務壓力不會轉成更狠的降價","consequence":"成長兌現，但每股價值被稀釋：回購降速、資本支出拉高、併購溢價吃掉報酬；或 VW 等客戶逼價，讓車用利潤率掉 50–100bp","ruling":"採納為監測項。管理層的三條併購準則（核心能力、近期增厚、不多付）是目前唯一的約束；任何超過市值 5%（約 $520M）的交易，都要重跑分析","watch":"每季回購金額（Q4 預計 $175M）、資本支出指引、併購公告、VW 長期評等","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"],"fact_refs":["f_ev_m","f_kpi3_free_cash_flow"]},{"view":"價格已反映太多","evidence":"股價營收比 0.74 倍，在近 4 個年度端點的最高點，EV/S 0.85 倍在 71 分位；共識 FY2027–FY2028 EPS 年增約 12–13%，但共識營收 FY2027 只增 4.1%；2025 年關稅成本 $108M，只回收 $80M","assumption":"共識已把渦輪發電機 $300M、利潤率續升與回購全部算進去，營收端倍數並不便宜","consequence":"若 2027 年只有回購帶來的成長，EPS 約 $5.5，10 倍只值 $55，上行僅約一成","ruling":"部分採納：這是估值只給合理、不給便宜的原因。但前瞻本益比 9.9 倍本身不要求倍數擴張，所以不構成迴避理由","watch":"2027 年指引的 EPS 中點與共識 5.90 的差距","evidence_refs":["reg_tariff_export#0"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2","f_rev_consensus_fy2_m"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 65.82 → 本次 52.2（-20.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=65.82","side_b":"本次 price_at_dd=52.2","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 65.82 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 65.82 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 65.82 美元：Bull 價 114.4、Bear 價 32.25，五年期望值 +3.8%，基準年化 1.7%，不對稱比 0.96","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.96。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 65.82 美元：五年期望值 +3.8%，基準年化 1.7%，不對稱比 0.96","side_b":"本次情境、股價 52.2 美元：五年期望值 +30.9%，基準年化 6.5%，不對稱比 2.08","ruling":"再換股價、情境不動：起點價下跌 20.7%，五年期望值多 27.1 個百分點，基準年化多 4.8 個百分點，不對稱比由 0.96 升到 2.08。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"side_a":"公司、賣方與事實表三方一致：自由現金流強（2025 年 $1.21B、2026 年指引 $0.9–1.1B），回購持續，2026 年在產量下滑中利潤率仍擴張","side_b":null,"ruling":"一致，不需要裁決；這是 H3 的證據基礎","evidence_level":"高","settle_metric":"年度自由現金流","if_then":[],"evidence_refs":[]},{"axis":"賣方目標價與股價方向相反","cause":null,"side_a":"賣方平均目標價 $78.57（MarketBeat 2026-10-10，共識偏買進）；Q2 後 JPMorgan 上調到 $85、Barclays 上調到 $85；FY1 共識 EPS 近 3 個月上修 1.54%","side_b":"股價由前份的 $65.82 跌到 $52.2（−21%），26 週報酬 −6.77%，RSI 27.7。盈餘上修而股價下跌，等於倍數由約 12.7 倍壓到 9.9 倍","ruling":"性質：不可調和（方向相反）。裁決站市場一側的一半。賣方目標價隱含約 13 倍 FY2027 EPS，需要倍數重新評價；而 Q3 的 EPS 上修來自回購與稅率，營收區間上緣反而下修，有機營收指引由 −3.5%～−1.5% 降到 −4%～−2.5%。市場為 2027 年車市逆風打折（CFO 點名利率與購車負擔）有根據。決勝的硬數據是 2027 年 2 月的指引。現在就買的最強論證：自由現金流殖利率約 9.5%，股息 1.3% 加回購約 5%；即使 EPS 零成長、倍數不變，也有中個位數報酬。而且 RSI 已超賣，股價離 104 週均線 $45.78 只剩約 12%","evidence_level":"高（公司指引與共識快照）","settle_metric":"2027 年調整後 EPS 指引中點與有機營收指引","if_then":["若 2027 年指引的有機營收不落後市場，且調整後 EPS 中點 ≥$5.75，則重跑分析後以 2% 首倉分批建立","若股價先跌到 $45 以下，但最近一季有機營收年減未逾 5%，則分批反買，倉位上限 3%","反向：若指引的 EPS 中點 <$5.26，或有機營收年減逾 5%，則不建倉，已持有者減碼一半"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"EPS 上修與營收下修","cause":null,"side_a":"Q3 調整後 EPS $1.39，高於共識約 $1.24（二手來源）；全年調整後 EPS 指引由 $5.05–5.30 上調到 $5.20–5.35","side_b":"Q3 營收年減約 2.9%；全年營收區間上緣由 $14.3B 降到 $14.2B；有機營收指引由 −3.5%～−1.5%（2026-08-05 CFO Craig Aaron）降到 −4%～−2.5%（2026-10-29）。EPS 上調的原因是回購與稅率","ruling":"性質：可調和（程度差異）。盈餘品質靠成本控制與回購，不是靠量；這支撐 H3，不支撐 H1，所以 2027 年有機營收是決勝數據","evidence_level":"高（公司前後兩次指引）","settle_metric":"2027 年有機營收指引減加權市場","if_then":["若 2027 年有機營收指引不落後市場，則 H1 成立，依首倉條件分批建立","若有機營收落後市場逾 2pp，而 EPS 仍靠回購上修，則不追，維持觀望"],"evidence_refs":[]},{"axis":"管理層 8 月承諾與 10 月實績","cause":null,"side_a":"2026-08-05 CEO Joseph Fadool：渦輪發電機組裝廠設備預計第三季開始安裝；今年會有部分電池儲能訂單；對目前超越市場的幅度不滿意，新案會改善","side_b":"2026-10-29 CEO：廠房完工，產線與設備安裝預計 12 月，年底開始試產；電池儲能只說專注拿下第一張訂單，2027 年再多說；Q3 輕型車營收仍只與市場同步。已兌現的部分：UL 子系統認證大致完成，微電網逆變器樣品由 4 家客戶增到 7 家","ruling":"性質：可調和（時程延後約一季，未改 2027 年 $300M 目標）。但三項承諾裡有兩項落後，Base 只給渦輪發電機 2027 年營收約六成把握，其餘放在 Bull","evidence_level":"中（管理層口頭陳述，沒有合約揭露）","settle_metric":"2026 年底試產是否完成；2027 年初揭露的出貨曲線與首批客戶","if_then":["若 2027 年 Q1 法說確認試產完成，並揭露首批終端客戶，則 Base 維持 $300M","若 2027 年 Q1 仍無客戶合約，或目標下修，則把渦輪發電機貢獻移出 Base，Bear 機率上調到 35%"],"evidence_refs":[]},{"axis":"客戶多元的說法與集中度數據","cause":null,"side_a":"2026-10-29 CEO：公司大概是動力系統領域客戶組合最多元的一家，一家客戶輸、另一家客戶就贏","side_b":"10-K：VW 13%（2024 年 10%）、Ford 12%，前十大 71%；VW 2025-03 遭 Moody's 降到 Baa1，展望負面","ruling":"性質：可調和（相對同業多元，絕對值仍集中）。列為中期風險，不當護城河證據","evidence_level":"高（10-K）","settle_metric":"年度前兩大客戶占比與 VW 評等","if_then":["若 VW 或 Ford 任一失去主要平台、占比跌到 8% 以下，則減碼一半","若 VW 長期評等再降到投資級最低一級以下，則停止加碼"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"axis":"估值與評等（股價下跌）","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份 2026-05-24：股價 $65.82，評等 B，估值合理，裁決為等 W52 拉回 $46–50 後分批進場","side_b":"本次 2026-11-03：股價 $52.2（−21%）；FY1 共識 EPS 三個月由 5.18 升到 5.26；前瞻本益比由約 12.7 倍（以 5.18 粗算）降到 9.92 倍。估值仍判合理，但由偏上移到偏下；評等維持 B；裁決與角色依本次輸入重算","ruling":"估值改善全部來自股價，基本面只小幅上修。維持合理而非便宜，理由見估值題：利潤率在高點，營收端倍數在 4 年端點的高位","evidence_level":"高","settle_metric":"前瞻本益比與 2027 年指引","if_then":["若股價跌到 $45 以下，而有機營收年減未逾 5%，則分批反買"],"evidence_refs":[]},{"axis":"價值陷阱判讀","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險為 🟡","side_b":"本次仍為 🟡：衰退信號亮兩項（EPS 成長高於營收成長逾 5pp；燃油零件被替代技術壓縮）。新證據是 Q3 渦輪與熱管理分部的營收與利潤率同步下滑，以及 10-K 的 OEM 自製風險","ruling":"結論不變，依據換成本季的分部數據","evidence_level":"中","settle_metric":"渦輪與熱管理分部有機營收","if_then":["若亮燈增加到 3 項，則改判高風險並停止加碼"],"evidence_refs":["end_markets#0"]},{"axis":"前份未記錄的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這七欄皆為空（舊格式未產出）","side_b":"本次：護城河方向 →；五年後跑道 🟡；主型為循環/商品；循環位置為中循環；情境機率 20／50／30；最大回撤 −35%～−55%","ruling":"這不是判斷翻轉，是格式補欄；之後以本次為比較基準","evidence_level":"—","settle_metric":"下一份判斷的同欄比較","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場欄；裁決文字為「等 W52 拉回 $46-50 後分批進場」","side_b":"本次：2027-02 公布的 2027 年指引，有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75，則重跑分析後以首倉 2% 分批建立；若價格先到 $45 以下，且有機營收年減未逾 5%，則可提前分批反買、加碼","ruling":"由價格錨改為事件錨。股價已跌到 $52.2、接近前份區間，但 Q3 有機營收指引下修，CFO 又點名 2027 年逆風，決勝點從價格變成 2027 年車市。價格條件下移到 $45（約 FY2027 共識 7.6 倍），只留作反買用","evidence_level":"中","settle_metric":"2027 年指引","if_then":["若 2027 年指引符合條件，則首倉 2% 分批建立","若指引的 EPS 中點 <$5.26，則不建倉"],"evidence_refs":[]},{"axis":"出場門檻（減碼與清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（空）；前份的風險門檻為：連 4 季集團營業利益率 <9.5%，連 4 季 Air Management 有機營收 <−7%","side_b":"本次：TTM 調整後營業利益率連 3 季 <9.6% 則清倉；有機營收連 2 季落後市場逾 2pp 則減碼；2027 年 EPS 指引中點 <$5.26 則減碼一半；渦輪與熱管理分部有機營收連 4 季 <−5% 則停止加碼；年度自由現金流 <$0.81B 則減碼","ruling":"門檻改用與 H1、H3 漂移規則同一套數字（偏離 5%／10%）。燃油分部門檻由 −7% 收緊到 −5%，因為 Q3 已出現約 −4.5% 的營收跌幅，等到 −7% 會太晚","evidence_level":"中","settle_metric":"季報","if_then":[],"evidence_refs":["end_markets#0"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（空）","side_b":"本次 Single Thing：2027-02 公布的 2027 年調整後 EPS 指引中點，低於 2026 年水準（約 $5.26）","ruling":"選這一項，是因為車市量能是數學上最大的單一敏感度：量每少 10%，EPS 約少 18–20%；而年度指引是最早、最明確的二元觀察點。渦輪發電機延遲對 EPS 的影響約 $0.17，較小","evidence_level":"中","settle_metric":"2027 年指引","if_then":["若發生，則不建倉，已持有者減碼一半"],"evidence_refs":[]},{"axis":"假設與風險改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：eProducts 2027 年營收 ≥$4.3B（占 25%）且利潤率 ≥8%；R1：連 4 季集團營業利益率 <9.5%；R2：合併案與中國電動車價格戰；R3：連 4 季 Air Management 有機營收 <−7%","side_b":"本次 eProduct 前九月約 $1,968M（18%）、Q3 約 $708M（20%），年化約 $2.8B，2027 年 $4.3B 已不可能達成。H1 改為車用本業利潤率防守與不落後市場；eProduct 改為 2030 年占比 ≥30% 的五年假設（H4）；燃油分部風險改用渦輪與熱管理分部口徑；前份 R2 的價格戰併入護城河威脅中的供應商利潤率重置項","ruling":"前份 H1 依新證據判為失敗並退休，理由是 eProduct 的實際規模只有目標的約三分之二。前份 R1 的 9.5% 門檻保留在 H1 反轉線附近（9.6%），沒有刪除","evidence_level":"高（10-Q）","settle_metric":"eProduct 占營收比","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 2 月財報給出 2027 年指引：有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75","type":"估值rearm","maps_to":"H1","metric":"2027 年有機營收指引減加權市場；調整後 EPS 指引中點","threshold":"≥0pp 且 ≥$5.75","action":"觸發後重跑分析，確認後以首倉 2% 分三批建立，上限 3%","source_freq":"年度指引（Q4 財報）","date":"2027-02"},{"n":2,"text":"股價先跌到 $45 以下，但最近一季有機營收年減未逾 5%","type":"加碼","maps_to":"H3","metric":"股價；季度有機營收年增率","threshold":"≤$45 且 ≥−5%","action":"分批反買 1%，總倉位上限 3%","source_freq":"每日股價／季報","date":null},{"n":3,"text":"Single Thing：2027 年調整後 EPS 指引中點低於 2026 年水準","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年調整後 EPS 指引中點","threshold":"<$5.26","action":"不建倉；已持有者減碼一半，Bear 機率上調到 40%","source_freq":"年度指引","date":"2027-02"},{"n":4,"text":"車市衰退：有機營收連 2 季年減逾 5%，且調整後營業利益率跌破 10%","type":"減碼","maps_to":"R1","metric":"季度有機營收年增率；調整後營業利益率","threshold":"連 2 季 <−5% 且 <10%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":5,"text":"H1 反轉：TTM 調整後營業利益率連 3 季低於 9.6%","type":"清倉","maps_to":"H1","metric":"TTM 調整後營業利益率","threshold":"連 3 季 <9.6%","action":"清倉","source_freq":"季報","date":null},{"n":6,"text":"燃油零件萎縮加速：渦輪與熱管理分部有機營收連 4 季年減逾 5%，或分部利潤率跌破 13%","type":"風險","maps_to":"R4","metric":"渦輪與熱管理分部有機營收年增率；分部調整後營業利益率","threshold":"連 4 季 <−5% 或 <13%","action":"停止加碼，Bear 機率上調到 35%","source_freq":"10-Q 分部揭露（每季）","date":null,"evidence_refs":["end_markets#0","substitute_technology#1"]},{"n":7,"text":"渦輪發電機兌現：年底完成試產，2027 年 Q1 揭露首批終端客戶與出貨曲線","type":"假設驗證","maps_to":"H2","metric":"首批終端客戶合約；2027 年營收目標","threshold":"2027 年 Q1 前揭露，且目標維持 ≥$300M","action":"未兌現就把渦輪發電機移出 Base","source_freq":"季度法說","date":"2027-05"},{"n":8,"text":"關稅吸收失敗：關稅淨成本（費用減客戶回收）年化逾 $100M，或 USMCA 未續約","type":"風險","maps_to":"R3","metric":"關稅費用減回收；USMCA 續約結果","threshold":"逾 $100M／年，或未續約","action":"停止加碼","source_freq":"10-K／10-Q MD&A","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":9,"text":"主要客戶流失：VW 或 Ford 任一占營收跌到 8% 以下","type":"減碼","maps_to":"R2","metric":"前兩大客戶營收占比","threshold":"<8%","action":"減碼一半","source_freq":"10-K（每年）","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":10,"text":"Q4 2026 財報與 2027 年指引公布後重跑分析","type":"複審日期","maps_to":null,"metric":"—","threshold":"—","action":"重跑分析","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"TTM 調整後營業利益率","bear_threshold":"連 3 季 <9.6% → 清倉","window":"2027–2028 年","source":"季度新聞稿","last_status":"ok"},{"metric":"季度有機營收年增率減加權輕型車市場","bear_threshold":"連 2 季落後逾 2pp → 減碼","window":"2027 年","source":"季度法說（公司的市場口徑）","last_status":"ok"},{"metric":"2027 年調整後 EPS 指引中點","bear_threshold":"<$5.26 → 減碼一半","window":"2027-02","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"渦輪與熱管理分部有機營收年增率","bear_threshold":"連 4 季 <−5% → 停止加碼","window":"2027–2028 年","source":"10-Q 分部揭露","last_status":"warning"},{"metric":"年度自由現金流","bear_threshold":"<$0.81B → 減碼","window":"FY2026–FY2028","source":"10-K 現金流量表","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027-02 公布的 2027 年指引：有機營收成長不低於加權市場，且調整後 EPS 中點 ≥$5.75","exec_line":"觸發後重跑分析，確認後以 2% 首倉分三批建立，上限 3%；若股價先跌到 $45 以下、但有機營收年減未逾 5%，可分批反買；Single Thing 發生則不建倉","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027-02 公布的 2027 年指引：有機營收不落後加權市場，且調整後 EPS 中點 ≥$5.75；或股價先跌到 $45 以下，且有機營收年減未逾 5%"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-6.77, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027-02 公布的 2027 年指引：有機營收不落後加權市場，且調整後 EPS 中點 ≥$5.75；或股價先跌到 $45 以下，且有機營收年減未逾 5%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"車用本業在產量下滑中守住調整後營業利益率，2027 年起有機營收不落後加權市場","2y":"FY2026 調整後營業利益率落在指引 10.7–10.9%；FY2027 ≥10.5%，且有機營收成長 ≥ 加權輕型車市場","5y":null,"10y":null,"threshold":"FY2026 調整後營業利益率 ≥10.7%；FY2027 ≥10.5%；有機營收成長減加權市場 ≥0pp","source":"季度新聞稿與法說（公司以地理曝險加權的輕型車產量作為市場口徑）","drift_rule":"TTM 調整後營業利益率連 2 季低於 10.2%（偏離 5%）＝削弱；連 3 季低於 9.6%（偏離 10%）＝反轉"},{"id":"H2","text":"渦輪發電機 2027 年營收約 $300M，首年增量利潤率中十幾 %","2y":"2026 年底完成試產；2027 上半年揭露客戶與出貨曲線；2027 年營收 ≥$300M","5y":null,"10y":null,"threshold":"2027 年營收 ≥$300M（管理層 2026-08-05 與 2026-10-29 兩次重申）；增量轉換 ≥13%","source":"2026-10-29 法說，CEO Joseph Fadool、CFO Craig Aaron；公司承諾 2027 年初揭露的成長曲線","drift_rule":"2027 年指引把 $300M 下修 5% 以上、連 2 季＝削弱；全年低於 $270M（偏離 10%）＝反轉"},{"id":"H3","text":"自由現金流每年 ≥$0.9B，約七成回饋股東，流通股每年減約 3–5%，支撐每股盈餘年增 ≥7%","2y":null,"5y":"FY2026–FY2030 平均自由現金流 ≥$0.9B；流通股數 FY2030 ≤172M 股（由約 200.8M 股每年減 3%）；調整後 EPS FY2030 ≥$7.0","10y":null,"threshold":"年度自由現金流 ≥$0.9B；年度股數減幅 ≥3%","source":"10-K／10-Q 現金流量表與稀釋股數","drift_rule":"TTM 自由現金流連 4 季低於 $855M（偏離 5%）＝削弱；連 6 季低於 $810M（偏離 10%）＝反轉"},{"id":"H4","text":"電動化產品轉為穩定獲利，避免燃油零件萎縮時整體利潤率被稀釋","2y":null,"5y":"PowerDrive 分部 2027 年調整後營業利益轉正，2030 年利潤率 ≥8%；eProduct 占營收由 2026 年 Q3 的 20% 升到 2030 年 ≥30%","10y":null,"threshold":"PowerDrive 分部 2027 全年調整後營業利益 ≥0；eProduct 占比每年增加 ≥2pp","source":"10-Q 分部揭露、季度法說","drift_rule":"PowerDrive 分部 TTM 利潤率連 4 季低於 0%，且 eProduct 營收年增 <15%＝削弱；連 6 季＝反轉"}],"R":[{"id":"R1","text":"2027–2028 年車市衰退式下滑：量一掉，遞減率會讓高檔利潤率快速回落。2009 年 Q2 營業利益率只剩 0.1%，2020 年 Q2 調整後 EBIT 只剩去年同期的約一成","h_ref":"H1","clock":"⚡","threshold":"有機營收連 2 季年減逾 5%，且調整後營業利益率 <10%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R2","text":"客戶集中與客戶信用：VW 13%、Ford 12%、前十大 71%，VW 評等降到 Baa1 且展望負面；失去主要平台或客戶逼價，衝擊會不成比例","h_ref":"H1","clock":"🔥","threshold":"VW 或 Ford 任一占營收 <8%，或 VW 長期評等再降一級以上","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"關稅與貿易協定：2025 年關稅成本約 $108M，客戶回收約 $80M；USMCA 2026 年待續約；IEEPA 退款已收約 $35M，但金額與時點不確定，尚未認列","h_ref":"H1","clock":"🔥","threshold":"關稅淨成本年化 >$100M，或 USMCA 未續約","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"id":"R4","text":"燃油零件結構萎縮加上 OEM 自製：渦輪與熱管理分部營收與利潤率同步下滑，中國本土 OEM 把零件收回自製，eProduct 轉盈跟不上","h_ref":"H4","clock":"🐢","threshold":"渦輪與熱管理分部有機營收連 4 季年減逾 5%，或分部利潤率 <13%","evidence_refs":["end_markets#0","substitute_technology#1","competitive_share_entrants#1","customer_second_source#0","supply_demand_durability#1"]},{"id":"R5","text":"渦輪發電機時程或客戶落空：設備安裝 8 月說第三季開始，10 月改為 12 月；CEO 承認政治環境可能拖慢合約定案；交期、EBIT 與合約規模都未揭露","h_ref":"H2","clock":"🔥","threshold":"2027 年 Q1 前沒有揭露首批終端客戶，或下修 2027 年 $300M 目標","evidence_refs":[]}],"single_thing":{"description":"2027-02 公布的 2027 年調整後 EPS 指引中點，低於 2026 年水準（約 $5.26）","why_fatal":"公司每年靠回購減股約 4–5%，指引若仍是零成長，代表營業利益至少衰退約 5%，也就是車市衰退或高檔利潤率開始回落。這會同時打掉利潤率防守（H1）與回購複利（H3），倍數也會從約 10 倍往 7.5 倍走，股價對應約 $40 以下","if_happens":"不建倉；已持有者減碼一半，Bear 機率上調到 40%，重跑情境樹","how_monitor":"Q4 2026 財報（2027-02）。在那之前，看 2026 年 Q4 實際營收是否接近 CFO 給的約 $3.43B，以及法說會對 2027 年市場的說法","probability":"20%（12–24 個月）：CFO 已點名利率與購車負擔，但同時預期 2027 年有新案、渦輪發電機約 $300M，以及小幅超越市場"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.85,"peg_fy2":0.84,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.93,"FY2026E":5.26,"FY2027E":5.9,"FY2028E":6.66},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（非 GAAP）。FY2025A 4.93 由 2026-10-29 法說 CFO「2026 年指引中點約較 2025 年調整後 EPS 增 7%」回推（5.275 ÷ 1.07），事實表未直接收錄；FY2026E–FY2028E 為 Koyfin 2026-10-31 共識；2025 年 GAAP 稀釋 EPS 為 1.28"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"渦輪發電機北卡羅來納組裝廠安裝產線與設備，年底前開始試產","impact":"中","watch":"Q4 法說是否確認試產完成"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年全年指引","impact":"高","watch":"有機營收是否不落後加權市場、調整後 EPS 中點是否 ≥$5.75"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"管理層承諾在 2027 年初揭露渦輪發電機出貨曲線與客戶","impact":"高","watch":"是否有終端客戶合約、$300M 目標是否維持"},{"date":"2026","date_precision":null,"type":"regulatory","event":"USMCA 2026 年續約","impact":"中","watch":"是否續約、新條款是否不利於車用零件"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"微電網逆變器 UL 認證預計 2027 年初完成","impact":"低","watch":"認證是否完成、首張訂單是否落地"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
