你是 DD 管線 v20 的判斷層閘（gate），標的 TPC（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1720.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000077543/000007754326000218/tpc20261104ex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：StockStory 稱共識約 1.63B（單一聚合站來源，未獨立驗證）
- `f_kpi1_income_from_construction`（q1_business）｜Income from construction operations (GAAP 營業利益)＝125.4 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（同上）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝— %｜期間與口徑：Q3 FY2026／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司未揭露 non-GAAP 營業利益；僅揭露 adjusted diluted EPS（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026）
- `f_kpi5_guidance_fy2026_adjusted`（q1_business）｜Guidance: FY2026 adjusted diluted EPS＝5.90–6.10 USD｜期間與口徑：Q3 FY2026 新聞稿（2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026 新聞稿（2026-11-04））
- `f_kpi6_backlog`（q1_business）｜Backlog＝20353.3 USD m｜期間與口徑：Q3 FY2026（2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（2026-09-30，公告於 2026-11-04））
- `f_peer_tpc_gross_margin_pct`（q2_moat）｜TPC 毛利率＝11.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpc_operating_margin_pct`（q2_moat）｜TPC 營業利益率＝5.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpc_fcf_margin_pct`（q2_moat）｜TPC FCF 利潤率＝10.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gva_operating_margin_pct`（q2_moat）｜GVA 營業利益率＝7.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GVA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gva_fcf_margin_pct`（q2_moat）｜GVA FCF 利潤率＝8.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GVA.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_strl_operating_margin_pct`（q2_moat）｜STRL 營業利益率＝18.62 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STRL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_operating_margin_pct`（q2_moat）｜PWR 營業利益率＝6.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_operating_margin_pct`（q2_moat）｜FIX 營業利益率＝16.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.38 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.07 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6481.93 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（2 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7338.17 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（4 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow_derived`（q1_business）｜Free cash flow (derived)＝291.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿：營業現金流 330.9 − capex 39.6；FCF 為自行推算，公司未報（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi4_share_based_compensation`（q1_business）｜Share-based compensation＝19.3 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-634.34 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 476.71、現金 1111.05（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝52.61 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.3 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝89.89 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.71 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 5.38，分子＝快照價 89.89｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝34.18 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 5.38 → 5.38（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝4095.2 USD m｜期間與口徑：2026-11-08／市值 4729.54 ＋ 淨負債 -634.34｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝0.63 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_w52`（q5_valuation）｜52 週均線＝78.74 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝58.97 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝31.14 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（3 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：競爭激烈，失敗可能降低市占與利潤；漸進式設計建造趨勢可能增加競爭、壓低部分案件毛利。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：單一客戶（多專案，跨 Civil/Building/Specialty）占合併營收 2025 年 14.1%、2024 年 17.6%、2023 年 16.3%；2025 年另有第二大客戶占 11.4%，兩者合計約 25.5%。
  - 來源：SEC EDGAR 10-K FY2025 Major Customers 附註（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：通膨與關稅曾使公司成本上升，且可能無法在固定價格、單價與 GMP 合約中完全回收；法規與關稅變動會影響材料或設備價格。2025 年國際營收 $489.7M（9%）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":212.5,"bear_5y_price":42.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":33.9,"ev5y_pct":33.4,"irr_base_pct":6.0,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":6.0,"pe":14.98,"basis":"FY2026E 調整後 EPS 指引中值 6.00，股價 89.89 美元；終端倍數同樣套用調整後 EPS。"},"eps":{"bull":[7.4,8.9,10.2,11.3,12.5],"base":[6.9,7.8,8.3,8.2,8.6],"bear":[6.2,5.5,4.4,3.8,4.2]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.3,"net_buyback":0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TPC_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Gary Smalley｜guidance：CEO 宣布上調 2026 年調整後 EPS 財測至 5.15–5.45 美元（原 4.90–5.30）（原話："we are raising our 2026 adjusted EPS"）
