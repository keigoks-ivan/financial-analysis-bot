你是 DD 管線 v20 的判斷層閘（gate），標的 GM（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_total_net_sales_and_reve`（q1_business）｜Total net sales and revenue (GAAP)＝50015 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_kpi1_ebit_adjusted_non_gaap_o`（q1_business）｜EBIT-adjusted (non-GAAP operating profit proxy)＝4106 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_kpi2_ebit_adjusted_margin`（q1_business）｜EBIT-adjusted margin＝8.2 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_kpi6_gmna_ebit_adjusted_margi`（q1_business）｜GMNA EBIT-adjusted margin＝8.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_kpi7_wholesale_volume_total`（q1_business）｜Wholesale volume (total)＝1028 thousand vehicles｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_kpi8_fy2026_guidance`（q1_business）｜FY2026 guidance（更新後）＝EBIT-adj $14.5–15.5B；adj. auto FCF $11.5–12.5B；EPS-diluted-adj $12.75–13.75 range｜期間與口徑：Q3 2026（公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（公告於 2026-10-20））
  - 註記：共識 FY1 EPS 13.37（財報後 10-21 快照，見 consensus_revision）
- `f_peer_gm_gross_margin_pct`（q2_moat）｜GM 毛利率＝5.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gm_operating_margin_pct`（q2_moat）｜GM 營業利益率＝0.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tsla_operating_margin_pct`（q2_moat）｜TSLA 營業利益率＝4.61 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSLA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsla_gross_margin_pct`（q2_moat）｜TSLA 毛利率＝18.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSLA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝186269.54 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝189497.13 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.37 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝15.14 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝16.82 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝877.45 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_adjusted_automotive_free`（q1_business）｜Adjusted automotive free cash flow＝5882 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：GM Q3 2026 press release (SEC 8-K Ex.99)（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查得
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.907 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝5.69 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 13.37，分子＝快照價 76.11｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝104053.0 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 128772.0、現金 24719.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝76.11 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝16.65 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝59.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝59.9 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.92 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝29.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝29.1 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.53 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 12.79 → 13.37（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝170835.83 USD m｜期間與口徑：2026-10-22／市值 66782.83 ＋ 淨負債 104053.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-3.25 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.5｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝79.18 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w104`（q5_valuation）｜104 週均線＝65.36 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：中國、印度等低成本製造商已在新興市場成為競爭者並進入成熟市場，對 GM 定價、份額造成並預期持續造成顯著負面影響；另有科技公司支持的新創與非傳統競爭者進入
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-27）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：GM 2025 全球批發量 3,799 千輛，較 2024 的 4,010 千輛減少；GMI 由 547 降至 503 千輛
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-01-27）｜affects：moat_trend
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：GM 2026 Q3 美國銷量 670,974 輛，年減 5.5%；Cox 預估 GM 年初至今份額 16.7%，去年 17.4%；底特律三強 Q3 份額創紀錄低點
  - 來源：DBusiness／GM Authority 2026 Q3 銷量報導（as_of 2026-10-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：CPCA：2026 H1 三家中國車廠進入全球前十，BYD 全球份額 4.8%
  - 來源：CarNewsChina 2026-08-05（as_of 2026-08-05）｜affects：moat_trend
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：GM 2026 Q3 美國交車約 670,974 輛，年減約 5.5%（前年同期 710,347）；GM 歸因於 EV 市場縮小與停產車款，並稱最大量車款需求仍穩。
  - 來源：General Motors Q3 2026 Earnings Preview (INDmoney)（as_of 2026-10-15）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：GM 10-K（FY2025）Item 3 揭露：與 Ultium Cells 合資廠有關的 TSCA 進口違規已於 2023-11 與 EPA 以同意協議和解，截至 2025-12-31 GM 已累計估計 $18.2 million 民事罰款，EPA 發出 TSCA 5(e) 命令前罰款將持續增加，由 GM 與 Ultium Cells LLC 連帶負責。
  - 來源：SEC EDGAR｜GM 10-K FY2025 Item 3. Legal Proceedings（as_of 2026-01-27）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：GM 2025 年關稅對 EBIT-adjusted 衝擊 31 億美元；公司預估 2026 年衝擊 30–40 億美元。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-01-27）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：關稅可能超出公司現有估計，減緩措施（調整美國生產計畫、減少或暫停部分進口）短期內無法完全抵銷；USMCA 檢討與部分關稅法律挑戰待決。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明電動車電池原料加工與萃取集中於中國，可能受進出口限制或關稅影響；中美貿易緊張亦是中國業務風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-01-27）｜affects：moat_trend、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：GM 2026 Q1 10-Q 新增中東衝突風險因子（涉及伊朗及鄰國），列出供應鏈與物流中斷、制裁限制交易、原料與能源成本上升等潛在影響。
  - 來源：GM Form 10-Q for quarter ended 2026-03-31 (SEC)（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：GM 2026 年關稅毛成本預估約 30–40 億美元；2025 年透過定價、產線調整與降本抵銷逾 40%。
  - 來源：Nasdaq/Zacks: Will Tariffs Remain a Major Headwind for General Motors in 2026?（as_of 2026-01-01）｜affects：valuation、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Cox Automotive 預測 GM 2026 年迄今美國市佔 16.7%（去年同期 17.4%），銷量約降 6%；Detroit 三大 Q3 市佔約 36% 創新低，亞系品牌過半，主因油電混合需求。
  - 來源：GM Authority: GM 2026 calendar year sales expected to drop by 6 percent（as_of 2026-09-25）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：GM 10-K 風險因子：產業正經歷重大變動，除傳統對手外，另須因應新創與大型科技公司支持的軟體、叫車服務等非傳統競爭者，這些新進者以新技術、產品、直銷通路、交通方式與車輛所有權模式衝擊產業舊商業模式。
  - 來源：SEC EDGAR GM 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：AlixPartners 全球汽車展望：中國車廠在智慧連網車的優勢來自速度、成本競爭力與組織敏捷度，並預期從軟體定義車走向 AI 定義車
  - 來源：AlixPartners 23rd Annual Global Automotive Outlook (China)（as_of 2026-01-15）｜affects：moat_trend、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露多起集體訴訟仍在進行：Duramax 柴油排放集體訴訟（第六巡迴法院 2025-06 部分維持／部分撤銷並發回）及 8 速變速箱集體訴訟（2025-06 第六巡迴法院撤銷 26 個州子集團認證並發回）；公司無法估計可能損失。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 Note 16（as_of 2026-01-27）｜affects：decision_inputs.bear、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-01-08 8-K：因消費者稅務優惠終止與排放法規放寬，北美 EV 需求 2025 年放緩；GM 主動縮減 EV 產能，Orion 廠轉產內燃機大型 SUV／皮卡，並把 Ultium Cells Lansing 廠權益賣給 LG Energy Solution。
  - 來源：SEC EDGAR 8-K Item 8.01 (2026-01-08)（as_of 2026-01-08）｜affects：thesis.R、valuation
- `major_events#2`（major_events｜方向 -｜狀態 ok）：NHTSA 於 2026-08 對約 997,743 輛 GM 皮卡與 SUV（2021–2026 年式、L87 6.2L V8）展開工程分析，評估 2025 年召回修復是否有效。
  - 來源：ARY News／Reuters 轉載：US opens probe into 1 million GM pickups, SUVs（as_of 2026-08-21）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 載明 8 速變速箱集體訴訟於 2025-06 被第六巡迴法院撤銷 26 個州子集團認證並發回。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 Note 16（as_of 2026-01-27）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA 2026-08 對約 997,743 輛 L87 6.2L V8 車款展開調查，評估2025年召回修復成效。
  - 來源：ARY News／Reuters 轉載（as_of 2026-08-21）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":167.2,"bear_5y_price":54.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":38.7,"ev5y_pct":34.6,"irr_base_pct":6.8,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.37,"pe":5.69,"basis":"FY2026E 共識調整後稀釋 EPS（10-21 快照），終端倍數同為調整後當年盈餘口徑"},"eps":{"bull":[15.5,17.6,19.3,20.8,22.3],"base":[14.6,16.0,15.6,16.6,17.6],"bear":[12.8,9.5,8.2,9.6,10.8]},"pe":{"bull":7.5,"base":6.0,"bear":5.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.907,"net_buyback":9.4},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GM_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：CFO 上調全年 EBIT adjusted 指引至 $14–16B（前 $13.5–15.5B）（原話："We now expect EBIT adjusted of $14 billion to $16 billion"）
