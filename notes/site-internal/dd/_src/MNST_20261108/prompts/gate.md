你是 DD 管線 v20 的判斷層閘（gate），標的 MNST（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝2563.1 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MNST 8-K Ex.99-1 新聞稿（SEC EDGAR）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝748.1 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MNST 8-K Ex.99-1 新聞稿（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝718.7 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MNST 8-K Ex.99-1 新聞稿（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi3_gaap_gross_margin`（q1_business）｜GAAP gross margin＝54.7 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MNST 8-K Ex.99-1 新聞稿／10-Q（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi4_diluted_eps_gaap_non_gaa`（q1_business）｜Diluted EPS (GAAP / Non-GAAP)＝0.29 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：MNST 8-K Ex.99-1 新聞稿（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-05 date｜期間與口徑：2026-11-05／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-05）
- `f_peer_mnst_gross_margin_pct`（q2_moat）｜MNST 毛利率＝55.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNST.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mnst_operating_margin_pct`（q2_moat）｜MNST 營業利益率＝29.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNST.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mnst_fcf_margin_pct`（q2_moat）｜MNST FCF 利潤率＝22.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNST.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ko_operating_margin_pct`（q2_moat）｜KO 營業利益率＝32.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KO.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pep_operating_margin_pct`（q2_moat）｜PEP 營業利益率＝15.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PEP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_celh_operating_margin_pct`（q2_moat）｜CELH 營業利益率＝17.5 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CELH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_kdp_operating_margin_pct`（q2_moat）｜KDP 營業利益率＝14.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KDP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.15 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.31 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.48 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝9837.64 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝10764.4 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝4.2 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 SBC $30.4M ÷ GAAP 營業利益 $718.7M 換算（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3614.19 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 90.06、現金 3704.25（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1957.51 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝45.72 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝39.76 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.15，分子＝快照價 45.72｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝41.56 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝67.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝67.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.15 → 1.15（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝48.83｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝5.97 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝42.24 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝35.87 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝29.8 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述持續面對能量飲料、能量shot、啤酒及 beyond beer 類別的新進入者；功能性飲料業者（BODYARMOR、Prime、Starbucks 等）加入補充成分搶位，公司認為其成分含量較低、定位不同。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-27）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：競爭對手整併與配銷結盟：KDP 配銷 C4、Bloom 並同意收購 GHOST；Celsius 收購 Alani Nu；PepsiCo 2022 年與 Celsius 簽長期配銷協議。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 / Item 1A（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：公司風險因子承認競爭壓力可能導致價格侵蝕與市占下滑，並無法保證維持現有市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：Coca-Cola Europacific Partners 占淨銷售約 15%（2025）、14%（2024）、13%（2023）；Coca-Cola Consolidated 各年約 10%。
  - 來源：Monster Beverage FY2025 10-K (SEC)（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：S&P 於 2025 年 11 月維持 Coca-Cola Consolidated BBB+，展望由穩定調為負面（買回 24 億美元股票後）；2026 年未查到評等下調。
  - 來源：investing.com 報導 S&P 展望調整（as_of 2025-11-20）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Celsius 組合（含 Alani Nu）Q3 2026 占美國 RTD 能量飲料金額份額約 20.7%，貢獻無糖能量品類 7.73 億美元成長的約 28%
  - 來源：Pulse 2.0: Celsius Holdings: Brands Drive 30% Of Zero-Sugar Energy Category Growth（as_of 2026-11-05）｜affects：decision_inputs.bear、moat_trend
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：英國政府確認 16 歲以下高咖啡因能量飲料禁售將自 2027 年 4 月起生效（待國會批准）。
  - 來源：The Drinks Business（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露：美國加徵鋼鋁關稅並擴大適用範圍，另對多數進口商品課關稅；額外關稅或他國報復可能推高原料（鋁罐）成本，公司若無法轉嫁將影響獲利。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露：美國對全球、中國、加拿大、墨西哥等提出或實施關稅，貿易夥伴可能報復，可能擾亂國際市場並推高成本；海外銷售占 41%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：CEO稱2026Q1關稅與鋁價對毛利影響小於1%，預期成本至少到2026年底續升；鋁罐成本部分來自50%鋁關稅與中西部鋁溢價飆升；波斯灣中斷與荷莫茲海峽問題收緊鋁供給
  - 來源：FoodNavigator-USA / BeverageDaily: Monster Beverage Corp may raise prices as aluminum costs surge amid global tensions（as_of 2026-05-08）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K風險因子：部分代工(co-packing)合約允許代工廠依其自身成本上升調高費用；美國已提高鋼鋁關稅並擴大適用範圍；鋁罐等包材業界曾短缺、可能再發生，公司通常不避險
  - 來源：Monster Beverage FY2025 Form 10-K（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Jefferies 認為 Red Bull 新口味主要從 Celsius、其次從 Monster 取得份額（市佔競爭面）
  - 來源：TipRanks/The Fly: Red Bull's new flavors gaining share from Celsius, Monster says Jefferies（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 揭露：iced tea、咖啡、果汁、強化水、運動飲料等業者(BODYARMOR、Vitamin Water、CORE、Arizona、Powerade、Prime、Starbucks 等)加入補充成分，主打「功能性/能量」飲料;公司認為其成分含量較低、定位不同。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：多數銷售來自能量飲料，預期新進者使競爭持續激烈，可能面臨價格壓力與市占波動。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026（2026-11 公布）調整後 EPS $0.30 小幅優於共識 $0.2984，營收 $2.56B 優於預估 $2.49B；毛利率 54.7%（去年 55.7%）、營業利益率 28.0%（去年 30.7%），股價財報後下跌。未找到 Q4／全年 guidance 或財報後預估修正。
  - 來源：24/7 Wall St: Monster Beverage Q3 2026 Beat Overshadowed by Margin Slide（as_of 2026-11-06）｜affects：valuation、thesis.R、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":78.5,"bear_5y_price":26.0,"p_bull_pct":25,"p_bear_pct":25,"upside_5y_pct":24.0,"ev5y_pct":19.2,"irr_base_pct":4.4,"asym_ratio":1.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.15,"pe":39.76,"basis":"FY2026E 共識 EPS（FY1），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[1.35,1.56,1.79,2.04,2.31],"base":[1.27,1.42,1.57,1.72,1.89],"bear":[1.19,1.21,1.24,1.27,1.3]},"pe":{"bull":34,"base":30,"bear":20},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.0,"net_buyback":0.3},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MNST_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Hilton Schlosberg｜guidance：管理層說美國已啟動與夥伴討論，擬於2026年第四季實施選擇性漲價（原話："pricing actions effective during the 2026 fourth quarter"）
