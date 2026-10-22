你是 DD 管線 v20 的判斷層閘（gate），標的 COF（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_total_net_revenue_gaap`（q1_business）｜Total net revenue（GAAP）＝16.3 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi3_pre_provision_earnings_n`（q1_business）｜Pre-provision earnings（non-GAAP）＝7.5 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi5_provision_for_credit_los`（q1_business）｜Provision for credit losses＝2.9 USD bn（淨沖銷 $3.1bn；準備金釋出 $225m）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi6_net_interest_margin`（q1_business）｜Net interest margin＝8.41 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi8_period_end_loans_held_fo`（q1_business）｜Period-end loans held for investment＝462.5 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：n/a
- `f_kpi9_period_end_deposits`（q1_business）｜Period-end deposits＝480.7 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：n/a
- `f_kpi4_efficiency_ratio_gaap`（q1_business）｜Efficiency ratio（GAAP／調整後）＝54.19 %（調整後 48.76%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到
- `f_kpi7_cet1_ratio_basel_iii_sta`（q1_business）｜CET1 ratio（Basel III Standardized，初步）＝13.8 %｜期間與口徑：2026-09-30（Q3 2026 公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[7]，as_of 2026-09-30（Q3 2026 公告於 2026-10-20））
  - 註記：n/a
- `f_kpi1_gaap_net_income_diluted_`（q1_business）｜GAAP net income / diluted EPS＝5.61 USD/share（淨利 $3.5bn）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到（財報前 FY1 共識見 consensus_revision）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.548 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_peer_cof_fcf_margin_pct`（q2_moat）｜COF FCF 利潤率＝47.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COF.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_axp_fcf_margin_pct`（q2_moat）｜AXP FCF 利潤率＝19.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AXP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jpm_fcf_margin_pct`（q2_moat）｜JPM FCF 利潤率＝-83.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JPM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_c_fcf_margin_pct`（q2_moat）｜C FCF 利潤率＝-26.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.C.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_v_operating_margin_pct`（q2_moat）｜V 營業利益率＝65.61 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.V.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.56 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝24.07 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝28.08 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝64060.01 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝67545.92 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.31 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 19.71 → 20.56（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝613.48 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝10.05 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 20.56，分子＝快照價 206.66｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝206.66 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝13.27 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝14.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝14.7 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝4.44 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝58.63｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-10-22／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
  - 原文：「price 206.66 / W52 206.2 / W104 199.27 / W250 149.35 / W250 13週斜率 0.7%」
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.7 %｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_kpi2_adjusted_eps_non_gaap`（q1_business）｜Adjusted EPS（non-GAAP，排除調整項）＝6.69 USD/share｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未查到

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出收購 Global Payment Network 後，COF 與其他支付網路競爭 Network Partners，並與 Visa、Mastercard 的競爭可能影響既有合作；另面臨穩定幣、代幣化存款等新興替代支付業者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出部分競爭者（含數位與行動支付、金融科技業者）不受同等監管，且部分對手規模遠大於 COF，可能在資金成本與通路上占優。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：KPMG 2026 年 4 月發卡機構簡報：10% 信用卡利率上限法案（S.381／H.R.1944）尚未出委員會、聯邦利率上限未立法；KPMG 稱 10% 上限可能對發卡機構經濟性造成重大影響，包含收緊核貸標準、信用可得性下降。
  - 來源：KPMG: Top of Mind – Credit Card Issuers, April 2026（as_of 2026-04-30）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因子：監管機關可能限制公司的併購或擴張能力，且重疊調查、罰款、限制產品等可能損害業務。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 載明商家與商家團體對發卡銀行（含公司）提起多起反壟斷訴訟，主張交換費等做法違反聯邦反壟斷法；英國、加拿大等地對交換費設有上限或自願協議。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：decision_inputs.bear、valuation
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：Law360 報導一群消費者請求加州聯邦法官阻止 Capital One 51.5 億美元收購 Brex，主張違反反壟斷法（付費牆，未見裁定結果）。
  - 來源：Law360 'Capital One's $5B Brex Purchase Must Be Blocked, Judge Told'（as_of 2026-03-16）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：COF 10-K FY2025 風險因素把貿易戰、貿易壁壘、關稅、制裁與供應鏈中斷（含對汽車產業的影響）列為可能影響其業務的總體風險；非直接產品／供應鏈暴露。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：核心IT基礎設施與客戶應用已大部分遷至雲端，AWS為主要供應商；雲端供應商中斷可能造成服務中斷與非預期成本
  - 來源：SEC EDGAR Capital One FY2025 Form 10-K（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：Q1 2026 調整後 EPS $4.42 低於共識 $4.50，信用損失準備 $4.07B 高於預期（來源為低品質聚合站，待核）；BofA 維持 Buy、目標價 $234。
  - 來源：accred.deac.org 聚合頁（Q1 2026 Earnings Miss）（as_of 2026-04-23）｜affects：decision_inputs.bear、valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：Discover 卡片產品誤分類：商家集體訴訟和解獲法院初步核准（2025-07-30），Discover 提列 12 億美元；股東集體訴訟 2025-03-31 被駁回（無損害駁回），原告 5-14 申請修訂；Discover 另受 SEC 調查，公司配合中。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 附註（as_of 2026-02-19）｜affects：decision_inputs.bear、valuation
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-04-15 於維吉尼亞東區聯邦法院提起集體訴訟，指控單方關閉帳戶並取消已賺得信用卡回饋；2026-06-04 另案指控因錯誤「已故」註記關閉帳戶未依 ECOA 發出不利行動通知。
  - 來源：Law360「Capital One Hit With Class Action Over Canceled Rewards」；Top Class Actions 2026-06-26（as_of 2026-06-26）｜affects：decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：360 Savings 利率集體訴訟 4.25 億美元和解於 2026-04-20 獲最終核准。
  - 來源：Top Class Actions（as_of 2026-04-20）｜affects：decision_inputs.bear
- `financial_capital_credit_cycle#0`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：COF 2026 Q2 合併淨沖銷率 1.48%，較去年同期升 18bp；上半年 1.59%，升 14bp（搜尋摘要轉述，未讀原頁）
  - 來源：Capital One Form 10-Q (period ended 2026-06-30)（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Discover 卡片產品誤分類商家集體訴訟和解，提列 12 億美元；股東集體訴訟曾被駁回後申請修訂。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-19）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-04-15 回饋取消集體訴訟（維吉尼亞東區）。
  - 來源：Law360（as_of 2026-04-15）｜affects：decision_inputs.bear
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：Discover 曾受 SEC 就卡片產品誤分類事件調查，公司配合中。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-19）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":432.0,"bear_5y_price":150.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":51.5,"ev5y_pct":39.3,"irr_base_pct":8.7,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":20.56,"pe":10.05,"basis":"FY2026E 共識 EPS（Koyfin）；終端倍數乘在 FY2030E 當年 EPS 上，口徑一致"},"eps":{"bull":[20.8,24.6,28.8,32.5,36.0],"base":[20.56,23.6,26.6,29.0,31.3],"bear":[20.2,18.5,15.0,17.5,20.0]},"pe":{"bull":12,"base":10,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.548,"net_buyback":6.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COF_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜margin：Q2 淨利差 8.01%，較上季高 14bp（原話："Our second quarter net interest margin was 8.01%,"）
- 2026-07-21｜CFO｜margin：下季淨利差預期因平均現金追上期末現金而回補（原話："there should be a bit of a NIM catch-up"）
- 2026-07-21｜CFO｜margin：下半年每季多一天，帶來 9bp 淨利差順風（原話："So that adds a 9 basis point tailwind to NIM."）
- 2026-07-21｜CFO｜margin：結構性淨利差參考去年下半年水準（原話："the back half of last year as a pretty decent proxy for a"）
- 2026-07-21｜CFO｜margin：NII 對利率近乎中性，但 Fed 動作短期可能影響 NIM（原話："neutral to rates over time, but if and when the Fed moves"）
- 2026-07-21｜CFO｜capital_allocation：CET1 13.7%，較上季低 70bp（含回購、Brex、風險加權資產增加）（原話："ended the quarter at 13.7%, 70 basis points lower"）
- 2026-07-21｜CFO｜capital_allocation：11% 是長期資本『需求』而非目標（原話："long-term capital need as opposed to a target"）
- 2026-07-21｜CFO｜capital_allocation：不急著把資本比率壓到特定數字（原話："we are not in a race to drive it down as quickly as"）
- 2026-07-21｜CFO｜risk：卡業務備抵釋出 7.05 億美元（原話："we released $705 million of allowance."）
- 2026-07-21｜CEO｜risk：國內卡淨沖銷率 4.71%，較上季降 39bp（原話："was 4.71%, down 39 basis points from the prior quarter"）
- 2026-07-21｜CEO｜risk：國內卡逾期率 3.39%（原話："delinquency rate was 3.39% at quarter end"）
- 2026-07-21｜CEO｜risk：6 月逾期是今年第一個沒有優於季節性的月份（原話："it's the first month that didn't actually"）
- 2026-07-21｜CEO｜risk：回收庫存預期未來一年左右趨緩（原話："our recoveries inventory should taper off a bit"）
- 2026-07-21｜CEO｜risk：2024、2025 年新增帳戶表現優於 2022、2023（原話："2024 and 2025 originations coming in better than"）
- 2026-07-21｜CEO｜risk：支付率明顯高於疫情前（原話："meaningfully above prepandemic levels across all of our"）
- 2026-07-21｜CEO｜risk：管理層稱其客戶數據未見 K 型分化（原話："We don't, in our own numbers, see this K-shaped economy"）
- 2026-07-21｜CEO｜risk：車貸淨沖銷率 1.43%（原話："The auto charge-off rate for the quarter was 1.43%"）
- 2026-07-21｜CEO｜customer：消費者表現良好（原話："the consumer continues to perform remarkably well"）
- 2026-07-21｜CEO｜guidance：Discover 卡貸款預期短期續縮，谷底約在第四季（原話："we expect continued contraction in the near term"）
- 2026-07-21｜CEO｜guidance：Discover 貸款收縮谷底時點（原話："sort of the bottom of the brownout will be somewhere around"）
- 2026-07-21｜CEO｜product：Discover 卡貸款年減 1.5%（原話："The legacy Discover card loans shrank 1.5% from"）
- 2026-07-21｜CEO｜product：Discover 新發卡約一半已上 Capital One 技術平台（原話："50% of Discover originations are now on Capital One's tech"）
- 2026-07-21｜CEO｜commitment：Discover 舊帳戶要到明年第一季才完全轉入（原話："until the first quarter of next year"）
- 2026-07-21｜CEO｜product：遷移分批進行（7 月、10 月、1 月）（原話："A wave in July, a wave in October, a wave in January."）
- 2026-07-21｜CEO｜product：Legacy Capital One 購買量（含 Brex 與公司卡）年增約 14%（原話："grew about 14% year-over-year"）
- 2026-07-21｜CEO｜product：全球支付網路交易量約 1,900 億美元（原話："was approximately $190 billion"）
- 2026-07-21｜CEO｜product：金融卡轉 Discover 網路已完成，管理層形容成功（原話："I would call it a smashing success"）
- 2026-07-21｜CEO｜product：信用卡轉網路仍在測試，之後才定最終遷移量與時程（原話："we will then make our final choices about how"）
- 2026-07-21｜CEO｜capital_allocation：行銷費用約 17 億美元，年增 23%（原話："marketing expense in the quarter was about $1.7 billion"）
- 2026-07-21｜CFO｜capital_allocation：行銷費用下半年通常較高（原話："upward slope and particularly in the back half of the year"）
- 2026-07-21｜CEO｜capital_allocation：網路投資只是眾多投資之一，技術與 AI 花費更多（原話："upward slope and particularly in the back half"）
- 2026-07-21｜CEO｜commitment：Discover 完整 25 億美元綜效維持不變（原話："spending a lot more money than that on Capital One"）
- 2026-07-21｜CEO｜commitment：剩餘營運費用綜效預計 2027 下半年達成（原話："remain on track to deliver the full $2.5 billion"）
- 2026-07-21｜CEO｜guidance：整合後盈餘能力與併購宣布時預期一致（原話："to be consistent with what we expected at the time"）
- 2026-07-21｜CEO｜margin：不就效率比率給具體指引（原話："But we're not specifically guiding on that."）
- 2026-07-21｜CEO｜margin：效率比率隨營收、費用、投資與綜效而變（原話："The efficiency ratio will continue to reflect our revenue"）
- 2026-07-21｜CEO｜guidance：盈餘能力不給精確數字（回應 20% 報酬問題）（原話："We're not branding a precise number"）
- 2026-07-21｜CFO｜margin：盈餘能力以 ROTCE 衡量，分母採 12.5% CET1 僅為可比性（原話："the weighted average consensus for CET1 was 12.5%."）
- 2026-07-21｜CEO｜capital_allocation：近期最大化 ROTCE 不是公司整體目標函數（原話："isn't the maximization of ROTCE in the near term"）
- 2026-07-21｜CEO｜product：Brex：先前未說過從第一天就能加速成長（原話："I don't believe we said this from the second"）
- 2026-07-21｜CEO｜product：Brex 行銷整合需資料管線，較晚才會到（原話："So that will come a little further down the road."）
- 2026-07-21｜CEO｜product：旅遊入口併入 Brex 待 Hopper 建置完成（原話："we will be focused on the Hopper build-out"）
- 2026-07-21｜CEO｜commitment：Brex 投資將嚴格衡量價值（原話："we're going to very rigorously measure to be sure"）
- 2026-07-21｜CFO｜product：不拆分披露 Brex 損益（原話："we're going to very rigorously measure to be sure"）
- 2026-07-21｜CEO｜competition：管理層認為市場對公司估值未充分認可（原話："I believe that we probably don't get appropriate recognition"）

