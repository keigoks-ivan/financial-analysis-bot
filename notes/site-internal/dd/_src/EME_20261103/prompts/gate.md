你是 DD 管線 v20 的判斷層閘（gate），標的 EME（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（40 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝5540 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1) https://www.sec.gov/Archives/edgar/data/0000105634/000010563426000132/eme-ex991_2026930xq3.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝10.5 % (營業利益 $579.8m)｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1)；排除 $34.0m 美國建築服務無形資產減損（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝9.8 % (營業利益 $545.8m)｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1)（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_kpi3_diluted_eps_non_gaap`（q1_business）｜Diluted EPS (non-GAAP)＝9.6 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1)（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_kpi6_full_year_2026_guidance_`（q1_business）｜Full-year 2026 guidance（10-29 上調）＝營收 $20.6–21.0B；non-GAAP 營業利益率約 10%；non-GAAP EPS $34.50–35.50 range｜期間與口徑：Q3 FY2026（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1)（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（公告於 2026-10-29））
  - 註記：共識 FY1 EPS 34.29（2026-10-31 快照，來源：dd_numbers_extra.py consensus_revision）；yfinance FY1 營收共識 $20,703m
- `f_kpi7_remaining_performance_ob`（q1_business）｜Remaining performance obligations (RPO)＝18570 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：EMCOR Q3 2026 press release (8-K Ex.99.1)（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_peer_eme_gross_margin_pct`（q2_moat）｜EME 毛利率＝19.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_operating_margin_pct`（q2_moat）｜EME 營業利益率＝9.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_fcf_margin_pct`（q2_moat）｜EME FCF 利潤率＝7.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_operating_margin_pct`（q2_moat）｜FIX 營業利益率＝16.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_fcf_margin_pct`（q2_moat）｜FIX FCF 利潤率＝19.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_strl_operating_margin_pct`（q2_moat）｜STRL 營業利益率＝18.62 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STRL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_operating_margin_pct`（q2_moat）｜PWR 營業利益率＝6.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mtz_operating_margin_pct`（q2_moat）｜MTZ 營業利益率＝4.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTZ.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝34.29 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝39.1 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝45.02 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝20702.87 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝23328.76 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_free_cash_flow_q3`（q1_business）｜Free cash flow (Q3 單季，推算)＝759.6 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：推算：9M 營運現金流 $1,086.6m − 上半年 $289.9m = $796.7m；9M capex $97.0m − 上半年 $59.9m = $37.1m（Q3 與 Q2 8-K Ex.99.1；非公司直接申報）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未取得
- `f_kpi5_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝0.8 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：推算：9M SBC $19.7m − H1 $15.0m = Q3 約 $4.7m，÷ non-GAAP 營業利益 $579.8m（Q3 與 Q2 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-208.24 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 566.51、現金 774.75（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝43.78 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.231 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝692.67 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.2 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 34.29，分子＝快照價 692.67｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝20.03 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝61.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝61.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.53 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝84.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝84.3 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.52 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝85.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝85.7 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-23.82 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝16.83 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 29.35 → 34.29（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝42.78｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 686.88 / W52 748.63 / W104 631.66 / W250 388.18 / W250 13週斜率 2.37%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝748.63 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝631.66 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝388.18 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝2.37 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 自述：產業高度分散，進入障礙低，任何具足夠財力與技術的組織都可能成為競爭者；部分對手管理費用較低、報價較低，競標壓力可能壓低價格與利潤率。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-26）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出收購競爭：其他潛在收購方可能資源更多或條件更優，可能限制 EME 的併購機會。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-26）｜affects：thesis.R
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：CSIMarket：同業 Comfort Systems 2026 Q2 營收成長 50.26%，市占上升。
  - 來源：CSIMarket FIX Competitors（as_of 2026-08-01）｜affects：moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：EMCOR 10-K 風險因素揭露：可能面臨現有或潛在客戶自有 in-house 服務組織的競爭（尤其 building services），不確定客戶未來會否繼續外包。屬一般性風險，未指名最大客戶導入第二供應商。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：thesis.R、moat_trend
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2024 年曾因特定客戶破產提列 $11.0M 準備，影響美國建築服務部門利潤率 30bp。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 風險因子：EMCOR 暴露於銅、鋼等原物料價格與保護主義貿易措施；依賴第三方供應商供料；部分合約無法調價，關稅變動可能損及獲利與流動性
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：EMCOR 倚賴第三方供應商取得材料與設備，曾遇供應鏈延遲、部分材料設備交期長、材料與燃料價格上升；關稅可能使客戶減少使用其服務
  - 來源：EMCOR FY2025 Form 10-K（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St 社群敘事（投資人意見，非公司揭露）主張預製／模組化營建在業界擴大，可能降低現場安裝與維護的長期需求；同敘事亦指 EME 持續擴大預製、VDC、BIM 能力。
  - 來源：Simply Wall St community narrative: rising automation and tightening regulations will erode margins (EME)（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：產業趨勢文章稱模組化營建是短中期最具顛覆潛力的趨勢（可將最多 80% 現場工作移入工廠）；Autodesk 頁面指電力基礎建設規模將推動營建團隊走向預製與更佳協調。屬顧問／廠商部落格，數字未追溯至一手資料。
  - 來源：Bancolombia 營建創新趨勢；Autodesk 2026 Construction Trends（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：模組化營建被視為最具顛覆潛力的趨勢，可將最多 80% 現場工作移入工廠
  - 來源：Bancolombia 營建創新趨勢（as_of 2026-04-30）｜affects：moat_trend