- 2026-07-21｜CFO｜guidance：全年 EPS diluted adjusted 指引上調至 $12–14（原話："EPS diluted adjusted of $12 to $14, up from $11.50 to $13.50"）
- 2026-07-21｜CFO｜guidance：全年 adjusted automotive FCF 指引上調至 $9.5–11.5B（原話："free cash flow of $9.5 billion to $11.5 billion, up from $9"）
- 2026-07-21｜CFO｜guidance：指引前提：中東不明顯升級、大宗商品與通膨壓力不顯著增加（原話："assumes no material escalation in the Middle East and no"）
- 2026-07-21｜CFO｜guidance：北美全年定價預期約 +0.5%，位於先前指引高端（原話："year North America pricing to be up around 0.5%, which is at"）
- 2026-07-21｜CFO｜guidance：下半年定價效益較小，因為對上年度 2026 車型年漲價（原話："The pricing benefit is expected to be smaller in the second"）
- 2026-07-21｜CFO｜guidance：EV 虧損全年改善 $1–1.5B 維持不變（原話："We continue to expect losses to improve by $1 billion to"）
- 2026-07-21｜CFO｜guidance：保固全年改善上調為 $1–1.5B（前為 $1B）（原話："Warranty is tracking to a $1 billion to $1.5 billion"）
- 2026-07-21｜CFO｜guidance：排放法規節省全年 $500–750M 維持（原話："full year benefit of $500 million to $750 million, primarily"）
- 2026-07-21｜CFO｜guidance：全年毛關稅成本 $2.5–3.5B 維持（原話："We continue to expect gross tariff costs of $2.5 billion to"）
- 2026-07-21｜CFO｜guidance：大宗商品／物流／DRAM 逆風全年 $1.5–2B 維持（原話："DRAM costs to be a headwind of $1.5 billion to $2 billion"）
- 2026-07-21｜CFO｜guidance：今年投入 $1–1.5B 於回美國生產、供應鏈與軟體（原話："we're also investing approximately $1 billion to $1.5"）
- 2026-07-21｜CFO｜guidance：Q4 預期較季節性模式偏弱（新卡車投產、回美國成本）（原話："we expect the fourth quarter to be somewhat weaker than"）
- 2026-07-21｜CFO｜guidance：Q4 新卡車造成約 35,000 輛年減量逆風（原話："anticipated year-over-year volume headwind of approximately"）
- 2026-07-21｜CFO｜guidance：管理層對 2027 的初步看法：營收、利潤率、EBIT、FCF 皆可成長（原話："based on what we know today, we believe we can grow revenue"）
- 2026-07-21｜CFO｜margin：北美 Q2 EBIT 利潤率回到 8–10% 目標區間（原話："solidly back within our 8% to 10% margin target"）
- 2026-07-21｜CFO｜margin：新卡車變動利潤與定價的效益預期落在 2027 年後而非今年（原話："potentially more of a '27 and beyond tailwind than anything"）
- 2026-07-21｜CFO｜margin：回美國生產成本 2027 年相抵，整體大致平衡（原話："it's a little bit balanced into 2027"）
- 2026-07-21｜CFO｜margin：大宗商品：不預期下半年價格低於上半年（原話："I don't think we are projecting lower commodity prices for"）
- 2026-07-21｜CFO｜margin：保固被描述為多年期順風（原話："we think that this is part of the multiyear"）
- 2026-07-21｜CFO｜margin：OnStar 軟體營收遞延收入 $6.3B，年增近 50%（原話："Subscriber growth drove deferred revenue to $6.3 billion, up"）
- 2026-07-21｜CFO｜margin：2027 年已實現數位營收預計雙位數成長（原話："existing deferred and subscriber growth is expected to drive"）
- 2026-07-21｜CFO｜margin：車隊銷售成長未稀釋利潤（原話："Importantly, the growth in fleet comes without diluting"）
- 2026-07-21｜CFO｜margin：車隊定位轉變：不再是過剩產能出口（原話："fleet historically, I think, was an outlet for excess"）
- 2026-07-21｜CEO｜commitment：承諾持續擴張利潤率（原話："all of this supports our commitment to ongoing margin"）
- 2026-07-21｜CFO｜commitment：EV 重整現金費用大致完成，但保留補提空間（原話："While circumstances may change in the future and we may have"）
- 2026-07-21｜CFO｜commitment：預計持續穩定回購，剩餘授權 $3.5B（原話："We have $3.5 billion remaining under our current repurchase"）
- 2026-07-21｜CEO｜commitment：預計 2028 推出 eyes-off 系統，進度無變化（原話："the program overall is on track"）
- 2026-07-21｜CEO｜commitment：預計 2027–28 於電池研發中心建置經驗證的鈉離子電芯（原話："we believe that we'll be building production validated cells"）
- 2026-07-21｜CFO｜capital_allocation：Q2 公開市場買回 $2B（原話："In the second quarter, we made $2 billion in"）
- 2026-07-21｜CFO｜capital_allocation：對 EV 工廠資本投入持保守，拒絕多十億美元投資（原話："we turned down opportunities to put billions of dollars of"）
- 2026-07-21｜CEO｜customer：北美全尺寸皮卡市佔逾 42%（原話："our share of the U.S. full-size pickup market stands at more"）
- 2026-07-21｜CFO｜customer：整體市佔年減約 60 bps，管理層歸因於停產車型等三因素（原話："share was down by about 60 basis points versus the first"）
- 2026-07-21｜CEO｜customer：CEO 稱負擔能力疑慮尚未轉為對大型車需求的影響（原話："that's been predicted for several months now, and it's just"）
- 2026-07-21｜CEO｜product：新一代 Silverado／Sierra 輕型皮卡 12 月進展示間（原話："will further separate us from key competitors when they"）
- 2026-07-21｜CEO｜product：2027 因 Super Cruise 策略估計增加 160,000 套（原話："We're estimating 160,000 incremental Super Cruise units from"）
- 2026-07-21｜CFO｜product：Super Cruise 附加率約 30–40%（原話："we're seeing really encouraging attachment rates in the 30%"）
- 2026-07-21｜CEO｜product：新卡車量的真正成長在 2027 年底至 2028（原話："The real volume opportunity comes in the very late '27 or"）
- 2026-07-21｜CEO｜product：GM Defense 2026 營收預計近 $700M（原話："GM Defense expects 2026 revenue to grow to almost $700"）
- 2026-07-21｜CEO｜product：GM Defense 預期營收 CAGR 逾 30%（原話："We are expecting a top-line revenue CAGR for GM Defense of"）
- 2026-07-21｜CEO｜product：美國陸軍 ISV 採購可能超過 10,000 輛（待撥款）（原話："plans to procure more than 10,000 if the appropriation is"）
- 2026-07-21｜CEO｜product：GM Insurance 從 3 州擴至 21 州（原話："scaled from 3 states in early 2024 to 21 states today"）
- 2026-07-21｜CEO｜competition：CEO 形容中國智駕定價競爭不可持續（原話："there's intense pricing competition that, frankly, is"）
- 2026-07-21｜CFO｜risk：DRAM 供應：與 Micron 擴大合作（原話："On DRAM, specifically, our expanded collaboration with"）