### 問答異常語氣（迴避／改口／保留）
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Darrin Peller 問 Brex 與公司卡的備考購買量成長｜答法：CFO 稱 Brex 占比小、不拆分 P&L；Norris 重述已給的 14% 數字
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Ryan Nash 問是否至少 20% 報酬｜答法：CEO 不給精確數字，只說與當初預期一致
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Erika Najarian 問盈餘能力基準（2027 EPS 約 24.5、ROTCE 中 20 幾）算法錯在哪｜答法：CFO 只說假設不符、股價等變數已動，未確認或否定其數字，回到 ROTCE 定義
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Sanjay Sakhrani 問 Brex 與行銷投資對效率比率的邊際影響｜答法：CEO 稱不就效率比率給指引，改談盈餘能力
- COF_Q2_2026_Earnings_Call_20260721.md｜問：Mihir Bhatia 問 6 月沖銷率大降｜答法：CEO 稱手邊無 6 月數字，主動指出 6 月逾期未優於季節性

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 5 | 2 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 3 |
| financial_capital_credit_cycle | found | 4 | 3 |
| financial_regulatory_capital_rules | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260722","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Discover synergy 兌現至 $2.5B 年化（2H2027）：cost + network economics（debit 已繞過 Durbin 完成、卡量遷移待測），驅動 EPS 從 2025 CECL 低點正常化至 FY26 $19.71 / FY28 $28.44"},{"id":"H2","text":"信用週期維持「正常化」（國內卡 NCO 4.5-6% 區間、不結構性反轉）至 FY27：失業率不破 5.5% + subprime 損失回歸 through-cycle 中樞"},{"id":"H3","text":"估值修復：市場把 COF 從「受監管 subprime lender」8x 重估回「正常化優質銀行」10-11x + P/TBV 向 warranted ~2.6x 靠攏"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"信用週期反轉 + 失業率破 5.5% → subprime 卡 NCO 升向 8-9%（COF ~26% subprime 曝險為結構性 binary risk）；疊加 macro overlay 已部分釋出 + recoveries 順風將退坡（管理層自認「未來一年左右」）＝改善引擎熄火，若此時週期轉向損失反彈更陡"},{"id":"R2","text":"Discover synergy 大幅 miss（大型銀行併購典型 30-40% miss）→ re-rate 動能消失；back book 轉換（Jul/Oct/Jan 波次）造成客戶流失加劇、brownout 未如期 Q4 觸底"},{"id":"R3","text":"監管尾部（三面夾）：① 聯邦 10% 信用卡利率上限提案（2026-01 Trump 於 Davos 重申支持一年期 10% 上限；2026-04/05 Warren 續質詢執行進度、至今未決）——若成真將直接摧毀 COF 8% NIM 的 near/subprime 卡經濟，是對 thesis 最大的單一尾部風險（雖低機率）；② CCCA（2026-01 重提，2026-03 未成功附掛住房法案）——雙向：若強制 routing 競爭可能壓 interchange 池（利空），亦可能把量導向 COF 自有 Discover 網絡（對沖）；③ CFPB late-fee RFI（2026-07 送審，現規則已於 2025-04 遭 N.D. Texas vacate）→ subprime 費收"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","irr_base_pct":12.0,"ev5y_pct":54.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":4.1,"ev5y_pct":54.0,"irr_base_pct":12.0,"max_dd_pct":-52.0,"bull_5y_price":433.0,"bear_5y_price":150.0,"p_bull_pct":25.0,"p_bear_pct":25.0,"rearm_trigger":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","price_at_dd":206.22,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"COF","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Capital One Financial Corporation"},"oneliner":"Discover 綜效進度超前、卡信用處低點；前瞻本益比約 10 倍只要求盈餘持平，主要尾部是聯邦利率上限與信用循環轉向","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COF_20261022/scenario.json","answers":{"q1_business":{"verdict":"賺持卡人的循環利息與交換費：錢卡在核貸定價模型與低成本零售存款；收購 Discover 後，網路端分潤也收回自家","reasoning":"Q3 總營收 163 億美元，淨利差 8.41%（季增 40bp，來自國內卡收益率、現金下降與多一天），撥備前盈餘 75 億美元；提列 29 億美元，含淨沖銷 31 億、準備金釋出 2.25 億。期末放款 4,625 億美元，存款 4,807 億美元，存款大於放款，資金不靠批發市場。分部：國內卡 Q3 營收年增 5%、收入率 17.8%、沖銷率 3.98%；消費金融營收年增約 17%（Discover 營收綜效與車貸）；商業銀行營收季增 6%。分部營收占比事實表未涵蓋。產業時鐘判在擴張期：信用損失從 2024 年高點回落、準備金釋出中，但逾期改善自 6 月起只跟季節性，擴張後段。供需持久性：週期性將反轉，卡信用損失有循環，不是結構性改善。產業態勢雙向拉鋸：競爭面惡化（大型同業資金成本更低、高端卡行銷加碼，10-K 稱支付業競爭加劇）；結構面轉好（借記卡轉 Discover 網路完成，網路交易量年增 25%）；監管面變動（10% 利率上限提案、Visa／Mastercard 交換費和解 11 月終審）。單點依賴：核心系統大多在 AWS，列入風險。","fact_refs":["f_kpi0_total_net_revenue_gaap","f_kpi3_pre_provision_earnings_n","f_kpi5_provision_for_credit_los","f_kpi6_net_interest_margin","f_kpi8_period_end_loans_held_fo","f_kpi9_period_end_deposits","f_kpi4_efficiency_ratio_gaap"],"verdict_values":{"revenue_quality":"以利息收入為主（淨利差 8.41%），交換費與網路費為輔；Q3 準備金釋出 2.25 億美元與高回收屬一次性或週期性順風，非經常性","unit_econ_note":"國內卡收入率 17.8% 減沖銷率 3.98%，風險調整後收入率約 13.8%；信用轉壞時這個差距是盈餘的第一道緩衝","archetype":{"primary":"金融","secondary":null,"confidence":"高","fingerprint":"發卡行＋全國數位零售銀行＋自有支付網路"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：管理層 Q3 法說稱逾期改善已轉為只跟季節性，Q2 法說稱回收庫存一年內退坡","bargaining":{"up":"資金端：零售存款 4,807 億美元大於放款，管理層稱存款保險覆蓋比例高、客戶關係深，對資金供給方議價強","down":"持卡人換卡成本低，靠回饋與高端權益留客；商家透過反壟斷訴訟與和解壓縮交換費","geo":"業務集中美國；英國、加拿大已有交換費上限先例"},"profit_pool_dir":"網路端利潤池（Visa 營業利益率 65.61%）透過轉網部分收回；發卡端交換費池受和解與訴訟壓縮","tam_table":{"expanded":false,"reason":"美國信用卡為成熟市場，成長來自份額、網路量與高端客群而非滲透率；事實表未涵蓋市場規模與份額數據"}}}},"q2_moat":{"verdict":"護城河持平：Discover 網路與資料核貸是真優勢，綜效進度超前；但交換費與利率監管、高端卡行銷競爭把定價權壓住","reasoning":"機制：規模化資料核貸加上自有網路與全國數位銀行的低成本存款。銀行不看 ROIC，改看報酬與效率：Q3 調整後效率比率 48.76%、GAAP 54.19%，都低於 60%；CET1 13.8%。同業 ROTCE 事實表未涵蓋，無法做報酬差距對照，評分用綜合分加敘述：執行 8、定價 7。當期報酬屬高利益率低周轉；四檢查點中社會容忍度為紅。增量報酬約 20% 是法說會分析師推估的量級，管理層未確認；再投資率約 12%（Q3 回購 26 億美元加股息約 5 億美元，占淨利 35 億美元約 88%），內生成長上界約 2.4%。高報酬、低再投資空間，多餘資本以回購配回，符合紀律。","fact_refs":["f_kpi4_efficiency_ratio_gaap","f_kpi7_cet1_ratio_basel_iii_sta","f_kpi1_gaap_net_income_diluted_","f_dividend_yield_ttm","f_peer_cof_fcf_margin_pct","f_peer_axp_fcf_margin_pct","f_peer_jpm_fcf_margin_pct","f_peer_c_fcf_margin_pct","f_peer_v_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模化資料核貸與即時風控、自有 Discover 支付網路、無分行的全國數位銀行低成本存款，三者疊加","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：綜效年化 18 億美元超前、Discover 新發卡 100% 上公司系統、國內卡沖銷率年降 65bp；定價權縮減：交換費和解將下調收入、行銷年增 14% 高於國內卡營收年增 5%、利率上限提案未解；兩者相抵判持平","competitor_notes":[{"name":"AXP","strategy_note":"高端卡最強對手，閉環網路加高消費客群；公司往上打高端客群必然正面碰撞，行銷成本由此墊高"},{"name":"JPM","strategy_note":"規模與資金成本優勢最大的發卡行，正是 10-K 點名的大型對手類型；現金流利潤率為負是銀行口徑，不可比"},{"name":"C","strategy_note":"大型發卡同業，以聯名卡為主；現金流指標同樣不適用於比較"},{"name":"V","strategy_note":"原本收網路費的一方；公司把借記卡與部分信用卡轉到自有網路，等於從它手上拿回網路端分潤，其營業利益率顯示這塊利潤池之厚"}],"spread_notes":null,"peer_na_reason":"同業對照只有現金流利潤率，對銀行無意義；同業 ROTCE 與有形淨值報酬事實表未涵蓋","threats":[{"level":"🔴","text":"監管攻擊整個生態：10% 利率上限提案與交換費和解直接壓縮發卡經濟，監管也可能限制併購與擴張","p":"10%","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#2","regulatory_antitrust#1"]},{"level":"🟡","text":"高端卡行銷競爭：規模更大、資金成本更低的同業持續重金投入，公司 2027 年要再加碼行銷","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"新支付業者（穩定幣、代幣化存款、代理商務）攻網路端；BofA 研究認為較屬估值壓力而非基本面","p":"15%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（淨利差 8.41%，資產負債表重）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者都是持卡人；消費支付與短期信用是需要不是想要。Q3 購買量年增 11%，舊 Capital One 卡放款年增約 6%"},{"item":"決策層級","level":"🟡","text":"替代性要在單一消費者的錢包層衡量：換卡成本低，但回饋點數、高端權益與主要存款帳戶綁定提高黏著；借記卡轉網後管理層稱客戶量有保住，但流失率數據事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"交換費池由網路、發卡行、商家三方分；擁有 Discover 網路後可同時拿發卡與網路兩端，但商家反壟斷訴訟與 Visa／Mastercard 和解在壓縮整個池子，且多數交換費以回饋轉給消費者"},{"item":"社會容忍度","level":"🔴","text":"高利率信用卡是政治敏感產品：10% 利率上限法案、遲繳費規則、交換費訴訟同時存在；實際定價上限由政治決定，低於經濟上限"}],"roiic":"約 20%（法說會分析師推估的報酬量級，管理層未確認；股東權益事實表未涵蓋）","reinvest_rate":12,"endo_ceiling":2.4,"formula_note":"內生成長＝增量報酬約 20%×再投資率約 12%＝約 2.4%（總盈餘口徑）；再投資率＝1−（Q3 回購 26 億＋股息約 4.9 億）÷Q3 淨利 35 億；股息以殖利率 1.548%×市值估算"}}}},"q3_growth":{"verdict":"跑道中等：美國信用卡已成熟，五年後成長靠網路量、高端客群、全國數位銀行的份額，以及回購","reasoning":"共識 EPS：FY2026 20.56、FY2027 24.07、FY2028 28.08 美元，兩年年增約 17%；同期共識營收 FY2026 640.6 億、FY2027 675.5 億美元，只增約 5%。FY2025 GAAP EPS 4.03 含併購一次性費用與準備金首提，不能當成長基期，三年 CAGR 改看 FY2026→FY2028。缺口（約 17% 對內生上界約 2.4%）可以歸因：淨回購每年約 6–8%（Q3 回購 26 億美元，約市值 2% 一季），其餘來自綜效與信用正常化帶動的利潤率，不依賴估值重估。管理層 Q3 說剩餘綜效與交換費和解損失大致抵銷，2027 年行銷再加碼，所以共識 FY2027 之後的斜率偏樂觀。滲透率與份額事實表未涵蓋，跑道年數無法量化；五年後成長沒有明確第二曲線（網路轉信用卡仍在測試），判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量（卡購買量、車貸、存款、網路交易量）＋併購綜效（成本與網路經濟）＋淨回購；價（收益率）中性偏壓，交換費和解將下調","runway_years":"事實表未涵蓋滲透率與份額，無法估算","runway_post_y5":"🟡","endo_ceiling_basis":"內生成長上界約 2.4%（增量報酬約 20%×再投資率約 12%，總盈餘口徑）；共識 EPS 年增約 17% 的缺口歸因淨回購與利潤率（綜效、信用正常化），不依賴重估","segments":[{"item":"國內卡","value":"Q3 營收年增 5%、購買量年增 11%、期末放款年增約 2%（扣除 Discover 約 6%）、收入率 17.8%"},{"item":"消費金融（車貸、零售存款、網路）","value":"Q3 營收年增約 17%、放款年增約 13%、車貸撥款年增 22%、網路交易量約 1,910 億美元年增 25%"},{"item":"商業銀行","value":"Q3 營收季增 6%、放款季增約 1%、沖銷率 0%"},{"item":"分部營收占比","value":"事實表未涵蓋"}],"decay_signals":["EPS 成長顯著高於營收成長：亮（共識 FY2027 EPS 年增 17%，營收年增 5%）","核心市占近 12 個月縮減：部分亮（Discover 舊卡放款年減 2.9%、購買量持平；舊 Capital One 卡放款年增約 6%）","毛利率連 2 季年減：不適用，銀行看淨利差，Q3 8.41% 季增 40bp","現金轉換與 SBC 類訊號：不適用或事實表未涵蓋","產業估值倍數近 3 年系統性下移：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置良好：在約 10 倍本益比下大額回購，資本比率仍留緩衝；Discover 併購報酬要到 2027 完整年度才驗得到","reasoning":"Q3 回購 26 億美元加股息，約占淨利 35 億美元的 88%，CET1 仍維持 13.8%。CFO 在 Q2 法說稱 11% 是長期資本需求而非目標，不急著壓低。Fed 2026 壓力測試嚴重不利情境下 CET1 最低 11.0%，壓力資本緩衝 4.5% 維持到 2027-09-30（此緩衝在併入 Discover 前計算，2027 年可能重算）。回購收益率以前瞻本益比 10.05 倍換算約 10%；10 年期公債殖利率事實表未涵蓋，除非高於 8%，否則回購買入收益率過門檻。Discover 綜效年化 18 億美元、進度超前，但併購投入資本與增量報酬事實表未涵蓋，暫不判過。SBC 事實表未涵蓋；股數在大額回購下下降，另有 Brex 發行約 1,060 萬股。ROTCE 事實表未涵蓋。","fact_refs":["f_kpi7_cet1_ratio_basel_iii_sta","f_kpi1_gaap_net_income_diluted_","f_dividend_yield_ttm","f_shares_diluted_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Discover 綜效年化 18 億美元超前，管理層稱盈餘能力符合交易時預期；但併購投入資本與實現報酬事實表未涵蓋，待 2027 完整年度驗證"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"Q3 回購 26 億美元；買入收益率約 10%（1÷前瞻本益比 10.05）；10 年期殖利率事實表未涵蓋，低於 8% 即過"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 事實表未涵蓋；淨股數因回購下降，Brex 發行約 1,060 萬股，無法拆出 SBC 本身稀釋率"}]},"governance":{"capital_returns":[{"item":"Q3 回購","value":"26 億美元"},{"item":"CET1","value":"13.8%；管理層稱長期需求 11%，不急著壓低"},{"item":"股息殖利率","value":"約 1.55%（過去 12 個月）"},{"item":"Brex 收購","value":"51.5 億美元（27.5 億現金＋約 1,060 萬股），2026-06-30 完成"},{"item":"壓力測試","value":"嚴重不利情境 CET1 最低 11.0%；壓力資本緩衝 4.5% 維持至 2027-09-30"}]}}},"q5_valuation":{"verdict":"現價只要求盈餘持平：前瞻本益比約 10 倍、FY2027 共識下約 8.6 倍；我相信盈餘至少持平，所以偏便宜","reasoning":"現價 206.66 美元，FY2026 共識 EPS 20.56 對應 10.05 倍，FY2027 共識 24.07 對應 8.6 倍。今年準備金釋出（Q2 約 6.6 億、Q3 2.25 億美元，以 22% 稅率估稅後約每股 1.1 美元）扣掉後約 10.6 倍，結論不變。FY1 共識近 3 個月上修 4.31%。賣方目標價均值依聚合站不同落在 236–259 美元。銀行的主錨有形淨值倍數與 ROTCE 事實表未涵蓋，這是估值判斷最大的缺口。trailing 本益比只有四個年度端點、且 FY2025 分母被併購一次性費用壓低，不當五年分位使用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026 共識 EPS）為主；有形淨值倍數事實表未涵蓋","tier":"美國大型發卡行","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或有形淨值倍數；現金流利潤率對銀行無意義，不作估值錨"},"fwd_pe":10.05,"peg":0.59,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 10.05 倍÷FY2026→FY2028 共識 EPS 年增約 16.9%＝PEG 約 0.59；扣除準備金釋出後約 10.6 倍，仍只隱含盈餘持平；短期上行＝基本情境 FY2027 EPS 23.6×10 倍＝236 美元（+14.2%），中期＝FY2028 EPS 26.6×10 倍＝266 美元（+28.7%）；五年分位事實表只有四個年度端點、基期失真，不採用","upside_short_pct":14.2,"upside_mid_pct":28.7,"denominator_disputed":false,"denominator_note":"trailing 分母含 FY2025 併購一次性費用（GAAP EPS 4.03），改用前瞻錨；前瞻分母含今年準備金釋出，已扣除測試，結論不變"}}},"q6_how_wrong":{"verdict":"最可能看錯在信用循環：盈餘高點含準備金釋出與回收順風，而逾期改善已經停在季節性水準","reasoning":"三條主要看錯路徑：一是信用轉向，CECL 下準備金一次補提，跌幅比 2008 年陡（CEO 自述當年大量放款在表外、且無 CECL）；二是綜效全到位但被行銷競爭與交換費下調吃掉；三是 10% 利率上限立法。股價 26 週僅漲 4.44%，RSI 58.6，週線均線排列達標但 250 週均線 13 週斜率只有 0.7%，價格沒有先反映好消息。Q3 提列 29 億美元仍含 2.25 億釋出，扣掉後盈餘品質略低於帳面。","fact_refs":["f_kpi5_provision_for_credit_los","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度陷阱風險：盈餘高點含準備金釋出與回收順風，EPS 成長遠高於營收成長"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":20.56,"pe":10.05,"basis":"FY2026E 共識 EPS（Koyfin）；終端倍數乘在 FY2030E 當年 EPS 上，口徑一致"},"eps":{"bull":[20.8,24.6,28.8,32.5,36.0],"base":[20.56,23.6,26.6,29.0,31.3],"bear":[20.2,18.5,15.0,17.5,20.0]},"pe":{"bull":12,"base":10,"bear":7.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.55,"net_buyback":6.0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":6},"max_dd":{"lo":-55,"hi":-35,"basis":"法說會分析師指出公司過去在衰退期股價曾跌到有形淨值附近（有形淨值事實表未涵蓋）；CEO 自述 2008 年有大量放款在表外且無 CECL，現在信用轉向時準備金一次補提會更陡；熊情境終點 −27% 是終點不是路徑低點，路徑低點取 −35% 至 −55%","trigger_time":null},"basis":{"bull":"綜效 2027 年超過 25 億美元、信用卡大規模轉網、Discover 放款 2027 年轉正、信用維持良性；終端 12 倍給自有網路溢價（同業本益比事實表未涵蓋）","base":"接近共識但打折：剩餘綜效與交換費和解抵銷、2027 行銷加碼，FY2027 23.6、FY2028 26.6；之後放款中個位數成長加每年約 6% 淨回購，每股 EPS 已含回購效果；終端 10 倍＝現價前瞻倍數，不給重估","bear":"2027–2028 信用循環轉向，國內卡沖銷率升到 7% 以上並補提準備金，FY2028 EPS 15，之後恢復；終端 7.5 倍為信用壓力期發卡行倍數假設（歷史低點事實表未涵蓋）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"逾期改善自 6 月起只跟季節性（Q2、Q3 法說），回收庫存預期一年內退坡，車貸次級占比回到疫情前；Q2 合併淨沖銷率年增 18bp","assumption":"失業率上升使國內卡沖銷率 2028 年升到 7% 以上，CECL 下一次補提準備金","consequence":"FY2028 EPS 跌到約 15 美元、本益比 7 倍，股價約 105 美元，五年虧損近 50%","ruling":"部分採納：已放進熊情境（機率 30%、FY2028 EPS 15）；目前國內卡逾期率仍年減 15bp，沒有轉向證據，不據此迴避","watch":"國內卡逾期率年比轉升連 2 季","evidence_refs":["financial_capital_credit_cycle#0"],"fact_refs":["f_kpi5_provision_for_credit_los"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 行銷年增 14%，CEO 稱 2027 年更用力投行銷、網路與 AI；剩餘綜效與交換費和解損失大致抵銷；10-K 稱大型對手資金成本更低","assumption":"綜效全數到位，但被行銷競爭與交換費下調吃掉，調整後效率比率停在 49% 上下","consequence":"EPS 成長只剩回購貢獻（每年約 6%），本益比不重估，五年報酬約每年 8%","ruling":"採納：基本情境 FY2027 EPS 23.6 低於共識 24.07，終端本益比不給重估","watch":"調整後效率比率；行銷年增對營收年增的差距","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0","regulatory_antitrust#2"],"fact_refs":["f_kpi4_efficiency_ratio_gaap"]},{"view":"價格已反映太多","evidence":"FY2026 共識含今年準備金釋出；Q3 是季節性強季；FY2028 共識年增 17% 高於營收 5%；Q1 調整後 EPS 曾低於共識（來源品質低，待核）","assumption":"市場已按綜效全到位加信用持續良性定價","consequence":"若盈餘只維持目前水準，股價沒有上行空間","ruling":"反駁：前瞻本益比 10 倍只隱含盈餘持平，扣掉準備金釋出約 10.6 倍。現在就賣的最強論證是信用已在低點、盈餘高點含一次性順風；但股價從 7 月到現在幾乎沒動（206.22→206.66），沒有先反映","watch":"前瞻本益比超過 12 倍而信用指標轉弱","evidence_refs":["capital_markets_pricing#5"],"fact_refs":["f_fwd_pe_latest","f_week26_return_pct"]},{"view":"論點失敗","evidence":"KPMG：10% 利率上限法案未出委員會，若立法將重創發卡經濟、緊縮核貸；10-K：監管可能限制併購與擴張；社會容忍度檢查為紅","assumption":"期中選舉後利率上限或 CCCA 推進","consequence":"卡業務收益率結構性下降，詳見唯一致命點","ruling":"採納為唯一致命點；法案目前未出委員會，機率低但不可忽視","watch":"S.381／H.R.1944 委員會進度","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1"],"fact_refs":["f_kpi6_net_interest_margin"]},{"view":"論點成功但股東經濟變差","evidence":"Discover 卡片誤分類和解提列 12 億美元且 SEC 調查中；回饋取消與錯誤註記集體訴訟；360 儲蓄 4.25 億美元和解；Brex 收購遭消費者反壟斷訴訟","assumption":"訴訟與罰款逐年吃掉盈餘","consequence":"一次性費用持續拉開 GAAP 與調整後 EPS 的差距（Q3 每股差 1.08 美元）","ruling":"反駁為致命項：已提列與和解金額相對 Q3 單季淨利 35 億美元有限；但 GAAP 與調整後差距要追","watch":"GAAP 與調整後 EPS 差距是否在 2027 年收斂","evidence_refs":["major_events#0","major_events#2","major_events#3","lawsuit_class_action#0","lawsuit_class_action#1","sec_investigation_restatement#0","regulatory_antitrust#3"],"fact_refs":["f_kpi1_gaap_net_income_diluted_","f_kpi2_adjusted_eps_non_gaap"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 206.22 → 本次 206.66（+0.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=206.22","side_b":"本次 price_at_dd=206.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 206.22 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 206.22 美元：Bull 價 433、Bear 價 150，五年期望值 +54.0%，基準年化 12.0%，不對稱比 4.1","side_b":"本次情境、股價仍用 206.22 美元：Bull 價 432、Bear 價 150，五年期望值 +39.6%，基準年化 8.7%，不對稱比 2.68","ruling":"先換情境、股價不動：五年期望值少 14.4 個百分點，基準年化少 3.3 個百分點。不對稱比由 4.1 變為 2.68。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 206.22 美元：五年期望值 +39.6%，基準年化 8.7%，不對稱比 2.68","side_b":"本次情境、股價 206.66 美元：五年期望值 +39.3%，基準年化 8.7%，不對稱比 2.65","ruling":"再換股價、情境不動：起點價上漲 0.2%，五年期望值少 0.3 個百分點，基準年化少 0.0 個百分點，不對稱比由 2.68 降到 2.65。合計五年期望值比前份少 14.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面判斷欄重審（結論未變）","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-22）：評等 B、估值偏便宜、陷阱中度、護城河持平、五年後跑道中等、金融類，裁決進場","side_b":"本次以 Q3 新證據重審：綜效年化 18 億美元超前、國內卡沖銷率 3.98% 年降 65bp、前瞻本益比 10 倍、股價幾乎沒動；評等、估值、陷阱、護城河方向、跑道、類別判斷都維持，裁決與部位由程式依同組輸入重算","ruling":"維持：新證據偏正面，但行銷加碼與交換費和解抵銷了一部分，不足以上調任何一欄","evidence_level":"公司新聞稿與 Q3 法說會","settle_metric":"2027 上半年綜效年化與調整後效率比率","if_then":["若 2027 Q2 綜效年化 <20 億美元且調整後效率比率未降，則基本情境 EPS 下修 5% 並停止加碼","反向：若綜效 ≥25 億美元提前達成且 Discover 放款轉正，則護城河方向上調為擴大"],"evidence_refs":[]},{"axis":"情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份牛 25、熊 25，最大回撤單點 −52%","side_b":"本次牛 20、基 50、熊 30；最大回撤改為範圍 −35% 至 −55%","ruling":"共識 EPS 年增約 17% 超過內生成長上界約 2.4%（差距靠回購、綜效與信用正常化），依規則熊機率拉到 30%；回撤改寫範圍以反映 CECL 補提路徑","evidence_level":"本次推導","settle_metric":"國內卡逾期率年比","if_then":["若逾期率年比連 2 季轉升，則熊機率再上調到 35% 並減碼一半","反向：若 2027 全年沖銷率 ≤4.5%，則熊機率回到 25%"],"evidence_refs":[]},{"axis":"循環位置","cause":"方法變動","prior_field":["cycle_position"],"side_a":"前份未填循環位置","side_b":"本次判中循環：損失從高點回落、準備金釋出中，但逾期改善已停在季節性","ruling":"補填；依據為 Q2、Q3 法說的逾期與回收描述","evidence_level":"公司法說","settle_metric":"逾期率年比","if_then":["若逾期率年比轉升，則改判晚循環並停止加碼"],"evidence_refs":["financial_capital_credit_cycle#0"]},{"axis":"加碼條件更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼：國內卡 NCO 連 2 季 ≤5% 且 Discover 年化 synergy ≥$2.0B（FY26 末）；或回檔 $180-190（P/TBV ~1.7x）分批加","side_b":"加碼：2027 Q2 綜效年化 ≥22 億美元且國內卡逾期率年比未轉升；或回檔至 180 美元以下分批加","ruling":"沖銷率條件已達成（Q2 4.71%、Q3 3.98%），綜效 18 億美元接近舊門檻，改看下一個里程碑；有形淨值事實表未涵蓋，價格門檻改用前瞻本益比約 8.8 倍","evidence_level":"公司新聞稿與法說","settle_metric":"綜效年化金額","if_then":["若 2027 Q2 綜效 ≥22 億美元且逾期未轉升，則加碼至目標部位","反向：若價格先到 180 美元以下但逾期率已轉升，則不加碼"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標（空白）","side_b":"國內卡沖銷率 >5.5% 連 2 季減碼；CET1 <12% 減碼；利率上限法案任一院通過清倉","ruling":"補上可監測的門檻，對應三大風險","evidence_level":"本次推導","settle_metric":"各指標季度讀數","if_then":["若任一減碼門檻觸發，則減碼一半","若利率上限法案任一院通過，則清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點空白（未設）","side_b":"聯邦信用卡利率 10% 上限立法通過","ruling":"前份把利率上限列在監管風險之一；本次判它是數學上最大的單一敏感度項，獨立成唯一致命點","evidence_level":"KPMG 簡報與 10-K","settle_metric":"法案進度","if_then":["若法案出委員會，則減碼一半","若任一院通過，則清倉"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"盈餘能力說法與投資加碼","cause":"新證據","prior_field":null,"side_a":"CEO（2026-10-20）：併購後盈餘能力現在就看得到，與交易時預期一致；剩餘綜效與交換費和解大致抵銷","side_b":"同場 CEO：2027 年更用力投行銷、網路與 AI，不給效率比率指引；7 月法說也迴避 20% 報酬與效率比率的追問","ruling":"可調和、程度差異：盈餘能力指的是扣投資前的底盤，投資加碼會吃掉一部分；採保守側，基本情境 FY2027 EPS 23.6 低於共識","evidence_level":"Q2、Q3 法說原話","settle_metric":"2027 全年調整後效率比率","if_then":["若 2027 調整後效率比率高於 2026，則下修基本情境 EPS 5% 並停止加碼","反向：若效率比率下降且行銷年增低於營收年增，則上調基本情境至共識"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"Discover 放款谷底改口","cause":"新證據","prior_field":null,"side_a":"CEO（2026-07-21）：Discover 放款收縮谷底約在今年第四季","side_b":"CEO（2026-10-20）：預期未來數季繼續收縮，之後才轉正；Q3 Discover 卡放款年減 2.9%（Q2 為 1.5%）","ruling":"時程延後屬實，但新發卡已 100% 上公司系統、新發卡年增為併購後首次，判延後而非失敗","evidence_level":"Q2、Q3 法說原話","settle_metric":"Discover 卡放款年比","if_then":["若 2027 Q2 Discover 放款年減仍 ≥2%，則停止加碼並下修網路假設","反向：若 2027 Q2 年減收斂到 1% 以內，則維持"],"evidence_refs":["regulatory_antitrust#3","capital_markets_pricing#5"]},{"axis":"合併沖銷率上升對卡沖銷率下降","cause":"新證據","prior_field":null,"side_a":"Q2 合併淨沖銷率 1.48%，年增 18bp","side_b":"Q3 國內卡沖銷率 3.98%，年降 65bp；逾期率年減 15bp","ruling":"可調和：合併數字受 Discover 併入組合變動與車貸次級占比回升影響；卡業務改善屬實，但逾期已只跟季節性","evidence_level":"10-Q 搜尋摘要與 Q3 法說","settle_metric":"國內卡逾期率年比","if_then":["若國內卡逾期率年比轉升連 2 季，則減碼一半"],"evidence_refs":["financial_capital_credit_cycle#0"]}],"triggers":[{"n":1,"text":"綜效進度驗證","type":"假設驗證","maps_to":"H1","metric":"合併綜效年化金額","threshold":"2027 Q2 財報 ≥22 億美元","action":"達標續抱；<20 億美元停止加碼並下修基本情境 EPS 5%","source_freq":"季度法說會","date":"2027-07","evidence_refs":[]},{"n":2,"text":"國內卡信用轉向","type":"風險","maps_to":"R1","metric":"國內卡季度淨沖銷率與逾期率年比","threshold":"沖銷率 >5.5% 或逾期率年比 ≥+30bp，連 2 季","action":"減碼一半","source_freq":"季度新聞稿、月度信用資料","date":null,"evidence_refs":["financial_capital_credit_cycle#0"]},{"n":3,"text":"聯邦 10% 信用卡利率上限","type":"Single Thing","maps_to":"R2","metric":"S.381／H.R.1944 立法進度","threshold":"出委員會減碼一半；任一院通過清倉","action":"清倉","source_freq":"國會紀錄（事件）","date":null,"evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1"]},{"n":4,"text":"Visa／Mastercard 交換費和解終審","type":"風險","maps_to":"R2","metric":"終審結果與交換費收入變化","threshold":"11 月聽證核准後，2027 Q1 交換費損失大於剩餘綜效","action":"下修基本情境 EPS 並停止加碼","source_freq":"法院公告、季度財報","date":"2026-11","evidence_refs":["regulatory_antitrust#2"]},{"n":5,"text":"回檔分批加","type":"加碼","maps_to":"H1","metric":"股價與國內卡逾期率年比","threshold":"股價 ≤180 美元（前瞻本益比約 8.8 倍）且逾期率年比未轉升","action":"分批加碼至目標部位","source_freq":"每日價格、月度信用資料","date":null,"evidence_refs":[]},{"n":6,"text":"資本緩衝下降","type":"減碼","maps_to":"R1","metric":"CET1","threshold":"<12.0% 或回購暫停","action":"減碼三分之一","source_freq":"季報","date":null,"evidence_refs":[]},{"n":7,"text":"Discover 放款轉正","type":"假設驗證","maps_to":"H3","metric":"Discover 卡放款年比","threshold":"2027 Q2 年減仍 ≥2%","action":"停止加碼","source_freq":"季度法說會","date":"2027-07","evidence_refs":["regulatory_antitrust#3"]},{"n":8,"text":"訴訟與調查","type":"風險","maps_to":"R5","metric":"單案罰款或和解金額","threshold":">10 億美元，或 SEC 調查轉正式執法","action":"減碼三分之一","source_freq":"8-K、10-Q 附註","date":null,"evidence_refs":["sec_investigation_restatement#0","major_events#0"]},{"n":9,"text":"Q4 財報複審","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報","threshold":null,"action":"重跑判斷","source_freq":"季度","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"國內卡季度淨沖銷率","bear_threshold":">5.5%，連 2 季","window":"2026Q4–2027Q4","source":"公司季度新聞稿","last_status":"ok"},{"metric":"國內卡逾期率年比變動","bear_threshold":"≥+30bp，連 2 季","window":"2026Q4–2027Q4","source":"公司月度信用資料與季報","last_status":"ok"},{"metric":"CET1 比率","bear_threshold":"<12.0%","window":"每季","source":"公司季報","last_status":"ok"},{"metric":"合併綜效年化金額","bear_threshold":"2027 Q2 <20 億美元","window":"至 2027-07","source":"公司法說會","last_status":"ok"},{"metric":"聯邦 10% 信用卡利率上限法案","bear_threshold":"任一院通過","window":"持續","source":"國會紀錄","last_status":"ok"}],"action_conditions":{"rearm_trigger":"加碼：2027 Q2 綜效年化 ≥22 億美元且國內卡逾期率年比未轉升；或回檔至 180 美元以下分批加","exec_line":"現價 206.66 美元一帶依裁決建首倉，不追 230 美元以上（前瞻本益比 11 倍以上）；180 美元以下且信用未轉向時分批加","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場仍用併購年的低盈餘與利率上限、交換費和解等監管尾部折價，前瞻本益比約 10 倍只隱含盈餘持平；但前三季已看得到併購後盈餘能力，綜效進度超前、卡信用優於去年同期","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場仍用併購年的低盈餘與利率上限、交換費和解等監管尾部折價，前瞻本益比約 10 倍只隱含盈餘持平；但前三季已看得到併購後盈餘能力，綜效進度超前、卡信用優於去年同期"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=4.44, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Discover 併購綜效如期兌現：合併綜效年化由 2026 Q3 的 18 億美元升到 2027 年底 25 億美元，扣掉交換費和解損失後，盈餘能力仍符合交易時預期","2y":"2027 年底綜效年化 ≥25 億美元；FY2027 EPS ≥23 美元","5y":null,"10y":null,"threshold":"2027 Q2 財報綜效年化 ≥22 億美元；FY2027 EPS ≥23 美元","source":"季度法說會綜效進度、新聞稿 EPS","drift_rule":"綜效或季度 EPS 低於路徑 5% 以上連 2 季為削弱；低於 10% 以上連 3 季為反轉"},{"id":"H2","text":"國內卡信用維持良性：2027 年季度淨沖銷率不超過 5.0%，逾期率年比不轉升","2y":"2027 年國內卡年度淨沖銷率 ≤5.0%","5y":null,"10y":null,"threshold":"國內卡季度淨沖銷率 ≤5.0%；季末逾期率年比變動 ≤+30bp","source":"公司季度新聞稿與月度信用資料","drift_rule":"季度沖銷率超出門檻 5% 以上（>5.25%）連 2 季為削弱；>5.5% 連 3 季為反轉"},{"id":"H3","text":"自有網路放大規模：信用卡開始轉到 Discover 網路，網路交易量維持兩位數成長，Discover 卡放款 2027 下半年恢復正成長","2y":"Discover 卡放款 2027 Q4 年比轉正","5y":"信用卡轉網後，網路交易量年複合成長 ≥15%","10y":null,"threshold":"網路交易量年增 ≥15%（Q3 為 25%，主因借記卡轉網）；Discover 卡放款年減幅逐季收斂","source":"法說會消費金融網路交易量、Discover 卡放款年比","drift_rule":"連 4 季低於門檻 5% 以上為削弱；連 6 季低於門檻 10% 以上為反轉"}],"R":[{"id":"R1","text":"信用循環轉向：逾期改善已轉為只跟季節性，回收順風預期一年內退坡，車貸次級占比回到疫情前；CECL 下準備金一次補提，EPS 會跌得比 2008 年更陡","h_ref":"H2","clock":"🔥","threshold":"國內卡逾期率年比轉升 ≥30bp 連 2 季，或季度沖銷率 >5.5%","evidence_refs":["financial_capital_credit_cycle#0"]},{"id":"R2","text":"監管尾部：聯邦 10% 利率上限提案、Visa／Mastercard 交換費和解（11 月終審）、商家交換費反壟斷訴訟；監管機關也可能限制併購與擴張","h_ref":"H1","clock":"🐢","threshold":"利率上限法案出委員會；和解生效後交換費損失大於剩餘綜效","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#1","regulatory_antitrust#2"]},{"id":"R3","text":"競爭吃掉綜效：大型同業資金成本更低、高端卡行銷競爭，公司 2027 年要再加碼行銷；新支付業者（穩定幣、代幣化存款）攻網路端","h_ref":"H1","clock":"🔥","threshold":"2027 調整後效率比率高於 2026；行銷年增持續高於營收年增 5pp 以上","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"id":"R4","text":"Discover 放款緊縮拖長：7 月法說說谷底約在今年第四季，10 月改口為未來數季續縮再轉正；Brex 收購另有消費者反壟斷訴訟；Q1 財報曾低於預期","h_ref":"H3","clock":"⚡","threshold":"Discover 卡放款 2027 Q2 年減仍 ≥2%","evidence_refs":["regulatory_antitrust#3","capital_markets_pricing#5"]},{"id":"R5","text":"法律與營運：Discover 卡片誤分類（已提列 12 億美元、SEC 調查中）、回饋取消與錯誤註記集體訴訟、360 儲蓄 4.25 億美元和解；核心系統多在 AWS，雲端中斷風險；關稅衝擊車市","h_ref":"H1","clock":"🐢","threshold":"單案罰款或和解 >10 億美元，或 SEC 調查轉正式執法","evidence_refs":["major_events#0","major_events#2","major_events#3","lawsuit_class_action#0","lawsuit_class_action#1","sec_investigation_restatement#0","geo_supply_chain#0","reg_tariff_export#0"]}],"single_thing":{"description":"聯邦信用卡利率 10% 上限立法通過","why_fatal":"國內卡收入率 17.8%、淨利差 8.41% 主要靠循環利息；10% 上限讓次級與近優級客群無法定價，KPMG 指出會導致核貸緊縮、信用可得性下降，卡業務盈餘大幅下降（幅度事實表未涵蓋）","if_happens":"法案出委員會即減碼一半；任一院通過即清倉","how_monitor":"S.381／H.R.1944 委員會進度、期中選舉後國會組成","probability":"12–24 個月約 5%（法案尚未出委員會）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":8.59,"peg_fy2":0.51,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":4.03,"FY2026E":20.56,"FY2027E":24.07,"FY2028E":28.08},"fy_end_month":12,"eps_basis":"Koyfin 共識（事實表未標明 GAAP 或調整後）；基期 FY2025A 為 GAAP 稀釋 EPS 4.03，含 Discover 併購一次性費用與準備金首提，不宜作成長基期，成長改看 FY2026→FY2028"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"Visa／Mastercard 修正和解終審聽證","impact":"中","watch":"是否核准、交換費下調幅度"},{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉（利率上限、CCCA 政治動向）","impact":"中","watch":"國會組成與委員會議程"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與綜效進度","impact":"中","watch":"綜效年化、行銷費用、Discover 放款"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"Discover 舊帳戶轉換完成","impact":"中","watch":"客戶流失、Discover 放款轉向"},{"date":"2027-06","date_precision":"month","type":"regulatory","event":"Fed 年度壓力測試結果","impact":"中","watch":"併入 Discover 後壓力資本緩衝是否重算上調"}]}
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