- 2026-08-05｜Gary Smalley｜guidance：管理層預期 2027 年盈餘高於 2026（原話："with even higher earnings expected in 2027, by which time"）
- 2026-08-05｜Gary Smalley｜guidance：管理層說財測內含大量不確定事項的準備金（contingency）（原話："As usual, our guidance continues to factor in a significant"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 更新 2026 有效稅率假設為 26%–29%（原話："Our effective income tax rate for 2026 is now expected to"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 維持 2026 資本支出 1.25–1.35 億美元的預期（原話："capital expenditures are still anticipated to be"）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 說下半年營運現金流不會再創紀錄（去年全年 7.5 億美元），可能是史上第二佳（原話："we're not going to set a new record."）
- 2026-08-05｜Ryan Soroka｜guidance：CFO 說 2027 年股權報酬費用預期大幅下降（原話："we expect that our share-based compensation expense will be"）
- 2026-08-05｜Ryan Soroka｜margin：Civil 部門營業利益率 15.3%，CFO 說高於 12%–15% 預期區間上緣（原話："above the top end of the 12% to 15% margin range we expect"）
- 2026-08-05｜Ryan Soroka｜margin：CFO 拆解 Civil 去年同期營業利益含 2,800 萬美元有利調整，今年營業利益 1.25 億對去年 1.40 億（原話："large favorable adjustment of $28 million."）
- 2026-08-05｜Ryan Soroka｜margin：Building 部門利益率 5.6%，接近 3%–6% 預期區間上緣（原話："upper end of the 3% to 6% margin range we expect for the"）
- 2026-08-05｜Ryan Soroka｜margin：Specialty 部門長期利益率目標 5%–8%（本季 2.2%）（原話："eventually sustaining specialty margins in the 5% to 8%"）
- 2026-08-05｜Gary Smalley｜margin：CEO 說 Civil 利益率區間的歷史演進：先前講的是 8%–12%（原話："too long ago, we were talking about 8% to 12% margin."）
- 2026-08-05｜Ryan Soroka｜margin：調整後 EPS 口徑：排除股權報酬費用（扣除相關稅務利益）（原話："Excluding the impact of share-based compensation expense,"）
- 2026-08-05｜Ryan Soroka｜margin：CFO 說上半年現金流中僅小部分來自爭議和解（原話："with only a small amount attributable to dispute"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期九大專案至少以承接時利潤率交付，並預期後期可釋放準備金增加利潤（原話："deliver those projects at least at the as-sold margins."）
- 2026-08-05｜Gary Smalley｜commitment：CEO 稱大型專案內含的利潤高於目前認列（原話："more profit, we believe, in those projects than what we're"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 說投標與承接維持紀律、不為充實積壓訂單而接案（原話："We're not going to try to book projects just because we"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 表示現金運用將保守（原話："be conservative in how we administer the cash"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期 Building 預建階段專案將於第三、四季及 2027 年轉入積壓訂單（原話："it's greater than 90% hit rate"）
- 2026-08-05｜Gary Smalley｜commitment：CEO 預期年內 Midtown 公車總站專案再獲約 10 億美元資金（原話："We still anticipate approximately $1 billion of additional"）
- 2026-08-05｜Gary Smalley｜capital_allocation：季股利由 0.06 升至 0.09 美元（+50%）（原話："increase compared to the previous $0.06 dividend."）
- 2026-08-05｜Gary Smalley｜capital_allocation：管理層預期未來再做機會性庫藏股買回（授權餘額 1.7 億美元）（原話："we expect to make additional opportunistic share buybacks"）
- 2026-08-05｜Ryan Soroka｜capital_allocation：CFO 列出現金用途順序：機會性買回、股利、再投資與保證人支持，最後是併購（原話："the last component would really be M&A"）
- 2026-08-05｜Gary Smalley｜capital_allocation：CEO 解釋保留大量現金是為取得保證人核准、單獨承接大案而不必與合資夥伴分潤（原話："We like to pursue projects without joint ventures as much"）
- 2026-08-05｜Gary Smalley｜capital_allocation：CEO 說股利與回購對公司是新事物（原話："We haven't paid a dividend in some time."）
- 2026-08-05｜Ryan Soroka｜capital_allocation：7 月再融資：以 6.625% 新票據取代 11.875% 票據，到期延至 2033（原話："annual cash interest savings of $21 million going forward."）
- 2026-08-05｜Ryan Soroka｜capital_allocation：循環信貸額度重訂，未動用額度由 1.7 億增至 3.5 億美元、到期延至 2031（原話："We also amended and restated our revolving credit facility,"）
- 2026-08-05｜Ryan Soroka｜capital_allocation：淨現金口徑：現金減總負債為 5.42 億美元（原話："We ended the quarter with cash and cash equivalents"）
- 2026-08-05｜Gary Smalley｜customer：季末積壓訂單 199 億美元，近歷史高點，較上季略增（原話："record backlog of $19.9 billion, up slightly compared to"）
- 2026-08-05｜Gary Smalley｜customer：CEO 稱潛在機會管線逾 2,000 億美元，約為數年前三倍（原話："we have a massive pipeline of more than $200 billion in"）
- 2026-08-05｜Gary Smalley｜customer：九大巨型專案合計約 160 億美元，為未來營收能見度來源（原話："backlog, which includes 9 mega projects we have won over"）
- 2026-08-05｜Gary Smalley｜customer：CEO 希望擴大 Black Construction（關島）規模，視得標率與機會而定（原話："We certainly would like to double it."）
- 2026-08-05｜Gary Smalley｜product：資料中心業務僅追求電氣面、以德州電工短缺處有餘力承接為主，並強調仍以核心業務為重（原話："electricians are short, but we have the available capacity"）
- 2026-08-05｜Gary Smalley｜competition：CEO 重申大型固定價格案競爭有限（原話："we continue to see limited competition for the larger fixed"）
- 2026-08-05｜Gary Smalley｜competition：被問到區域業者回歸時，CEO 重申先前說法並提及得標紀錄（原話："We won 9 out of 11."）
- 2026-08-05｜Gary Smalley｜risk：被問通膨風險，CEO 說非巨型案也用預購（buydown）與合約條款保護（原話："There's also contractual terms that many times protect us"）
- 2026-08-05｜Gary Smalley｜risk：CEO 強調多項專案的「剩餘舊爭議」現金流預期仍在，且收入認列採保守原則（原話："the anticipated resolution of remaining legacy disputes."）

