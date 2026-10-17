你是 DD 管線 v20 的判斷層閘（gate），標的 JNJ（20261018）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap_reported_sales`（q1_business）｜營收（GAAP reported sales）＝25399 USD M｜期間與口徑：Q3 FY2026（公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 jnj.com Q3 2026 press release（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（公告於 2026-10-13））
  - 註記：未查得
- `f_kpi1_non_gaap_adjusted_income`（q1_business）｜Non-GAAP 稅前利益率（adjusted income before tax / sales；JNJ 不揭露 non-GAAP 營業利益，以此代替）＝30.2 %｜期間與口徑：Q3 FY2026（公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 adjusted income before tax 7,672 ÷ 營收 25,399（自算）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（公告於 2026-10-13））
  - 註記：未查得
- `f_kpi2_gaap_sm_a_r_d_ipr_d_othe`（q1_business）｜GAAP 營業利益／利益率（自算：毛利−SM&A−R&D−IPR&D減損−重組；不含 Other expense 5,780 的 talc 等一次性項目）＝23.0 %｜期間與口徑：Q3 FY2026（公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿損益表自算：17,302−6,285−4,652−339−181＝5,845M（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（公告於 2026-10-13））
  - 註記：未查得
- `f_kpi4_2026_10`（q1_business）｜管理層全年指引（2026，10 月上調）＝adjusted EPS $11.05–$11.15（中點 $11.10） USD｜期間與口徑：Q3 FY2026（公告於 2026-10-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 guidance 表（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（公告於 2026-10-13））
  - 註記：consensus FY1 EPS 11.08（dd_numbers_extra.py consensus_revision，2026-10-08 快照）
- `f_peer_jnj_gross_margin_pct`（q2_moat）｜JNJ 毛利率＝67.91 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JNJ.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jnj_operating_margin_pct`（q2_moat）｜JNJ 營業利益率＝26.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JNJ.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-13 date｜期間與口徑：2026-10-13／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-13）
- `f_peer_jnj_fcf_margin_pct`（q2_moat）｜JNJ FCF 利潤率＝22.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JNJ.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mrk_operating_margin_pct`（q2_moat）｜MRK 營業利益率＝10.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRK.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lly_operating_margin_pct`（q2_moat）｜LLY 營業利益率＝49.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LLY.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abbv_operating_margin_pct`（q2_moat）｜ABBV 營業利益率＝33.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bsx_operating_margin_pct`（q2_moat）｜BSX 營業利益率＝21.0 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BSX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bsx_gross_margin_pct`（q2_moat）｜BSX 毛利率＝69.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BSX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝11.08 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.18 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝14.8 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝4.23 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（14.2 → 14.8）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝101222.92 USD m｜期間與口徑：2026-10-18／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝107904.34 USD m｜期間與口徑：2026-10-18／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF，前三季累計，非單季）＝15100 USD M（約）｜期間與口徑：2026 前三季累計（估計，截至 2026-10-13 公告）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 overall financial results 表（~$15,100M；腳註為 YTD 估計）（numbers.latest_quarter_kpis.items[3]，as_of 2026 前三季累計（估計，截至 2026-10-13 公告））
  - 註記：未查得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝28278.0 USD m｜期間與口徑：2026-10-18／yfinance 最新一季：總債務 49036.0、現金 20758.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝2409.9 m shares｜期間與口徑：2026-10-18／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.066 %｜期間與口徑：2026-10-18／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-18）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝255.56 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝23.6 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 11.08，分子＝快照價 261.44｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-4.15 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 11.56 → 11.08（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝38.78 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.2 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.48 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.36 x｜期間與口徑：2026-10-18／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-18）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.83｜期間與口徑：2026-10-16（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-16（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝10.3 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-16（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（18 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Stelara 2026 Q1 銷售 6.56 億美元、年減約 59–60%，因生物相似藥進入；Q2 10-Q 預期 biosimilar 持續衝擊，Q2 約 -55.7%。Simponi 生物相似藥已於 2026 Q2 進入歐洲，美國可能 2026 年稍後出現。
  - 來源：JNJ Form 10-Q Q2 FY2026; Nasdaq 'Johnson & Johnson Q2 earnings call highlights'（as_of 2026-06-28）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：MedTech 2026 Q2 放緩：心血管受電生理競爭（脈衝電場消融 PFA）壓力與 Abiomed 銷售 -2%（英國研究使 Impella 使用放緩，J&J 稱為暫時）拖累，Shockwave 仍雙位數成長；電生理銷售 +3.1%。
  - 來源：Nasdaq/Zacks 'J&J's MedTech Performance Slows in Q2: Will Sales Improve in H2?'（as_of 2026-06-28）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：三大批發商分別約占總毛營收 21.8%、15.5%、11.1%（合計約 48.4%），FY2024 為 20.5%/15.6%/12.3%，集中度上升
  - 來源：JNJ Form 10-K FY2025（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：FTC 於 2026 年 6 月向第四巡迴上訴法院提交 amicus brief，主張地方法院駁回 CareFirst 對 J&J 以專利延遲 Stelara 生物相似藥競爭之反壟斷訴訟時，適用了錯誤的法律標準（應看競爭效果而非意圖）。這是私人訴訟，非 FTC 對 J&J 的調查。
  - 來源：GENE ONLINE / PSCA 'FTC Weighs in on Pharmaceutical Anti-Trust Case'（as_of 2026-06-01）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Biosense Webster（J&J 旗下）在 Innovative Health 的心導管再處理案中遭陪審團判反壟斷敗訴，法官將損害賠償三倍至 4.42 億美元；J&J 其後聲請推翻判決，搜尋未找到後續結果。
  - 來源：MassDevice 'Johnson & Johnson seeks to have $442 million antitrust verdict tossed out'（as_of 2025-12-31）｜affects：decision_inputs.bear、valuation
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：比利時競爭主管機關因『教科書式』的反競爭品類管理，對 J&J Consumer、Boehringer Ingelheim 與 Haleon 合計罰款 1,120 萬歐元。
  - 來源：Global Competition Review 組織頁 Johnson & Johnson（as_of 2025-11-30）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：一份顧問報告指出，截至 2026 年 6 月，Pfizer、J&J、GSK 仍無已確認的 Commerce 在地製造協議（與 J&J 1 月宣布的 MFN／關稅豁免協議的關係，搜尋結果未釐清）。
  - 來源：Exiger／intuitionlabs 等搜尋摘要（Pharma Tariffs 2026: Supply Chain & Manufacturing Impacts）（as_of 2026-06-30）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：J&J 2025 年關稅成本預估由約 4 億美元降至約 2 億美元，主要集中於醫療器材（MedTech）；2025 年 7 月 CFO 表示 2026 年關稅影響尚難預測。
  - 來源：Reuters via TradingView — Johnson & Johnson lifts 2025 forecast, halves tariff cost outlook（as_of 2025-07-16）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：J&J 財務長表示 2025 年關稅成本約 4 億美元，其中以中國關稅及中國報復性關稅為最大部分；2026 年影響當時尚難預測
  - 來源：MedTech Dive: J&J tariff costs $400 million 2025（as_of 2025-10-14）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：歷史單點失效案例：2010 年 McNeil Fort Washington 工廠因品質違規停工逾兩年；2021 年 Emergent Baltimore 廠（合約製造）混料致約 1,500 萬劑 J&J 新冠疫苗報廢。均為舊事件，非現況集中度證據
  - 來源：AboutResilience; Risk & Insurance; NPR (2021-04-01)（as_of 2021-04-01）｜affects：decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Q3 2026 MedTech 營運成長 2.5%，低於管理層預期；弱點在國際心血管、外科與 Abiomed；Vision +5.1%
  - 來源：J&J Q3 2026 results (search summary)（as_of 2026-10-13）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Q2 2026 Stelara 因生物相似藥銷售下滑 59.7% 至 $656.0M；公司預期生物相似藥持續衝擊；Tremfya 首度單季破 $2B
  - 來源：J&J 10-Q (Q2 2026) / MarketBeat Q2 call highlights（as_of 2026-07-15）｜affects：thesis.R、decision_inputs.bear
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：電生理面臨 PFA 導管競爭壓力；中國量採（VBP）為跨部門持續逆風；骨科預計 2027 年中前分拆 DePuy Synthes，2026 年相關分拆成本 $0.4B
  - 來源：J&J 10-Q Q2 2026 (search summary)（as_of 2026-07-15）｜affects：thesis.R、moat_trend、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：J&J FY2025 10-K 列為風險因素：新產品/製程/技術的研發競爭可能造成產品與製程過時；專利到期後會有學名藥、生物相似藥進入（通用條款，未點名特定替代技術）
  - 來源：SEC Form 10-K FY2025 (JNJ)（as_of 2025-12-28）｜affects：decision_inputs.bear、moat_trend
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Stelara 2026 年第一季銷售衰退快於公司預期，預期全年加劇；Amgen、Teva、Samsung Bioepis/Sandoz 等生物相似藥已在美上市；Simponi、Opsumit 預期 2026 起受學名藥衝擊
  - 來源：Zacks: can jnj sustain growth amid patent legal and china risks（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear、valuation
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：2026-04-14 第三巡迴上訴法院裁定 J&J 未能證明三星 Bioepis 第二個 Stelara 生物相似藥上市會損害其業務，J&J 敗訴
  - 來源：Bloomberg Law: J&J Loses Appeal to Block Samsung's Stelara Biosimilar Drug Copy（as_of 2026-04-14）｜affects：thesis.R、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：美國最高法院 2026-04-20 駁回 J&J 對滑石粉證券集體訴訟（class certification）的上訴請求；第三巡迴法院 2025-07 維持集體認證，2025-10 駁回 en banc 重審。
  - 來源：Mealey's / Harris Martin 報導（as_of 2026-04-20）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：滑石粉石棉揭露不實之證券集體訴訟（2018 起，股東期間 2013-02-22 至 2018-12-13）：最高法院 2026-04-20 駁回 J&J 上訴請求，集體認證確立，案件朝審判或和解推進。
  - 來源：Harris Martin Talc（as_of 2026-04-20）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":422.4,"bear_5y_price":177.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":20.4,"ev5y_pct":16.3,"irr_base_pct":3.8,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":11.08,"pe":23.07,"basis":"FY2026 共識調整後 EPS（含 Firefly／Sail 稀釋 0.64 美元）；終端倍數同樣套在當年度調整後 EPS"},"eps":{"bull":[12.0,14.4,15.9,17.5,19.2],"base":[11.2,12.9,14.0,15.1,16.2],"bear":[10.7,11.0,11.3,11.6,11.8]},"pe":{"bull":22,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.066,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JNJ_Q2_2026_Earnings_Call_20260715.md
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 將 2026 全年營運銷售成長財測調升 $4 億，區間 6.5%–7.1%（原話："range of 6.5% to 7.1% with a midpoint of $100.6 billion"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：調整後營運 EPS 區間上調，中點增 $0.18（原話："range to $11.50 to $11.65, which equates to an increase"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 稱下半年營運銷售成長將改善（原話："sales growth to improve in the second half of the year"）
- 2026-07-15｜CFO Joseph Wolk｜margin：稅前營業利益率改善預期由原先逾 50bp 調為約 75bp（原話："We now expect approximately a 75 basis point"）
- 2026-07-15｜CFO Joseph Wolk｜margin：利益率改善的支撐之一是關稅相關成本的減少與追回（原話："recoupment of certain tariff-related costs"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：全年有效稅率預期下調至 17.0%–18.0%（原話："expected to be lower in a range of 17.0% to 18.0%"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：財測不含 Firefly Bio 等待完成的併購（原話："Our current outlook does not include the impact of any"）
- 2026-07-15｜Ryan Koors｜margin：創新藥 adjusted 稅前利益率由 42.7% 降至 42.5%，原因為產品組合與上市投入（原話："declined from 42.7% to 42.5%, primarily driven by"）
- 2026-07-15｜Ryan Koors｜margin：醫療科技 adjusted 稅前利益率由 22.2% 降至 22%（原話："declined from 22.2% to 22%, primarily driven by"）
- 2026-07-15｜Ryan Koors｜margin：銷管費用因新產品上市投入而去槓桿 60bp（原話："administrative expenses deleveraged by 60 basis points"）
- 2026-07-15｜Ryan Koors｜margin：營運銷售成長 5.6% 已吸收約 460bp 的 STELARA 逆風（原話："despite an approximate 460 basis point headwind from STELARA"）
- 2026-07-15｜Ryan Koors｜risk：電生理成長受中國庫存調整影響，管理層估計拖累 400bp（原話："China inventory, which we estimate to be 400 basis points"）
- 2026-07-15｜Ryan Koors｜competition：電生理成長被 PFA 競爭壓力部分抵銷（原話："partially offset by competitive PFA pressures"）
- 2026-07-15｜Ryan Koors｜competition：STELARA 下滑 55.7%，歸因於生物相似藥競爭（原話："driven by share loss due to biosimilar competition"）
- 2026-07-15｜Ryan Koors｜product：DARZALEX 成長 17.6%，各線治療市佔提升（原話："strong share gains of 5 points across all lines of therapy"）
- 2026-07-15｜CFO Joseph Wolk｜risk：CFO 承認醫療科技心血管（主要是心臟復原）表現未達公司標準（原話："standards in cardiovascular, primarily heart recovery"）
- 2026-07-15｜CFO Joseph Wolk｜guidance：CFO 對 Abiomed 下調預期，復原要到明年，在 PROTECT IV 前僅溫和成長（原話："more modest growth until our PROTECT IV data comes out"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：管理層重申本十年末達雙位數成長的能見度（原話："of sight to double-digit growth by the end of the decade"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 稱 2026 年營收將首度突破 $1,000 億（原話："on track to meet our 2026 target of more than $100 billion"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 設定 2030 年成為腫瘤第一大公司、銷售額逾 $500 億（原話："on track to be the #1 oncology company by 2030"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：資本配置優先順序不變；併購是成長推手但非必要條件（原話："but they are not a requirement to deliver on our"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：預計第三季完成 Firefly Bio 收購，補強 KRAS 實體瘤平台（原話："recently announced agreement to acquire Firefly Bio"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：股東回饋以股息為主（原話："committed to returning capital directly to shareholders"）
- 2026-07-15｜CFO Joseph Wolk｜capital_allocation：全年自由現金流展望維持接近 $210 億（原話："full year free cash flow outlook approaching $21 billion"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：骨科（DePuy Synthes）分拆維持 2027 年中時程（原話："on track for a mid-2027 separation"）
- 2026-07-15｜CFO Joseph Wolk｜commitment：將於 12 月 8 日企業業務回顧說明策略與長期展望（原話："Enterprise business review on December 8"）
- 2026-07-15｜Jennifer Taubert｜customer：ICOTYDE 上市處方與患者數更新（原話："over 18,000 prescriptions have been written"）
- 2026-07-15｜Jennifer Taubert｜customer：ICOTYDE 90 天內取得逾半商業保險覆蓋（原話："within 90 days we already have over 50% of"）
- 2026-07-15｜Jennifer Taubert｜product：管理層稱 ICOTYDE 未拖慢 TREMFYA 在乾癬領域的表現（原話："has not slowed down TREMFYA in psoriatic disease at all"）
- 2026-07-15｜Jennifer Taubert｜commitment：ICOTYDE 加碼投入，直接面對消費者廣告前一日開播（原話："started our direct-to-consumer advertising yesterday"）
- 2026-07-15｜Jennifer Taubert｜product：INLEXZO 本季銷售較上季成長逾一倍並優於市場預期（未單獨揭露）（原話："we more than doubled sales in second quarter versus"）
- 2026-07-15｜Jennifer Taubert｜product：TREMFYA 在潰瘍性結腸炎 IL-23 誘導期市佔 58%（原話："58% share of induction"）
- 2026-07-15｜John Reed｜risk：milvexian 為事件驅動試驗，讀數時點可能在年底或明年初，無法給具體時程（原話："towards the end of this year, beginning of next year"）
- 2026-07-15｜John Reed｜risk：對 milvexian 房顫適應症的語氣為審慎樂觀（原話："we're cautiously optimistic, but are waiting for the"）
- 2026-07-15｜Tim Schmid｜risk：MedTech 管理層稱未見廣泛性手術量放緩（原話："not seeing evidence of a broad-based slowdown in demand"）
- 2026-07-15｜Tim Schmid｜risk：管理層稱 ACA 補貼到期尚未觀察到對手術量的實質影響（原話："observed any meaningful impact on procedure volumes"）
- 2026-07-15｜Tim Schmid｜risk：MedTech 負責人承認心血管本季成長低於公司自身預期（原話："frankly, it's not where we wanted it"）
- 2026-07-15｜Tim Schmid｜competition：Abiomed 稱目前沒有已商業化的競爭對手（原話："no current commercialized competitors"）
- 2026-07-15｜Tim Schmid｜commitment：PROTECT IV 預計 2027 年讀數（原話："which we expect to read out in 2027"）
- 2026-07-15｜Tim Schmid｜guidance：Abiomed 預期未來數季逐步回到雙位數成長（原話："back to double-digit growth over the coming quarters"）
- 2026-07-15｜Tim Schmid｜commitment：今年預計推出兩項機器人手術產品（OTTAVA、MONARCH 泌尿），以取得核准為前提（原話："committed to 2 large robotic launches this year"）
- 2026-07-15｜CEO Joaquin Duato｜commitment：CEO 稱機器人平台在本十年末將成為醫療科技成長的重要貢獻者（原話："contributor to MedTech growth by the end of the decade"）

### 問答異常語氣（迴避／改口／保留）
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Goldman Sachs 問 ICOTYDE 處方醫師數較 6 月更新、試用品/免費藥、納保談判及何時分拆銷售｜答法：回答了處方數、保險覆蓋與 DTC，但未回應試用品/免費藥規模與何時單獨揭露銷售
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Wells Fargo 問 2026 全年（不含額外一週）MedTech 是否仍會比去年成長更快｜答法：回答聚焦於手術量穩定與下半年加速，未直接回答排除第 53 週後的全年成長率
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Guggenheim 問 INLEXZO 患者/處方醫師數、社區 vs 學術使用，及 SunRISe-5 數據預期｜答法：給出市佔與新患者插入成長比例，未提供患者或處方醫師絕對數，亦未設定 SunRISe-5 預期
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Raymond James 問 Abiomed 新的成長預期（先前認為是中段兩位數成長）及除等 PROTECT IV 外的對策｜答法：未給出新的成長率數字，只說下半年強於上半年並逐步回到雙位數，也未說明先前中段兩位數預期是否調整
- JNJ_Q2_2026_Earnings_Call_20260715.md｜問：Wolfe Research 問 milvexian 房顫的信心程度與是否仍在年底前讀數｜答法：稱事件驅動無法給讀數時點，信心以審慎樂觀表述，未給成功機率

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 5 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 7 | 4 |
| substitute_technology | found | 4 | 4 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Johnson & Johnson largest customer concentration McKesson Cardinal AmerisourceBergen percent of sales 2026；Johnson & Johnson single-source supplier risk customer in-house biosimilar 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260716","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"新藥引擎（Darzalex／Tremfya／Carvykti ＋ 新上市 icotrokinra／Rybrevant／Caplyta）淨接棒 Stelara 懸崖，IM operational 成長 6-8%","columns":{"2Y（FY26-27）":"IM operational ≥ +6%；Darzalex 年化 $17B+、Tremfya $8B+、Carvykti $2.5B+","5Y（FY28-30）":"腫瘤 franchise 2030 目標 $50B；IM 2025-30 CAGR 5-7%","10Y（FY31-35）":"2030 後次世代 pipeline 銜接，避免第二輪懸崖","具體門檻":"Q2 2026 IM +6.8% operational；Darzalex Q2 $4.21B(+18.9%)、Tremfya $2.05B(+72.5%)、Carvykti $657M(+49.4%)","來源":"JNJ Q2 2026 法說＋ Enterprise Business Review","漂移觸發":"連 2 季 TTM IM ex-Stelara &lt; +6% → 削弱"}},{"id":"H2","text":"MedTech operational 恢復至中個位數＋、OI margin 守 ~24%，且 DePuy Synthes 骨科（~29% MedTech 營收）分拆／出售乾淨執行","columns":{"2Y（FY26-27）":"FY2026 MedTech operational ≥ +4%（Q2 +3.6% borderline）；核心心血管／外科／視力 re-rate","5Y（FY28-30）":"分拆後留存組合 OI margin 對標 ABT 24.5%／MDT 25.8%","10Y（FY31-35）":"心血管介入＋機器人外科為 MedTech 主引擎","具體門檻":"Q2 2026 MedTech +3.6% operational（miss ~$8.97B 估）；Cardiovascular $2.4B(+3.1%)","來源":"JNJ FY25 10-K 分部揭露；Bloomberg 2026-02 $20B+ 出售探詢","漂移觸發":"連 2 季 TTM MedTech operational &lt; +3% 或分拆對價／時程惡化 → 削弱"}},{"id":"H3","text":"Talc 逐案訴訟＋潛在全球和解控制在有限責任（準備金 ~$10-13B，最壞 &lt; $35B），不被迫 mega-settlement；Section 232 藥品關稅豁免落實","columns":{"2Y（FY26-27）":"2026H2-2027 個案判決可控；準備金無跳升","5Y（FY28-30）":"2027-2028 若達全球和解，總額 ≤ $30B（分 5-8 年支付、年化 hit ≤ $5B）","10Y（FY31-35）":"2030 後 talc 大致 cleared，僅留 contingent reserve","具體門檻":"單筆和解 ≤ $30B（現金流 $19B 的 ~1.6x）；再啟破產策略或 $40B+ → H3 反轉","來源":"MDL 2738；JNJ 10-Q Note；Reuters／Law360","漂移觸發":"連 2 季準備金新增 &gt; $3B，或一次性付 $35B+ → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Section 232 藥品關稅落地：100% 專利藥／API 關稅豁免未於生效日前定案，落在 Innovative Medicine（65% 營收）進口品項；與已實現的醫材關稅（Q1 曾拖累 OI margin）機制不同、規模未定價","columns":{"對應假設":"H3／H1","時間尺度":"⚡ 短期（生效日 ~2026-07-31）","監測指標":"① MFN 定價協議簽署狀態 ② USTR/Commerce Annex III 名單與豁免細則 ③ 法說對關稅假設的量化","警戒閾值":"豁免未落實且關稅生效 → 連 2 季監測 IM COGS 上升／margin 壓縮即減碼考量"}},{"id":"R2","text":"MedTech 恢復失速＋分拆執行風險：Abiomed（Impella 2026 多起 FDA 召回／安全警示）、電生理 VARIPULSE（2026 初暫停約 5 週、PFA 份額落後 BSX Farapulse）拖累；DePuy Synthes 骨科分拆時程／對價不確定","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"① MedTech 分部 operational 成長 ② Cardiovascular 子分部成長 ③ 分拆進度公告","警戒閾值":"連 2 季 MedTech operational &lt; +3%（Q1/Q2 已 borderline）→ MedTech moat 重評，§9 sub-score 下調"}},{"id":"R3","text":"Talc 訴訟黑天鵝：第三次破產策略（Red River Talc）已被否，轉逐案訴訟；被迫 $35-50B 全球和解或連續 mega-verdict（如 2025-12 巴爾的摩 $1.5B 間皮瘤判決）大幅消耗 FCF","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"① 法院指定調解進展 ② 10-Q 法律準備金新增 ③ 重大個案判決趨勢","警戒閾值":"單一情境總額 ≥ $35B ＋ 準備金連 2 季新增 &gt; $3B"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","irr_base_pct":7.7,"ev5y_pct":33.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":3.9,"ev5y_pct":33.0,"irr_base_pct":7.7,"max_dd_pct":-38.0,"bull_5y_price":420.0,"bear_5y_price":210.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","price_at_dd":247.02,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"JNJ","date":"2026-10-18","schema":"v15.2","contract":"v19","company_name":"Johnson & Johnson"},"oneliner":"新藥接棒 Stelara 懸崖已有實證（Q3 創新藥營運成長 +7.9%），但醫材連續未達標，2027 年收購稀釋每股 1.36 美元可能還沒進共識；前瞻本益比約 23 倍、基準年化報酬約 6%，等價格回落或 12/8 的 2027 指引。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JNJ_20261018/scenario.json","answers":{"q1_business":{"verdict":"賺醫師處方與醫院採購的錢，獲利集中在腫瘤與免疫新藥。錢卡在兩個節點：美國支付端的定價協議，以及三大批發商通路。","reasoning":"Q3 2026 營收 253.99 億美元。創新藥 168 億美元，約占 66%，營運成長 +7.9%；醫材 86 億美元，約占 34%，營運成長 +2.5%（Q3 法說 Ryan Koors）。獲利集中在創新藥：調整後稅前利益率創新藥 35.4%（去年同期 44.3%，差距主因約 10 億美元 Firefly 收購研發費用），醫材 22.9%。全公司調整後稅前利益率 30.2%，自算 GAAP 營業利益率 23.0%；TTM 毛利率 67.9%、營業利益率 26.8%。第一個卡點是美國支付端：2026-01 以 MFN 定價換取藥品關稅豁免，利益率指引已含這份協議的成本。第二個卡點是通路：三大批發商約占總毛營收 48.4%（FY2025 10-K），最大一家由 20.5% 升至 21.8%，三家合計與前一年同為約 48.4%。單點依賴方面，前兩大合計 37.3%，未達 40%，且批發商只是配送方、不是最終需求方，所以列為集中度風險而非護城河證據。供需耐久度判為結構性持久，但價格端在放緩：IQVIA 預估全球藥品市場至 2030 年年增約 5–8%，美國淨價年增 4–7%，低於過去五年的 9.4%。產業態勢是雙向拉鋸：競爭端在惡化（電生理脈衝電場消融、Stelara 與 Simponi 生物相似藥），結構端在轉好（藥品關稅零稅率至 2029-01-20、美國本土 550 億美元投資計畫）。","fact_refs":["f_kpi0_gaap_reported_sales","f_kpi1_non_gaap_adjusted_income","f_kpi2_gaap_sm_a_r_d_ipr_d_othe","f_kpi4_2026_10","f_peer_jnj_gross_margin_pct","f_peer_jnj_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"以經常性處方藥與醫材耗材為主。Q3 美國成長 +9.1%、美國以外 +1.8%，成長高度集中在美國。","unit_econ_note":"創新藥每 1 美元營收的調整後稅前利益約是醫材的 1.5 倍（35.4% 對 22.9%），組合往創新藥移動會拉高利益率。但新品上市費用、Intra-Cellular 無形資產攤銷與收購研發費用，暫時把差距壓縮。","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"大藥廠加醫材，新藥接棒專利懸崖，股東回饋以股息為主"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：IQVIA 預估全球藥品市場至 2030 年年增約 5–8%；但美國淨價成長降到 4–7%，價格端放緩。","bargaining":{"up":"上游原料與合約製造的占比事實表未涵蓋，議價結構無法量化。","down":"三大批發商約占總毛營收 48.4%；美國政府透過 MFN 協議、TrumpRx 與 Medicaid 國際價格設定價格天花板。","geo":"2025 年關稅成本約 2 億美元，集中在醫材，中國關稅為最大部分；藥品 232 關稅零稅率至 2029-01-20。"},"profit_pool_dir":"利潤池往腫瘤與免疫新藥集中；醫材的國際外科、亞太電生理與 Abiomed 在流出。","tam_table":{"expanded":false,"reason":"成長由個別藥品的份額與適應症驅動，不是低滲透品類的擴張；可引的只有 IQVIA 全球藥品市場增速，分產品滲透率事實表未涵蓋。"}}}},"q2_moat":{"verdict":"護城河方向持平：創新藥份額在擴大，醫材份額在流失，兩者相抵。","reasoning":"機制是腫瘤與免疫的臨床證據加上商業化規模。多發性骨髓瘤約八成病患在療程中用到 JNJ 療法；Darzalex 各線份額增加 5 點，一線增加 10 點；Tremfya 在 UC 與克隆氏症份額各增加 4 點，美國 IL-23 新病人份額居首（Q3 法說）。醫材方向相反：電生理受脈衝電場消融競爭，亞太壓力加劇；Abiomed −1.5%，外科 −1%（中國量採、中東）。同業只有利潤率可比：JNJ TTM 營業利益率 26.8%，低於 ABBV 33.9% 與 LLY 49.7%，高於 BSX 21.0% 與 MRK 10.5%。同業 ROIC 差距事實表未涵蓋，因此綜合分不給到 8 以上。執行力給 8 分：全年指引連續上調，八個品牌雙位數成長。定價力給 7 分：美國以外 Darzalex 有價格逆風，MFN 協議生效，美國淨價成長放緩。報酬持續期方面，投入資本事實表未涵蓋，只能依高營業利益率與大量併購無形資產判為高利益率、低周轉；增量報酬算不出。","fact_refs":["f_peer_jnj_gross_margin_pct","f_peer_jnj_operating_margin_pct","f_peer_jnj_fcf_margin_pct","f_peer_mrk_operating_margin_pct","f_peer_lly_operating_margin_pct","f_peer_abbv_operating_margin_pct","f_peer_bsx_operating_margin_pct","f_peer_bsx_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"腫瘤與免疫的臨床證據規模與商業化網路（多發性骨髓瘤約八成病患使用 JNJ 療法）；醫材靠醫院關係與耗材綁定。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"創新藥份額擴大（Darzalex 增加 5 點、Tremfya 增加 4 點，Q3 法說），醫材的電生理與國際外科份額縮減，淨方向持平。","competitor_notes":[{"name":"MRK","strategy_note":"營業利益率 10.5%、研發密度 45.8%，顯示近期重押研發或收購費用，不是可比的利潤標竿。"},{"name":"LLY","strategy_note":"營業利益率 49.7%，靠單一大類高價新藥；JNJ 組合較分散，但定價力不在頂層。"},{"name":"ABBV","strategy_note":"營業利益率 33.9%，同樣走過生物相似藥懸崖，可對照 JNJ 接棒 Stelara 的速度。"},{"name":"BSX","strategy_note":"電生理脈衝電場消融的直接對手。營業利益率 21.0% 低於 JNJ，但在電生理份額上施壓。"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用營業利益率與毛利率對照。","threats":[{"level":"🟡","text":"Stelara 生物相似藥：Q3 −54%，拖累創新藥約 690bp；已進入第二年，殘值在遞減。","p":0.9,"evidence_refs":["competitive_share_entrants#1","substitute_technology#1","substitute_technology#2","end_markets#3"]},{"level":"🟡","text":"Simponi（歐洲生物相似藥已進入，美國可能在 2026 年稍後）與 Opsumit 學名藥。","p":0.8,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"電生理脈衝電場消融競爭，亞太壓力加劇；VARIPULSE Pro 在歐洲已回到雙位數成長，美國第四季才上市。","p":0.5,"evidence_refs":["competitive_share_entrants#2","end_markets#5"]},{"level":"🟡","text":"中國量採擴大，壓縮外科國際業務。","p":0.7,"evidence_refs":["end_markets#5"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"病患、醫師、保險三方都成立；腫瘤與免疫屬於需要而非想要。ICOTYDE 上市不到一年已取得全國商業保險覆蓋，約 60% 病患是首次使用全身性治療（Q3 法說）。"},{"item":"決策層級","level":"🟡","text":"替代發生在醫師處方層，新病人份額一季可移動 4–5 點：Tremfya、Darzalex 是正向例子，Stelara 被生物相似藥與新機轉取代是反向例子。電生理導管同樣在醫師端被換平台，轉換成本比一般印象低。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈中最難取代的是專利期內的分子本身，這部分 JNJ 握有。但三大批發商約占總毛營收 48.4%，美國支付端也透過 MFN 與 Medicaid 國際價格分走一部分利潤。"},{"item":"社會容忍度","level":"🟡","text":"價格上限已由政治決定：2026-01 以 MFN 定價換關稅豁免，零稅率至 2029-01-20。利益率指引已含協議成本、全年仍上調，顯示目前可吸收；2029 年到期後的條件未明，已列入反證紀錄。"}],"roiic":"事實表未涵蓋（投入資本與近三年併購對價未收錄）","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，再投資率＝（資本支出−折舊攤銷＋營運資金變動＋收購淨額）÷稅後營業利益；兩項輸入缺失，不推估。"}}}},"q3_growth":{"verdict":"五年後的跑道中等。有出處的第二條曲線存在，但放在 1,000 億美元營收的規模上，單一新品都不到一成，專利懸崖會反覆出現。","reasoning":"成長以量為主，來自新藥份額與新適應症；併購補位，包括 Firefly 收購與 Sail 合作，2026 年稀釋每股 0.64 美元、2027 年稀釋 1.36 美元；價格為負向（美國以外定價逆風、MFN）；回購幾乎沒有。共識三年 EPS：FY2025A 調整後約 10.79 美元（由 2026 指引中點 11.10 與成長 2.9% 回推），到 FY2028E 14.8 美元，年複合約 11.1%（Koyfin 快照，分析師家數事實表未涵蓋）。內生上界算不出，因為投入資本與併購對價事實表未涵蓋。缺口歸因：約 2 個百分點來自 2026 年一次性交易費用的基期效應，其餘依賴併購資產放量與管理層「本十年末雙位數成長」的承諾，無法用內生數字驗證，長期信心上限為中。第二條曲線有出處：ICOTYDE 上市以來 2 萬名病患、近 9,000 名處方醫師；INLEXZO 年初至今約 2 億美元，平台目標 50 億美元以上；OTTAVA 7 月取得 De Novo 授權。但 Simponi 與 Opsumit 的到期已開始，Stelara 式懸崖會再來，因此跑道判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi4_2026_10"],"verdict_values":{"growth":{"driver_mix":"量為主（新藥份額）、併購補位（Firefly、Sail），價格為負向，回購趨近於零。","runway_years":"事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC × 再投資率；投入資本與近三年併購對價事實表未涵蓋，上界無法計算，保守視為共識成長已超出內生上界。","segments":[{"item":"創新藥（Q3 2026）","value":"營收 168 億美元，營運成長 +7.9%（美國 +11.1%），調整後稅前利益率 35.4%（去年 44.3%，含約 10 億美元收購研發費用）"},{"item":"醫材（Q3 2026）","value":"營收 86 億美元，營運成長 +2.5%（美國 +4.8%、美國以外 +0.1%），調整後稅前利益率 22.9%（去年 21.0%，含關稅追回）"}],"decay_signals":["毛利率：Q3 銷貨成本率年增 150bp（產品組合與 Intra-Cellular 無形資產攤銷）；Q2 是否同向事實表未涵蓋，暫記一項","核心市占：電生理受脈衝電場消融競爭，亞太壓力加劇（Q3 法說）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等。自由現金流足以支付股息、和解與小型併購，但併購回報無法驗證，回購幾乎沒有。","reasoning":"自由現金流穩定：FY2022–25 介於 171–193 億美元，FCF 利潤率約 20–21%。淨利因訴訟與一次性項目波動大，FCF 除以淨利 FY2023 為 0.51、FY2024 為 1.28、FY2025 為 0.72，未出現連 2 年低於 0.75。2026 年前三季自由現金流約 151 億美元，全年指引約 210 億美元（Q3 法說 CFO）。淨負債約 283 億美元，S&P 維持 AAA。現金去向：股息為主（Q2 法說 CFO），卵巢 talc 和解 55 億美元，Firefly 收購約 10 億美元；四分比例事實表未涵蓋。計分逐項看：併購回報 Firefly 與 Sail 尚未產生營收，已實現回報算不出；回購不適用；稀釋方面，以年度淨利除以稀釋 EPS 推得 FY2024 與 FY2025 稀釋股數皆約 24.3 億股，近乎零淨稀釋，通過。股權報酬費用占營收比事實表未涵蓋。","fact_refs":["f_kpi3_fcf","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_jnj_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Firefly 收購約 10 億美元收購研發費用、Sail 合作；2027 年合計稀釋每股 1.36 美元，已實現增量報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"股東回饋以股息為主（Q2 法說 CFO），近年無實質回購"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"淨利÷稀釋 EPS 推得稀釋股數 FY2024 約 24.29 億、FY2025 約 24.30 億，年淨稀釋趨近於零"}]},"governance":{"capital_returns":{"expanded":false,"reason":"管理層明說本十年末雙位數成長不假設併購（Q3 法說 CFO 回答 Goldman 提問），成長主要靠內部新藥；近三年現金去向四分事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 2027–28 年 EPS 照共識走（年增約 11%），且倍數守在 21 倍以上。這只能信一半：2027 年被交易稀釋壓住，基準情境年化約 6%，不夠。","reasoning":"現價 255.56 美元，以 FY2026 共識 EPS 11.08 計，前瞻本益比約 23.1 倍；剔除 0.64 美元交易稀釋後的 11.74 計，約 21.8 倍。PEG 以共識三年年複合約 11.1% 計約 2.1，偏貴。trailing P/E 38.8 倍、P/S 6.2 倍、EV/S 6.5 倍，皆在近 4 個年度端點的最高位；這不是五年分位，GAAP 本益比也被 talc 計提壓低分母，只作方向參考。FY2027 共識 12.18 美元很可能沒有完整反映 1.36 美元稀釋：依 CFO 說法，剔除交易後 EPS 成長略快於營收（約 5.4%），以 11.74 × 約 1.06 − 1.36 推得約 11.1 美元。FY1 共識近 3 個月 −4.15%，是 7 月納入交易稀釋所致，不是基本面下修。二手聚合平均目標價 254 與 271 美元，與現價相當；全距事實表未涵蓋。短期上檔以 2027 基準 EPS 11.2 × 22 倍計約 −3.6%，中期以五年基準終值計約 +20%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_ev_s_fwd"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026 共識調整後 EPS）搭配 PEG","tier":"大型多元藥廠","peers":{"expanded":false,"reason":"同業前瞻本益比事實表未涵蓋，只有利潤率可對照，不跨口徑當錨。"},"fwd_pe":23.1,"peg":2.08,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 23.1 倍（剔除交易 21.8 倍）、PEG 約 2.1；P/E、P/S、EV/S 皆在近 4 個年度端點的最高位（非五年分位）；基準年化約 6%，低於 8%。判為偏貴。","upside_short_pct":-3.6,"upside_mid_pct":20.4,"denominator_disputed":false,"denominator_note":"FY2026 EPS 含 Firefly／Sail 一次性稀釋 0.64 美元，剔除後前瞻本益比約 21.8 倍；分母差距不改變偏貴結論。真正的分母爭點在 FY2027 共識是否已扣 1.36 美元，已放進情境路徑。"}}},"q6_how_wrong":{"verdict":"最可能看錯在醫材與 2027 指引：Q4 外科與 Abiomed 若真的回升、12/8 給出高於共識的 2027 指引，觀望會錯過；反方向的風險是 talc 和解失效與定價協議到期。","reasoning":"動能不過熱：RSI(14) 43.8，26 週報酬 +10.3%，不構成追價障礙，也不構成撿便宜訊號。看錯的方式有三種。第一，醫材的暫時性歸因如果成立（VARIPULSE Pro 歐洲已回到雙位數，美國第四季上市；Abiomed 美國端季內改善），2027 年醫材回到 4% 以上，H2 恢復。第二，12/8 若給出不含 1.36 美元稀釋疑慮的 2027 指引，共識不下修，基準路徑偏保守。第三，反方向風險：卵巢 talc 和解需 95% 參與率才生效（CFO 稱正趨向達標），證券集體訴訟已確立集體認證；Stelara 反壟斷案若被第四巡迴法院發回，屬於新的負債來源。歷史最大回撤與訴訟總金額事實表未涵蓋。","fact_refs":["f_rsi14","f_week26_return_pct","f_net_debt_m","f_kpi3_fcf"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩項衰退信號（毛利率、電生理份額），尚非價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":11.08,"pe":23.07,"basis":"FY2026 共識調整後 EPS（含 Firefly／Sail 稀釋 0.64 美元）；終端倍數同樣套在當年度調整後 EPS"},"eps":{"bull":[12.0,14.4,15.9,17.5,19.2],"base":[11.2,12.9,14.0,15.1,16.2],"bear":[10.7,11.0,11.3,11.6,11.8]},"pe":{"bull":22,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.07,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-40,"hi":-25,"basis":"Bear 終點約 −31%（EPS 11.8 × 15 倍）作為下緣參考；途中再疊加 2027 指引下修、talc 和解失效等事件造成的超跌，上緣 −25% 對應共識下修約 8% 加倍數壓縮至 19 倍。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"12/8 指引證實共識已扣交易稀釋，ICOTYDE、INLEXZO、Rybrevant 放量，醫材在 2027 年回到 4% 以上；2028 年起交易稀釋消退，EPS 年複合約 12%，倍數回到 22 倍。","base":"2027 年依 CFO 口徑約 11.2 美元（剔除交易後成長略快於營收，再扣 1.36 美元）；2028 年起稀釋部分消退，EPS 年複合約 8%；成熟藥廠倍數回落至 19 倍。","bear":"Simponi、Opsumit 與後續專利到期接連發生，醫材停在 2–3%，MFN 協議擴大讓利，talc 和解失效；EPS 五年停在 11–12 美元，倍數壓到 15 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Simponi 歐洲生物相似藥已進入，美國可能在 2026 年稍後；Opsumit 學名藥；Stelara 衰退快於公司原預期，且三星 Bioepis 第二個生物相似藥阻擋上訴敗訴；IQVIA 預估美國淨價年增 4–7%，低於過去五年的 9.4%。","assumption":"新品接棒的速度，能持續蓋過每一輪專利到期與淨價放緩。","consequence":"EPS 五年停在 11–12 美元、倍數壓到 15 倍，股價約 177 美元（−31%）；再疊加 talc 失控，才會到 −50%。","ruling":"部分採納。Q3 創新藥在 Stelara −54% 下仍成長 +7.9%，接棒已有實證，所以不升為主情境；Bear 機率維持 30%。","watch":"創新藥季營運成長是否連 2 季低於 +6%。","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#3"],"fact_refs":["f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"Q3 醫材營運 +2.5%，低於管理層預期；Abiomed −1.5%，外科 −1%；電生理亞太競爭加劇；中東成為新增逆風。Q2 法說曾說 Abiomed 會在未來數季逐步回到雙位數。","assumption":"醫材疲弱屬於暫時性，2027 年可回到 4% 以上。","consequence":"醫材若停在 2–3%，DePuy Synthes 分拆後的留存組合難以支撐倍數，H2 失效。","ruling":"不採信也不否定：標為未證、監測，以兩季期限檢驗。","watch":"Q4 2026 與 Q1 2027 醫材營運成長是否皆低於 +3%。","evidence_refs":["competitive_share_entrants#2","end_markets#1","end_markets#5"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"成長靠收購補位：Firefly 約 10 億美元收購研發費用，2027 年交易稀釋每股 1.36 美元；卵巢 talc 和解 55 億美元，滑石粉證券集體訴訟已確立集體認證；Biosense Webster 反壟斷判決 4.42 億美元、比利時品類管理罰款；美國價格天花板由 MFN、TrumpRx 與 Medicaid 國際價格決定；三大批發商約占總毛營收 48.4%。","assumption":"營收成長能轉成每股自由現金流成長。","consequence":"營收達到雙位數，但 EPS 被併購稀釋、訴訟支出與定價讓利吃掉，每股價值成長停在中個位數。","ruling":"採納。長期信心上限為中，進場價以 2027 年稀釋後 EPS 計算。","watch":"12/8 的 2027 指引與 2028 年交易稀釋是否收斂；批發商合計占比是否超過 50%；2029-01-20 關稅零稅率到期前的協議延續。","evidence_refs":["customer_concentration_credit#0","major_events#1","lawsuit_class_action#0","regulatory_antitrust#2","regulatory_antitrust#3"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"前瞻本益比約 23 倍；P/E、P/S、EV/S 皆在近 4 個年度端點的最高位；二手聚合平均目標價 254–271 美元，與現價 255.56 相當；FY2027 共識 12.18 美元可能未完整反映 1.36 美元稀釋。","assumption":"市場以共識 FY2028 的 14.8 美元定價。","consequence":"共識下修約 8% 時，倍數不變也有約 8% 下行；基準年化報酬約 6%，低於 8%。","ruling":"採納。不追，等價格回落或 2027 指引。","watch":"12/8 之後共識 FY2027 EPS 的修正幅度。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 247.02 → 本次 255.56（+3.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=247.02","side_b":"本次 price_at_dd=255.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 247.02 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 247.02 美元：Bull 價 420、Bear 價 210，五年期望值 +33.0%，基準年化 7.7%，不對稱比 3.9","side_b":"本次情境、股價仍用 247.02 美元：Bull 價 422.4、Bear 價 177，五年期望值 +20.3%，基準年化 4.5%，不對稱比 2.09","ruling":"先換情境、股價不動：五年期望值少 12.7 個百分點，基準年化少 3.2 個百分點。不對稱比由 3.9 變為 2.09。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 247.02 美元：五年期望值 +20.3%，基準年化 4.5%，不對稱比 2.09","side_b":"本次情境、股價 255.56 美元：五年期望值 +16.3%，基準年化 3.8%，不對稱比 1.77","ruling":"再換股價、情境不動：起點價上漲 3.5%，五年期望值少 4.0 個百分點，基準年化少 0.7 個百分點，不對稱比由 2.09 降到 1.77。合計五年期望值比前份少 16.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 EPS：共識與管理層口徑","cause":"新證據","prior_field":null,"side_a":"共識 FY2027 EPS 12.18 美元（Koyfin 10-08 快照，早於 Q3 法說）。","side_b":"Q3 法說 CFO：2027 年 Firefly／Sail 合計稀釋每股 1.36 美元，剔除後 EPS 成長略快於營收（約 5.4%）；以剔除交易的 2026 基礎 11.74 × 約 1.06 − 1.36，推得約 11.1 美元。","ruling":"採管理層口徑，基準路徑 2027 年取 11.2 美元。兩邊方向一致、幅度不同，屬可調和；但共識可能要下修約 8%，是短期價格風險。","evidence_level":"一手法說原話加共識快照","settle_metric":"12/8 企業業務回顧的 2027 調整後 EPS 指引中點","if_then":["若指引中點 ≥12.0 美元，基準路徑上修，進場價上調至約 230 美元並重跑判斷","若指引中點 <10.8 美元，觸發唯一致命點，進場價下調至 ≤200 美元，不建倉"],"evidence_refs":[]},{"axis":"全年 EPS 指引前後數字","cause":"新證據","prior_field":null,"side_a":"二手整理稱 7 月指引為調整後 EPS 11.60–11.75 美元。","side_b":"Q3 新聞稿指引中點 11.10 美元。","ruling":"可調和。Q2 法說 CFO 明說 7/15 指引不含 Firefly 等待完成的交易；扣 0.64 美元稀釋後中點約 11.04，Q3 再上調 0.06 至 11.10，前後一致。FY1 共識近 3 個月 −4.15% 同屬這筆稀釋，不是基本面下修。","evidence_level":"一手法說原話","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"醫材：暫時性歸因與連續未達標","cause":"新證據","prior_field":null,"side_a":"管理層說法：Abiomed 屬短期逆風、非結構性，2026-07-15 Tim Schmid 稱未來數季逐步回到雙位數；外科第四季整體回到成長；手術量環境穩定。","side_b":"Q3 醫材營運 +2.5%，低於管理層自己的預期；Abiomed −1.5%，外科 −1%，電生理亞太競爭加劇；Q2 承諾今年兩項機器人上市，Q3 只見 OTTAVA，泌尿系統未提。","ruling":"不採信也不否定，標為未證、監測。預先登記期限：Q4 2026 與 Q1 2027 醫材營運成長皆低於 +3%，即視為暫時性歸因證偽，H2 反轉。","evidence_level":"一手季報加法說","settle_metric":"醫材季營運成長、Abiomed 季成長","if_then":["若 Q4 2026 外科轉正且醫材 ≥+4%，H2 恢復，進場價不變","若連 2 季低於 +3%，H2 反轉，醫材不再給溢價，Bear 機率上調至 35%"],"evidence_refs":["end_markets#1","competitive_share_entrants#2","end_markets#5"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"Q3 調整後 EPS 2.59 美元優於共識 2.53；全年指引上調；AAA 評等；股息殖利率約 2.1%；新品曲線多條（ICOTYDE、INLEXZO、Rybrevant、OTTAVA）；管理層說 2027 年會更好；動能不過熱。","side_b":"好生意已經反映在價格上：前瞻本益比約 23 倍，基準年化約 6%，2027 年 EPS 還有共識下修風險。","ruling":"不採。等價格回到 215 美元，或等 2027 指引確認共識不需下修。","evidence_level":"一手季報加共識","settle_metric":"股價與 2027 指引","if_then":["若股價 ≤215 美元且醫材未證偽，建首批三分之一","若價格先漲而指引未到，不追"],"evidence_refs":[]},{"axis":"前份漂移：價格與估值相關欄","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct","cycle_position"],"side_a":"前份股價 247.02 美元，估值偏貴，訊號 B，觀望；機率 25／45／30，最大回撤 −38%，非循環股。","side_b":"現價 255.56 美元（+3.5%），前瞻本益比約 23 倍，估值仍偏貴，訊號 B，觀望；機率維持 25／45／30，最大回撤改為 −25% 至 −40% 的範圍，仍非循環股。","ruling":"股價小漲 3.5% 未改變估值結論；回撤由單點改為範圍是表達方式的調整，下緣由 Bear 終點 −31% 推出。","evidence_level":"收盤價","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：護城河、跑道、類型與陷阱","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","trap"],"side_a":"前份：護城河持平、五年後跑道中等、品質複利成長、價值陷阱風險低。","side_b":"本次：護城河持平、跑道中等、類型不變；價值陷阱風險由低升為中，因為出現兩項衰退信號——Q3 銷貨成本率年增 150bp，電生理份額受脈衝電場消融競爭。","ruling":"Q3 新證據兩面都有：創新藥份額擴大、醫材份額流失，方向相抵，所以護城河與跑道不變；陷阱風險依兩項信號上調一級。","evidence_level":"一手季報加法說","settle_metric":"季毛利率年變化、電生理成長率","if_then":["若 Q4 毛利率年減幅收斂至 50bp 內且電生理恢復雙位數，陷阱風險回降"],"evidence_refs":["competitive_share_entrants#2","end_markets#5"]},{"axis":"進場條件改變（加碼與首批建倉門檻）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE 回落 ≤18x（約 $210-220）或 PEG ≤2；或 talc 全球和解定案 ≤$30B；或 Section 232 藥品關稅豁免正式確認","side_b":"股價≤$215（2027基準EPS的19倍）或12/8給出2027調整後EPS指引中點≥$12.0","ruling":"舊條件中的關稅豁免已在 2026-01-08 協議落定（零稅率至 2029-01-20），卵巢 talc 已以 55 億美元和解並計提，兩項事件條件失效。價格門檻改以 2027 稀釋後 EPS 為分母，金額與前份相近；新增指引條件，因為 2027 共識是本次的主要約束。","evidence_level":"一手新聞稿加法說","settle_metric":"股價、2027 指引","if_then":["若股價 ≤215 美元，建首批三分之一，Q4 醫材 ≥+3% 再加碼","若指引中點 ≥12.0 美元，重跑判斷後再決定是否進場"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":null,"side_a":"前份未設定唯一致命點。","side_b":"Single Thing：12/8 給出的 2027 調整後 EPS 指引中點低於 10.8 美元，代表剔除交易後的基礎 EPS 成長低於 4%。","ruling":"本次 EPS 路徑是估值最大的單一敏感項，而 2027 指引是第一個能一次定案的離散事件，因此設為唯一致命點；觸發即不建倉。","evidence_level":"一手法說原話","settle_metric":"2027 調整後 EPS 指引中點","if_then":["若觸發，不建倉，進場價下調至 ≤200 美元"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"新證據","prior_field":null,"side_a":"前份未設指標門檻。","side_b":"本次設四條：醫材季營運成長連 2 季低於 +3%；創新藥季營運成長連 2 季低於 +6%；2027 指引中點低於 10.8 美元；卵巢 talc 和解參與率低於 95% 或單季新增準備金超過 30 億美元。觸發時的動作為減碼或不建倉。","ruling":"前份只有文字警戒閾值，本次改為可逐季核對的數字，便於減碼與清倉判斷。","evidence_level":"一手季報","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份風險門檻的處置","cause":"新證據","prior_field":null,"side_a":"前份 R1：Section 232 豁免未於生效日前定案，即作減碼考量。前份 R3：準備金連 2 季新增超過 30 億美元。","side_b":"本次：232 風險降為 2029-01-20 到期風險，併入新 R4，門檻為毛利率年減超過 200bp 且公司歸因於關稅或定價協議時減碼。R3 改看卵巢和解參與率 ≥95%；Q3 單季計提 55 億美元屬和解定額，只有一季，不構成失控訊號。","ruling":"保留指標、門檻與資料來源，不安靜刪除。仍有一處未釐清：顧問報告稱截至 2026 年 6 月 JNJ 未確認商務部在地製造協議，與 1 月協議的關係不明，列入 R4 監測。","evidence_level":"一手新聞稿加二手顧問報告","settle_metric":"10-Q 法律附註、季毛利率","if_then":["若 2029-01-20 前未取得延續條件，R4 提前為中期風險"],"evidence_refs":["reg_tariff_export#2"]}],"triggers":[{"n":1,"text":"創新藥營運成長是否守住 6%","type":"假設驗證","maps_to":"H1","metric":"創新藥季營運成長","threshold":"連 2 季 <+6%","action":"延後進場；若已持有，減碼三分之一","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["end_markets#3"]},{"n":2,"text":"醫材是否回升","type":"假設驗證","maps_to":"H2","metric":"醫材季營運成長","threshold":"Q4 2026 與 Q1 2027 皆 <+3%","action":"H2 反轉，Bear 機率上調至 35%，不建倉","source_freq":"季報新聞稿／每季","date":"2027-04","evidence_refs":["end_markets#1","competitive_share_entrants#2"]},{"n":3,"text":"2027 指引是否跌破剔除交易後的成長下限","type":"Single Thing","maps_to":"H1","metric":"2027 調整後 EPS 指引中點","threshold":"<10.8 美元","action":"不建倉，進場價下調至 ≤200 美元","source_freq":"企業業務回顧／一次性","date":"2026-12-08","evidence_refs":[]},{"n":4,"text":"卵巢 talc 和解是否生效、有無新增準備金","type":"風險","maps_to":"R3","metric":"和解參與率；10-Q 新增法律準備金","threshold":"參與率 <95% 致和解失效，或單季新增準備金 >30 億美元（不含已計提的 55 億）","action":"已持有則減碼至半倉；未持有則進場價下調 10%","source_freq":"10-Q／每季","date":"2027-01","evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":5,"text":"反壟斷案是否復活","type":"風險","maps_to":"R3","metric":"第四巡迴法院 CareFirst 上訴裁定；Biosense Webster 4.42 億美元判決後續","threshold":"上訴法院發回重審 Stelara 壟斷案","action":"停止加碼，直到案情金額可量化","source_freq":"法院裁定／不定期","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3"]},{"n":6,"text":"定價協議與關稅是否吸收失敗","type":"風險","maps_to":"R4","metric":"季毛利率年變化","threshold":"年減 >200bp，且公司歸因於關稅或定價協議","action":"減碼三分之一","source_freq":"季報／每季","date":null,"evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1"]},{"n":7,"text":"價格回到合理區","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤215 美元","action":"建首批三分之一","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":8,"text":"通路集中度","type":"風險","maps_to":"R4","metric":"三大批發商占總毛營收","threshold":">50%","action":"定價力子分下調一分","source_freq":"10-K／每年","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"Q4 季報後複審","type":"複審日期","maps_to":"H2","metric":"醫材與創新藥營運成長、2027 指引","threshold":"季報公布","action":"重跑判斷","source_freq":"季報","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"醫材季營運成長","bear_threshold":"連 2 季 <+3%","window":"2026Q4–2027Q1","source":"公司季報新聞稿","last_status":"warning"},{"metric":"創新藥季營運成長（含 Stelara 拖累）","bear_threshold":"連 2 季 <+6%","window":"未來 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"2027 調整後 EPS 指引中點","bear_threshold":"<10.8 美元","window":"2026-12-08","source":"企業業務回顧","last_status":"unknown"},{"metric":"卵巢 talc 和解參與率與新增法律準備金","bear_threshold":"參與率 <95%，或單季新增 >30 億美元","window":"未來 6 季","source":"10-Q 法律附註與法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"證據本身標明是 2010 年工廠停工與 2021 年合約廠疫苗報廢兩件舊事件，並自註「非現況集中度證據」；沒有提供現行製造據點或單一廠營收占比，無法形成可監測的門檻。"}],"action_conditions":{"rearm_trigger":"股價≤$215（2027基準EPS的19倍）或12/8給出2027調整後EPS指引中點≥$12.0","exec_line":"現價不建倉。觸及 215 美元先建三分之一；Q4 2026 季報醫材營運成長 ≥+3% 再加碼第二批；唯一致命點觸發則取消。","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤215 美元（約 2027 基準 EPS 11.2 的 19 倍），或 12/8 給出 2027 調整後 EPS 指引中點 ≥12.0 美元","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=10.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"創新藥新品淨接棒：Darzalex、Tremfya、Carvykti、Rybrevant、Caplyta，加上新上市的 ICOTYDE 與 INLEXZO，吸收 Stelara、Simponi、Opsumit 的下滑後，創新藥營運成長維持 +6% 以上。","2y":"FY2026–27 創新藥營運成長 ≥+6%（Q3 2026 為 +7.9%，已含 Stelara −54%）","5y":"2030 年腫瘤銷售超過 500 億美元（管理層目標），創新藥 2026–30 年複合成長 ≥6%","10y":null,"threshold":"創新藥季營運成長 ≥+6%；Tremfya 季成長 ≥+30%（Q3 為 +68.2%）","source":"公司季報新聞稿與法說分品牌成長率（2026-10-13 Ryan Koors）","drift_rule":"季營運成長連 2 季 <+6% 削弱；連 3 季 <+5% 反轉"},{"id":"H2","text":"醫材的國際業務與 Abiomed 在 2027 年回升，醫材營運成長回到 +4% 以上；DePuy Synthes 在 2027 年中前完成分拆（目前傾向分拆上市）。","2y":"Q4 2026 外科轉正；FY2027 醫材營運成長 ≥+4%","5y":"OTTAVA 在 2030 年前成為外科成長支柱；分拆後留存醫材的調整後稅前利益率不低於 22.9%","10y":null,"threshold":"醫材季營運成長 ≥+3%（Q3 2026 為 +2.5%，Q2 為 +3.6%）","source":"公司季報新聞稿；2026-10-13 法說 Tim Schmid 與 Joe Wolk","drift_rule":"連 2 季 <+3% 削弱；連 3 季 <+3% 反轉（Q3 已有一季低於門檻）"},{"id":"H3","text":"法律與定價負債有上限：卵巢 talc 以 55 億美元和解生效（參與率 ≥95%）；證券集體訴訟與反壟斷案不吃掉超過一年自由現金流；MFN 協議成本在利益率指引內吸收。","2y":"卵巢和解生效；2026 年自由現金流約 210 億美元達標，2027 年 ≥200 億美元","5y":"55 億美元以外的 talc 累計新增準備金 ≤100 億美元；2029-01-20 後藥品關稅條件延續","10y":null,"threshold":"單季新增法律準備金 ≤30 億美元（已知和解除外）；全年自由現金流 ≥200 億美元","source":"10-Q 法律附註；2026-10-13 法說 Joe Wolk（和解金額、95% 參與條件、全年自由現金流指引）","drift_rule":"單季新增準備金超過 30 億美元且不是已知和解，連 2 季即削弱；和解失效即反轉"}],"R":[{"id":"R1","text":"醫材持續失速：電生理被脈衝電場消融平台搶份額，Abiomed 回不到成長，國際外科受中國量採與中東拖累。","h_ref":"H2","clock":"⚡","threshold":"Q4 2026 醫材營運成長 <+3%（連同 Q3 即連 2 季）","evidence_refs":["competitive_share_entrants#2","end_markets#1","end_markets#5"]},{"id":"R2","text":"2027 年 EPS 重設：1.36 美元交易稀釋、匯率轉為逆風，加上 Simponi 與 Opsumit 學名藥接續 Stelara 的衰退。","h_ref":"H1","clock":"🔥","threshold":"2027 指引中點 <11.2 美元，或創新藥季營運成長 <+6%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#3"]},{"id":"R3","text":"法律負債擴大：卵巢 talc 和解失效、滑石粉證券集體訴訟走向審判或和解、Stelara 反壟斷案經 FTC 表態後可能復活、Biosense Webster 4.42 億美元判決、比利時品類管理罰款。","h_ref":"H3","clock":"🐢","threshold":"和解參與率 <95%，或單季新增準備金 >30 億美元","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#2","regulatory_antitrust#3"]},{"id":"R4","text":"定價與關稅：MFN 協議擴大讓利；2029-01-20 零稅率到期；醫材的中國關稅；商務部在地製造協議是否已確認，目前證據不一致。","h_ref":"H3","clock":"🐢","threshold":"季毛利率年減 >200bp，且公司歸因於關稅或定價協議","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1"]}],"single_thing":{"description":"12/8 企業業務回顧給出的 2027 調整後 EPS 指引中點低於 10.8 美元，即剔除 1.36 美元交易稀釋後，基礎 EPS 成長低於 4%。","why_fatal":"這代表管理層說的「EPS 成長快於營收」不成立，營運槓桿消失；2028–31 年基準路徑整條下移，倍數從 23 倍壓向 17–19 倍，基準年化報酬掉到 3% 以下。","if_happens":"基準情境改用偏 Bear 的路徑，進場價下調至 ≤200 美元，不建倉。","how_monitor":"12/8 企業業務回顧，以及 2027 年 1 月 Q4 季報的指引表。","probability":"約 20%：依 CFO 口徑推算，2027 年約 11.1 美元，落在門檻之上；但匯率逆風與 Simponi 學名藥可能把數字壓到門檻附近。"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.0,"peg_fy2":1.89,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":10.79,"FY2026E":11.08,"FY2027E":12.18,"FY2028E":14.8},"fy_end_month":12,"eps_basis":"調整後 EPS（Non-GAAP，含收購研發費用）。FY2025A 由 2026 指引中點 11.10 與成長 2.9% 回推（Q3 法說 CFO），事實表沒有直接值；共識為 Koyfin 2026-10-08 快照；財年止於 12 月。"},"catalysts":[{"date":"2026-12-08","date_precision":null,"type":"guidance","event":"企業業務回顧：2027 展望、DePuy Synthes 分拆的模擬財務、早期管線","impact":"高","watch":"2027 調整後 EPS 指引中點與 1.36 美元稀釋的處理方式"},{"date":"2026-12-31","date_precision":"quarter","type":"regulatory","event":"VARIPULSE Pro 美國核准與上市；RYBREVANT FASPRO 頭頸癌美國核准","impact":"中","watch":"電生理份額能否止跌"},{"date":"2026-12-31","date_precision":"quarter","type":"product","event":"milvexian 次發性中風試驗讀數（事件驅動，可能落在今年）；ICOTYDE 乾癬性關節炎資料與對 Stelara 頭對頭資料","impact":"中","watch":"Factor XI 第二條曲線是否成立"},{"date":"2027-01-31","date_precision":"month","type":"guidance","event":"Q4 2026 季報","impact":"高","watch":"醫材營運成長是否 ≥+3%、外科是否轉正"},{"date":"2027-06-30","date_precision":"quarter","type":"other","event":"DePuy Synthes 分拆完成（目標 2027 年中）","impact":"中","watch":"分拆方式與留存醫材利益率"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