- `major_events#1`（major_events｜方向 -｜狀態 ok）：PEMEX Deer Park 煉油廠 2024-10-10 化學外洩，子公司 Repcon 與 EIS 被列為多起訴訟被告，公司預期保險涵蓋大部分或全部賠付。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 附註（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：PEMEX Deer Park 外洩案：Repcon 與 EIS 被列為多起合併訴訟（MDL）被告，公司預期保險涵蓋。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 附註（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1430.0,"bear_5y_price":462.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":42.9,"ev5y_pct":35.9,"irr_base_pct":7.4,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":34.29,"pe":20.2,"basis":"FY2026共識EPS（Koyfin 2026-10-31，調整後口徑）；終端倍數同樣套在當年度EPS，分母年期一致"},"eps":{"bull":[41.5,48.5,54.0,59.5,65.0],"base":[39.1,44.5,48.0,51.5,55.0],"bear":[37.0,34.0,30.0,31.5,33.0]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.231,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### EME_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CEO｜guidance：CEO 公布上修後的 2026 全年營收與 EPS 財測區間（原話："revenue of between $20 billion and $20.5 billion"）
- 2026-07-30｜CFO｜guidance：財測假設五家併購下半年貢獻 2.5–2.75 億美元營收（原話："$250 million and $275 million of revenue contribution"）
- 2026-07-30｜CFO｜guidance：CFO 說明財測低／中／高端對應的下半年利潤率隱含，且不含 10.6% 重現（原話："the back half of this year looks like the first half"）
- 2026-07-30｜CFO｜guidance：CFO 表示財測中並未假設 Q2 的 10.6% 利潤率重複（原話："not baked into our guidance is that the 10.6% margin repeat"）
- 2026-07-30｜CFO｜guidance：CFO 解釋上修利潤率的理由：營收加速帶來間接成本吸收與 SG&A 槓桿（原話："this is really going to be a revenue story for us"）
- 2026-07-30｜CEO｜guidance：CEO 指出中東情勢使下半年煉油廠停工檢修減少，預期影響第四季利潤率（原話："that's a small impact on margins but it's likely to"）
- 2026-07-30｜CFO｜guidance：CFO 稱併購的 EPS 影響在今年餘下時間有限，因無形資產攤銷與淨利息收入減少（原話："the impact to diluted earnings per share will be limited"）
- 2026-07-30｜CEO｜margin：Q2 營收、營業利益與營業利益率數字（原話："Operating income reached $547 million"）
- 2026-07-30｜CFO｜margin：CFO 拆解 Electrical 利潤率擴張來源：主要是毛利率而非 SG&A（原話："the vast majority of the increase in operating margin"）
- 2026-07-30｜CFO｜margin：CFO 解釋 Mechanical 利潤率下滑 110bp 來自專案組合（CM／prime、GMP／cost-plus 比重上升）（原話："an increase in the number of GMP or cost-plus contracts"）
- 2026-07-30｜CEO｜margin：CEO 稱利潤率以區間管理，Electrical 目前位於區間中點（原話："We always talk about margins in bands"）
- 2026-07-30｜CEO｜margin：CEO 量化合約組合轉向 GMP 的幅度，並指出轉變來自 AI 資料中心（原話："It probably shifted to mechanical 9% to 10%"）
- 2026-07-30｜CEO｜margin：CEO 說明 Q2 有季節性因素（Building Services 強、Industrial 較強）不利後續利潤率（原話："The second quarter is always a strong building"）
- 2026-07-30｜CFO｜margin：Building Services 利潤率擴張 130bp，拆為毛利率 +70bp、SG&A −60bp（site-based 重組）（原話："SG&A margin decreased by 60 basis points"）
- 2026-07-30｜CFO｜margin：CFO 稱 Mechanical 利潤率壓力與 Q1 所述一致，且不代表經營哲學改變（原話："I don't think it's an"）
- 2026-07-30｜CEO｜customer：RPO 創高 171.4 億美元，年增 44%，95% 為有機（原話："total RPOs reached a record $17.14 billion, an increase of"）
- 2026-07-30｜CFO｜customer：Electrical 營收成長主要來自資料中心（網通 sector 營收成長 45%）（原話："where revenues increased by 45%"）
- 2026-07-30｜CEO｜customer：被問及資料中心需求輪廓是否有變，CEO 直接回答沒有（原話："Short answer, none. The demand profile remains the same."）
- 2026-07-30｜CFO｜customer：CFO 列出資料中心 RPO 以維吉尼亞州最多，德州第二、喬治亞緊隨（原話："Texas is the second for us and followed closely by Georgia"）
- 2026-07-30｜CEO｜customer：CEO 描述資料中心規模放大與 AI 專案的乘數（原話："we get a multiplier of 1.5 to 2 on AI data center"）
- 2026-07-30｜CFO｜customer：半導體領域 RPO 年初至今與季增均約 7%，CFO 預期稍後出現成長（原話："RPOs are up in that space about 7%"）
- 2026-07-30｜CFO｜customer：CFO 說明年初需另行簽約並完成的營收比例已大幅下降（本年約 40%）（原話："I think this year, it was 40% of the"）
- 2026-07-30｜CFO｜customer：CFO 稱 RPO 12 個月內轉化比例由歷史約 85% 降至 75–76%，原因含水務組合與簽約量（原話："it's more like 75% or 76%"）
- 2026-07-30｜CFO｜customer：CFO 說明 RPO 成長快於營收財測，部分為動員時點（原話："Some of that is just the timing of mobilization"）
- 2026-07-30｜CEO｜competition：被問與透過併購進入市場的競爭者比較，CEO 稱各工種專業壁壘高、不會因做場地工程而獲得機電標案（原話："These trades are very"）
- 2026-07-30｜CEO｜competition：CEO 說明併購篩選標準未變：先看現場執行力（原話："can they execute in the field"）
- 2026-07-30｜CEO｜competition：CEO 稱機電綑綁投標很少見（原話："very rarely combine a bid"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明五家併購的 TTM 營收與 EBITDA（原話："collectively generated $625 million of revenues and $105"）
- 2026-07-30｜CFO｜capital_allocation：CFO 說明併購以現金及必要時信貸額度支應（原話："a combination of cash on hand and to the extent"）
- 2026-07-30｜CFO｜capital_allocation：CFO 披露其中兩筆交易最高 9,000 萬美元的 earn-out（原話："up to $90 million in earnouts for 2 of the deals"）
- 2026-07-30｜CFO｜capital_allocation：CFO 表示 2026 資本配置比例將與 2025 相近，M&A 占比上升（原話："as the percentage deployed towards M&A increases"）
- 2026-07-30｜CEO｜capital_allocation：CEO 稱併購管線強，聚焦機電工程與機械服務，不投資不熟悉領域（原話："The pipeline is strong."）
- 2026-07-30｜CEO｜capital_allocation：CEO 對單一市場、客戶或地理的公司持謹慎態度（原話："But we want to pay a fair price."）
- 2026-07-30｜CFO｜capital_allocation：CFO 描述現金流經驗法則（營運現金流至少等於淨利，約為營業利益 80–85%）並預期 2026 與前兩年相似（原話："We see no reason why the operating cash flow in '26"）
- 2026-07-30｜CFO｜commitment：CFO 預期併購的 EPS 貢獻在攤銷退場後逐步增加（原話："these acquisitions will provide further"）
- 2026-07-30｜CEO｜commitment：CEO 預告 Schmidt 與 Connelly 於第三季完成交割（原話："we look forward to closing"）
- 2026-07-30｜CFO｜commitment：CFO 對 2027 不予評論（原話："we won't comment on '27 at this point"）
- 2026-07-30｜CEO｜product：CEO 稱被併購公司可轉向資料中心，並會派員協助現場、前端估價與合約談判（原話："do we implant a couple of our folks"）
- 2026-07-30｜CEO｜product：Mechanical 資料中心可大量預製，減少鄉村市場現場人力（原話："you can have a large"）
- 2026-07-30｜CEO｜risk：CEO 提及宏觀風險（地緣衝突、商品成本、設備交期）（原話："geopolitical conflicts, commodity"）
- 2026-07-30｜CEO｜risk：CEO 談資料中心禁令與州級提案，稱屬局部且業主會找到建置地點（原話："It's sort of laughable that New York put a data center ban"）
- 2026-07-30｜CEO｜risk：CEO 說明勞動力調度方式，含在偏遠市場可能使用非工會營運（原話："there are opportunities for some nonunion operations"）

### 問答異常語氣（迴避／改口／保留）
- EME_Q2_2026_Earnings_Call_20260730.md｜問：UBS 問 Electrical 高利潤率是否有特殊因素，以及下半年是否可能維持 10% 以上｜答法：CEO 否認「everything went right」、改談 ebb and flow 與區間；CFO 不直接答可否維持 10%+，改以財測低／中／高端的隱含說法，並明言 10.6% 不在財測內
- EME_Q2_2026_Earnings_Call_20260730.md｜問：Cantor 問 2027 現金轉換率展望｜答法：CFO 明確拒絕給 2027 評論，改述 2026 的經驗法則與前兩年相似
- EME_Q2_2026_Earnings_Call_20260730.md｜問：Baird 問在 Mechanical 拖累與攤銷下為何仍上修利潤率財測｜答法：CFO 以營收加速帶來的吸收與 SG&A 槓桿回答，未給出攤銷或 Mechanical 拖累的量化數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 3 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：EMCOR Group business model shift 2026 prefabrication OR modular OR service strategy；EMCOR Group go-to-market change 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"觀望","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 資料中心 capex 結構性 5-10 年週期，EME 是 M&E 落地核心","columns":{"2Y 驗證點":"Hyperscaler 四家加總 2027 capex guidance ≥ 0B（即 vs 2026 0B 持平或上升）；EME RPO 2027 末 ≥ B","5Y 驗證點":"2031 全美 data center 容量達 100+ GW（vs 2025 50 GW）；EME data center 相關 revenue / total ≥ 35%","10Y 驗證點":"2036 AI 工作負載成熟，data center 從 hyperscale build-out 轉 maintenance + retrofit；EME building services 佔比擴大至 30%","驗證指標":"RPO 絕對額、data center exposure %、hyperscaler capex guidance","資料來源":"2Y: §6 RPO + §11；5Y: §8.A Runway；10Y: §8.A 路線圖 + §9 護城河趨勢"}},{"id":"H2","text":"勞工結構性短缺 + EMCOR 規模優勢轉化為持續定價權","columns":{"2Y 驗證點":"FY26-27 Gross margin 維持 18%+；OPM 維持 8%+","5Y 驗證點":"2031 GM 維持 17-19%，OPM 7-9%（cycle 平均上移）","10Y 驗證點":"2036 union labor 短缺問題尚未解決（美國技術職業教育投入仍跟不上需求）","驗證指標":"Gross Margin、OPM、員工數成長 vs 營收成長","資料來源":"§9 護城河、§10 財務、§11 議價權"}},{"id":"H3","text":"市場給予 EME 中等 PE 溢價（vs FIX 折價 ~40%），thesis 兌現後溢價收斂","columns":{"2Y 驗證點":"FY27 Forward PE 維持 22-28x（即不大幅 derate 至 &lt; 18x）；分析師上修 EPS 至 FY27 .50+","5Y 驗證點":"2031 EPS 達 .00+，PE 即使壓回 20x 仍給 .00 股價（+10% 5Y CAGR）","10Y 驗證點":"10Y EPS .00+，PE 18-22x，股價區間 ,300-1,600（年化 +6% CAGR）","驗證指標":"Forward PE、PEG、分析師目標價中位、FY+2 EPS 共識","資料來源":"§13.1 / §13.5 / §6 共識追蹤"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Hyperscaler capex cycle peak — 任一家 (AWS/MSFT/GOOG/META) 大幅下修 2027 capex","columns":{"對應假設":"H1","時間尺度":"短期（12 月內）⚡","監測指標":"四家加總 2027 capex guidance；EME RPO QoQ 動能","警戒閾值":"四家加總 2027 capex guidance &lt; 0B（即 vs 2026 0B 下修 8%+）；或 EME RPO 連續 2 季 QoQ 轉負且絕對額下降 — 削弱閾值"}},{"id":"R2","text":"Margin cycle peak — FY25 OPM 8.7% 為 10 年新高，回歸 cycle 均值 ~6%","columns":{"對應假設":"H2","時間尺度":"中期（2-3 年）🔥","監測指標":"Gross Margin / OPM 趨勢；勞工通膨 vs 議價權","警戒閾值":"Gross margin 連 2 季 YoY 下滑 &gt; 1.5pp；或 OPM FY27 跌破 7% — 削弱閾值；FY27 OPM &lt; 6% — 反轉閾值（H2 thesis 部分失效）"}},{"id":"R3","text":"整合失敗 — Miller Electric M 收購若 integration charge 或 culture clash","columns":{"對應假設":"H1 / H2","時間尺度":"短期（12 月內）⚡","監測指標":"Miller Electric segment 貢獻；無預期 integration cost","警戒閾值":"FY26-27 Miller Electric segment 公布 impairment 或 segment EBITDA 低於 acquisition deck 50%；或管理層淡化「accretive」承諾 — 削弱閾值"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":913.11,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"EME","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"EMCOR Group, Inc."},"oneliner":"EME：資料中心在手訂單翻倍，2027年的營收有訂單撐住；但利潤率四年翻倍，2028年後需求節奏是最大未知。股價半年跌24%，現約18倍明年盈餘，價格合理但不便宜，等620美元以下或更強的2027年財測再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/EME_20261103/scenario.json","answers":{"q1_business":{"verdict":"EME賺的是美國非住宅業主的機電施工與維護錢，七成營收來自電氣與機械營建，錢卡在現場技工調度與工地執行。資料中心約占營收三分之一、在手訂單近半，是目前的利潤引擎。","reasoning":"營收結構：FY2025營建占72%、建築服務21%、工業服務7%，97%在美國（10-K）。2026年第三季分部（法說會逐字稿）：電氣營建18.5億美元，年增44.3%，營益率13.3%；機械營建25.5億美元，年增43.1%，營益率12.1%；建築服務8.524億美元，年增4.7%，營益率7.8%；工業服務2.875億美元，與去年持平，營業利益510萬美元。全公司營收55.4億美元，毛利率20%，非GAAP營業利益率10.5%；GAAP為9.8%，差額是3,400萬美元無形資產減損。錢卡在現場執行：設備與材料各家都買得到，誰能按時把電力、冷卻與消防裝好，誰就拿到下一案。資料中心年初至今約占營收三分之一，在手訂單87.4億美元，約占總RPO 47%。這部分分散在多家客戶，管理層稱不依賴一兩家，客戶以大型雲端業者為主，少做新興雲。單點依賴：沒有揭露占營收超過一成的單一客戶，集中度風險落在終端產業（資料中心），不在單一客戶。FY2025小於1,000萬美元的專案約占電機營建營收42%。產業時鐘判為擴張期，依據是RPO年增47%、快於營收的28.8%，財測三度上調，非資料中心市場的RPO多數也是兩位數成長，目前尚未見到價格戰或大量取消。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_diluted_eps_non_gaap","f_kpi6_full_year_2026_guidance_","f_kpi7_remaining_performance_ob","f_peer_eme_gross_margin_pct"],"verdict_values":{"revenue_quality":"專案制但可見度高：RPO 185.7億美元，約為2026年營收指引中點的0.89倍；RPO只計已簽約、不可取消的部分，取消極少；建築服務多為長約維護，屬經常性收入。","unit_econ_note":"第三季毛利率20%，營業費用率9.5%。大型案需要的專案經理較少，GMP合約又能把部分管理費列入工地一般條件，所以營業費用率下降。管理層以區間管理利潤率：電氣12–13%，機械12–12.5%。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"輕資產，營運資金由客戶預收支應，淨現金；營收跟著非住宅營建週期走，營業利益率四年由5.1%升到約10%，有複利特徵也帶循環性。"},"industry":{"clock_phase":"II","sd_verdict_source":"屬週期性需求，2027年前持久：RPO年增47%，12個月內轉成營收的比例由約85%降到75–76%，代表工期拉長；電工缺口預估2027年見頂，北美資料中心專案普遍延誤，供給受限撐住訂價。但需求集中在雲端與AI資本支出，2028年後反轉機率上升（來源：公司8-K、第二與第三季法說、IIR、AIA、JLL）。","bargaining":{"up":"上游是工會技工與設備材料商：銅、鋼與長交期設備受關稅與延誤影響，部分固定價合約無法轉嫁；燃油成本約五到七成可轉嫁給客戶。","down":"下游大型雲端業者議價力強，指定GMP與成本加成合約，壓低材料與分包加成；但想合作的業主多於EME能服務的量，EME可以挑案。","geo":"97%營收在美國；英國建築服務已於2025-12-01出售。"},"profit_pool_dir":"利潤池往資料中心機電移動。AI資料中心的冷卻需求擴大了機械範疇，第二季法說稱AI資料中心的機電金額是一般雲端的1.5–2倍；EME與FIX是主要受益者。","tam_table":[{"item":"資料中心RPO（2026Q3）","value":"87.4億美元，年增逾一倍、季增13%，約占總RPO 47%"},{"item":"資料中心營收占比（2026年初至今）","value":"約三分之一，分散在多家客戶（第三季法說）"},{"item":"資料中心支出預測","value":"AIA共識2026年+26.3%、2027年+16.5%"},{"item":"雲端與AI組合","value":"約65–70%雲端、30% AI，管理層預期未來趨近各半"},{"item":"TAM絕對值、滲透率、五年利潤池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河B級，方向持平。優勢在規模化的現場技工調度與執行紀錄，讓EME能挑客戶；弱點是競標制、進入門檻低，而最強同業的利潤率與成長都更高。","reasoning":"機制：電氣與機械營建多數靠競標，但邀標以經驗、技術與財務實力為門檻。EME靠領班與技工規模、預製與虛擬設計施工能力，讓大型雲端客戶回頭找它；管理層稱想合作的資料中心業主多於能服務的量，所以可以挑案。執行力給8分：電氣段營益率13.3%，年增200bp，主要來自毛利率；建築服務7.8%創高；全年非GAAP營業利益率約10%，高於年初財測9.0–9.4%。定價力給6分：機械段因統包與GMP、成本加成合約比重上升，營益率降80bp，管理層改追利潤金額；燃油成本約五到七成可轉嫁。同業對照：EME營業利益率9.88%，高於PWR與MTZ，但低於FIX的16.66%與STRL的18.62%；自由現金流率7.47%也遠低於FIX。對最強機電同業FIX的利差為負，所以方向不標上升。產業態勢分三面看：競爭面，FIX擴張較快，10-K也自承進入門檻低，屬轉差；結構面，資料中心與電工缺口撐住需求到2027年，屬轉好；其他面，有地方暫停令與銅鋼關稅。綜合裁決是雙向拉鋸。報酬結構：營業利益率偏低、周轉高（營運資金由客戶預收支應，資本支出低於營收1%），屬低利益率×高周轉。投入資本含大量商譽，事實表未涵蓋，當期ROIC無法精算。","fact_refs":["f_peer_eme_gross_margin_pct","f_peer_eme_operating_margin_pct","f_peer_eme_fcf_margin_pct","f_peer_fix_operating_margin_pct","f_peer_fix_fcf_margin_pct","f_peer_strl_operating_margin_pct","f_peer_pwr_operating_margin_pct","f_peer_mtz_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"領班與技工規模、預製與虛擬設計施工能力，加上過往執行紀錄形成的投標資格門檻，讓大型雲端客戶回頭指定，EME得以挑案。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"電氣營益率年增200bp、建築服務增50bp，但機械段因統包與GMP比重上升減80bp；管理層自稱以區間管理利潤率（電氣12–13%、機械12–12.5%）。同業FIX的利潤率與成長都更高，沒有EME份額擴大的直接證據，所以不標上升；也沒有份額流失的證據，所以不標下降。","competitor_notes":[{"name":"FIX","strategy_note":"最直接的機電對手，利潤率與自由現金流率明顯高於EME，還做整棟模組化，資料中心份額擴張較快，是EME最嚴格的比較基準。"},{"name":"PWR","strategy_note":"以電網與輸配電為主，在資料中心供電上與EME有交集但工種不同，利潤率低於EME。"},{"name":"MTZ","strategy_note":"以管線與通訊基建為主，利潤率最低，與EME機電業務的直接競爭有限。"},{"name":"STRL","strategy_note":"以場地整備為主的資料中心承包商，利潤率高於EME；EME第二季法說稱做場地工程拿不到機電標案，兩者多為上下游關係。"}],"peer_na_reason":"同業ROIC與本益比事實表未涵蓋，只能以營業利益率與自由現金流率對照。","threats":[{"level":"🟡","text":"FIX以整棟模組與更高利潤率擴張資料中心份額，屬點對點競爭。","p":"50%","evidence_refs":["competitive_share_entrants#4"]},{"level":"🟡","text":"多數業務進入門檻低，有財力與技術的組織都能競標，部分對手管理費較低、報價較低，可能壓低標價。","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"客戶自建建築服務團隊，減少外包。","p":"15%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"預製與模組化把現場工作移入工廠，長期可能削弱現場技工優勢；EME自己也在擴建預製能力。","p":"25%","evidence_refs":["substitute_technology#1","substitute_technology#2","substitute_technology#3"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（資料中心營運商、醫院、學校、水務）、決策者（業主與總包）與付款者（業主）三者一致。這些是需要而非想要，延後建置代價高。醫療RPO年增31%、水務38%、教育機構25%，需求不只來自資料中心。要分清急迫性與持久性：資料中心這一塊仍依賴雲端與AI資本支出。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一專案層級：多數營收來自競標，邀標雖以經驗、技術與財務實力為門檻，但客戶在下一個專案可以換承包商，換手成本只在專案進行中才高。管理層稱想合作的資料中心業主多於能服務的量，目前EME握有挑案權。"},{"item":"價值鏈分配","level":"🟡","text":"資料中心價值鏈最稀缺的是電力設備、晶片與土地電力取得，機電安裝拿到的是施工加成。大型雲端客戶指定GMP合約，壓低材料與分包加成，EME改追利潤金額而非利潤率；長期需求存在，不代表這一環節能多分。"},{"item":"社會容忍度","level":"🟡","text":"EME自身收費沒有碰到社會容忍上限，但下游需求受地方授權約束：勞登郡暫停新案、紐約州暫停令、德州州長暫停新核准，選舉期間也有大型資料中心暫停令的提案，屬政策風險。"}],"roiic":28.5,"reinvest_rate":53,"endo_ceiling":15.1,"formula_note":"內生成長上界＝增量報酬率約28.5%×再投資率約53%≈15.1%。再投資率：2026年至9月底收購近8億美元，資本支出低於營收1%，營運資金由客戶預收支應、視為零，對比全年淨利約15億美元（FY1共識EPS×現有股數）。增量報酬率：2025到2026年淨利增量約2.3億美元，除以收購投入約8億美元。收購本身：第二季法說揭露五家併購TTM EBITDA 1.05億美元，對比約8億美元價款，稅前約13%（兩者口徑未必一致）。這家公司有機成長幾乎不耗資本，公式會低估有機成長潛力。投入資本與折舊攤銷事實表未涵蓋，數字為推估、信心低。"}}}},"q3_growth":{"verdict":"成長跑道中等。2027年有創新高的在手訂單撐住；之後要看資料中心以外的市場能否接手，五年後的空間屬中段。","reasoning":"成長拆解：第三季有機成長25.5%、總成長28.8%，收購約補3.3個百分點；競標制下價格貢獻有限；一年內股數約降3%。三年共識EPS：FY2026E 34.29美元、FY2027E 39.10美元、FY2028E 45.02美元。以FY2025 GAAP稀釋EPS 28.19美元為基期，年化約16.9%；基期是GAAP、共識是調整後口徑，數字略有高估。內生上界約15.1%（見護城河段），缺口約1.8個百分點，來源是2026年非GAAP營業利益率由FY2025的9.23%升到約10%，加上淨回購；不依賴估值重評。跑道：管理層的長期框架是全公司營收成長比非住宅營建多約600bp、營建段多700–900bp。AIA預測資料中心支出2026年+26.3%、2027年+16.5%，IIR預估電工缺口2027年見頂。第二季法說稱RPO在12個月內轉成營收的比例由約85%降到75–76%，代表工期拉長，可見度延伸到2028年。滲透率與TAM絕對值事實表未涵蓋，跑道暫估五到七年。五年後：資料中心建置會逐步轉向維護與改建，由建築服務承接，但建築服務目前只成長4.7%，第二條成長曲線還沒成形，所以給中等。十類衰退信號亮1個（EPS成長遠高於營收），價值陷阱與長期成長性都屬中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi7_remaining_performance_ob","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_full_year_2026_guidance_"],"verdict_values":{"growth":{"driver_mix":"以量為主（有機成長25.5%）；收購約補3個百分點；回購每年讓股數縮減約1–3%；競標制下價格貢獻有限。","runway_years":"約5–7年（依管理層「營收成長高於非住宅營建約600bp」的框架推估；滲透率數據事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"引自護城河段：內生上界約15.1%。三年共識EPS年化約16.9%，缺口約1.8個百分點，來自2026年利潤率由9.23%升到約10%與淨回購，非依賴估值重評。","segments":[{"item":"電氣營建（2026Q3，法說逐字稿）","value":"營收18.5億美元、年增44.3%、營益率13.3%；資料中心營收年增68%"},{"item":"機械營建（2026Q3）","value":"營收25.5億美元、年增43.1%、營益率12.1%；資料中心營收年增近130%"},{"item":"建築服務（2026Q3）","value":"營收8.524億美元、年增4.7%、營益率7.8%"},{"item":"工業服務（2026Q3）","value":"營收2.875億美元、與去年持平、營業利益510萬美元；年初至今營收+10.4%"}],"decay_signals":[{"signal":"毛利率連2季年減","status":"未亮","evidence":"第三季毛利率20%，年增60bp"},{"signal":"核心市占近12個月縮減","status":"未亮","evidence":"FIX第二季營收年增約50%、擴張較快，但EME營建段年增逾40%，沒有直接份額下滑證據"},{"signal":"提價後銷量下滑","status":"未亮","evidence":"競標制，未見此現象"},{"signal":"EPS年化成長高於營收逾5個百分點","status":"亮","evidence":"FY2022到FY2025稀釋EPS由8.10升到28.19美元，年化約51.5%；營收年化約15.3%；主因營業利益率由5.1%升到9.23%"},{"signal":"自由現金流／淨利連2年低於0.75","status":"未亮","evidence":"FY2024約1.32、FY2025約0.93"},{"signal":"SBC／營收大於5%且逐年上升","status":"未亮","evidence":"SBC約占非GAAP營業利益0.8%"},{"signal":"TAM萎縮或被替代技術壓縮","status":"未亮","evidence":"模組化替代的證據來自部落格與投資人敘事，未見一手數據"},{"signal":"產業估值倍數近3年系統性下移","status":"未亮","evidence":"本益比位於年度端點61.8分位，未見下移"},{"signal":"維持性資本支出占自由現金流超過60%","status":"未亮","evidence":"資本支出低於營收1%"},{"signal":"停止投資新產能且營收3年內下滑","status":"未亮","evidence":"未來兩季將新增預製廠"}],"trap_rating":"🟡（衰退信號亮1個：盈餘成長多來自利潤率擴張）"}}},"q4_capital":{"verdict":"資本配置中等：現金轉換穩、股權稀釋極低、回購持續；但今年收購金額放大，實際報酬還沒經過驗證，本季又剛有一筆舊收購提列減損。","reasoning":"自由現金流／淨利：FY2022約1.10、FY2023約1.30、FY2024約1.32、FY2025約0.93。2026年營運現金流指引15–17億美元，淨利約15億美元，維持在一倍上下。第三季單季自由現金流7.596億美元。淨現金約2.08億美元。SBC約占非GAAP營業利益0.8%，股權稀釋可忽略。現金去向（2026年至9月底）：收購近8億美元，回購加股利5.1億美元，資本支出低於營收1%；10月另新增5億美元回購授權。營運槓桿：第三季營收年增28.8%、非GAAP營業利益年增43%，沒有利潤率壓縮。疑慮在收購：兩筆交易附最高9,000萬美元的業績對賭款；2027年收購相關攤銷約1.28億美元；本季對一筆能源效率業務的舊收購減損3,400萬美元；10-K也提到收購標的有其他買家競價。債務到期結構、加權利率與回購均價，事實表未涵蓋。","fact_refs":["f_kpi4_free_cash_flow_q3","f_kpi5_sbc_non_gaap","f_net_debt_m","f_shares_diluted_m","f_peer_eme_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"2026年至9月底收購近8億美元；第二季法說揭露五家併購TTM營收6.25億美元、EBITDA 1.05億美元，對比約8億美元價款，稅前約13%。收購後的實際報酬還沒有一年資料，本季又對一筆舊收購（能源效率業務）提列3,400萬美元減損；加權資金成本事實表未涵蓋，暫不判定。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋。以現價盈餘殖利率約4.95%（FY1 EPS 34.29÷692.67）計，十年期公債殖利率要低於2.95%才過關；公債殖利率事實表未涵蓋，保守判為不過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC約占非GAAP營業利益0.8%（第三季推算），年化約2,600萬美元，不到市值0.1%；股數由FY2025稀釋約45.15百萬股降到43.78百萬股（兩者口徑不同，方向供參）。"}]},"governance":{"capital_returns":[{"item":"2026年至9月底收購","value":"近8億美元（第三季法說）"},{"item":"同期回購加股利","value":"5.1億美元"},{"item":"新增回購授權","value":"5億美元（2026-10-29）"},{"item":"資本支出","value":"營收1%以下（管理層）"},{"item":"業績對賭款","value":"兩筆交易最高9,000萬美元（第二季法說）"},{"item":"債務到期結構與加權利率","value":"事實表未涵蓋"}]}}},"q5_valuation":{"verdict":"現價約20倍今年盈餘、18倍明年盈餘，等於假設資料中心建置在2027年後平緩交棒、利潤率守在區間。我大致相信，但基準情境五年年化報酬不到8%，價格合理而非便宜。","reasoning":"現價692.67美元，等於FY1共識34.29美元的20.2倍、FY2共識39.10美元的17.7倍。要讓這個價格划算，必須相信兩件事：2027–2028年EPS大致照共識兌現；之後成長降到高個位數時，本益比不跌破18倍。前一件有創高RPO支撐，我相信；後一件取決於資料中心消化期何時來。PEG：20.2÷16.9≈1.2。正常化檢查：若營業利益率回到FY2023的約7%，以2026年營收指引中點208億美元、淨利約為營業利益81%計，EPS約27美元，本益比約26倍。也就是說，現價並沒有替利潤率高點打折。短期上檔：FY2027共識×20倍≈782美元，+12.9%；中期：基準情境五年價格約990美元，+42.9%。賣方7–8月平均目標價930–1,044美元，早於近期下跌，各站樣本與日期不一，不採用。估值依賴：基準情境倍數由20.2倍降到18倍，報酬全部來自EPS成長，不屬於估值依賴型。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY1共識34.29美元）搭配PEG，以自身歷史年度端點對照；同業本益比事實表未涵蓋。","tier":"機電專業承包商","peers":{"expanded":false,"reason":"事實表只有同業毛利率、營業利益率與自由現金流率，沒有同業本益比或EV/EBITDA，無法建立倍數對照；終端倍數改以自身年度端點與成長熄火情境推估。"},"fwd_pe":20.2,"peg":1.2,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Forward P/E 20.2倍；以三年共識EPS年化16.9%計，PEG約1.2，落在1到2的合理區。本益比在四個年度端點中位於61.8分位（不是五年連續分位，五年高低點事實表未涵蓋，所以五年分位留空）。股價營收比與EV/S都在八成以上分位，反映利潤率已翻倍；若利潤率回到7%，正常化本益比約26倍，所以不給便宜。","upside_short_pct":12.9,"upside_mid_pct":42.9,"denominator_disputed":false,"denominator_note":"分母的主要爭點在2028年以後，不在今年：2026年EPS已有三季實績與上調的財測支撐，第三季的3,400萬美元減損也已在調整後EPS中排除。利潤率高點的風險改用正常化檢查與悲觀情境處理。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是資料中心建置節奏：如果雲端業者2027年起進入消化期，在手訂單燒完後，營收與利潤率會同時回落。其次是把利潤率高點當成常態。","reasoning":"最大回撤：悲觀情境谷底EPS約30美元×12–14倍，對現價跌39%–48%；消化期初期市場常先殺倍數，區間取−35%至−52%。這波26週已跌23.8%；股價686.88美元，低於52週均線748.63美元、高於104週均線631.66美元，均線排列成立但長期斜率平緩。空方最強的數字：FY2022–2025 EPS年化51.5%，營收只有15.3%，盈餘成長多來自利潤率翻倍。訴訟：2024年PEMEX Deer Park煉油廠外洩，子公司Repcon與EIS是多起合併訴訟的被告，公司預期保險涵蓋大部分或全部賠付；金額與時程事實表未涵蓋。上一季法說有三處迴避，對照本季：一是UBS問10%以上利潤率能否維持，財務長稱不在財測內，本季交出10.5%，已兌現；二是2027年現金轉換率拒答，本季仍不談2027年，只重申營運現金流介於淨利與營業利益的80–85%之間；三是收購攤銷未量化，本季給出2027年約1.28億美元。管理層談地方暫停令的口吻偏輕，認為選後會自然消退；本報告不採信，改用每季資料中心RPO來驗證。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"盈餘成長多來自利潤率擴張，需求集中在資料中心"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":34.29,"pe":20.2,"basis":"FY2026共識EPS（Koyfin 2026-10-31，調整後口徑）；終端倍數同樣套在當年度EPS，分母年期一致"},"eps":{"bull":[41.5,48.5,54.0,59.5,65.0],"base":[39.1,44.5,48.0,51.5,55.0],"bear":[37.0,34.0,30.0,31.5,33.0]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.23,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-52,"hi":-35,"basis":"悲觀情境谷底在2029年：EPS約30美元×12–14倍＝360–420美元，對現價跌39%–48%；消化期初期市場常先殺倍數、再等盈餘落底，所以下緣放寬到−52%；上緣−35%對應谷底EPS約30美元、倍數15倍。對照：這波26週已跌23.8%。","trigger_time":null},"basis":{"bull":"雲端與AI資料中心建置延續到2029年，機械冷卻範疇擴大，營收年增約12%，非GAAP營業利益率守在10.5%；終端22倍，前提是2031年成長仍有兩位數。","base":"2027–2028年貼近共識（39.1、44.5美元），之後資料中心放緩、其他非住宅市場接手，EPS年增約7%，利潤率約10%；終端18倍，低於現價的20.2倍，反映成長降速。回購效果已含在每股盈餘路徑內，淨回購殖利率不重複計入。","bear":"2028年起資料中心進入消化期，營收下滑一成以上，利潤率回到FY2023約7%的水準；EPS由2027年37美元降到2029年約30美元後緩步回升。終端14倍，介於成長熄火情境中成長降至5%（約13倍）與降至10%（約16倍）之間。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"資料中心RPO 87.4億美元，約占總RPO 47%；機械段資料中心營收年增約130%。勞登郡暫停新案、紐約州暫停令、德州州長暫停新核准；JLL稱57%北美資料中心專案延誤三個月以上。2024年曾因單一客戶破產提列1,100萬美元準備。","assumption":"雲端業者資本支出延續到2028年以後，地方暫停令只是拉長週期。","consequence":"若2028年進入消化期，營收下滑一成以上、利潤率回到7%，EPS跌到約30美元，本益比壓到12–14倍，股價較現價跌四到五成；景氣反轉時客戶信用風險也會同步上升。","ruling":"部分採納：2027年前有訂單保護，風險落在2028年以後，悲觀機率給30%。管理層稱目前在建專案多不受政治雜音影響，屬未證說法，不據此下修悲觀機率。","watch":"每季資料中心RPO與季增率；雲端業者每年1–2月公布的資本支出指引。","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","customer_concentration_credit#2"],"fact_refs":["f_kpi7_remaining_performance_ob"]},{"view":"論點成功但股東經濟變差","evidence":"10-K指出其他收購方可能資源更多、條件更好；銅鋼關稅與供應延誤可能落在無法調價的合約；機械段因統包與GMP合約，利潤率年減80bp；2027年收購相關攤銷約1.28億美元；本季一筆舊收購減損3,400萬美元。","assumption":"資料中心需求延續，但EME用收購補產能、用低加成合約換量。","consequence":"營收照共識成長，但每股盈餘成長落後營收，增量報酬率由約28.5%下滑，自由現金流率停在7%上下。","ruling":"部分採納：基準情境假設利潤率不再擴張，終端倍數下修到18倍；收購改以累計減損、以及收購支出對自由現金流的比率作為門檻。","watch":"收購支出／自由現金流、攤銷與減損金額、機械段利潤率能否守在12–12.5%。","evidence_refs":["competitive_share_entrants#2","reg_tariff_export#0","geo_supply_chain#0"]},{"view":"價格已反映太多","evidence":"股價營收比1.53倍、EV/S 1.52倍，分別位於年度端點的84.3與85.7分位；利潤率較FY2022翻倍，若回到7%，正常化本益比約26倍。","assumption":"市場用高點的利潤率給倍數。","consequence":"即使營收照預期成長，利潤率一旦回歸，EPS與倍數會同時被壓低。","ruling":"部分採納：股價半年跌23.8%後，Forward P/E 20.2倍、FY2027約17.7倍，已不算貴；但以正常化盈餘看仍偏高，所以不給便宜，等620美元以下。","watch":"股價與FY2027共識本益比；非GAAP營業利益率是否守在區間。","fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"FIX第二季營收年增約50%、市占上升；10-K自承多數業務進入門檻低，對手報價可能更低；客戶可能自建建築服務團隊；顧問與廠商文章稱模組化可把最多80%的現場工作移入工廠。","assumption":"現場技工與執行紀錄仍是拿下大型案的關鍵。","consequence":"若整棟模組化成為主流，價值移到工廠端廠商，EME的現場優勢縮小，份額與定價雙降。","ruling":"大致反駁：替代技術的證據多來自部落格與投資人敘事，數字沒有追溯到一手資料；EME自己也在擴建預製廠，並替雲端客戶做管線模組。FIX的份額擴張屬點對點競爭，列入觀察，不扣分。","watch":"EME營建段有機成長與FIX營收成長的差距；預製廠對外接單情況。","evidence_refs":["substitute_technology#1","substitute_technology#2","substitute_technology#3","competitive_share_entrants#4","customer_second_source#0"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 913.11 → 本次 692.67（-24.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=913.11","side_b":"本次 price_at_dd=692.67","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 913.11 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 913.11 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 913.11 美元：Bull 價 1,430、Bear 價 462，五年期望值 +3.1%，基準年化 1.6%，不對稱比 0.95","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.95。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 913.11 美元：五年期望值 +3.1%，基準年化 1.6%，不對稱比 0.95","side_b":"本次情境、股價 692.67 美元：五年期望值 +35.9%，基準年化 7.4%，不對稱比 2.66","ruling":"再換股價、情境不動：起點價下跌 24.1%，五年期望值多 32.8 個百分點，基準年化多 5.8 個百分點，不對稱比由 0.95 升到 2.66。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論與總評漂移","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-05-18）股價913.11美元，估值判為偏貴，總評B。","side_b":"本次股價692.67美元，FY1共識上修到34.29美元後，Forward P/E約20倍、PEG約1.2，估值改判合理；總評仍為B，因為基準情境五年年化報酬不到8%。","ruling":"估值由偏貴降為合理，主因是股價下跌24%，其次是共識EPS三個月上修16.8%。總評不升，因為價格改善還不足以讓基準報酬跨過10%。","evidence_level":"高（股價與共識皆為事實表數據）","settle_metric":"股價與FY2027共識EPS","if_then":["若股價≤620美元且資料中心RPO未季減，則重跑研究後分批建首倉","若股價反彈到780美元以上而FY2027共識沒有再上修，則不追"]},{"axis":"補做完整檢查後新增或改判的欄位","cause":"方法變動","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份價值陷阱判為低風險；護城河方向、五年後跑道、公司類型、循環位置、裁決角色、情境機率與最大回撤都沒有記錄。","side_b":"本次逐項檢查十類衰退信號：FY2022–2025 EPS年化51.5%，遠高於營收的15.3%，亮一燈，陷阱風險改為中等。護城河方向持平，五年後跑道中等，類型為品質複利型兼循環性，位於中循環；情境機率樂觀25%、基準45%、悲觀30%，最大回撤區間−35%至−52%。","ruling":"差異來自本次補做完整檢查，不是基本面轉差：利潤率帶動盈餘成長這件事在前份就已存在，只是當時沒有計入。","evidence_level":"中","settle_metric":"非GAAP營業利益率近四季走勢","if_then":["若近四季非GAAP營業利益率跌破9%，則陷阱風險升為高，停止任何加碼","若2027年營收成長仍比非住宅營建高6個百分點以上、利潤率守在10%左右，則陷阱風險降回低"]},{"axis":"重新進場條件由無到有","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設定重新進場條件（空值）。","side_b":"股價≤620美元（基準情境五年年化報酬達10%）時建首倉；若2027年EPS財測中點≥42美元，價位上移到670美元。","ruling":"前份觀望沒有點名約束條件。本次綁定的約束是價格：基準情境五年年化報酬要達10%才建首倉，條件是這個約束的否定。","evidence_level":"中","settle_metric":"股價、2027年EPS財測中點","if_then":["若價格先到620美元而資料中心RPO同時季減，則不建首倉，先等下一季數據","若財測中點≥42美元且股價≤670美元，則重跑研究後分三批建首倉"]},{"axis":"減碼與清倉門檻由無到有","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定退出門檻（空值）。","side_b":"資料中心RPO連兩季季減或跌破70億美元→減碼一半；非GAAP營業利益率近四季低於9%→停止加碼；總RPO年增率轉負且資料中心RPO跌破60億美元→清倉。","ruling":"前份的風險門檻掛在雲端業者資本支出加總上；本次改用公司每季揭露的資料中心RPO，資料頻率更高，也直接對應營收。","evidence_level":"高","settle_metric":"資料中心RPO、總RPO年增率","if_then":["若資料中心RPO連兩季季減，則減碼一半","若總RPO年增率轉負且資料中心RPO低於60億美元，則清倉"]},{"axis":"Single Thing由無到有","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設定 Single Thing（空值）。","side_b":"Single Thing：主要雲端業者集體把資料中心建置轉入消化期，EME資料中心在手訂單首次出現連續季減。","ruling":"本季資料中心RPO約占總RPO 47%、年初至今營收約三分之一，機械段資料中心營收年增約130%，成為數學上最大的單一敏感項，所以設為 Single Thing。","evidence_level":"高","settle_metric":"每季資料中心RPO","if_then":["若資料中心RPO連兩季季減，則不建倉，已持有就減碼一半","若2027年上半年資料中心RPO續創新高，則悲觀機率可降到25%"]},{"axis":"論點與風險門檻改寫","cause":"新證據","prior_field":["H","R"],"side_a":"前份風險二：FY27營業利益率跌破7%為削弱、跌破6%為反轉（前份記載FY25營業利益率8.7%）；風險三：Miller Electric收購出現減損，或EBITDA低於收購簡報的50%。","side_b":"本次風險二：非GAAP營業利益率近四季低於9%即停止加碼；風險三：收購累計減損超過1億美元，或收購支出連兩年高於自由現金流，即減碼三分之一。","ruling":"事實表年度口徑FY2025營業利益率是9.23%，2026年已到約10%，管理層也公布了電氣12–13%、機械12–12.5%的區間，7%門檻太鬆。2026年收購近8億美元並出現首筆3,400萬美元減損，收購檢查改看整體投入，不再只盯單一案。","evidence_level":"高","settle_metric":"非GAAP營業利益率、收購減損與收購支出","if_then":["若近四季非GAAP營業利益率低於9%，則停止加碼","若收購累計減損超過1億美元，則減碼三分之一"]},{"axis":"股價走勢與盈餘上修方向相反","cause":null,"prior_field":null,"side_a":"股價26週下跌23.8%，跌破52週均線。","side_b":"同期FY1共識EPS三個月上修16.8%，財測三度上調，RPO年增47%。","ruling":"可調和，是時間尺度不同。市場折價的是2028年後資料中心消化期與利潤率高點，盈餘上修反映的是2026–2027年已入帳的訂單，兩者不衝突。以2027年資料中心訂單能否延續作為決勝數據。","evidence_level":"高","settle_metric":"2027年上半年資料中心RPO與新簽約","if_then":["若2027年2月財報資料中心RPO季增且2027年EPS財測中點≥42美元，則下跌屬過度折價，在670美元以下分批建首倉","若資料中心RPO連兩季季減，則市場看對了，不建倉，悲觀機率升到40%"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"現在就買的最強論證與觀望","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：股價比7–8月賣方平均目標價930–1,044美元低25–34%；FY2027本益比約17.7倍，2027年有創高RPO撐住；公司淨現金，新增5億美元回購授權；下跌主要來自選前政治雜音。","side_b":"目標價快照停在8月初，早於這波下跌，各站樣本與日期不一。基準情境五年年化報酬約7–8%，悲觀機率30%下，期望值不足以補償循環風險。","ruling":"維持觀望。賣方目標價最高與最低之比約1.5倍，分歧不大，但資料已過時，不作進場依據。","evidence_level":"中","settle_metric":"賣方更新後目標價中位數、2027年財測","if_then":["若股價≤620美元，則不必等財測，重跑研究後建首倉","若股價續漲但2027年財測未高於共識，則不追"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"管理層前後說法對照（第二季對第三季）","cause":null,"prior_field":null,"side_a":"2026-07-30第二季法說，財務長沒有量化收購攤銷與機械段利潤率拖累，並稱財測未假設10.6%的利潤率重現。","side_b":"2026-10-29第三季法說，非GAAP營業利益率仍達10.5%；財務長首次給出2027年收購相關攤銷約1.28億美元（第四季3,530萬美元），並稱機械段利潤率將守在12–12.5%。","ruling":"可調和：管理層兌現了上一季的保守承諾，可信度加分。但2027年攤銷金額不小，以約25%稅率粗估約每股2.2美元（稅率事實表未涵蓋），FY2027共識是否已計入不明，是FY2027 EPS的下行風險。","evidence_level":"中","settle_metric":"2027年2月財報的2027年EPS財測與共識對照","if_then":["若2027年EPS財測中點低於37美元，則把基準情境2027年EPS下修到財測中點，重新跑情境","若財測中點≥42美元，則把重新進場價位上移到670美元"]}],"triggers":[{"n":1,"text":"股價跌到620美元以下，基準情境五年年化報酬達10%","type":"估值rearm","maps_to":"H1","metric":"EME收盤價","threshold":"≤620美元","action":"重跑完整研究後分三批建首倉","source_freq":"每日收盤","date":null},{"n":2,"text":"2027年2月第四季財報：資料中心RPO不低於87.4億美元、總RPO不低於180億美元","type":"假設驗證","maps_to":"H1","metric":"資料中心RPO、總RPO","threshold":"資料中心RPO≥87.4億美元且總RPO≥180億美元","action":"成立則維持論點並上調2027年EPS錨；不成立則悲觀機率升到35%","source_freq":"每季財報","date":"2027-02"},{"n":3,"text":"資料中心RPO連兩季季減，或單季跌破70億美元","type":"Single Thing","maps_to":"Single Thing","metric":"資料中心RPO","threshold":"連2季季減，或低於70億美元","action":"不建倉；已持有則減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"]},{"n":4,"text":"非GAAP營業利益率近四季跌破9%","type":"風險","maps_to":"R2","metric":"非GAAP營業利益率（近四季）","threshold":"<9.0%","action":"停止加碼，陷阱風險改判為高","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#0"]},{"n":5,"text":"收購累計減損超過1億美元，或收購支出連兩年高於自由現金流","type":"減碼","maps_to":"R3","metric":"收購減損；收購支出對自由現金流","threshold":"減損>1億美元，或收購支出>自由現金流連2年","action":"減碼三分之一","source_freq":"季報與年報","date":null,"evidence_refs":["competitive_share_entrants#2"]},{"n":6,"text":"PEMEX Deer Park外洩訴訟：公司揭露保險不足額，或提列未保險損失","type":"風險","maps_to":"法律風險（不對應論點）","metric":"訴訟相關提列金額","threshold":"未保險提列>1億美元","action":"停止加碼，直到金額確定","source_freq":"10-Q與10-K附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":7,"text":"營建段有機成長連四季落後FIX超過15個百分點","type":"風險","maps_to":"R4","metric":"EME營建段有機成長對FIX營收成長","threshold":"落後超過15個百分點，連4季","action":"護城河方向改判下降，停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["competitive_share_entrants#4","substitute_technology#1"]},{"n":8,"text":"總RPO年增率轉負，且資料中心RPO跌破60億美元","type":"清倉","maps_to":"H1","metric":"總RPO年增率、資料中心RPO","threshold":"年增率<0%且資料中心RPO<60億美元","action":"清倉","source_freq":"每季財報","date":null},{"n":9,"text":"已建首倉後，2027年EPS財測中點≥42美元且股價≤720美元","type":"加碼","maps_to":"H1","metric":"2027年EPS財測中點、股價","threshold":"財測中點≥42美元且股價≤720美元","action":"加碼第二批","source_freq":"2027年2月財報","date":"2027-02"},{"n":10,"text":"第四季財報與2027年展望複審","type":"複審日期","maps_to":"H1","metric":"全年財報、資料中心RPO、收購攤銷","threshold":"財報公布即複審","action":"重跑研究","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"資料中心RPO季變化","bear_threshold":"連續2季季減，或單季低於70億美元","window":"2027–2028年每季","source":"公司季報新聞稿（8-K附件）","last_status":"ok"},{"metric":"非GAAP營業利益率（近四季）","bear_threshold":"<9.0%","window":"滾動四季","source":"公司季報新聞稿（8-K附件）","last_status":"ok"},{"metric":"總RPO年增率","bear_threshold":"<0%","window":"每季","source":"公司季報新聞稿（8-K附件）","last_status":"ok"},{"metric":"自由現金流／淨利（全年）","bear_threshold":"<0.8，連2年","window":"年度","source":"年報現金流量表","last_status":"ok"}],"action_conditions":{"rearm_trigger":"股價≤620美元（基準五年年化報酬達10%）；若2027年EPS財測中點≥42美元，價位上移至670美元","exec_line":"觸發後先重跑研究。首倉分三批，每批間隔一次季報；第三批要等資料中心RPO連兩季未季減。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤620美元（基準情境五年年化報酬達10%）；若2027年EPS財測中點≥42美元，價位上移到670美元"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-23.82, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價≤620美元（基準情境五年年化報酬達10%）；若2027年EPS財測中點≥42美元，價位上移到670美元'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心與多元非住宅需求，在2027年前把創新高的在手訂單轉成兩位數營收成長，利潤率守在10%左右","2y":"2027年營收≥233億美元（FY2共識）、非GAAP營業利益率≥9.5%、2027年底總RPO≥170億美元","5y":null,"10y":null,"threshold":"2027年營收≥233億美元且非GAAP營業利益率≥9.5%","source":"公司季報新聞稿（8-K附件）、10-Q與法說會","drift_rule":"兩年期：近四季營收對路徑偏離，連2季≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"現場技工規模與預製能力，讓EME持續比非住宅營建市場多長約600bp，營建段利潤率守在管理層公布的區間","2y":null,"5y":"2027–2031年三年滾動有機成長比非住宅營建高≥400bp，電氣與機械營建合計營業利益率≥11%","10y":null,"threshold":"有機成長超額≥400bp，營建合計營業利益率≥11%","source":"公司年報與季報分部數據、AIA非住宅營建統計","drift_rule":"五年期：連4季偏離≥5%為削弱、連6季≥10%為反轉"},{"id":"H3","text":"資本配置維持每股複利：現金轉換穩定、收購不出現大額減損、股數持續下降","2y":null,"5y":"2027–2031年自由現金流／淨利平均≥0.9、累計收購減損<2億美元、稀釋股數每年降≥1%","10y":null,"threshold":"自由現金流／淨利≥0.9且股數每年降≥1%","source":"年報現金流量表與附註、季報股數","drift_rule":"五年期：連4季偏離≥5%為削弱、連6季≥10%為反轉"}],"R":[{"id":"R1","text":"雲端業者資本支出進入消化期，或地方暫停令擴散，造成資料中心新簽約斷層","h_ref":"H1","clock":"⚡","threshold":"資料中心RPO連2季季減，或單季低於70億美元","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"]},{"id":"R2","text":"利潤率回落：機械段統包與GMP合約比重上升，銅鋼關稅與供應延誤落在固定價合約，技工薪資上漲","h_ref":"H1","clock":"🔥","threshold":"非GAAP營業利益率近四季<9%，或電氣段單季<11.5%","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0","competitive_share_entrants#0"]},{"id":"R3","text":"收購競價推高買價，攤銷與減損侵蝕每股盈餘","h_ref":"H3","clock":"🔥","threshold":"收購累計減損>1億美元，或收購支出連2年高於自由現金流","evidence_refs":["competitive_share_entrants#2"]},{"id":"R4","text":"預製與模組化把現場工作移入工廠，FIX以整棟模組搶下資料中心份額，削弱EME的現場技工優勢","h_ref":"H2","clock":"🐢","threshold":"營建段有機成長連4季落後FIX超過15個百分點","evidence_refs":["competitive_share_entrants#4","substitute_technology#1","substitute_technology#2","substitute_technology#3"]}],"single_thing":{"description":"主要雲端業者集體把資料中心建置轉入消化期，EME資料中心在手訂單首次出現連續季減。","why_fatal":"資料中心約占在手訂單47%、年初至今營收三分之一，機械段資料中心營收年增約130%。需求一旦轉向，營收與營運槓桿同步反轉，利潤率回到7%區間，EPS與本益比雙降。","if_happens":"不建倉；已持有則減碼一半，悲觀機率升到40%以上，重估2028年EPS。","how_monitor":"每季財報揭露的資料中心RPO與季增率；雲端業者每年1–2月公布的資本支出指引；勞登郡、紐約州、德州等地方暫停令進度。","probability":"約20%（12–24個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.7,"peg_fy2":1.17,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":28.19,"FY2026E":34.29,"FY2027E":39.1,"FY2028E":45.02},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（年度財報）；FY2026E到FY2028E為Koyfin共識（2026-10-31，公司調整後口徑），兩者口徑不完全一致。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"美國期中選舉後，各州與地方資料中心暫停令的走向（紐約州、勞登郡、德州）","impact":"中","watch":"新增暫停令是否擴及EME主要市場：維吉尼亞、德州、喬治亞"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報、2027年展望與收購攤銷實際數","impact":"高","watch":"資料中心RPO季增率；2027年EPS財測中點是否≥42美元"},{"date":"2027-02","date_precision":"month","type":"macro","event":"大型雲端業者公布2027年資本支出指引","impact":"高","watch":"資本支出年增率是否轉負"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"新增兩座只做預製的工廠，對內外同時接單","impact":"低","watch":"對外預製接單，以及是否延伸到安裝"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"勞登郡恢復核發新資料中心案（CEO預期年中）","impact":"中","watch":"維吉尼亞新簽約是否恢復"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：channel_business_model_shift（通路／商業模式轉移）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