### 問答異常語氣（迴避／改口／保留）
- TPC_Q2_2026_Earnings_Call_20260805.md｜問：Steven Fisher：區域業者似乎回歸大型案，是個案還是更廣泛趨勢？｜答法：CEO 未直接評論區域業者是否回歸，改重申『競爭有限』並談得標紀錄（9/11、此前 0/4~0/5）與管線規模
- TPC_Q2_2026_Earnings_Call_20260805.md｜問：Michael Dudas：淨現金組成、營運資金需求、保證人（surety）定位如何支持積壓訂單成長？｜答法：CFO 只答下半年現金流與資本配置順序，未給營運資金需求或保證額度的數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 1 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | none | 0 | 3 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 2 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：Tutor Perini largest customer concentration 2026 10-K
- **regulatory_antitrust**（none）：TPC Tutor Perini antitrust OR monopoly investigation 2026；Tutor Perini regulation OR regulatory scrutiny Engineering & Construction 2026；TPC Tutor Perini DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）：Tutor Perini technology disruption construction automation AI threat 2026；Tutor Perini 10-K 2025 risk factors technology innovation competitors modular construction AI；construction industry disruption modular prefabrication robotics large civil building contractors 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 衛星候選","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Adj EBITDA margin 從 5% → 8-9% 結構改善持續","columns":{"2Y 驗證":"FY26-27 Adj EBITDA margin 連 4 季 ≥ 7.5%","5Y 驗證":"FY28-30 達 mid-cycle 9-10%","10Y 驗證":"結構持平於 9-10% mid-cycle","數字門檻":"FY26 全年 ≥ 8.0%（mgmt guide mid）","來源":"mgmt FY26 guide $4.90-5.30 隱含 Adj EBITDA $470M / Rev $6.27B = 7.5%","漂移觸發條件":"連 2 季"}},{"id":"H2","text":"Backlog 持續創高 + mega-project 連續中標","columns":{"2Y 驗證":"Backlog 維持 $19B+ rolling 4Q","5Y 驗證":"Backlog $22B+ by FY30 Q4","10Y 驗證":"Civil + Building 雙引擎結構升級","數字門檻":"book-to-bill ≥ 1.0 rolling 4Q + 每年至少 2-3 個 mega-project win","來源":"Q1 26 法說：「9 mega-project win 過去 1-3 年」","漂移觸發條件":"連 2 季 book-to-bill"}},{"id":"H3","text":"Ronald Tutor 18M 退出 + 估值倍數修復（trap 🟡 → 🟢）","columns":{"2Y 驗證":"2027 Q3 前 Tutor 完成主要持股賣出 + Fwd PE 修復至 15-17x","5Y 驗證":"FY29 Fwd PE 達 18x mid-cycle","10Y 驗證":"機構持股比例升至 90%+","數字門檻":"2027 Q3 法說期間 confirmed Tutor 持股","來源":"Form 4 / 13D 公告","漂移觸發條件":"Tutor 退出進度落後（2027 Q3 仍 > 8% 持股）→ trap 🟡 持續"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Ronald Tutor 18M 計畫退出觸發機械性賣壓","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Form 4 賣出量 + 股價短期 panic","警戒閾值":"單次 > 1M 股賣出 + 股價 -15% 急跌 → 視 fundamentals 決定加碼 / 觀望"}},{"id":"R2","text":"新一輪 mega-project cost overrun + 法律 disputes（重演 2018-2023 噩夢）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"任一 mega-project cost overrun 公告 + Adj EBITDA margin 連 2 季崩","警戒閾值":"任一 cost overrun > $200M 公告 且 Adj EBITDA margin 連 2 季崩 50bp+ → 反轉，重評持倉"}},{"id":"R3","text":"聯邦 budget 不確定 / Trump admin 削減大型基建 spend","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"federal infrastructure 撥款進度 + Trump admin 行政命令","警戒閾值":"FY27 federal civil spend YoY"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":72.76,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TPC","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Tutor Perini"},"oneliner":"大型基建承包商 Tutor Perini 在手訂單 204 億美元，2026 年調整後 EPS 指引上修到 5.90–6.10，獲利能見度到 2028 年；但 Civil 利潤率處於高區，現價約 15 倍指引，基礎情境年化僅約 6%，不追價，等回檔或利潤率再獲驗證。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPC_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺公共工程業主的錢，利潤卡在 Civil 部門的大型固定價格案：Q3 部門營業利益 77% 來自 Civil，能否守住 12–15% 利潤率決定全公司獲利。","reasoning":"Q3 營收 17.2 億美元，年增 22%；營業利益 1.25 億美元，利益率 7.3%；TTM 毛利率 11.75%。分部方面，Civil 營收 8.94 億、利益率 14%，Building 5.41 億、利益率 5%，Specialty 2.86 億、利益率 3.5%。三部門營業利益合計約 1.62 億，Civil 占 77%，營收只占 52%。收錢方式是按工程進度認列與請款，九個巨型案合計 160 億美元，多數仍在早期，CEO 說 2027 年營收超過四分之三已在訂單內。產業位置判為擴張期，依據是機會管線逾 2,000 億美元、約為兩年前三倍，大型固定價格案投標者變少，與股價無關。供需持久性：週期性，能見度到 2028 年，供給端可逆，退場的對手可以回來。單點依賴不在客戶（前兩大合計 25.5%，未達警戒），而在專案類型：九大案任一出現超支，影響大於任何一個客戶流失。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_income_from_construction","f_kpi2_non_gaap_operating_incom","f_kpi5_guidance_fy2026_adjusted","f_kpi6_backlog","f_peer_tpc_gross_margin_pct","f_peer_tpc_operating_margin_pct"],"verdict_values":{"revenue_quality":"專案按完工比例認列，能見度高，品質取決於成本估計是否準確。Q3 指引上修的理由包含先前已辨識專案風險的化解，這部分不能外推。","unit_econ_note":"單位經濟看單案標價利潤與合約條款。Civil 14%、Building 5%、Specialty 3.5%，公司未揭露單案利潤率，也未揭露新案與舊案的利潤差距。","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"盈餘由巨型案承接週期與固定價格風險決定；2022–2024 連三年虧損後翻正，訂單能見度長但不是複利型生意。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉，時點不在 2028 年前。需求端多為州與地方資金，CEO 稱未受聯邦政策阻礙；供給端的對手減少可逆。來源：10-K FY2025 與 2026-11-04 法說。","bargaining":{"up":"對材料商與分包商較強：得標後買斷鋼材、混凝土並簽固定價分包，把漲價風險往上游轉；電工在部分地區短缺是弱點。","down":"對業主改善中：投標者少，合約條款較平衡；但每案重新競標，沒有轉換成本。","geo":"國際及美屬地營收占 9%，Black Construction 的印太軍事案受環評時程影響。"},"profit_pool_dir":"利潤往願意承擔大型固定價格風險的少數業者集中；五年營業利益池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與份額數據，滲透率框架也不適合逐案競標的工程業；改用管理層揭露的 2,000 億美元管線與 204 億美元訂單判斷，且管線屬管理層口徑，未經第三方驗證。"}}}},"q2_moat":{"verdict":"護城河方向向上，但等級只到中下：投標對手變少加上合約條款改善是近三年的順風，尚未經過完整循環考驗。","reasoning":"機制是大型固定價格土木案的承接能力，包含保證額度、工程管理經驗與資產負債表，再加上願意投標的對手變少。方向證據是 Civil 利潤率區間上移到 12–15%、九大案得標率大幅改善，以及淨現金讓公司可單獨投標。TPC 的 TTM 營益率 5.64% 是五家最低（GVA 7.11%、PWR 6.81%、FIX 16.66%、STRL 18.62%），優勢目前反映在新案標價，還沒反映在全公司利潤率。同業 ROIC 事實表未涵蓋，改用得標率與利潤率區間當可比軸。執行與定價都給 6 分：連七季亮眼，但前面有連三年虧損。","fact_refs":["f_peer_tpc_gross_margin_pct","f_peer_tpc_operating_margin_pct","f_peer_tpc_fcf_margin_pct","f_peer_gva_operating_margin_pct","f_peer_gva_fcf_margin_pct","f_peer_strl_operating_margin_pct","f_peer_pwr_operating_margin_pct","f_peer_fix_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"大型固定價格案的保證額度、複雜工程經驗與資產負債表，加上投標對手減少。","execution":6,"pricing":6,"grade":"C","trend":"↑","trend_evidence":"2026-11-04 法說，CEO Gary Smalley 稱新案以更高利潤率投標，Civil 區間短中期有上行壓力，九大案約 9 勝 12。10-K 也寫大型固定價格案競爭減少。此判斷只代表近三年方向，主要來源是公司自述與公司利潤率，反向訊號列在威脅。","competitor_notes":[{"name":"GVA","strategy_note":"營益率 7.11%、毛利率 16.08%，都高於 TPC；TPC 的 FCF 利潤率 10.75% 較高，但含訂單早期收款效果，不代表賺錢能力較強。"},{"name":"PWR","strategy_note":"營益率 6.81% 接近 TPC，FCF 利潤率 8.46%；業務組合事實表未涵蓋，只作利潤率參考。"},{"name":"STRL","strategy_note":"營益率 18.62%，是 TPC 的三倍多；差距太大，不作同層級估值錨。"},{"name":"FIX","strategy_note":"營益率 16.66%、FCF 利潤率 19.46%，顯示專業工程商的利潤上限遠高於 TPC 的 Specialty 3.5%，但業務差異未經事實表驗證。"},{"name":"FlatironDragados、Kiewit、Lane、OHL USA、Skanska、Walsh","strategy_note":"10-K 列為 Civil 主要對手，事實表無其財務與投標資料，對手是否回流無法量化。"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 事實表未涵蓋，只有毛利率、營益率與 FCF 利潤率。","threats":[{"level":"🟡","text":"漸進式設計建造若成為主流，投標門檻下降，部分案件毛利被壓低；10-K 已列為風險，目前沒有實際案例數字。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"高利潤吸引區域業者回流。2026-08-05 法說 Steven Fisher 提問時，CEO Gary Smalley 未正面回答；2026-11-04 法說 CEO 也說不預期再有九大案那樣的得標率。","p":35,"evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×高周轉（方向判斷，周轉率事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是民眾，決策與付款者是公共機關，政府客戶占訂單 86%；基建更新屬必要支出，CEO 稱多數資金來自州與地方。風險是時程延後，例如 Black 最大待決案仍在等環評。"},{"item":"決策層級","level":"🟡","text":"決策單位是單一專案，每案重新競標，開工後才有換手成本。代理變數是得標率：約 9 勝 12，但 CEO 自己說不預期維持。"},{"item":"價值鏈分配","level":"🟡","text":"公司能把材料風險轉給供應商與分包商，但合資夥伴也分走利潤，2026 年非控制權益預估 6,500–7,500 萬美元；單獨投標可收回一部分，代價是自己承擔全部風險。TTM 毛利率 11.75% 為五家最低。"},{"item":"社會容忍度","level":"🟡","text":"客戶用公共資金，14% 的 Civil 利潤率與過去爭議史都容易受檢視；業主轉向漸進式設計建造本身就是分攤風險、壓低承包商議價力的做法。實際定價上限受公共預算與採購制度約束。"}],"roiic":"事實表未涵蓋投入資本，無法計算。","reinvest_rate":"資本支出中值 1.30 億減折舊攤銷 0.45 億為 0.85 億美元，其中 0.75–0.85 億由業主出資；扣除後接近零，營運資金近年是現金流入，再投資率接近零或為負。ΔWC 與 NOPAT 完整數字事實表未涵蓋。","endo_ceiling":null,"formula_note":"公式在本公司失靈：成長主要由客戶進度款支應，再投資率接近零，算出來的內生成長沒有意義。實際天花板是保證額度、工程人力與得標率。"}}}},"q3_growth":{"verdict":"五年後能見度中等：現有訂單的施工峰值約在 2028 年下半，2029 年起要靠新單接力，沒有第二條成長曲線。","reasoning":"成長以量為主、利潤率為輔，沒有併購：Q3 營收年增 22%，調整後 EPS 年增 59%。訂單 203.5 億美元約為 FY1 共識營收的 3.1 倍。三年共識 EPS CAGR 無法計算，第三年共識事實表未涵蓋；FY1 到 FY2 共識增幅 12.8%，但快照未反映 11-04 上修。基礎情境以 FY2026 指引中值 6.00 為起點，FY2031 EPS 8.60，年化 7.5%，主要靠放量與利潤率，不靠倍數擴張。內生天花板因再投資率接近零而無法計算，缺口無法歸因，長期信心上限為中。資料中心僅占訂單 0.2%，CEO 明說不是重點，因此不算第二曲線。","fact_refs":["f_kpi0_revenue_gaap","f_kpi6_backlog","f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_fy2026_adjusted"],"verdict_values":{"growth":{"driver_mix":"量為主、利潤率次之，無併購，回購金額事實表未涵蓋。","runway_years":"約 5 年：訂單約 3.1 倍年營收，施工峰值約 2028 年下半，之後靠補單。","runway_post_y5":"🟡","endo_ceiling_basis":"公式不適用，改用訂單消化與保證額度判斷；管線逾 2,000 億美元為管理層口徑，保證額度數字事實表未涵蓋。","segments":[{"item":"Civil","value":"Q3 營收 8.94 億美元，年增 16%，利益率 14%，區間 12–15%；占 2026-06-30 訂單約 50%。"},{"item":"Building","value":"Q3 營收 5.41 億美元，年增 29%，利益率 5%，區間 3–6%；占訂單約 35%，另有約 7.5 億美元預建案待轉入訂單。"},{"item":"Specialty Contractors","value":"Q3 營收 2.86 億美元，年增 26%，利益率 3.5%，管理層目標 2027 年內進入 5–8%；占訂單約 15%。"}],"decay_signals":["EPS 成長遠高於營收成長：Q3 調整後 EPS 年增 59%，營收年增 22%，差距來自利潤率回升，已亮燈。","核心市占、產業倍數變化與維護性資本支出占比事實表未涵蓋，未計入。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀錄還太短：再融資明顯省息、淨現金大增，但回購價格與現金去向事實表未涵蓋，現金也未必都能分給股東。","reasoning":"FY2025 FCF 5.67 億美元、淨利 0.80 億，FCF 為淨利約 7 倍，這不是獲利品質高，而是舊爭議收款與巨型案進度款造成，後期可能回吐。Q3 SBC 占營收 1.1%，2027 年將再下降。7 月以 6.625% 票據取代 11.875% 票據，每年省息 2,100 萬美元。季股利由 0.06 升至 0.09 美元，回購授權餘額 1.7 億美元。2026-08-05 法說 CFO Ryan Soroka 把併購排在現金用途最後，CEO Gary Smalley 說保留現金是為取得保證人核准。近三年現金去向四分、債務到期結構事實表未涵蓋。","fact_refs":["f_kpi3_free_cash_flow_derived","f_kpi4_share_based_compensation","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無併購，管理層把併購列為現金用途最後一項。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購授權餘額 1.7 億美元（2026-08-05 法說），買回金額與均價事實表未涵蓋，無法比較。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"FY2025 由淨利 8,044 萬美元除以 EPS 1.51 反推約 5,330 萬股，2026 年指引 5,400 萬股，年增約 1.4%，低於 1.5%；股數為反推，誤差約 0.3 個百分點。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購，且現金去向四分與回購均價事實表未涵蓋，展開只能列片段數字。"}}}},"q5_valuation":{"verdict":"現價要求高利潤率延續到 2031 年且 2029 年後訂單補得上；我相信前半段到 2028 年，後半段還沒有數據，價格合理但不便宜。","reasoning":"現價 89.89 美元。前瞻本益比 16.71 倍用的是 5.38 的舊共識，數字仍落在 Q2 指引區間內，未反映 11-04 上修；用新指引中值 6.00 算是 15.0 倍。Trailing 34.18 倍被 Q3 債務清償損失 5,100 萬與退休金結算 3,400 萬拉高，不適合使用。同業前瞻倍數事實表未涵蓋，相對估值無法下結論。基礎情境 FY2031 EPS 8.60 乘 14 倍約 120 美元，年化約 6.4%，拆解為 EPS 複利約 +7.5%、倍數約 −1.3%、股息約 +0.4%，報酬不靠倍數擴張。機率加權五年約 +33%，上下檔比約 2.1 倍。賣方目標價都早於 Q3 財報，8 月共識 86.50 美元，各站 76–113.25 美元，高低比約 1.5 倍；現價高於 8 月共識，支持不追，但資料已舊，只算弱證據。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct","f_ev_m","f_net_debt_m","f_rev_consensus_fy1_m","f_ev_s_fwd","f_dividend_yield_ttm","f_kpi5_guidance_fy2026_adjusted"],"verdict_values":{"valuation":{"basis":"調整後 EPS 乘本益比，分母用 FY2026 指引中值 6.00，不用已過期的共識 5.38。","tier":"大型基建承包商","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，只有利潤率，無法做同層級倍數對照；終端倍數改以本公司現值 15.0–16.7 倍為參考。"},"fwd_pe":16.71,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"指引中值約 15 倍，前瞻本益比除以 FY1 到 FY2 共識增幅 12.8% 得 PEG 約 1.3，落在合理區；第三年共識缺失，所以只能用單年成長。基礎情境年化約 6.4%，低於 8%。五年分位事實表未涵蓋，只有 1–4 個年度端點。合併判為中性。","upside_short_pct":7.5,"upside_mid_pct":21.5,"denominator_disputed":true,"denominator_note":"分母有三項爭議：調整後 EPS 排除股權報酬（Q3 為 1,930 萬美元）；共識 5.38 未反映 11-04 上修；指引 6.00 建立在高區利潤率上，且上修含先前辨識風險的化解。因此不能以低本益比主張便宜。"}}},"q6_how_wrong":{"verdict":"最可能看錯兩處：把峰值利潤當常態，或反過來低估合約條款帶來的結構改善。","reasoning":"偏多的錯誤路徑是巨型案後期出現超支，重演 2022–2024 年營業利益率 −5.4%、−2.95%、−2.4%。偏空的錯誤路徑是 Civil 區間真的再上移、訂單持續補上，股價不回檔，我們錯過這段。還有兩個未解資訊：2026-08-05 法說對區域業者回歸與保證額度的問題未獲正面回答。歷史最大回撤、未結爭議金額明細事實表未涵蓋；未請款成本餘額 7.67 億美元約為市值 16%，是舊爭議結算的主要曝險。","fact_refs":["f_price_at_dd","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi6_backlog","f_peer_tpc_operating_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"峰值利潤待驗證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":6.0,"pe":14.98,"basis":"FY2026E 調整後 EPS 指引中值 6.00，股價 89.89 美元；終端倍數同樣套用調整後 EPS。"},"eps":{"bull":[7.4,8.9,10.2,11.3,12.5],"base":[6.9,7.8,8.3,8.2,8.6],"bear":[6.2,5.5,4.4,3.8,4.2]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.4,"net_buyback":0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":3},"max_dd":{"lo":-65,"hi":-40,"basis":"下緣約等於跌回 250 週線 31.14 美元（−65%）；上緣略深於跌回 104 週線 58.97 美元（−34%）。空頭情境終點約 −53%，加上 2022–2024 連續虧損史，所以範圍偏深。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"Civil 區間再上移，Specialty 進入 5–8%，2,000 億美元管線帶來持續大案，單獨投標減少合資分潤；17 倍高於現值 15.0 倍，反映市場承認結構改善。同業倍數事實表未涵蓋。","base":"2027–2028 年依訂單放量，施工峰值後成長放緩，2029 年起靠新單接力，利潤率略降；14 倍略低於現值 15.0 倍，反映工程業循環性。同業倍數事實表未涵蓋。","bear":"巨型案出現超支或新案標價回落，Civil 回到約 8–10%，EPS 跌破 2026 年水準；成長熄火且有虧損前科，倍數 10 倍。機率 30% 依據是 2022–2024 連三年虧損，而內生天花板無法驗證。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2022–2024 年連三年營業虧損；九大案多在早期，Q3 指引上修部分來自先前辨識風險的化解；10-K 也提醒固定價格合約的成本可能無法完全回收。","assumption":"合約條款改善足以防止前份所說的 2018–2023 年問題重演。","consequence":"FY2031 EPS 約 4.2 美元、10 倍，股價約 42 美元，五年約 −53%。","ruling":"採納，與唯一致命事件同一條路徑，空頭機率給 30%。","watch":"單案認列損失、Civil 利潤率、TTM 毛利率。","evidence_refs":["reg_tariff_export#0"],"fact_refs":["f_peer_tpc_gross_margin_pct","f_peer_tpc_operating_margin_pct"]},{"view":"論點失敗","evidence":"2026-08-05 法說，Steven Fisher 問區域業者是否回歸，CEO 只重申競爭有限；Michael Dudas 問營運資金與保證額度，CFO 未給數字。10-K 警告設計建造趨勢可能增加競爭。","assumption":"投標者少的狀態至少延續到 2029 年以後。","consequence":"新案標價下滑時，已簽案仍賺錢，但 2029 年後的 EPS 接不上，基礎情境失效。","ruling":"部分採納，目前沒有對手回流的數據，先列為中度威脅，不降方向。","watch":"法說得標清單、Civil 區間是否上修、公司對競爭家數的描述是否改變。","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_kpi6_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"帳上現金約 11 億美元，可用於一般公司用途只有 5.04 億；2026 年非控制權益預估 6,500–7,500 萬美元；FY2025 FCF 約為淨利 7 倍；CEO Gary Smalley 2026-08-05 說保留現金是為取得保證人核准。","assumption":"淨現金 7.07 億美元全屬股東，且未來現金流等於獲利。","consequence":"巨型案到後期進度款回吐，現金流低於獲利；單獨投標需保留更多現金，股東拿到的比損益表少。","ruling":"採納。估值用獲利不用 FCF，企業價值另看可動用現金口徑約 46 億美元，高於表列 41 億。單獨投標減少合資分潤可部分抵銷。","watch":"可動用現金、TTM 營運現金流對調整後淨利、實際回購金額。","fact_refs":["f_net_debt_m","f_ev_m","f_kpi3_free_cash_flow_derived"]},{"view":"價格已反映太多","evidence":"股價是 250 週線 31.14 美元的 2.9 倍；P/S、EV/S 都在 4 個年度端點最高；較前份 72.76 美元上漲 23.5%，大於同期指引中值上修 17.6%。","assumption":"約 15 倍指引已經算便宜。","consequence":"若市場改用常態利潤率看 EPS，不需要壞消息，股價也可能回到 70 多美元。","ruling":"部分採納。倍數由 14.3 倍升到 15.0 倍，並不離譜，但盈餘處於高區，基礎情境年化只有約 6%，所以不追。","watch":"股價對 52 週線乖離、更新後的共識 EPS。","fact_refs":["f_price_at_dd","f_ma_w250","f_ps_percentile","f_ev_s_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 72.76 → 本次 89.89（+23.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=72.76","side_b":"本次 price_at_dd=89.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 72.76 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 72.76 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 72.76 美元：Bull 價 212.5、Bear 價 42，五年期望值 +64.8%，基準年化 10.6%，不對稱比 3.79","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.79。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 72.76 美元：五年期望值 +64.8%，基準年化 10.6%，不對稱比 3.79","side_b":"本次情境、股價 89.89 美元：五年期望值 +33.4%，基準年化 6.0%，不對稱比 2.13","ruling":"再換股價、情境不動：起點價上漲 23.5%，五年期望值少 31.4 個百分點，基準年化少 4.6 個百分點，不對稱比由 3.79 降到 2.13。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"Civil 利潤率是結構還是週期","cause":"新證據","prior_field":null,"side_a":"2026-11-04 法說，CEO Gary Smalley：合約條款改善、對手減少，Civil 區間短中期有上行壓力。","side_b":"2022–2024 年營業利益率 −5.4%、−2.95%、−2.4%；10-K 警告設計建造趨勢可能增加競爭、壓低部分案件毛利。","ruling":"可調和，差別在時間。已簽案 160 億美元的利潤率可信到 2028 年；2029 年以後要看尚未簽約的案子，現在沒有數據，所以基礎情境讓 EPS 放緩，不把 14% 當常態。","evidence_level":"中：利潤率是實際數字，原因來自管理層說法。","settle_metric":"Civil 季度利益率；新案標價利潤未揭露，以區間是否上修代替。","if_then":["若 2027 年財報正式上修 Civil 區間且連兩季 ≥14%，上調基礎情境並分批建立首倉。","反向：若 Civil 連兩季低於 12%，減碼一半並停止加碼。"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"帳上淨現金有多少屬於股東","cause":"新證據","prior_field":null,"side_a":"2026-11-04 法說，CFO Ryan Soroka：現金超過總債務 7.07 億美元，財務彈性大。","side_b":"同場揭露可用於一般公司用途的現金 5.04 億美元，扣總債務 4.04 億後僅約 1 億；其餘的限制內容公司未拆解。","ruling":"採可動用口徑。企業價值看約 46 億美元而非 41 億，EV 對 FY1 營收 0.71 倍而非 0.63 倍，不因淨現金給溢價。","evidence_level":"高：兩個數字都是公司揭露。","settle_metric":"可動用現金與總債務。","if_then":["若可動用現金連兩季高於 7 億美元且回購啟動，加回淨現金價值並上調基礎情境目標價。","反向：若可動用現金跌破 3 億美元，停止加碼。"],"evidence_refs":[]},{"axis":"管理層前後說法","cause":"新證據","prior_field":null,"side_a":"2026-08-05 法說：CFO Ryan Soroka 說今年營運現金流不會破紀錄；CEO Gary Smalley 說九大案 9 勝 11、Civil 舊區間 8–12%，預建案第三、四季及 2027 年轉入訂單。","side_b":"2026-11-04 法說：前九月營運現金流 6.65 億美元，Q4 超過約 0.85 億就破去年 7.5 億；CEO 改說約 9 勝 12、舊區間 8–10%，約 7.5 億美元預建案時程講到 12–18 個月。","ruling":"現金流與指引屬保守後超標，可信度加分；得標率與舊區間的出入小，不影響結論，但 CEO 口頭數字不宜當精確引用；預建案時程略為後延，記錄不扣分。","evidence_level":"高：兩場法說原話。","settle_metric":"2026 全年營運現金流；預建案實際轉入訂單時點。","if_then":["若全年營運現金流超過 7.5 億美元，維持管理層指引偏保守的判斷，情境不變。","反向：若 7.5 億美元預建案到 2028 年第一季仍未轉入訂單，停止加碼。"],"evidence_refs":[]},{"axis":"共識修正 0% 與指引上修","cause":"新證據","prior_field":null,"side_a":"Koyfin 11-07 快照：FY2026 EPS 5.38、FY2027 EPS 6.07，近三個月修正 0%。","side_b":"11-04 指引中值 6.00，比 5.38 高 11.5%；管理層另說 2027 年盈餘雙位數成長。","ruling":"0% 應視為資料延遲，不是共識停滯的證據，但延遲本身是推論。FY2027 的 6.07 只比 2026 指引高 1.2%，與管理層說法不符，情境路徑不用它當錨。","evidence_level":"中：數字是原始資料，延遲原因未經查證。","settle_metric":"下一次共識快照。","if_then":["若更新後 FY2027 共識仍低於 6.60 美元，停止加碼。","若更新後 FY2027 共識超過 7.40 美元而股價先漲，仍不追。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"約 13 倍 FY2027 基礎 EPS，連七季亮眼，指引今年上修兩次，共識尚未更新；2027 年營收超過四分之三已在訂單內。","side_b":"EPS 處於高區，施工峰值就在 2028 年下半，五年基礎報酬年化約 6%，下檔約 −53%；等回檔的代價低於追高後遇到超支的代價。","ruling":"不追。唯一約束是價格相對尚未驗證的利潤率持續期，論點本身沒有破。","evidence_level":"中：短期數字扎實，2029 年後沒有數據。","settle_metric":"股價與 Civil 利潤率；2027-02 指引。","if_then":["若 2027-02 財報的 FY2027 EPS 指引下緣 ≥7.40 美元且 Civil 區間上修，取消 78 美元限制，重跑研究後分批建立首倉。","若股價續漲而利潤率未再獲驗證，不追。","若股價下跌但 Civil 仍 ≥12%，分批反買。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭軸：10-K 與 2026-11-04 法說都說大型固定價格案投標者減少；但 10-K 同時警告設計建造趨勢可能增加競爭，區域業者回流的提問也未獲正面回答。","side_b":"結構軸：機會管線逾 2,000 億美元，資金多來自州與地方。其他軸：關稅與通膨靠買斷與分包轉嫁，尚未見吸收失敗。","ruling":"結構性轉好中：需求與投標家數同向，競爭軸有反向提問但沒有數據。ABC 指資料中心榮景掩蓋整體疲弱，TPC 資料中心訂單僅 0.2%，不受益也較少受其回落影響。","evidence_level":"中：多為公司與 10-K 自述。","settle_metric":"得標率、Civil 區間、TTM 毛利率。","if_then":["若公司揭露大型案競爭家數增加且得標率明顯下滑，改判雙向拉鋸並停止加碼。"],"evidence_refs":["competitive_share_entrants#1","reg_tariff_export#0"]},{"axis":"前份空白欄位首次判定","cause":"方法變動","prior_field":["archetype","cycle_position","moat_trend","runway_post_y5","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位未填，沒有可比較的舊值。","side_b":"本次首次判定：循環型、中循環、護城河向上、五年後能見度中等，空頭機率 30%，最大回撤 −40% 到 −65%。","ruling":"這些差異來自框架補欄，不代表基本面轉向。","evidence_level":"高：前份確實為空值。","settle_metric":"下一份研究逐欄比較。","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉中性","cause":"方法變動","prior_field":["val"],"side_a":"前份：72.76 美元，當時指引中值 5.10，約 14.3 倍，結論偏便宜。","side_b":"本次：89.89 美元，指引中值 6.00，約 15.0 倍，結論中性。","ruling":"倍數只升 0.7 倍，主因不是價格。本次把盈餘分母列為爭點，並加入 2029–2031 年放緩路徑，便宜的說法不再成立。","evidence_level":"中：倍數是實算，分母爭議是判斷。","settle_metric":"Civil 利潤率與更新後共識。","if_then":["若股價回到 78 美元以下且 Civil ≥12%，重跑研究後分批建立首倉。"],"evidence_refs":[]},{"axis":"綜合等級與陷阱評估未變，理由更新","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：綜合等級 B，獲利陷阱評為中度，風險集中在舊爭議與持股賣壓。","side_b":"本次：等級與中度評估不變；舊爭議壓力下降（未請款成本餘額 7.67 億美元，為 2014 年底以來最低），風險轉為高區利潤率能否持續。","ruling":"等級不動，但主要風險由過去的爛帳轉為未來的峰值。創辦人持股資料本包未涵蓋，維持資料缺口。","evidence_level":"中：財務數字扎實，持股資料缺失。","settle_metric":"未請款成本餘額、Civil 利潤率。","if_then":["若未請款成本餘額降至 6 億美元以下且無結算損失，陷阱評估可下修。","反向：若單季舊爭議結算損失 ≥5,000 萬美元，減碼一半。"],"evidence_refs":[]},{"axis":"Single Thing 由未設定改為巨型案超支","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點，原文為空。","side_b":"九大巨型案任一出現重大成本超支，單案累計認列損失達 2 億美元以上。","ruling":"採用此事件。Civil 利潤率是模型最大敏感度，每 100 個基點約影響年 EPS 0.48 美元；前份 R2 的同類風險因此升為唯一致命點。","evidence_level":"中：敏感度為推算。","settle_metric":"10-Q 專案調整揭露。","if_then":["若事件發生，清倉。"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設退出指標；最接近的是 R2：任一 cost overrun > $200M 公告 且 Adj EBITDA margin 連 2 季崩 50bp+ → 反轉，重評持倉。","side_b":"單案累計損失 ≥2 億美元清倉；≥1 億美元或 Civil 連兩季低於 12% 減碼一半。","ruling":"2 億美元門檻沿用，但取消兩條件同時成立的要求，因為超支通常分季認列，等兩季會坐滿損失。Adj EBITDA 本包未提供，改用公司每季揭露的 Civil 利潤率。","evidence_level":"中：門檻為判斷。","settle_metric":"單案損失與 Civil 季度利益率。","if_then":["觸發 1 億美元或 Civil 條件時減碼一半；觸發 2 億美元時清倉。"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設定，原文為空。","side_b":"股價≤78美元（約52週線、13倍FY2026指引中值）且最新一季 Civil 利潤率≥12%，重跑研究後才建首倉。","ruling":"以價格為主要條件，因為目前的約束是價格相對尚未驗證的利潤率持續期；Civil 條件用來確認回檔不是論點破裂。","evidence_level":"中：價位由指引與 52 週線推得。","settle_metric":"股價與最新季 Civil 利潤率。","if_then":["條件成立時重跑研究並分批建立首倉；股價跌破但 Civil 低於 12%，不買。"],"evidence_refs":[]},{"axis":"假設與風險門檻調整","cause":"方法變動","prior_field":null,"side_a":"前份 H1：FY26 全年 Adj EBITDA margin ≥ 8.0%；H3 與 R1：Tutor 18 個月退出，單次 > 1M 股賣出且股價急跌 15%。","side_b":"本次 H1 改看 Civil 與 Specialty 分部利潤率；持股賣壓保留為風險，指標與門檻不變，標資料缺口。","ruling":"Adj EBITDA 本包未提供，公司每季揭露分部利潤率，較可追蹤。持股現況本包完全未涵蓋，不得視為風險解除，保留 Form 4 監測。前份 H2 的 190 億與 220 億美元門檻沿用。","evidence_level":"中：持股部分為資料缺口。","settle_metric":"Form 4 申報；分部利潤率。","if_then":["若單次賣出超過 100 萬股且股價急跌 15%，基本面未破時分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Civil 利潤率守住已簽案標價水準","type":"假設驗證","maps_to":"H1","metric":"Civil 部門季度營業利益率","threshold":"≥12%（最新季 14%）","action":"達標續抱；未達標轉入減碼條件","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":2,"text":"訂單持續補上","type":"假設驗證","maps_to":"H2","metric":"在手訂單與滾動四季訂單出貨比","threshold":"訂單 ≥190 億美元且出貨比 ≥1.0","action":"達標續抱；未達標停止加碼","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":3,"text":"現金流以營運為主","type":"假設驗證","maps_to":"H3","metric":"TTM 營運現金流對調整後淨利；可動用現金","threshold":"營運現金流 ≥調整後淨利；可動用現金 ≥5 億美元","action":"未達標停止加碼","source_freq":"公司季報，每季","date":"2027-02 起每季"},{"n":4,"text":"九大巨型案任一重大超支","type":"Single Thing","maps_to":"Single Thing","metric":"單案累計認列損失","threshold":"≥2 億美元","action":"清倉","source_freq":"10-Q 專案調整揭露，每季","date":"每季財報日","evidence_refs":["reg_tariff_export#0"]},{"n":5,"text":"對手回流或設計建造壓低標價","type":"風險","maps_to":"R2","metric":"Civil 區間、得標清單、競爭家數描述","threshold":"公司下修 Civil 區間，或連續四季未得 10 億美元以上新案","action":"停止加碼","source_freq":"法說會，每季","date":"每季財報日","evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"價格回到可承接區","type":"估值rearm","maps_to":"H1","metric":"股價與最新季 Civil 利潤率","threshold":"股價 ≤78 美元且 Civil ≥12%","action":"重跑研究後分批建立首倉","source_freq":"每日股價、每季財報","date":null},{"n":7,"text":"利潤率結構改善獲得驗證","type":"加碼","maps_to":"H1","metric":"Civil 區間與 FY2027 指引","threshold":"Civil 區間上修且 FY2027 EPS 指引下緣 ≥7.40 美元","action":"重跑研究後分批加碼","source_freq":"公司財報","date":"2027-02"},{"n":8,"text":"利潤率或單案損失轉壞","type":"減碼","maps_to":"R1","metric":"Civil 季度利益率；單案累計損失；TTM 毛利率","threshold":"Civil 連兩季 <12%，或單案損失 ≥1 億美元，或 TTM 毛利率 <10%","action":"減碼一半","source_freq":"公司季報，每季","date":"每季財報日","evidence_refs":["reg_tariff_export#0"]},{"n":9,"text":"客戶集中轉為實際損失","type":"風險","maps_to":"R3","metric":"最大客戶營收占比與相關專案取消","threshold":"單一客戶占比 >25%，或前兩大客戶的專案遭取消、延付","action":"減碼一半","source_freq":"10-K，每年；重大事件即時","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":10,"text":"Q4 財報與 2027 指引後複審","type":"複審日期","maps_to":"H1","metric":"2027 指引、Civil 區間、更新後共識","threshold":"財報發布","action":"重跑情境樹並更新等待價位","source_freq":"公司財報","date":"2027-02"}],"kill_metrics":[{"metric":"Civil 部門季度營業利益率","bear_threshold":"連續兩季低於 12%：減碼一半","window":"連續 2 季","source":"公司季報與法說會","last_status":"ok"},{"metric":"九大巨型案單案累計認列損失","bear_threshold":"≥1 億美元減碼一半；≥2 億美元清倉","window":"任一季","source":"10-Q 專案調整揭露","last_status":"ok"},{"metric":"在手訂單與滾動四季訂單出貨比","bear_threshold":"訂單低於 190 億美元且出貨比低於 1.0","window":"滾動 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"TTM 營運現金流對調整後淨利","bear_threshold":"連續四季低於 1.0 倍","window":"連續 4 季","source":"公司季報","last_status":"ok"},{"metric":"創辦人 Form 4 賣出量與股價反應","bear_threshold":"單次超過 100 萬股且股價急跌 15%","window":"單一事件","source":"SEC Form 4，本包未涵蓋，資料缺口","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤78美元（約52週線、13倍FY2026指引中值）且最新一季 Civil 利潤率≥12%，重跑研究後才建首倉","exec_line":"現價不追。跌到 78 美元以下且論點未破時分批建首倉；股價續漲但 Civil 區間未上修，繼續不追；股價下跌而 Civil 仍 ≥12%，分批反買，不當停損。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 78 美元以下（約 52 週線、FY2026 指引中值 13 倍）且 Civil 利潤率仍 ≥12%；若 2027-02 財報上修 Civil 區間，重算等待價位。"},"thesis":{"H":[{"id":"H1","text":"已簽巨型案按標價利潤率交付，Civil 維持 12–15% 區間，Specialty 於 2027 年進入 5–8%。","2y":"FY2027–FY2028 Civil 年度利益率 ≥13%，Specialty 2027 年內 ≥5%","5y":"FY2031 Civil 利益率仍 ≥11%，調整後 EPS 約 8.6 美元","10y":null,"threshold":"季度 Civil ≥12%；Specialty 於 2027 年底前 ≥5%","source":"公司季報與法說會分部數字","drift_rule":"Civil 低於 12% 連兩季為削弱，連三季且低於 10.8% 為反轉；Specialty 到 2027 年底仍低於 5%，舊案拖累的說法視為不成立。"},{"id":"H2","text":"在手訂單補得上，巨型案持續得標且不犧牲標價。","2y":"在手訂單維持 190 億美元以上，滾動四季訂單出貨比 ≥1.0","5y":"FY2030 Q4 在手訂單 ≥220 億美元","10y":"Civil 與 Building 雙引擎持續，不依賴單一專案週期","threshold":"滾動四季訂單出貨比 ≥1.0；每年至少 2 個 10 億美元以上新案","source":"公司季報新聞稿與法說會得標清單","drift_rule":"滾動四季訂單出貨比連兩季低於 1.0 為削弱，連三季為反轉。"},{"id":"H3","text":"現金流以營運為主，不靠爭議和解；可動用現金累積後開始回饋股東。","2y":"2026–2027 年營運現金流高於調整後淨利，可動用現金 ≥5 億美元","5y":"五年累計 FCF 至少三成透過股利與回購回到股東","10y":null,"threshold":"可動用現金 ≥5 億美元；TTM 營運現金流 ≥調整後淨利","source":"公司季報與法說會現金口徑","drift_rule":"TTM 營運現金流連四季低於調整後淨利為削弱，連六季且偏離 ≥10% 為反轉。"}],"R":[{"id":"R1","text":"固定價格巨型案成本超支，或通膨與關稅無法回收。","h_ref":"H1","clock":"🔥","threshold":"單案累計損失 ≥1 億美元，或 TTM 毛利率跌破 10%（最新 11.75%）","evidence_refs":["reg_tariff_export#0"]},{"id":"R2","text":"高利潤吸引對手回流，或漸進式設計建造壓低標價。","h_ref":"H2","clock":"🐢","threshold":"公司下修 Civil 區間，或連續四季未得 10 億美元以上新案","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"前兩大客戶 2025 年合計占營收 25.5%，專案取消或延付會同時影響多個部門。","h_ref":"H2","clock":"🔥","threshold":"單一客戶占比 >25%，或前兩大客戶專案遭取消、延付","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"舊爭議結算低於帳面，未請款成本餘額 7.67 億美元約為市值 16%。","h_ref":"H3","clock":"🔥","threshold":"單季舊爭議結算損失 ≥5,000 萬美元","evidence_refs":[]},{"id":"R5","text":"創辦人 Ronald Tutor 持股賣壓，沿用前份指標；本包未涵蓋持股現況，屬資料缺口。","h_ref":"H3","clock":"⚡","threshold":"Form 4 單次賣出超過 100 萬股且股價急跌 15%","evidence_refs":[]},{"id":"R6","text":"聯邦預算或環評拖慢印太與基建案。CEO 稱多數資金來自州與地方，2027 年展望未計新聯邦資金。","h_ref":"H2","clock":"🐢","threshold":"Black 待決三案約 10 億美元到 2027 年中仍未決標；前份聯邦支出年增門檻在摘要中不完整，資料缺口","evidence_refs":[]}],"single_thing":{"description":"九大巨型案任一出現重大成本超支，單案累計認列損失達 2 億美元以上。","why_fatal":"Civil 占部門營業利益 77%。2 億美元損失稅後約每股 2.7 美元，約為基礎情境 FY2027 EPS 的四成；市場也可能重新用虧損年代的眼光定價，倍數由 15 倍往 10 倍靠近。Civil 利潤率每掉 100 個基點，年 EPS 約少 0.48 美元，是模型最大的單一敏感度。","if_happens":"清倉，不等下一季解釋，因為超支通常分季認列。","how_monitor":"每季 10-Q 的專案調整揭露、法說會對九大案進度的描述、Civil 利潤率與未請款成本餘額變化。","probability":"12–24 個月約 15%。固定價格案過去確實出過事，案子越到後期越看得出超支；條款改善與材料買斷壓低機率。此機率為判斷，無統計基礎。"}},"appendix_a":{"growth_durability":6,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.81,"peg_fy2":1.15,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.51,"FY2026E":5.38,"FY2027E":6.07,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2026E、FY2027E 為 Koyfin 調整後 EPS 共識，未反映 2026-11-04 指引上修（5.90–6.10）。FY2028E 共識事實表未涵蓋，留空。FY2025A 1.51 為 GAAP 稀釋 EPS，調整後口徑事實表未涵蓋，與共識口徑不同，不可用來算 CAGR。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"大部分負債型股權獎酬年底歸屬，2027 年股權報酬費用將大幅下降","impact":"低","watch":"GAAP 與調整後 EPS 差距是否縮小"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 2027 年指引，可能正式上修 Civil 利潤率區間","impact":"高","watch":"FY2027 調整後 EPS 指引、Civil 區間、全年營運現金流是否破 7.5 億美元"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"Black Construction 印太三案約 10 億美元決標，最大案待環評完成，時點為估計","impact":"中","watch":"決標時點與是否得標"},{"date":null,"date_precision":null,"type":"macro","event":"新聯邦運輸法案進度，管理層 2027 年展望未計入","impact":"中","watch":"法案是否通過與撥款規模，時程事實表未涵蓋"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=8.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：regulatory_antitrust（法規／反壟斷）、substitute_technology（替代技術）（尾部風險或事件型，不擋）。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