- 2026-08-06｜Hilton Schlosberg｜guidance：管理層預期鋁成本至少到2026年底持續溫和環比上升（原話："aluminum costs through at least the end of 2026"）
- 2026-08-06｜Hilton Schlosberg｜guidance：7月銷售（排除酒類、未調匯率）約年增14.3%（原話："approximately 14.3% higher than the comparable"）
- 2026-08-06｜Hilton Schlosberg｜margin：Q2毛利率55.9%，上升來自訂價與產品組合，被鋁罐、地區組合、進貨運費部分抵銷（原話："pricing actions and product sales mix partially offset by"）
- 2026-08-06｜Hilton Schlosberg｜margin：配送費用占比由3.9%升至4.7%，歸因運費與燃料（原話："largely reflecting higher freight and fuel costs"）
- 2026-08-06｜Hilton Schlosberg｜margin：銷售費用占比由9.3%升至10.6%，歸因社群數位等行銷、贊助與代言（原話："increased social, digital media and other marketing"）
- 2026-08-06｜Hilton Schlosberg｜margin：管理層說明國際銷售的毛利率較美國低，並稱重視金額而非百分比（原話："we bank dollars, we don't bank percentages"）
- 2026-08-06｜Hilton Schlosberg｜margin：Q2調整後營業利益年增13.3%，低於淨銷售年增20.2%（為兩個數字的並列陳述）（原話："drive revenue ahead of volume and profit ahead of revenue"）
- 2026-08-06｜Rob Gehring｜margin：管理層對訂價與利潤的目標說法：營收快於銷量、利潤快於營收（原話："a very limited market that we have hedged, but probably not"）
- 2026-08-06｜Hilton Schlosberg｜risk：鋁對沖：管理層承認Midwest premium的對沖可能不足（原話："current tariffs will have a material impact on the company's"）
- 2026-08-06｜Hilton Schlosberg｜risk：管理層稱目前關稅預期不會對營運結果造成重大影響（原話："depletions far exceeded our shipments"）
- 2026-08-06｜Hilton Schlosberg｜risk：南韓Q2銷售因經銷商庫存波動而下滑，出貨遠低於實際銷售（原話："depletions far exceeded our shipments in the quarter"）
- 2026-08-06｜Hilton Schlosberg｜risk：管理層提醒單月銷售不宜視為整季或未來的指標（原話："should not necessarily be imputed to or regarded as"）
- 2026-08-06｜Hilton Schlosberg｜competition：美加Monster品牌家族Q2價值市占增加70個基點（原話："gained 70 basis points of value market share"）
- 2026-08-06｜Hilton Schlosberg｜competition：EMEA旗下品牌貢獻該地區能量飲料品類價值成長的46%（原話："our portfolio delivered 46% of the value sales"）
- 2026-08-06｜Hilton Schlosberg｜competition：歐洲零糖區隔：Monster價值占有率44.5%並為領導者（原話："market leader in the Zero Sugar segment of the category"）
- 2026-08-06｜Rob Gehring｜competition：家戶調查中Monster拉新客的速度約為品類的兩倍（原話："bringing in consumers at twice the rate of the category"）
- 2026-08-06｜Hilton Schlosberg｜product：Ultra Red, White and Blue限量品自5月全國上市占Circana銷售5%（原話："accounted for 5% of sales in Circana"）
- 2026-08-06｜Hilton Schlosberg｜product：今年創新改為分批上市，不同於過去的一次性上市（敘事變化）（原話："staggered launches of our innovation versus onetime launches"）
- 2026-08-06｜Hilton Schlosberg｜product：FLRT：行銷6月才開始，管理層稱言之過早但仍承諾投入（原話："too early to tell, but we remain committed to the brand"）
- 2026-08-06｜Hilton Schlosberg｜product：零糖占品類成長逾75%，管理層稱家戶滲透率尚未見頂（原話："zero sugar accounts for more
than 75% of category growth"）
- 2026-08-06｜Hilton Schlosberg｜customer：Marriott與可口可樂的合作被管理層視為食品服務通路的重大配送機會（原話："open significant distribution opportunities for Monster"）
- 2026-08-06｜Hilton Schlosberg｜customer：管理層稱許多FSOP客戶現在要求供應能量飲料（原話："a lot of FSOP customers now are requiring energy drinks"）
- 2026-08-06｜Hilton Schlosberg｜customer：日本於6月起進入可口可樂裝瓶商持有的自動販賣機（原話："sales commenced in June
and are off to a good start"）
- 2026-08-06｜Hilton Schlosberg｜customer：國際淨銷售Q2年增34.6%，占總銷售約46%（去年同期約41%）（原話："Net sales to customers outside the United States increased"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：Q2未回購股票，截至8月5日回購授權剩約9億美元（原話："no shares of the company's common stock were repurchased"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：董事會批准1拆2，預計8月11日以拆分後價格交易（原話："approved
and declared a 2-for-1 split of its common stock"）
- 2026-08-06｜Hilton Schlosberg｜capital_allocation：巴西等地加大冷藏櫃投資；管理層稱未來有重大冷櫃投資（原話："we have major
investments going forward with coolers"）
- 2026-08-06｜Hilton Schlosberg｜commitment：SAP S/4HANA升級預計2028年1月1日上線（原話："SAP S/4HANA with a planned go-live date of January 1, 2028"）
- 2026-08-06｜Hilton Schlosberg｜commitment：計畫2026年12月1日在紐約舉辦投資人會議（原話："SAP S/4HANA with a planned go-live date of January 1, 2028"）
- 2026-08-06｜Hilton Schlosberg｜commitment：管理層將於10月NACS展示2027年完整創新時程（原話："host an investor meeting in New York City on December 1"）
- 2026-08-06｜Hilton Schlosberg｜commitment：EMEA歐洲部分市場已漲價，另提議年內在其他市場再漲價（原話："we have a full innovation calendar that we will be"）