### 問答異常語氣（迴避／改口／保留）
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Spak：Super Cruise 普及後是否調整價格結構（前期成本／月費）｜答法：未給具體答覆，稱「沒有具體要宣布的」，改談成長機會與附加率
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Rosner：2027 是否有逆風（大宗商品、DRAM）可一併說明｜答法：稱尚未量化，只說會有通膨壓力，轉回講多年期順風
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Narayan：現有回美國生產是否足以符合 50% 美國含量提案｜答法：未直接回答是否足夠，改談供應鏈韌性與美墨加談判
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Delaney：Micron 記憶體協議對 2027 成本能見度的影響｜答法：未揭露定價，只談關係與技術路線圖
- GM_Q2_2026_Earnings_Call_20260721.md｜問：Levy：定價、保固、批發、商品皆較佳但指引上調幅度偏小，抵銷項目為何｜答法：未列出具體抵銷項，強調不預期商品價格下降並「謹慎」

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 5 | 3 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 4 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Capital allocation 持續主動（buyback + 分紅 + 紀律）","columns":{"2Y":"2026-27 EBIT $13-15B/yr + $6B buyback 完成","5Y":"累計回購 ≥ 50% shares outstanding","10Y":"EPS CAGR 包含 buyback +7-10%/yr","具體門檻":"buyback / 分紅每季 announcement","來源":"Q1 26 法說會 + Feb 2026 board approval"}},{"id":"H2","text":"EV 段虧損穩定漸縮 / 不再 impairment","columns":{"2Y":"FY26-27 EV 段虧損","5Y":"EV 段損平 2028","10Y":"EV 占比 30%+ 且 margin 平","具體門檻":"季度 EV 段 EBIT、Equinox EV 銷量","來源":"Q1 26 已 $1.1B 額外調整，需觀察是否最後一輪"}},{"id":"H3","text":"OEM 估值 mean revert（mid-cycle PE 8x+）","columns":{"2Y":"Fwd PE 7x+ → 股價 +12%","5Y":"同業中位 8x+ 確認","10Y":"—","具體門檻":"同業中位 Fwd PE","來源":"StockAnalysis / Macrotrends 5Y 歷史"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"✅","trap":"🟡","moat_trend":"穩定","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":78.79,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GM","date":"2026-10-22","schema":"v15.0","contract":"v19","company_name":"General Motors"},"oneliner":"全尺寸皮卡與大額回購撐住每股盈餘，但美國份額流失、2027 年約 20 億美元原料逆風與循環後段，讓 5.7 倍前瞻本益比不算錯價；等 2027 年 1 月指引確認成本吸收再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GM_20261022/scenario.json","answers":{"q1_business":{"verdict":"賺北美燃油大車的錢：利潤卡在全尺寸皮卡與 SUV 的定價和混合比，國際與 EV 不賺錢","reasoning":"Q3 營收 500.2 億美元、EBIT 調整後 41.1 億美元（利潤率 8.2%）。北美營收約 414 億美元，EBIT 調整後約 36 億美元，利潤率 8.7%，約占全公司 EBIT 的 88%。國際（不含中國權益）損益兩平，中國權益收入 3,200 萬美元，GM Financial 稅前 7 億美元，OnStar 與 Super Cruise 認列營收逾 8 億美元。單點依賴：北美大車撐起近九成本業利潤，新一代輕型皮卡 Q3 起先在墨西哥 Silao 投產，關稅與投產品質是集中風險。供需持久性屬週期性：美國 SAAR 全年約 1,650 萬輛，處於中段水位，需求靠消費者撐住；原料通膨與利率上行是將反轉的訊號。GM 自稱多數車款產能滿載，供給可逆性中等。產業時鐘判為過熱期：量持平、利潤率在目標區、投入成本 7 月以來再漲 10–15%（較去年均價約 50%），屬獲利面後段，量面並未過熱。產業態勢雙向拉鋸：一邊是競爭惡化（日系混動拿下美國過半份額、中國車廠全球份額上升），一邊是美國需求穩、皮卡折扣紀律好；另有關稅與排放法規放寬兩項結構變數。","fact_refs":["f_kpi0_total_net_sales_and_reve","f_kpi1_ebit_adjusted_non_gaap_o","f_kpi2_ebit_adjusted_margin","f_kpi6_gmna_ebit_adjusted_margi","f_kpi7_wholesale_volume_total","f_kpi8_fy2026_guidance"],"verdict_values":{"revenue_quality":"以整車批發收入為主（量乘價），屬一次性交易，隨循環波動。唯一的經常性來源是軟體與服務：Q3 認列營收逾 8 億美元，約占營收 1.6%；年底遞延營收接近 75 億美元。","unit_econ_note":"Q3 批發 102.8 萬輛、營收 500 億美元，每輛約 4.9 萬美元；每輛調整後 EBIT 約 4,000 美元（41 億美元除以 102.8 萬輛）。利潤集中在全尺寸皮卡與 SUV 的高配車型。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"低利潤率高周轉，盈餘隨美國 SAAR 與原料成本擺動，每股盈餘成長主要靠回購"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性。依據：Q3 法說稱 SAAR 在 1,600 萬輛中高段、全年約 1,650 萬輛；鋼與銅較去年均價約高 50%；分析師已在問利率上行與消費者體質，GM Financial 違約率尚未上升。","bargaining":{"up":"供應端議價力弱：鋼、銅、記憶體與物流 7 月以來再漲，2026 原料物流逆風約 20 億美元，GM 仍在找抵銷項","down":"對終端有中等議價力：經銷商獨立，皮卡換代期折扣率比歷次換代低數百基點，北美全年定價僅 +0.5%","geo":"232 鋼鋁關稅仍在，墨西哥與加拿大進口車受 USMCA 檢討影響；2026 毛關稅成本落在 25–35 億美元區間低端"},"profit_pool_dir":"利潤池往北美燃油大車與軟體服務集中，EV 與國際縮小；全球份額往中國車廠移動","tam_table":{"expanded":false,"reason":"美國新車市場已成熟，GM 不屬低滲透或新品類故事；事實表只有 SAAR，沒有分區段 TAM 與利潤池占比，無法誠實展開"}}}},"q2_moat":{"verdict":"護城河穩定但窄：只在北美全尺寸皮卡與 SUV 成立，整體份額正被混動與中國品牌侵蝕","reasoning":"護城河機制只在北美全尺寸皮卡與 SUV 成立。法說稱全尺寸皮卡份額逾 42%，換代期折扣率比歷次換代低數百基點；四品牌 3 月平均成交價年增 3.8%。執行面在擴大：北美利潤率 8.7%，年增 2.5 點，保固年改善約 11 億美元，兩次上調全年指引。定價面在縮減：美國整體份額 16.7%（去年 17.4%），流失集中在 EV 縮減、停產車款，以及 GM 沒有車的混動區隔。2027 原料逆風約 20 億美元能否轉嫁仍未知，CFO 也提醒不要用 2019 換代的漲價幅度推估。兩向抵銷，判為穩定，執行 7 分、定價 5 分。同業比較：事實表只有利潤率。GM 近四季 GAAP 營業利益率 0.98%，低於特斯拉的 4.61%，但這個數字含 EV 重整費用；投入資本缺漏，無法算 ROIC 差距，改看份額與折扣率。報酬持續期：屬低利潤率×高周轉，四檢查點皆為黃燈。增量報酬事實表未涵蓋；管理層自設新投資門檻 20%，沒有實現值驗證。內生成長上界以共識營收成長代理，約 3%。","fact_refs":["f_peer_gm_gross_margin_pct","f_peer_gm_operating_margin_pct","f_peer_tsla_operating_margin_pct","f_peer_tsla_gross_margin_pct","f_kpi6_gmna_ebit_adjusted_margi","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"moat":{"mechanism":"全尺寸皮卡與 SUV 的規模和品牌忠誠（美國全尺寸皮卡份額逾 42%、皮卡銷量連續七年第一），加上經銷網與自有融資，撐住高配車價與折扣紀律；這套機制在國際市場與小型車上不成立","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：北美利潤率年增 2.5 點，皮卡銷量年增 9%，換代期折扣偏低。定價面縮減：美國整體份額年減約 0.7 點，混動區隔缺席，2027 成本轉嫁未證。兩向抵銷，判為穩定。","competitor_notes":[{"name":"TSLA","strategy_note":"近四季營業利益率 4.61%、毛利率 18.85%，高於 GM 的 GAAP 數字，但 GM 含 EV 重整費用；兩家在 EV 與自駕直接對打，GM 的利潤池在燃油大車，與特斯拉重疊有限"},{"name":"AMZN","strategy_note":"同業表列入亞馬遜，但它不是整車廠，利潤率對比沒有意義，不作護城河判讀依據"},{"name":"底特律皮卡同業","strategy_note":"法說提到一家同業皮卡經銷商庫存偏高、長年用較高折扣；GM 以較低折扣仍拿到份額，是定價紀律的直接對照"},{"name":"日系車廠","strategy_note":"Q3 底特律三強美國份額約 36% 創新低，亞系品牌過半，主因油電混合；GM 在小型、中型轎車與廂型車沒有車"},{"name":"BYD 與中國車廠","strategy_note":"2026 上半年 BYD 全球份額 4.8%，已高於 GM 的 4.5%；在南美等市場與 GM 正面競爭，GM 稱南美份額守住"}],"peer_na_reason":"事實表沒有同業投入資本與 ROIC，無法算報酬差距；改以份額與折扣率作可比軸","threats":[{"level":"🔴","text":"中國低價車廠進入新興與成熟市場，10-K 自承已對定價、份額與獲利造成顯著負面影響；電池原料加工集中在中國，供應鏈也受制","p":35,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4","reg_tariff_export#2"]},{"level":"🟡","text":"日系混動在美國拿走份額，GM 在小型、中型轎車與廂型車沒有車；法說稱多個區隔將推混動、不需額外資本支出，但時程未揭露","p":40,"evidence_refs":["end_markets#1"]},{"level":"🟡","text":"軟體定義車走向 AI 定義車，中國車廠速度與成本領先；大型科技公司支持的新進者衝擊直銷與所有權模式。GM 以 Super Cruise 百萬輛保有量與 2028 年高速公路免看路系統應戰","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"買車是可延後的購買，急迫性低；Q3 SAAR 在 1,600 萬輛中高段，GM Financial 違約率未見變化。但管理層把 2027 成長前提明寫為需求維持，消費者信心調查已偏弱"},{"item":"決策層級","level":"🟡","text":"替代決策發生在家庭每次換車，轉換成本低。皮卡買家忠誠度高（份額逾 42%、折扣率低），但混動需求把小型與中型車買家帶向日系"},{"item":"價值鏈分配","level":"🟡","text":"上游鋼、銅、記憶體與物流在 2026 年多拿走約 20 億美元，GM 尚未找到抵銷；經銷商獨立，價值鏈中 GM 只在皮卡與 SUV 有定價空間"},{"item":"社會容忍度","level":"🟡","text":"新車負擔能力已是政策與輿論話題，北美全年定價只 +0.5%。排放法規放寬帶來約 5 億美元節省，屬政策紅利，法規回頭就會消失；關稅也取決於政策"}],"roiic":"事實表未涵蓋；管理層自設新投資報酬門檻 20%（2026-10-20 法說，CEO），沒有實現值驗證","reinvest_rate":"事實表未涵蓋；資本支出落在 100–120 億美元指引下半區，折舊攤提未收","endo_ceiling":3,"formula_note":"增量 ROIC 與再投資率無法從事實表算出，改用代理：共識營收 FY1 約 1,862.7 億美元到 FY2 約 1,895.0 億美元（+1.7%），加上利潤率小幅改善，內生成長上界取約 3%"}}}},"q3_growth":{"verdict":"成長跑道窄：量持平、價小幅，每股盈餘成長主要靠回購","reasoning":"共識調整後 EPS 由 FY2026E 13.37 美元升到 FY2028E 16.82 美元，兩年複合約 12.2%。共識營收 FY1 到 FY2 只增 1.7%。內生上界約 3%，缺口約 9 個百分點：主要來自淨回購（稀釋股數年減約 9%），其次是利潤率改善（保固、EV 虧損縮小、軟體），併購為零。法說稱 2027 皮卡產量與 2026 持平，2028 才有增量產能；軟體遞延營收年增 40%，但認列營收占比不到 2%，撐不起第二條成長曲線。美國新車市場已成熟，判跑道窄。衰退訊號十項亮兩項：美國份額縮減，以及每股盈餘成長遠高於營收成長。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"量：2027 皮卡產量與 2026 持平，2028 有增量產能；價：北美全年 +0.5%；併購：無；回購：每股盈餘成長的主力","runway_years":"不適用：美國新車市場已成熟，GM 美國份額約 17%，成長靠份額與價格，談不上滲透率","runway_post_y5":"🔴","endo_ceiling_basis":"內生上界約 3%。增量 ROIC 與再投資率事實表未涵蓋，以共識營收 +1.7% 加利潤率小幅改善代理。共識 EPS 兩年複合約 12.2%，缺口約 9 個百分點，主要歸因淨回購，其次是利潤率改善","segments":[{"item":"北美","value":"Q3 營收約 414 億美元，年增 2.1%；EBIT 調整後約 36 億美元，利潤率 8.7%"},{"item":"國際（不含中國權益）","value":"Q3 EBIT 調整後損益兩平，年減 2 億美元，含 Momenta 投資評價損失約 1 億美元"},{"item":"中國權益收入","value":"Q3 3,200 萬美元，連續 8 季獲利，新能源車占 GM 中國銷量逾 60%"},{"item":"GM Financial","value":"Q3 調整後稅前 7 億美元，全年指引 25–30 億美元，季配 2.5 億美元給母公司"},{"item":"軟體與服務","value":"Q3 認列營收逾 8 億美元，年增 15%；年底遞延營收接近 75 億美元，2027 年認列預期雙位數成長"},{"item":"GM Defense","value":"2026 營收約 7 億美元，管理層預期營收年增逾 30%；ISV 潛在合約逾 10 億美元，需國會撥款"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q3 北美調整後利潤率年增 2.5 點；季度 GAAP 毛利率事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"美國份額 16.7%，去年 17.4%"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"全尺寸輕型皮卡銷量年增 9%"},{"signal":"每股盈餘成長高於營收成長逾 5 點","lit":true,"note":"共識 EPS 兩年複合約 12%，營收只增 1.7%，差距來自回購"},{"signal":"自由現金流與淨利比連 2 年低於 0.75","lit":false,"note":"合併口徑 2024 為負、2025 約 0.66，但調整後汽車自由現金流 2026 指引 115–125 億美元；兩口徑差異的拆解事實表未涵蓋，不計入"},{"signal":"股權酬勞占營收超過 5% 且上升","lit":null,"note":"事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"混動與中國低價車屬份額替代，美國總量未萎縮，已計入份額項"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":null,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"2025 營收年減 1.3%，但 2027–28 有皮卡、SUV 與回美國生產的產能投資"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置積極且合理：自由現金流大量轉成回購，在低估值下回購效益高","reasoning":"現金去向如下。2026 年迄今回購 63 億美元，完成前次授權；新授權 200 億美元、多年期，約當市值三成。資本支出落在 100–120 億美元下半區。EV 重整現金費用累計 74 億美元，已付 46 億美元（其中 2026 年付 42 億），Q4 再付約 10 億，餘額 2027 年付清。股息殖利率約 0.9%。稀釋股數 Q3 約 8.66 億，年減約 9%。管理層的框架是：新投資要求 20% 報酬、維持投資等級，其餘回饋股東；四家信評皆給投資等級。自由現金流轉換：調整後汽車自由現金流 2026 指引 115–125 億美元，與調整後盈餘約略相當。合併口徑自由現金流 2022–2024 為負、2025 為 17.7 億美元，兩口徑落差的拆解事實表未涵蓋。合併淨負債 1,040 億美元，金融子公司與汽車本業的拆分事實表未涵蓋。股權酬勞占營收事實表未涵蓋。計分方面：近 12 個月無併購；回購以前瞻盈餘殖利率約 17.6% 買入，股數淨減，兩項通過。風險在於回購是在盈餘高原執行，若循環下行，同一筆錢在更低價位能買更多股。","fact_refs":["f_kpi4_adjusted_automotive_free","f_kpi8_fy2026_guidance","f_shares_diluted_m","f_dividend_yield_ttm","f_fwd_pe_latest","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無併購交割，只出售 Ultium Cells Lansing 廠權益給 LG Energy Solution"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"以前瞻本益比 5.69 倍回購，盈餘殖利率約 17.6%；事實表未收 10 年期公債殖利率，但差距大到結論不受影響"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數年減約 9%（Q3 約 8.66 億股），淨稀釋為負"}]},"governance":{"capital_returns":[{"item":"回購","value":"2026 年迄今 63 億美元，含 Q3 25 億、10 月 10 億；新授權 200 億美元多年期"},{"item":"股息","value":"近 12 個月殖利率約 0.9%"},{"item":"資本支出","value":"2026 年落在 100–120 億美元指引下半區"},{"item":"EV 重整現金費用","value":"累計 74 億美元，已付 46 億，Q4 約 10 億，餘額 2027 年付清"}]}}},"q5_valuation":{"verdict":"現價隱含盈餘將從高原回落；只要 2027 盈餘守住，回購就能推升每股價值，但我不認為市場明顯錯價","reasoning":"現價 76.11 美元、前瞻本益比 5.69 倍，等於市場只願付不到六年的盈餘，隱含盈餘將從高原回落。要讓現價划算，只需要 2027–28 年調整後 EPS 守在 14–16 美元並持續回購；我估守得住的機率約五成，衰退情境約三成。近四季 GAAP 本益比 16.65 倍的分母被 EV 重整費用壓低，不作依據。企業價值營收比 0.92 倍，在四個年度端點中落在 29 分位；事實表沒有真正的五年分位。以共識 FY2026E 到 FY2028E 兩年複合約 12.2% 計，PEG 約 0.47，但成長主要來自回購。12 個月 Base：2027E 14.6 美元乘 6 倍，約 88 美元（+15%）；3 年：2029E 15.6 美元乘 6 倍，約 94 美元（+23%）。賣方年中平均目標價約 98–101 美元，區間 61–132 美元，最高與最低之比約 2.2 倍。我的估值低於賣方，是因為把 2027 原料逆風扣進盈餘。事實表沒有同業前瞻本益比，終端倍數只能對照自身歷史與現價。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_ev_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（調整後稀釋 EPS，FY2026E）","tier":"整車廠","peers":{"expanded":false,"reason":"事實表沒有同業前瞻本益比；同業表只有利潤率，且亞馬遜不可比"},"fwd_pe":5.69,"peg":0.47,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 5.69 倍；以共識兩年 EPS 複合約 12.2% 計，PEG 約 0.47；企業價值營收比在四個年度端點中落在 29 分位。便宜成立，但盈餘處於循環高原、成長主要靠回購，便宜不等於錯價。","upside_short_pct":15.1,"upside_mid_pct":23.0,"denominator_disputed":false,"denominator_note":"GAAP 近四季本益比 16.65 倍的分母被 EV 重整費用壓低，改用調整後前瞻 EPS 錨定。重整現金費用管理層稱已大致認列，本輪不視為爭點；循環高原的分母風險已放進 Bear 機率 30%。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是循環位置：盈餘在高原，衰退或成本失控會讓低本益比變成陷阱","reasoning":"盈餘停在 EBIT 145–155 億美元的高原，原料、關稅與份額三項逆風同時存在；衰退一來，5.7 倍本益比就會變成陷阱。衰退訊號十項亮兩項，陷阱風險中度。股價 26 週 −3.25%、RSI 35.5，位於 52 週均線 79.18 美元之下、104 週均線 65.36 美元之上，動能不熱。最大回撤推估 −38% 至 −55%（Bear 谷底 EPS 約 8.2 美元乘 4.5–5.5 倍）；歷史回撤事實表未涵蓋。三個反證視角見反證紀錄。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高原上的低本益比"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.37,"pe":5.69,"basis":"FY2026E 共識調整後稀釋 EPS（10-21 快照），終端倍數同為調整後當年盈餘口徑"},"eps":{"bull":[15.5,17.6,19.3,20.8,22.3],"base":[14.6,16.0,15.6,16.6,17.6],"bear":[12.8,9.5,8.2,9.6,10.8]},"pe":{"bull":7.5,"base":6.0,"bear":5.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.91,"net_buyback":9.4},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"max_dd":{"lo":-55,"hi":-38,"basis":"Bear 谷底 EPS 約 8.2 美元（2029E）乘 4.5–5.5 倍，得 37–45 美元，對現價 76.11 美元為 −41% 至 −51%；再加上衰退訊號初現時市場先殺倍數的超跌緩衝，取 −38% 至 −55%。事實表未涵蓋歷史最大回撤，此範圍為推導值。","trigger_time":null},"basis":{"bull":"新卡車混合比與 2028 增量產能拉高皮卡份額，原料回落，軟體雙位數成長；EBIT 年增中個位數，加上股數每年縮 5–6%；倍數回到 7.5 倍","base":"2027 原料逆風吃掉大部分保固與 EV 改善，EBIT 持平；2029 年溫和循環下修約一成後回升；每股盈餘成長主要來自股數每年縮約 5%，已含在 EPS 路徑內，回購殖利率不應重複加計；倍數 6 倍","bear":"2028–29 年美國衰退，SAAR 跌破 1,450 萬輛，北美利潤率掉到 5% 以下，回購放緩；谷底 EPS 約 8.2 美元，2031 年回到 10.8 美元；倍數 5 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層把 2027 成長綁在需求維持與原料回落兩個前提；美國份額正在流失；10-K 自承關稅可能超出估計","assumption":"美國需求維持在 SAAR 1,600 萬輛上下，原料自高點回落","consequence":"若衰退與原料高檔同時發生，EPS 可能在 2–3 年內從 13 美元級回落到 8–9 美元，倍數同時壓到 4.5–5 倍，股價腰斬","ruling":"採納：這是五年虧五成最可能的路徑，已寫成唯一致命點，Bear 機率給 30%","watch":"SAAR 月度數字、GM Financial 違約率、北美利潤率","evidence_refs":["end_markets#1","reg_tariff_export#1","supply_demand_durability#1"],"fact_refs":["f_kpi6_gmna_ebit_adjusted_margi","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"EV 政策已反覆一次：2025–26 年 EV 重整現金費用累計 74 億美元。CFO 說油價可能推高 EV 滲透、要做好準備，2028–29 年 LMR 電池將再推一輪；回購又是在盈餘高原執行","assumption":"回購資金不被 EV 再投資或下一輪政策轉向吃掉","consequence":"皮卡賺的錢再度投入低報酬的 EV 產能，或高價回購遇上循環下行，每股價值不增","ruling":"部分採納：管理層 7 月稱曾拒絕數十億美元的 EV 廠投資，有紀律紀錄；但政策再翻轉的可能存在，列入風險監測","watch":"EV 相關資本支出與重整費用是否再出現；回購均價對盈餘的倍數","evidence_refs":["major_events#1"],"fact_refs":["f_kpi4_adjusted_automotive_free"]},{"view":"價格已反映太多","evidence":"前瞻本益比 5.69 倍；2027 共識 EPS 15.14 美元，近 3 個月 FY1 共識上修 4.5%","assumption":"共識尚未完全扣掉 7 月以來的原料漲價","consequence":"若共識下修約 4–8%，在倍數不變下股價下行有限","ruling":"反駁：倍數已在整車廠低檔，價格沒有反映太多；風險在盈餘分母，不在倍數，已放進論點失敗那條","watch":"1 月指引公布後的 2027 共識 EPS 修正","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 78.79 → 本次 76.11（-3.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=78.79","side_b":"本次 price_at_dd=76.11","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 78.79 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 78.79 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 78.79 美元：Bull 價 167.25、Bear 價 54，五年期望值 +30.0%，基準年化 6.0%，不對稱比 2.38","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.38。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 78.79 美元：五年期望值 +30.0%，基準年化 6.0%，不對稱比 2.38","side_b":"本次情境、股價 76.11 美元：五年期望值 +34.6%，基準年化 6.8%，不對稱比 2.75","ruling":"再換股價、情境不動：起點價下跌 3.4%，五年期望值多 4.6 個百分點，基準年化多 0.7 個百分點，不對稱比由 2.38 升到 2.75。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"2027 盈餘方向（管理層前後說法）","cause":"新證據","prior_field":null,"side_a":"2026-07-21 CFO：依目前所知，2027 年營收、利潤率、EBIT 與自由現金流都能成長","side_b":"2026-10-20 CFO：要原料價格從現水準回落一些才有信心成長；按 7 月以來漲幅年化，2027 逆風合計約 20 億美元","ruling":"不可調和，採 B 側：Base 路徑 2027 EPS 14.6 美元，比共識 15.14 低約 4%。現在就買的最強論證是：前瞻 5.7 倍、調整後汽車自由現金流約當市值 18%、新回購授權約當市值三成，就算 EBIT 持平，股數每年縮 5% 以上也能推升每股盈餘。不採的理由是這套算術在衰退時同樣反向放大，而 1 月指引這個決勝數據三個月內就到。觀望的約束只有一個：2027 原料成本能否吸收。","evidence_level":"公司法說原話（兩場）","settle_metric":"2027 年 1 月全年指引的 EBIT 調整後中值","if_then":["若中值 ≥ 150 億美元且第四季北美利潤率 ≥ 8%，首倉 2%","若中值 < 140 億美元，不追，並把 Base 2027 EPS 下修到 13.5 美元","價格先走、證據未到：若指引前股價跌到 66 美元以下且第四季數字未惡化，分批反買首倉 2%"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"份額","cause":"新證據","prior_field":null,"side_a":"美國整體份額 16.7%（去年 17.4%），底特律三強 Q3 份額創新低","side_b":"全尺寸皮卡銷量年增 9%、份額逾 42%，燃油車銷量年增；流失集中在 EV 縮減、停產車款與 GM 未參與的混動區隔","ruling":"可調和，屬程度差異：利潤池未失守，但混動缺口是慢性流失，列入風險，不判定護城河下滑","evidence_level":"公司法說與第三方銷量估計","settle_metric":"2027 年美國整體份額與全尺寸皮卡份額","if_then":["若美國份額連 4 季年減 ≥ 0.5 個百分點，停止加碼","若混動車型 2027 年上市且份額止跌，維持現有判斷"],"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"axis":"關稅成本估計","cause":"新證據","prior_field":null,"side_a":"10-K（2026-01）：2026 年關稅對 EBIT 調整後衝擊 30–40 億美元","side_b":"Q3 法說：2026 毛關稅成本落在 25–35 億美元低端，年迄今淨額約 18 億美元（含 IEEPA 退款）","ruling":"可調和：差異來自 IEEPA 關稅被推翻後的退款。232 鋼鋁關稅仍在，CFO 自承退款 2027 年不會重複，2027 關稅成本以毛額看","evidence_level":"10-K 與法說原話","settle_metric":"2027 指引中的關稅成本估計","if_then":["若 2027 關稅估計高於 2026 毛額上緣，Base 路徑再下修"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#3"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 78.79 美元，估值判為便宜","side_b":"現價 76.11 美元、前瞻本益比 5.69 倍，FY1 共識近 3 個月上修 4.5%","ruling":"估值結論不變：價格小跌、分母上修，倍數更低，但便宜的成因仍是循環高原","evidence_level":"事實表價格與共識快照","settle_metric":"前瞻本益比","if_then":[],"evidence_refs":[]},{"axis":"品質評級、陷阱與護城河方向漂移","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份：整體評級 B、陷阱風險中度、護城河穩定","side_b":"本輪三項不變：北美利潤率回升到 8.7%、皮卡銷量年增 9%，抵銷美國整體份額下滑與原料逆風","ruling":"維持：Q3 證據兩向都有，淨方向未改變","evidence_level":"Q3 季報與法說","settle_metric":"北美利潤率與美國份額","if_then":[],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"跑道、類型、循環位置與情境機率","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未評跑道、類型、循環位置與情境機率（皆為空），倚賴本益比回到 8 倍以上的均值回歸論點","side_b":"跑道窄（美國新車市場成熟、無足量第二曲線）；類型為循環/商品，循環位置為晚循環；情境機率 20／50／30，最大回撤 −38% 至 −55%；Base 終端倍數 6 倍","ruling":"方法變動：本輪改用循環股框架，前份的倍數均值回歸假設只保留在 Bull 路徑（7.5 倍）","evidence_level":"判斷方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設進場重啟條件","side_b":"2027 年 1 月指引的 EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%","ruling":"新設：觀望的唯一約束是成本吸收，重啟條件即該約束的否定","evidence_level":"判斷方法","settle_metric":"2027 全年指引","if_then":[],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻","side_b":"北美利潤率連 2 季 < 6% 清倉；SAAR 連 3 個月 < 1,450 萬輛清倉；美國份額全年 < 16.0% 減碼；稀釋股數年減 < 3% 減碼","ruling":"新設：依循環股特性，把需求、利潤率、份額與回購四個承重變數各設一條門檻","evidence_level":"判斷方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"Single Thing：美國進入衰退、新車 SAAR 連 3 個月跌破 1,450 萬輛","ruling":"新設：北美大車占近九成本業利潤，需求下滑是數學上最大的單一敏感項","evidence_level":"判斷方法","settle_metric":"SAAR 月度數字","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 全年指引確認原料成本吸收","type":"估值rearm","maps_to":"H3","metric":"2027 年 EBIT 調整後指引中值；第四季北美利潤率","threshold":"中值 ≥ 150 億美元且北美利潤率 ≥ 8%","action":"首倉 2%","source_freq":"第四季財報與全年指引（每年一次）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"北美利潤率跌出目標區","type":"假設驗證","maps_to":"H2","metric":"北美 EBIT 調整後利潤率","threshold":"連 2 季 < 8%","action":"不追；若已持有，停止加碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":3,"text":"美國進入衰退","type":"Single Thing","maps_to":"Single Thing","metric":"美國新車 SAAR","threshold":"連 3 個月 < 1,450 萬輛","action":"清倉","source_freq":"Cox Automotive 月度","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"美國份額持續流失","type":"風險","maps_to":"R2","metric":"GM 美國市佔年變化","threshold":"連 4 季年減 ≥ 0.5 個百分點","action":"停止加碼","source_freq":"季度銷量公告","date":null,"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"n":5,"text":"L87 V8 調查擴大為召回","type":"風險","maps_to":"R3","metric":"NHTSA 工程分析結論與召回費用","threshold":"召回確定且單一費用 > 10 億美元","action":"減碼","source_freq":"NHTSA 公告與 8-K","date":null,"evidence_refs":["product_recall_warning#0","major_events#2"]},{"n":6,"text":"回購放緩","type":"減碼","maps_to":"H1","metric":"稀釋股數年減幅","threshold":"< 3%","action":"減碼","source_freq":"季報","date":null,"evidence_refs":[]},{"n":7,"text":"價格回落而基本面無損","type":"加碼","maps_to":"H1","metric":"股價對 104 週均線；全年指引","threshold":"股價 ≤ 66 美元且指引未下修","action":"分批反買，首倉 2%","source_freq":"每週","date":null,"evidence_refs":[]},{"n":8,"text":"第四季財報後複審","type":"複審日期","maps_to":"H3","metric":"2027 指引與第四季數字","threshold":"財報公布","action":"重跑完整判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"北美 EBIT 調整後利潤率","bear_threshold":"連 2 季 < 6%（清倉）","window":"2027 Q1 至 2028 Q4","source":"GM 季報新聞稿","last_status":"ok"},{"metric":"美國新車 SAAR","bear_threshold":"連 3 個月 < 1,450 萬輛（清倉）","window":"未來 24 個月","source":"Cox Automotive 月度預估","last_status":"ok"},{"metric":"GM 美國市佔","bear_threshold":"全年 < 16.0%（減碼）","window":"2027 全年","source":"Cox Automotive 與 GM 季度銷量","last_status":"warning"},{"metric":"稀釋股數年減幅","bear_threshold":"< 3%（減碼）","window":"每季滾動 4 季","source":"GM 季報","last_status":"ok"}],"action_conditions":{"rearm_trigger":"2027 年 1 月指引的 EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%","exec_line":"條件成立後首倉 2%；2027 Q1 財報確認新卡車放量、北美利潤率仍 ≥ 8% 再加到 4%；循環股倉位上限 4%","holding_cap":"4%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 1 月全年指引：EBIT 調整後中值 ≥ 150 億美元，且第四季北美利潤率 ≥ 8%"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"7","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":true,"basis":"runway_post_y5='🔴'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🔴', val='🟢', moat_trend='→', week26=-3.25, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['7']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"回購持續壓低股數，本業持平時每股盈餘仍能成長","2y":"2026–27 年稀釋股數每年減 ≥ 5%；調整後汽車自由現金流每年 ≥ 100 億美元","5y":"五年累計股數再減 ≥ 25%","10y":null,"threshold":"稀釋股數年減 ≥ 5%","source":"季報稀釋股數、回購公告（新授權 200 億美元）","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉；5 年期：連 4 季偏離 ≥ 5% 視為削弱，連 6 季偏離 ≥ 10% 視為反轉"},{"id":"H2","text":"新一代全尺寸皮卡順利投產並帶動混合比，北美利潤率守住 8–10% 目標區","2y":"2027 年各季北美利潤率 ≥ 8%；2028 年增量產能帶動皮卡份額上升","5y":null,"10y":null,"threshold":"北美利潤率 ≥ 8%","source":"季報北美分部；法說投產進度（Silao、Fort Wayne、Orion）","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉"},{"id":"H3","text":"保固、EV 虧損與軟體收入的改善，抵銷約 20 億美元原料逆風，2027 EBIT 不低於 2026","2y":"2027 年 EBIT 調整後 ≥ 2026 年實際值（2026 指引 145–155 億美元）","5y":null,"10y":null,"threshold":"2027 指引中值 ≥ 150 億美元","source":"2027 年 1 月全年指引；季報保固與 EV 損益","drift_rule":"2 年期：連 2 季偏離 ≥ 5% 視為削弱，連 3 季偏離 ≥ 10% 視為反轉"}],"R":[{"id":"R1","text":"原料、物流、記憶體與關稅成本吸收失敗：2026 原料逆風約 20 億美元，2027 若按 7 月以來漲幅年化再加 10–15 億美元；10-K 自承關稅可能超出估計，短期緩解無法完全抵銷；中東衝突推高物流與原料成本","h_ref":"H3","clock":"⚡","threshold":"2027 年 1 月指引的 EBIT 調整後中值 < 140 億美元，或北美利潤率連 2 季 < 8%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#3","geo_supply_chain#0"]},{"id":"R2","text":"美國份額慢性流失：2026 年迄今份額 16.7%（去年 17.4%），Q3 美國銷量年減 5.5%，2025 年全球批發量減至 379.9 萬輛；混動區隔缺席","h_ref":"H2","clock":"🔥","threshold":"美國份額連 4 季年減 ≥ 0.5 個百分點，或全年 < 16.0%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","end_markets#1","supply_demand_durability#1"]},{"id":"R3","text":"新卡車投產品質與保固：NHTSA 對約 99.8 萬輛 L87 6.2L V8 皮卡與 SUV 評估 2025 年召回修復成效；新一代車型同時換上三款新引擎","h_ref":"H2","clock":"⚡","threshold":"調查升級為召回且單一費用 > 10 億美元，或保固年改善轉為惡化","evidence_refs":["major_events#2","product_recall_warning#0"]},{"id":"R4","text":"訴訟與法規罰款：Duramax 柴油排放與 8 速變速箱集體訴訟已發回重審，公司無法估計損失；Ultium TSCA 罰款累計 1,820 萬美元且持續增加。受影響營收與結案時點事實表未涵蓋","h_ref":"H1","clock":"🐢","threshold":"任一集體訴訟重新取得認證並出現不利和解，或單筆和解 > 10 億美元","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]},{"id":"R5","text":"EV 政策再翻轉：2026-01 已縮減 EV 產能並出售 Ultium Lansing 權益；若油價推高 EV 需求或法規回頭，可能再投入產能，吃掉回購資金","h_ref":"H1","clock":"🐢","threshold":"再出現 EV 相關重整費用，或 EV 資本支出顯著上調","evidence_refs":["major_events#1"]}],"single_thing":{"description":"美國進入衰退，新車 SAAR 連 3 個月跌破 1,450 萬輛","why_fatal":"北美大車占近九成本業利潤，營運槓桿高；量一掉，利潤率會跌出 8–10% 目標區，回購同時放緩，每股盈餘的兩個引擎一起熄火","if_happens":"清倉；等 SAAR 回升且北美利潤率重回 8% 以上，再重跑判斷","how_monitor":"Cox Automotive 月度 SAAR、GM Financial 違約率、經銷商庫存天數（目標 50–60 天）","probability":"約 25%（12–24 個月）；依據：管理層自己把 2027 成長綁在需求維持，分析師已在問利率上行與消費者體質，但 GM Financial 尚未見違約上升"}},"appendix_a":{"growth_durability":3,"quality_score":5,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":5.03,"peg_fy2":0.45,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":13.37,"FY2027E":15.14,"FY2028E":16.82},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（非 GAAP，Koyfin 共識 10-21 快照）；FY2025A 調整後實際值事實表未涵蓋，年報 GAAP 稀釋 EPS 3.27 美元含 EV 重整費用，不作基期"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年指引（董事會 12 月核定預算）","impact":"高","watch":"EBIT 調整後中值是否 ≥ 150 億美元，以及原料逆風估計"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"Fort Wayne 皮卡廠停工 4 週後以新車型復工","impact":"中","watch":"投產節奏與皮卡庫存天數"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"Orion 廠投產新一代輕型皮卡","impact":"中","watch":"2028 年增量產能是否如期"},{"date":null,"date_precision":null,"type":"regulatory","event":"NHTSA 對約 99.8 萬輛 L87 V8 車款的工程分析結論","impact":"中","watch":"是否擴大召回，以及費用規模"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