### 問答異常語氣（迴避／改口／保留）
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Kaumil Gajrawala（Jefferies）請求漲價的地點與幅度細節｜答法：Rob Gehring談訂價哲學與目標，未給美國漲價幅度或範圍；Guy Carling僅給EMEA『aggregate low single-digits』，未給細節
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Kevin Grundy（BNP）問國際成長的可持續性與跑道（市占）｜答法：Guy Carling與Hilton講各地區驅動因素與品類佔比，未直接回答持續性或跑道的量化
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Bonnie Herzog（Goldman）問每箱配送與銷售費用Q2是否為合理run rate、後續是否下降｜答法：Hilton解釋運費燃料與行銷活動原因，未回答run rate或後續是否下降
- MNST_Q2_2026_Earnings_Call_20260806.md｜問：Chris Carey（Wells Fargo）問無全球大幅漲價下對保護毛利率的信心是否提升｜答法：Hilton談通膨、鋁對沖、國際毛利率較低，未直接回答信心變化，並以『we bank dollars』收尾

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 1 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 2 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"Q1 26 數字爆表(Rev +27%／EPS +29%／國際 +45%／China/India +95%)；新 .5B 回購；但估值已追平 5Y median；PEG 2.44 仍在 🟠 區；現價 .09 貼 BB 上軌(.70)+ 接近 52W 高 .77。Thesis 完整(品質 A／長期信心高／護城河 9/10)但時機不到 → B 觀望。等 PEG <2.0 或 MA 短回測 W52(./股) 再加碼。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國際擴張持續：EMEA / APAC / LatAm 三 region 加總增長 ≥ 30% 連 2-3 年，國際 mix 從 45% → 55%","columns":{"2Y 驗證點":"2027 國際合計 ≥ 30% YoY；EMEA / APAC / LatAm 三個都不能個別跌至 15% 以下","5Y 驗證點":"2030 國際 mix ≥ 55%；其中 APAC ≥ 25% 的全球 mix","10Y 驗證點":"2035 國際 mix ≥ 65%；中國 + 印度 + 巴西 三個合計 ≥ 25% 全球","具體數字門檻 + 來源":"30% / 55% mix（公司法說 Q1 26 Schlosberg 言論）","漂移觸發條件":"連 2 季 TTM 國際合計 &lt; 25%（季節性過濾 QC-34）"}},{"id":"H2","text":"美國 Monster Energy 主品牌維持 ≥ 10% 美加成長：剔除 Bang/Reign 衰退，主力品牌 不能 falter","columns":{"2Y 驗證點":"2027 美加 Monster Energy 品牌 ≥ 10%","5Y 驗證點":"2030 美加 Monster Energy 品牌 ≥ 8%（成熟區較低但 still positive）","10Y 驗證點":"2035 美加 Monster Energy 品牌 ≥ 5%","具體數字門檻 + 來源":"13.3% Q1 26 美加（Schlosberg Earnings Call 5/8）","漂移觸發條件":"連 2 季 美加 Monster Energy &lt; 8%（核心防線）"}},{"id":"H3","text":"毛利率反彈：Q3-Q4 26 H2 GM 回到 55%+，FY27 全年 GM 56%+（pricing actions 抵銷成本）","columns":{"2Y 驗證點":"FY27 全年 GM ≥ 56%","5Y 驗證點":"FY30 全年 GM ≥ 57%（國際 scale 後 mix 改善）","10Y 驗證點":"FY35 全年 GM ≥ 58%","具體數字門檻 + 來源":"55.8% FY25 GM（Macrotrends Income Statement）","漂移觸發條件":"連 2 季 GM &lt; 54%（結構性質變閾值）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"美國 Celsius/Alani 搶 Monster Energy 主品牌份額（不只搶 Reign/Bang）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Monster Energy 美加 YoY%","警戒閾值":"連 2 季 &lt; 8%"}},{"id":"R2","text":"毛利率結構性下移（國際 mix + 鋁罐 + Midwest premium 持續）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度 GM YoY 變動","警戒閾值":"連 2 季 GM &lt; 54%"}},{"id":"R3","text":"監管：caffeine 強制標示 / 18+ 限制 / 廣告限制（美國跟進 EU）","columns":{"對應假設":"整體","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"FDA / Congress 動向","警戒閾值":"需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":87.09,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MNST","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Monster Beverage Corporation"},"oneliner":"全球能量飲料的品牌與通路贏家，第三季營收年增 16.7%，但增量營益率只剩約 14%。現價約 40 倍 FY2026E，基礎情境五年年化約 4%～5%，等股價回到 38 美元以下再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MNST_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球便利通路每一罐能量飲料的品牌溢價，錢卡在品牌與可口可樂體系的貨架位置，不在產能。","reasoning":"第三季淨銷售 25.63 億美元，Monster Energy 飲料分部 23.7 億美元占約 92%，策略品牌 1.56 億美元占約 6%，酒類 2,850 萬美元且年減 13.6%。GAAP 毛利率 54.7%，GAAP 營益率 28.0%，調整後營益率 29.2%。生產與配銷交給代工廠和可口可樂體系裝瓶商，資本用得少，代價是 EMEA、亞太、拉美毛利率只有 37%～48%。單點依賴：Coca-Cola Europacific Partners 占第三季淨銷售約 17%，Coca-Cola Consolidated 約 9%，兩家同屬一個體系，這既是通路護城河，也是集中風險。產業時鐘在擴張期，依據是 2026-11-05 法說引用的第三季品類成長：美國 12.4%、EMEA 14.7%、亞太 11.3%、拉美 28.3%。供需持久性判為結構性持久，但增速會降溫：GlobalData 預期到 2030 年全球高個位數成長，美國零售商預期 2027 年降到約 7%。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income","f_kpi3_gaap_gross_margin","f_kpi4_diluted_eps_gaap_non_gaa","f_earnings_recency"],"verdict_values":{"revenue_quality":"營收幾乎全部來自重複購買的消費品，第三季匯率只貢獻 810 萬美元，也沒有併購墊高；短期雜訊來自裝瓶商庫存與出貨時點。","unit_econ_note":"第三季新增約 3.6 億美元營收，只帶來約 5,000 萬美元調整後營業利益，增量營益率約 14%，去年同期整體是 31.8%。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"輕資產品牌商、淨現金、借可口可樂體系出貨，成長靠國際鋪貨而非併購"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久，依據 2026-11-05 法說引用的 GlobalData 到 2030 年高個位數成長與 Nielsen 第三季各區雙位數品類成長；NACS 報導美國 2027 年降溫到約 7%。","bargaining":{"up":"鋁罐與代工廠議價偏弱：FY2025 10-K 稱通常不避險，部分代工合約可轉嫁成本，Midwest Premium 又受關稅推高。","down":"前兩大裝瓶商合計約 26%，可口可樂體系同時是通路夥伴；零售端靠冷櫃與貨架爭奪，品牌強勢時議價偏向公司。","geo":"美國以外占第三季 47%，關稅影響集中在鋁；英國年齡限制與印度標示令是地區監管風險。"},"profit_pool_dir":"利潤池往美國以外移，金額增加但百分比較低；五年份額變化事實表未涵蓋。","tam_table":[{"item":"美國能量飲料零售額 2025 年","value":"269 億美元，五年高個位數成長（Monster 主管所述）"},{"item":"第三季品類成長","value":"美國 12.4%、EMEA 14.7%、亞太 11.3%、拉美 28.3%（2026-11-05 法說引用 Nielsen 等）"},{"item":"第三方預測","value":"GlobalData 到 2030 年全球高個位數成長（2026-11-05 法說引用，非公司數字）"},{"item":"全球 TAM、滲透率、營業利益池占比","value":"事實表未涵蓋，12 月 1 日投資人日待補"}]}}},"q2_moat":{"verdict":"護城河穩定：國際份額還在擴大，定價能抵成本但抵不過地區組合，美國是唯一要盯的缺口。","reasoning":"機制是品牌加上可口可樂體系的鋪貨與冷櫃。同業 ROIC 事實表未涵蓋，可證方向改用份額：EMEA 第三季價值份額增加 190 個基點，歐洲零糖區隔 46.0%（第二季 44.5%），Oceania 增加 150 個基點，英國、埃及、塞爾維亞拿到價值第一；2026-08-06 法說報美加份額增加 70 個基點。TTM 營益率 29.16%，高於 CELH 17.50%、PEP 15.32%、KDP 14.84%，低於 KO 32.11%，只有單期，看不出利差方向。本輪從前份 9 分下調：定價權給 8 分，因為第三季定價只是大致抵銷鋁與投入成本，美國 11 月 1 日漲價的銷量反應還沒有數字；Celsius 加 Alani Nu 與 KDP 整合形成的對手體系再扣一分，合併落在 B。","fact_refs":["f_peer_mnst_gross_margin_pct","f_peer_mnst_operating_margin_pct","f_peer_mnst_fcf_margin_pct","f_peer_ko_operating_margin_pct","f_peer_pep_operating_margin_pct","f_peer_celh_operating_margin_pct","f_peer_kdp_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"品牌心智加上可口可樂全球裝瓶體系的鋪貨、冷櫃與新品上架能力","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大（EMEA 份額增加 190 個基點），定價權穩定（第三季定價大致抵銷鋁與投入成本），美國份額缺數字，合併看穩定。","competitor_notes":[{"name":"KO","strategy_note":"既是配銷夥伴也是利潤率標竿，TTM 營益率 32.11% 高於 MNST 29.16%；Rob Gehring 轉任可口可樂後雙方合作可能更深，利益分界也要多看一眼。"},{"name":"PEP","strategy_note":"靠 2022 年起與 Celsius 的長約配銷切入能量飲料，TTM 營益率 15.32%。"},{"name":"CELH","strategy_note":"最直接的對手，併 Alani Nu 後美國金額份額約 20.7%，貢獻無糖成長約 28%，但 TTM 營益率只有 17.50%，遠低於 MNST。"},{"name":"KDP","strategy_note":"走配銷整合路線，帶 C4、Bloom 並收購 GHOST，TTM 營益率 14.84%，整合效果還要時間證明。"},{"name":"Red Bull","strategy_note":"未上市，財務數字事實表未涵蓋；新口味分走份額，但歐盟競爭調查對它形成約束。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用份額方向與單期營益率。","threats":[{"level":"🔴","text":"美國出現對手體系：Celsius 有 PepsiCo 長約配銷並收購 Alani Nu，金額份額約 20.7%；KDP 配銷 C4、Bloom 並收購 GHOST。攻擊點是無糖與女性客群，第三季美加淨銷售增速低於品類。","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#1"]},{"level":"🟡","text":"Red Bull 新口味搶份額，Jefferies 認為主要取自 Celsius，其次才是 Monster。","p":"30%","evidence_refs":["end_markets#3"]},{"level":"🟡","text":"BODYARMOR、Prime、Starbucks 等加入機能成分搶能量場景，公司認為成分含量較低、定位不同，目前是點對點分流。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多半是同一人。第三季品類美國年增 12.4%、EMEA 14.7%，歐洲每年約 30% 新客，公司稱 Gen Z 家戶觸及 58%。屬於想要而非必需，但價位低、習慣已形成。"},{"item":"決策層級","level":"🟡","text":"替代要看單次購買：消費者在冷櫃前換牌幾乎沒有成本，黏著靠品牌與鋪貨。最好的代理變數是漲價後銷量，美國 11 月 1 日漲價的第一個完整季要到 2027 年 5 月才看得到。"},{"item":"價值鏈分配","level":"🟡","text":"品牌商拿走大部分利潤，TTM 營益率 29.16%。但最大客戶占比升到 17%，海外區域毛利率 37%～48%，代表海外的利潤分配對公司較不利；裝瓶商利潤率事實表未涵蓋。"},{"item":"社會容忍度","level":"🟡","text":"英國 16 歲以下禁售預計 2027 年 4 月生效，待國會批准；印度 FSSAI 要求停用能量飲料字樣，德里高等法院 10 月只給暫時救濟。目前壓力在年齡與標示，還沒有壓到價格。"}],"roiic":"事實表未涵蓋投入資本，無法直接算。代理：FY2022～FY2025 稅後營業利益約增 6.3 億美元（稅率假設 24%），FY2023～FY2025 累計淨利與自由現金流各約 50.5 億美元（財務歷史表，yfinance 年報），帳面淨再投資接近 0，比率沒有意義。","reinvest_rate":"約 0%（代理：FY2023～FY2025 累計淨利減自由現金流，FY2023 含營運資金回收）","endo_ceiling":null,"formula_note":"內生成長等於增量報酬乘再投資率，此處再投資率近零，算式給不出上界。資金不是成長的限制，真正上限是品類成長加份額與價格。行銷費用走損益，帳面看起來像零再投資；2026-08-06 法說 Schlosberg 預告冷櫃將有重大投資，再投資率之後可能上升。周轉率事實表未涵蓋，象限依生產外包與現金轉換推定。"}}}},"q3_growth":{"verdict":"五年後還有跑道但要打折：美國以外還在快速鋪貨，全球滲透率查不到，新增長也比舊生意薄。","reasoning":"成長以量為主、價為輔，沒有併購，回購貢獻很小。三年共識 EPS 從 FY2025A 0.97 美元到 FY2028E 1.48 美元，年化 15.1%（Koyfin 11-07 快照）；營收 FY2025 82.94 億美元到 FY2027E 107.64 億美元，年化 13.9%。內生上界算不出來，資金也不是限制，缺口改用共識自身拆：FY2027 EPS 年增 13.9%、營收 9.4%，多出的 4.5 個百分點全靠利潤率擴張，這正是本輪不採信的部分，長期信心上限為中。全球滲透率事實表未涵蓋，無法算到 30% 的年數。下一條成長曲線有證據但不夠厚：第三季印度當地貨幣年增 86.5%、巴西 60.4%、中國 35.5%，餐飲通路與蛋白飲料還沒有數字。第三季營收與 GAAP 營業利益增速差 10.3 個百分點，遠超 3 個百分點的警戒。若 12 月 1 日投資人日給出全球滲透率且低於 35%，跑道可上調一級。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔；無併購，回購貢獻很小。","runway_years":"事實表未涵蓋全球滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本事實表未涵蓋，增量報酬乘再投資率算不出上界；實際上限看品類高個位數成長加份額與價格，基礎情境 EPS 年化 10.5% 不依賴外部資金。","segments":[{"item":"Monster Energy 飲料分部","value":"第三季 23.7 億美元，年增 17.1%"},{"item":"策略品牌分部","value":"第三季 1.56 億美元，年增 19.8%"},{"item":"酒類分部","value":"第三季 2,850 萬美元，年減 13.6%"},{"item":"美加","value":"第三季年增 9.5%"},{"item":"EMEA","value":"第三季年增 24.9%，毛利率 37.2%"},{"item":"亞太","value":"第三季年增 12.3%，毛利率 42.1%"},{"item":"拉美","value":"第三季年增 48.8%，毛利率 47.7%"}],"decay_signals":["核心市占：美加第三季淨銷售年增 9.5%，低於 Nielsen 美國品類 12.4%，第三季法說也沒有再報美國份額；口徑不完全相同，算半亮，計一個。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本紀律沒有大錯，但閒錢太多：帳上淨現金約 36 億美元，回購在 40 倍附近買得很貴。","reasoning":"自由現金流對淨利 FY2023 0.91 倍、FY2024 1.07 倍、FY2025 1.02 倍（財務歷史表，yfinance 年報）。SBC 第三季 3,040 萬美元，占淨銷售約 1.2%，年化稀釋約 0.14%。現金去向四分事實表未涵蓋，只知道第三季回購 1 億美元、均價 43.87 美元，第二季沒有回購，無股息，截至 11 月 4 日授權餘額約 8 億美元，近 12 個月無併購。","fact_refs":["f_kpi5_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購；過往併購的投入金額事實表未涵蓋，無法計算已實現報酬。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"FY2026E EPS 1.15 美元除以第三季回購均價 43.87 美元，約 2.62%。10 年期殖利率事實表未涵蓋，但要過門檻，10 年期須低於 0.62%，判未過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季 SBC 3,040 萬美元年化約 1.22 億美元，除以市值 894.97 億美元，約 0.14%／年，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自身品牌與品類，近 12 個月無併購，資本報酬表不影響本輪結論。"}}}},"q5_valuation":{"verdict":"現價要 FY2031 EPS 做到約 2.24 美元、年化 14.3%，再守住 30 倍，才有 8% 年化；我只信 1.89 美元、年化 10.5%。","reasoning":"現價 45.72 美元約當 FY2026E 39.76 倍、FY2027E 34.9 倍。PEG 以 FY2025A 到 FY2028E 年化 15.1% 算為 2.63，高於前份 2.44。分位數只有 4 個年度端點：本益比 67.9%，股價營收比與企業價值營收比都在最高點，不能當五年區間用，五年高低點事實表未涵蓋。前份價格 87.09 美元是拆股前，換算 43.55 美元，本次實際上漲約 5%。同業倍數事實表未涵蓋，只能和自身比。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"valuation":{"basis":"FY2026E 共識 EPS 的本益比，搭配 PEG；公司已獲利，不用營收倍數當主尺。","tier":"飲料品牌高成長","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，屬資料缺口，無法做跨公司倍數比較。"},"fwd_pe":39.76,"peg":2.63,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026E 39.76 倍、PEG 2.63，高於 2 算貴；基礎情境五年年化約 4%～5%，低於 8%。本益比在 4 個年度端點的 67.9% 分位，還沒到頂，RSI 48.83，動能不熱，所以判偏貴，還不到最貴一檔。短期空間：FY2027 基礎 EPS 1.27 美元乘 36 倍約 45.7 美元；中期空間：FY2029 基礎 EPS 1.57 美元乘 32 倍約 50.2 美元。","upside_short_pct":0.0,"upside_mid_pct":9.9,"denominator_disputed":false,"denominator_note":"FY2026E 已接近完成，未見一次性項目墊高；爭點在 FY2027 利潤率，放在情境路徑處理。"}}},"q6_how_wrong":{"verdict":"最可能看錯在利潤率：漲價與費用槓桿若提早見效，38 美元可能等不到；美國份額若也掉，跌幅不只兩成。","reasoning":"成長熄火壓力：以 FY2028 基礎 EPS 1.42 美元為起點，FY2029 成長 15%、10%、5% 配 36、30、20 倍，股價約 58.8、46.9、29.8 美元，對現價約＋29%、＋3%、−35%，三項過兩項。十類衰退訊號只有美國份額半亮，毛利率第三季年減一次，第二季還是上升，再差一季就亮第二個。管理層連兩季不回答利潤率節奏：2026-08-06 對 Herzog 的費用 run rate、對 Carey 的毛利率信心，2026-11-05 對 Galbo 的組合影響、對 Herzog 的第四季與明年節奏，都沒有正面答案。歷史最大回撤事實表未涵蓋。","fact_refs":["f_kpi3_gaap_gross_margin","f_kpi1_non_gaap_operating_incom","f_fwd_pe_latest","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"不是低價陷阱，風險是用高倍數買到利潤率下滑"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.15,"pe":39.76,"basis":"FY2026E 共識 EPS（FY1），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[1.35,1.56,1.79,2.04,2.31],"base":[1.27,1.42,1.57,1.72,1.89],"bear":[1.19,1.21,1.24,1.27,1.3]},"pe":{"bull":34,"base":30,"bear":20},"p":{"bull":25,"base":50,"bear":25},"yield_pct":{"dividend":0.0,"net_buyback":0.3},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":7},"max_dd":{"lo":-50,"hi":-35,"basis":"事實表未涵蓋歷史最大回撤，改用倍數推算：FY2026E EPS 下修 5% 到 1.09 美元，倍數壓到 21～27 倍，股價 22.9～29.5 美元，對應 −50%～−35%；250 週線 29.80 美元約等於 −35%。","trigger_time":null},"basis":{"bull":"國際維持約 20%、美加約 11%，營收年化約 13.5% 到約 185 億美元；美國漲價站穩，營益率升到約 30.5%；股數持平，34 倍。","base":"營收年化約 10% 到約 159 億美元，毛利率往 53% 滑，費用槓桿抵銷後營益率 28.6%～28.9%；股數持平。30 倍約當 PEG 3；同業倍數事實表未涵蓋，無法附同業對照，以自身現值 39.76 倍與成長降溫推算。","bear":"美國份額流失、國際降到高個位數，營收年化約 5% 到約 126 億美元，成本與促銷把營益率壓到約 24%；用成長降到 5% 的情境給 20 倍。機率 25%，因為美國對手體系與利潤率下滑都已有實際數字，但歐洲份額仍在擴大，不再往上加。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"第三季美加淨銷售年增 9.5%，低於 Nielsen 美國品類 12.4%；Celsius 組合份額約 20.7%；增量營益率約 14%。","assumption":"美國份額流失與成本壓力同時發生，公司用更多行銷與促銷防守。","consequence":"五年後虧 50% 的路徑：美加成長掉到中個位數，營益率落到 24%，FY2031 EPS 1.30 美元，20 倍，股價 26 美元，途中再多跌一段。","ruling":"部分採納，機率 25%。反駁面是 EMEA 份額與歐洲零糖 46.0% 都還在擴大。此路徑與唯一致命點部分重疊，營益率是共同變數，這裡多了美國份額一項。","watch":"美加淨銷售增速、美國份額表、調整後營益率","evidence_refs":["supply_demand_durability#1","competitive_share_entrants#1"]},{"view":"論點成功但股東經濟變差","evidence":"美國以外占第三季 47% 且仍快於美國，區域毛利率 37.2%～47.7%；2026-11-05 法說 Schlosberg 說「we bank dollars, we don't bank percentages」；2026-08-06 法說 Schlosberg 預告冷櫃重大投資。","assumption":"國際成長達成，但新增營收的利益率長期低於舊生意，還要多投冷櫃與平價品牌。","consequence":"營收超預期、EPS 不超預期，倍數照樣下來。推算每多 1 個百分點國際占比，毛利率少約 0.13～0.33 個百分點，占比到 56% 約再少 1.2～3.0 個百分點。","ruling":"採納，這是本輪最重要的修正，第三個假設從毛利率反彈改成營業利益金額跟上營收。","watch":"增量營益率、區域毛利率、資本支出","evidence_refs":["capital_markets_pricing#3"]},{"view":"價格已反映太多","evidence":"FY2026E 39.76 倍、PEG 2.63，股價營收比在 4 個年度端點的最高點；賣方平均目標價拆股調整後約 45.29 美元，幾乎等於現價。","assumption":"五年後倍數仍高，但會隨成長降溫往 30 倍走。","consequence":"基礎情境成真，五年年化也只有 4%～5%，要靠牛市情境才到約 11%。","ruling":"採納。卡住進場的只有價格，生意本身沒有壞。","watch":"股價相對 38 美元；FY2027 共識 EPS 是否下修"}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 87.09 → 本次 45.72（-47.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=87.09","side_b":"本次 price_at_dd=45.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 87.09 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 87.09 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 87.09 美元：Bull 價 78.54、Bear 價 26，五年期望值 −37.4%，基準年化 −8.2%，不對稱比 0.14","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.14。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 87.09 美元：五年期望值 −37.4%，基準年化 −8.2%，不對稱比 0.14","side_b":"本次情境、股價 45.72 美元：五年期望值 +19.2%，基準年化 4.4%，不對稱比 1.66","ruling":"再換股價、情境不動：起點價下跌 47.5%，五年期望值多 56.6 個百分點，基準年化多 12.6 個百分點，不對稱比由 0.14 升到 1.66。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份空欄補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位都是空值，當時的格式沒有產出。","side_b":"本輪護城河方向穩定，五年後跑道中等，類型為品質複利成長，最大回撤 −35%～−50%，牛熊機率各 25%，不屬循環股，週期位置留空。","ruling":"這是格式補齊，不是看法改變，無法和前份比方向。","evidence_level":"格式差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"結論與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B、陷阱風險中等，理由是時機不到，等回檔加碼。","side_b":"本輪評級 B、陷阱風險中等，但理由換了：第三季毛利率 54.7% 跌破前份 55% 的反彈假設，增量營益率約 14%，美加增速低於品類。","ruling":"等級不變，內容變差。前份看的是價格時機，本輪多了利潤率這個基本面問題，長期信心由高降到中。","evidence_level":"實績","settle_metric":"FY2026 第四季毛利率與增速差","if_then":["若第四季毛利率低於 54%，下一季再低於 54% 就減碼三分之一","若連 2 季增速差縮到 3 個百分點內，陷阱風險降一級"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值偏貴，PEG 2.44，拆股前 87.09 美元，換算 43.55 美元。","side_b":"本輪仍偏貴，PEG 2.63，45.72 美元，較前份拆股調整價約高 5%。","ruling":"結論不變。股價小漲而共識沒有上修，PEG 略升。前份的 87.09 美元不可和現價直接比，否則會誤讀成腰斬。","evidence_level":"實績","settle_metric":"FY2027 共識 EPS 與股價","if_then":[],"evidence_refs":[]},{"axis":"建倉與加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 PEG <2.0 或 MA 短回測 W52 再加碼","side_b":"股價回到 38 美元以下，基礎情境五年年化回到 8% 以上；觸發後重跑研究再建首倉","ruling":"舊條件作廢。52 週線現在 42.24 美元，回測到那裡基礎情境年化只有約 6.4%，不夠補償利潤率風險；PEG 用的三年共識成長正是本輪不採信的部分，改用報酬率直接定價。任何加碼前先重跑研究。","evidence_level":"本研究推算","settle_metric":"股價與基礎情境報酬","if_then":["若股價跌到 38 美元以下且毛利率未連 2 季低於 54%，分批反買","若股價先漲、利潤數字未改善，不追"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份沒有獨立的清倉或減碼指標，只有警戒：美加 Monster Energy 連 2 季 <8%；GM 連 2 季 <54%。","side_b":"保留 8% 與 54% 兩個數字，美加改用公司有揭露的總額；新增 FY2027 調整後營益率 <27.5% 與增速差連 3 季 >7 個百分點，觸發時減碼；營益率破線且美加連 4 季 <5% 才清倉。","ruling":"舊數字不放寬。新增利潤率門檻，是因為地區組合會讓毛利率單獨看失真。","evidence_level":"格式與新增指標","settle_metric":"每季財報","if_then":[],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（欄位為空）","side_b":"FY2027 全年調整後營業利益率跌破 27.5%","ruling":"本輪新設 Single Thing。選營益率是因為敏感度最大：1 個百分點約等於 FY2027 EPS 的 3.2%，高於國際增速少 5 個百分點的約 2.4%。","evidence_level":"本研究推算","settle_metric":"FY2027 年報","if_then":["若 FY2027 全年調整後營益率低於 27.5%，減碼一半，未持有則不建倉"],"evidence_refs":[]},{"axis":"假設門檻重訂","cause":"新證據","prior_field":["thesis.H"],"side_a":"2027 國際合計 ≥30% YoY；2027 美加 Monster Energy 品牌 ≥10%；FY27 全年 GM ≥56%","side_b":"FY2027 美國以外年增 ≥18%；美加淨銷售年增 ≥8%；FY2027 調整後營益率 ≥28.5%","ruling":"國際增速第一季約 45%、第二季 34.6%、第三季 28.1%，基期變大，30% 已不適合當兩年門檻。毛利率反彈假設被否定：第三季 54.7%，2026-11-05 法說 Schlosberg 明說國際成長會持續拖累，FY27 56% 的門檻正式退休，改看利潤金額。門檻下調同時，基礎 EPS 也調到低於共識，沒有放寬結論。","evidence_level":"實績＋管理層說法","settle_metric":"FY2027 年報","if_then":[],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"FY2027 利潤率方向","cause":null,"prior_field":null,"side_a":"共識：FY2027 營收年增 9.4%、EPS 年增 13.9%，推算營益率從約 29% 升到約 30%；11 月 7 日快照三年 EPS 全部沒動。","side_b":"第三季營收年增 16.7%、調整後營業利益只增 7.1%，第二季是 20.2% 對 13.3%；2026-11-05 法說 Schlosberg 說國際成長對毛利率的拖累是大家都得接受的事，鋁成本上升延到至少 2027 年第一季。","ruling":"方向相反，必須選邊。採第三季實績這一側：基礎情境 FY2027 EPS 1.27 美元，低於共識約 3%。依據是增量營益率約 14%，而美國漲價 11 月 1 日才生效，效果還沒有數字。市場若錯，錯在成長基準，把漲價當成已經抵銷成本與組合拖累。快照在財報後兩天，賣方可能還沒改模型，在第一個驗證數字出來前凍結加碼。","evidence_level":"實績與管理層說法為高，隱含營益率為本研究推算","settle_metric":"FY2026 第四季與 FY2027 第一季的營收年增減調整後營業利益年增","if_then":["若連 2 季增速差 ≤3 個百分點，基礎 EPS 上修到共識，可建倉價調到 40 美元","若連 3 季增速差 >7 個百分點，取消建倉計畫，已持有則減碼三分之一","若股價先漲、利潤數字未改善，不追","若股價跌到 38 美元以下而利潤率未破門檻，分批反買"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"美國份額","cause":null,"prior_field":null,"side_a":"2026-08-06 法說 Schlosberg：美加價值份額第二季增加 70 個基點；同場 Gehring：家戶調查拉新客速度約品類兩倍。","side_b":"2026-11-05 法說沒有再給美國份額數字，只報 EMEA 與 Oceania；美加淨銷售年增 9.5%，Nielsen 美國品類 12.4%。Jefferies 認為 Red Bull 新口味也取走部分份額。","ruling":"目前不可裁決。淨銷售與掃描數據口徑不同，裝瓶商庫存也會造成差異，不能直接算成掉份額；但管理層少報了上一季報過的數字，本身是警訊，先記半個衰退訊號。決勝數據在 8-K 的區域掃描附件，本次資料未收錄，2027 年 2 月財報前要補。","evidence_level":"公開實績，但口徑不完全可比","settle_metric":"8-K 附件 Nielsen 美國份額年變化","if_then":["若美國份額連 2 季年減超過 50 個基點，第二個假設改判削弱並停止加碼","若美國份額回到年增，這個衰退訊號熄燈"],"evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"axis":"管理層利潤說法","cause":null,"prior_field":null,"side_a":"2026-08-06 法說（摘錄標為 Rob Gehring，該段講者與原話有錯位）：營收快於銷量、利潤快於營收。","side_b":"第二季調整後營業利益年增 13.3%、營收 20.2%；第三季 7.1%、16.7%，連兩季做不到。2026-11-05 法說 Schlosberg 改強調「we bank dollars」，不回答第四季與明年節奏。","ruling":"採實績。這句話出自訂價討論，未必是全公司承諾，但連兩季反向就不能當利潤率會回升的證據。","evidence_level":"實績＋法說摘錄","settle_metric":"FY2026 第四季增速差","if_then":["若第四季調整後營業利益增速仍低於營收 5 個百分點以上，基礎情境維持低於共識，停止加碼"],"evidence_refs":[]},{"axis":"鋁成本時程與避險","cause":null,"prior_field":null,"side_a":"2026-08-06 法說 Schlosberg：鋁成本至少到 2026 年底持續溫和上升，摘錄也記錄管理層承認 Midwest Premium 避險可能不足。FY2025 10-K：公司通常不避險。","side_b":"2026-11-05 法說 Schlosberg：延到至少 2027 年第一季，原鋁一年漲 36%，仍稱影響溫和，並說有在做避險。","ruling":"不採信也不否定「溫和」。第三季定價確實大致抵銷成本，毛利率下滑主要來自地區組合；但時程已往後延一季，這項歸因列為未證、監測。","evidence_level":"管理層說法","settle_metric":"GAAP 毛利率","if_then":["若到 2027 年第二季報告時毛利率連 2 季低於 54%，「溫和」的說法算證偽，減碼三分之一"],"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"調整項是否一次性","cause":null,"prior_field":null,"side_a":"公司把第三季設備減損 1,990 萬美元、數位轉型 1,470 萬美元列為 G&A 內的特殊項目。","side_b":"SAP S/4HANA 要到 2028 年 1 月 1 日上線，數位轉型費用至少還有 5 季。","ruling":"減損先當一次性，數位轉型不算一次性，所以本輪同時看 GAAP 營益率 28.0%。未證、監測：減損類項目若連 3 季出現，就不再視為一次性。","evidence_level":"實績","settle_metric":"GAAP 與調整後營業利益差額","if_then":[],"evidence_refs":[]},{"axis":"賣方目標價口徑","cause":null,"prior_field":null,"side_a":"Tickergate 彙整 44 位分析師 12 個月平均目標價 90.58 美元，區間 77～103 美元；Morgan Stanley 103 美元、Bernstein 95 美元。","side_b":"這些都在 8 月拆股前。除以 2 後平均 45.29 美元，區間 38.5～51.5 美元，比現價低約 1%。","ruling":"不能用 90.58 美元算出接近翻倍的空間。現價已貼著拆股調整後平均目標價，支持觀望。最高與最低目標價相差 1.34 倍，分歧不大。目標價都在第三季財報前，下次要重查。","evidence_level":"二手彙整，日期未標明","settle_metric":"投資人日與第四季財報後的目標價","if_then":[],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"營收年增 16.7%，國際 28.1%，歐洲零糖份額 46.0%，淨現金約 36 億美元；美國 11 月 1 日漲價加上 2027 年費用基期墊高，利潤率可能反彈；FY2027 營收共識只有年增 9.4%，明顯偏低，10 月銷售還有 11.6%。","side_b":"就算營收比共識高 3%，營益率不回升，EPS 也只到共識附近；40 倍已經把反彈算進去。","ruling":"不買。多頭說的營收上修我同意，基礎情境營收高於共識；差異在利潤率與倍數。卡住進場的只有價格。","evidence_level":"本研究推算","settle_metric":"FY2027 第一季調整後營益率","if_then":["若 FY2027 第一季調整後營益率 ≥30% 且股價 ≤43 美元，可建倉價調到 43 美元並重跑研究","若 FY2027 第一季調整後營益率低於 28% 而股價高於 38 美元，不追"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：Celsius 併 Alani Nu、KDP 併 GHOST，新進者持續增加。","side_b":"結構：美國零售額 2025 年 269 億美元，第三季各區品類雙位數成長，GlobalData 看到 2030 年高個位數。其他變數：英國年齡限制與印度標示令。","ruling":"雙向拉鋸。品類需求結構性轉好，美國競爭同時惡化，監管是第三個慢變數。","evidence_level":"公司申報＋第三方資料","settle_metric":"美國份額與品類增速","if_then":[],"evidence_refs":["competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"股價回到 38 美元以下，重跑研究後建首倉","type":"估值rearm","maps_to":"H3","metric":"MNST 收盤價","threshold":"≤38 美元","action":"分批反買","source_freq":"每日收盤","date":null},{"n":2,"text":"FY2027 全年調整後營益率跌破 27.5%","type":"Single Thing","maps_to":"H3","metric":"調整後營業利益除以淨銷售","threshold":"<27.5%","action":"減碼一半，未持有則不建倉","source_freq":"每季新聞稿，年度定案","date":"2028-02"},{"n":3,"text":"GAAP 毛利率連 2 季低於 54%","type":"風險","maps_to":"R2","metric":"GAAP 毛利率","threshold":"連 2 季 <54%","action":"減碼三分之一","source_freq":"每季新聞稿","date":"2027-05","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","capital_markets_pricing#3"]},{"n":4,"text":"營收與調整後營業利益增速差回到 3 個百分點內","type":"假設驗證","maps_to":"H3","metric":"營收年增減調整後營業利益年增","threshold":"連 2 季 ≤3 個百分點","action":"基礎 EPS 上修到共識，可建倉價調到 40 美元","source_freq":"每季新聞稿","date":"2027-05"},{"n":5,"text":"美加淨銷售年增連 2 季低於 8%","type":"風險","maps_to":"R1","metric":"美加淨銷售年增","threshold":"連 2 季 <8%","action":"減碼三分之一","source_freq":"每季 10-Q","date":"2027-05","evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"n":6,"text":"營益率破線且美加成長同時失守","type":"清倉","maps_to":"H2、H3","metric":"FY2027 調整後營益率與美加淨銷售年增","threshold":"營益率 <27.5% 且美加連 4 季 <5%","action":"清倉","source_freq":"每季財報","date":"2028-02"},{"n":7,"text":"年齡與標示限制擴散：英國 2027 年 4 月生效，印度案件未結","type":"風險","maps_to":"R3","metric":"新增立法市場數、印度當季營收","threshold":"第三個主要市場立法且擴散機率 ≥50%，或印度終局敗訴且當季營收年減","action":"減碼三分之一","source_freq":"法規公告與法院公告","date":"2027-04","evidence_refs":["regulatory_antitrust#2"]},{"n":8,"text":"投資人日複審：看全球滲透率、長期利潤率框架與冷櫃投資","type":"複審日期","maps_to":"H1、H3","metric":"管理層揭露內容","threshold":"提供滲透率或利潤率框架","action":"更新五年後跑道與基礎情境","source_freq":"一次性","date":"2026-12-01"},{"n":9,"text":"股價先漲、利潤數字沒有改善","type":"估值rearm","maps_to":"H3","metric":"收盤價與增速差","threshold":"股價高於 45.72 美元且增速差仍 >5 個百分點","action":"不追","source_freq":"每季財報與每日收盤","date":null},{"n":10,"text":"裝瓶商集中或信用惡化","type":"風險","maps_to":"R4","metric":"單一裝瓶商占淨銷售、前兩大信評","threshold":"單一裝瓶商 >20% 或信評低於 BBB-","action":"停止加碼","source_freq":"每季 10-Q 與評等公告","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]}],"kill_metrics":[{"metric":"FY2027 全年調整後營業利益率","bear_threshold":"<27.5%","window":"FY2027 全年","source":"財報新聞稿調整後損益調節表","last_status":"ok"},{"metric":"GAAP 毛利率","bear_threshold":"連 2 季 <54%","window":"連續 2 季","source":"財報新聞稿","last_status":"warning"},{"metric":"美加淨銷售年增","bear_threshold":"連 2 季 <8%","window":"連續 2 季","source":"10-Q 地區營收","last_status":"ok"},{"metric":"營收年增減調整後營業利益年增","bear_threshold":"連 3 季 >7 個百分點","window":"連續 3 季","source":"財報新聞稿","last_status":"warning"},{"metric":"美國以外淨銷售 TTM 年增","bear_threshold":"連 3 季 <16.2%","window":"連續 3 季","source":"10-Q 地區營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到 38 美元以下，基礎情境五年年化回到 8% 以上；觸發後重跑研究再建首倉","exec_line":"現在不追。38 美元以下分批建首倉，第一筆前先重跑研究；12 月 1 日投資人日與 2027 年 2 月財報前不加碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 38 美元以下，基礎情境五年年化回到 8% 以上","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"美國以外仍是第一成長引擎，增速從第三季 28.1% 回落，但 FY2027 仍守得住 18% 以上。","2y":"FY2027 美國以外淨銷售年增 ≥18%，占總營收 ≥49%","5y":"FY2031 美國以外占總營收 ≥56%，EMEA、亞太、拉美沒有一區連兩年衰退","10y":null,"threshold":"FY2027 年增 ≥18%，占比 ≥49%（第三季為 28.1%、47%）","source":"每季財報新聞稿與 10-Q 的地區淨銷售，法說的區域數字","drift_rule":"TTM 年增連 2 季低於 17.1% 算削弱，連 3 季低於 16.2% 算反轉"},{"id":"H2","text":"美加基本盤守住高個位數成長，份額不被對手體系明顯侵蝕。","2y":"FY2027 美加淨銷售年增 ≥8%","5y":"FY2031 美加淨銷售年增 ≥6%","10y":null,"threshold":"美加淨銷售年增 ≥8%（第三季 9.5%），美國價值份額年減不超過 50 個基點","source":"10-Q 地區營收；8-K 附件的 Nielsen 份額表（本次資料未收錄，下次須補）","drift_rule":"TTM 年增連 2 季低於 7.6% 算削弱，連 3 季低於 7.2% 算反轉"},{"id":"H3","text":"百分比會被地區組合拖累，但營業利益金額要跟得上營收，FY2027 調整後營益率守住 28.5%。","2y":"FY2027 調整後營益率 ≥28.5%，營收與調整後營業利益增速差 ≤3 個百分點","5y":"FY2031 營益率 ≥28.5%，毛利率 ≥52.5%","10y":null,"threshold":"調整後營益率 ≥28.5%（第三季 29.2%）；增速差 ≤3 個百分點（第三季 9.6、第二季 6.9）","source":"每季財報新聞稿的調整後損益調節表","drift_rule":"TTM 調整後營益率連 2 季低於 27.1% 算削弱，連 3 季低於 25.7% 算反轉；增速差已連 2 季超過 5 個百分點，先記削弱觀察"}],"R":[{"id":"R1","text":"美國對手體系成形：Celsius 加 Alani Nu 金額份額約 20.7%，KDP 整合 C4、Bloom、GHOST，Red Bull 新口味也分走份額；美洲主管 Rob Gehring 又轉任可口可樂，接班安排法說未交代。","h_ref":"H2","clock":"🔥","threshold":"美加淨銷售年增連 2 季低於 8%（沿用前份數字，改用公司有揭露的美加總額），或連 2 季落後 Nielsen 美國品類 3 個百分點以上（第三季 2.9）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#1","end_markets#3"]},{"id":"R2","text":"毛利率與營益率往下：地區組合是結構性拖累，鋁價與 Midwest Premium、運費、代工費是成本面壓力，避險也不完整。","h_ref":"H3","clock":"⚡","threshold":"GAAP 毛利率連 2 季低於 54%（沿用前份，不因毛利走低而放寬；第三季 54.7%）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","capital_markets_pricing#3"]},{"id":"R3","text":"監管從標示走向年齡限制：英國 16 歲以下禁售預計 2027 年 4 月生效，待國會批准；印度 FSSAI 禁用能量飲料字樣，德里高等法院 10 月只給暫時救濟，案件未結。兩國營收金額事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"第三個主要市場立法限制年齡或咖啡因上限，且評估擴散機率達 50% 以上才砍倉；印度終局敗訴且當季印度營收年減則減碼","evidence_refs":["regulatory_antitrust#2"]},{"id":"R4","text":"客戶集中升高：Coca-Cola Europacific Partners 占淨銷售從 2023 年 13% 升到 2026 年第三季 17%，Coca-Cola Consolidated 約 9%，後者 2025 年 11 月遭 S&P 展望調負。","h_ref":"H1","clock":"🐢","threshold":"單一裝瓶商占淨銷售 >20%，或前兩大裝瓶商任一信評低於 BBB-","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]}],"single_thing":{"description":"FY2027 全年調整後營業利益率跌破 27.5%（第三季 29.2%）。","why_fatal":"這是最大的單一敏感度：營益率每差 1 個百分點，FY2027 EPS 差約 3.2%，國際增速少 5 個百分點只差約 2.4%。共識 1.31 美元隱含營益率約 30%，跌破 27.5% 代表 EPS 約低 6%～9%，利潤追上營收的說法失效，倍數往 28～30 倍靠，股價約 34～37 美元，跌 19%～26%。","if_happens":"未持有就不建倉，持有就減碼一半，基礎情境的營益率中樞改為 27%。","how_monitor":"每季新聞稿的調整後營業利益除以淨銷售；2027 年 8 月公布上半年後先看半年值，2028 年 2 月定案。","probability":"約 25%（未來 12～24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":34.9,"peg_fy2":2.31,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.97,"FY2026E":1.15,"FY2027E":1.31,"FY2028E":1.48},"fy_end_month":12,"eps_basis":"FY2025A 為拆股調整後 GAAP 稀釋 EPS（yfinance 年報）；FY2026E～FY2028E 為 Koyfin 11 月 7 日共識快照，GAAP 或調整後口徑事實表未標明。"},"catalysts":[{"date":"2026-12-01","date_precision":null,"type":"guidance","event":"紐約投資人日","impact":"高","watch":"長期利潤率框架、全球滲透率、冷櫃投資"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 第四季財報","impact":"高","watch":"毛利率是否低於 54%、增速差、美國份額"},{"date":"2027-03","date_precision":"month","type":"product","event":"Monster Protein 上市","impact":"低","watch":"鋪貨進度與對基本款的稀釋"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"英國 16 歲以下禁售預計生效，待國會批准","impact":"中","watch":"英國銷量與其他市場是否跟進"},{"date":"2027-05","date_precision":"month","type":"other","event":"FY2027 第一季財報，美國 11 月 1 日漲價的第一個完整季","impact":"高","watch":"銷量反應、調整後營益率"},{"date":"2028-01-01","date_precision":null,"type":"other","event":"SAP S/4HANA 上線","impact":"中","watch":"轉換期的出貨中斷與費用"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=5.97, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
