你是 DD 管線 v20 的判斷層閘（gate），標的 KLAC（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝4136.0 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KLA Q1 FY27 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi1_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝46.1 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KLA Q1 FY27 新聞稿；營業利益為由損益表項目推算（約 1,904.7M），新聞稿未直接列示（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝45.0 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KLA Q1 FY27 新聞稿；營業利益為推算（約 1,861.7M）（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝1336.2 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KLA Q1 FY27 新聞稿（營運現金流 1,530.9 − 資本支出 194.8）（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi5_guidance_q2_fy2027_reven`（q1_business）｜Guidance: Q2 FY2027 revenue＝4.7B ±0.2B（4.5–4.9B） USD｜期間與口徑：Q1 FY2027 財報（公告於 2026-10-28），指引季別＝季末 2026-12-31／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：KLA Q1 FY27 新聞稿（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027 財報（公告於 2026-10-28），指引季別＝季末 2026-12-31）
- `f_kpi6_non_gaap_diluted_eps`（q1_business）｜Non-GAAP diluted EPS＝1.22 USD｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：KLA Q1 FY27 新聞稿（已調整 2026-06-11 十比一分割）（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_klac_gross_margin_pct`（q2_moat）｜KLAC 毛利率＝61.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_klac_operating_margin_pct`（q2_moat）｜KLAC 營業利益率＝42.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_klac_fcf_margin_pct`（q2_moat）｜KLAC FCF 利潤率＝27.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_asml_gross_margin_pct`（q2_moat）｜ASML 毛利率＝54.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_asml_operating_margin_pct`（q2_moat）｜ASML 營業利益率＝38.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_asml_fcf_margin_pct`（q2_moat）｜ASML FCF 利潤率＝53.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amat_operating_margin_pct`（q2_moat）｜AMAT 營業利益率＝31.09 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_lrcx_operating_margin_pct`（q2_moat）｜LRCX 營業利益率＝36.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LRCX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_8035_t_operating_margin_pct`（q2_moat）｜8035.T 營業利益率＝26.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8035.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8035_t_fcf_margin_pct`（q2_moat）｜8035.T FCF 利潤率＝6.53 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8035.T.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.74 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.04 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.4 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝18856.39 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（23 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝22373.59 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝4.5 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 SBC 84.1M ÷ 推算 GAAP 營業利益 1,861.7M（占營收 2.0%）（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-28））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1251.45 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 5992.64、現金 4741.19（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1302.96 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.532 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝39.58 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝46.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝14.18 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝48.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝157.91 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝27.51 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.74，分子＝快照價 157.91｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝46.2 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝10.98 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.94 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 5.47 → 5.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-8.3 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝39.98｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝169.83 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：部分競爭對手可能捆綁產品並以顯著低於 KLA 的價格銷售競品設備，且面臨專攻局部市場的新興小公司競爭。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-06）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Onto Innovation 在先進封裝檢測、量測挑戰 KLA，Dragonfly 檢測業務 2026Q2 季增30%。
  - 來源：Nasdaq: KLA Gains From Advanced Packaging: Can it Outpace ONTO & AMAT?（as_of 2026-08-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 與 FY2025 各有一家客戶約占總營收 19%（FY2024 約 13%）；10% 以上客戶為 TSMC
  - 來源：SEC EDGAR KLA 10-K FY2026 Item 8（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：週期性疑慮：Lam 稱 2027 成長由 DRAM 領軍，其次先進邏輯與 NAND；Bernstein 估 DRAM 2027 +53%、2028 +37%，中國 2026–27 持平；SEMI 預測報導指出期末將面臨永續性考驗。結構性論點僅見少數分析文章，無共識。
  - 來源：Search aggregation: Lam Research, Bernstein (techflowpost), SEMI forecast coverage（as_of 2026-07-30）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因子提到美國商務部依 Section 232 對半導體及半導體製造設備進口展開國安調查，結果未知，可能帶來額外關稅與貿易限制。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-06）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美國對中國出口管制（Entity List、2022/2023 BIS 規則）限制 KLA 對中國先進製程客戶的銷售、出貨與支援，無法保證出口許可會獲准，影響可能重大。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2025-09 BIS 發布 Affiliates Rule（持股50%以上關聯方納入管制），2025-11 暫停一年至 2026-11。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-06）｜affects：triggers、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Section 232 半導體及設備調查結果未知，可能帶來額外關稅；既有關稅已推升KLA進口零組件成本；2026-02 最高法院裁定IEEPA關稅無授權，關稅與退款不確定性升高。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：2026-04 BIS 出口管制更新被報導為KLA FY2026 營收逆風（限制特定先進設備出口及對特定中國客戶服務），股價當日跌約4.2%；二手聚合來源，未核一手。
  - 來源：Yahoo Finance 文章（搜尋摘要）（as_of 2026-04-16）｜affects：thesis.R、valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：部分零件與原料僅單一或少數供應商可供應，斷供會延誤出貨(FY2020–FY2025 10-K 均有此語)
  - 來源：KLA Form 10-K FY2025 (SEC)（as_of 2025-08-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 中國營收與前一年持平：成熟製程投資抵銷出口管制對先進技術交易的衝擊;出口管制預估至 2026 曆年累計減少營收 $300–350 百萬
  - 來源：KLA Form 10-K FY2026 (SEC) / Q1 FY2026 earnings call（as_of 2026-08-01）｜affects：thesis.R、valuation、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：KLA 10-K FY2026 risk factor：公司稱無法預測 AI 發展的步調，AI 驅動的顛覆可能以難以預測的方式影響半導體供應鏈；競爭對手可能在 AI 策略上更成功。未點名具體替代技術。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子列「可能無法跟上產業技術變化」，為公司自述的技術風險之一。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-06）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":319.8,"bear_5y_price":96.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":32.4,"ev5y_pct":28.4,"irr_base_pct":5.8,"asym_ratio":2.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.74,"pe":27.51,"basis":"FY1（2027 年 6 月止財年）共識 EPS 5.74，現價 157.91 元；終端倍數同樣是該財年 EPS 的本益比，與起點同口徑"},"eps":{"bull":[5.95,7.6,9.3,10.8,12.3],"base":[5.74,7.0,7.9,8.6,9.5],"bear":[5.6,5.9,4.8,5.3,6.0]},"pe":{"bull":26,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.532,"net_buyback":1.3},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### KLAC_Q4_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：FY26 九月季營收財測 $4B ±$200M（原話："revenue of $4 billion, plus or minus $200 million."）
- 2026-07-28｜CFO｜guidance：九月季毛利率財測 62.5% ±1pp（原話："forecasted to be 62.5%, plus or minus 1 percentage point."）
- 2026-07-28｜CFO｜guidance：九月季 non-GAAP EPS 財測 $1.16 ±$0.10（原話："EPS is expected to be $1.16, plus or minus $0.10"）
- 2026-07-28｜CFO｜guidance：九月季毛利率財測較上季財測高 75bp，管理層歸因於營收成長的營運槓桿（原話："it is up 75 basis points from gross margin"）
- 2026-07-28｜CFO｜guidance：日曆 2026 WFE（含先進封裝）預期上修至 150 億美元出頭區間，前次為 140 億以上（原話："$150 billion range in calendar 2026, up from our prior"）
- 2026-07-28｜CFO｜guidance：2026 下半年營收較上半年成長約 20%（原話："over the first half to be approximately 20%"）
- 2026-07-28｜CEO｜guidance：預期 2026 下半年動能加速、2027 持續顯著成長（原話："significant growth to continue in calendar 2027."）
- 2026-07-28｜CFO｜guidance：2027 WFE 市場共識約 1,900 億美元，管理層稱換算為約 20% 中段成長（原話："that's somewhere in and around the $190 billion range."）
- 2026-07-28｜CFO｜guidance：$190B 對應 mid-20s 成長率，與 2026 相近（原話："$190 billion or so translates into a mid-20s type"）
- 2026-07-28｜CEO｜guidance：先進封裝製程控制系統 2026 營收約 $1.1B，年增逾 70%（原話："$1.1 billion in calendar 2026, up more than 70%"）
- 2026-07-28｜CEO｜guidance：Specialty Process、PCB、元件檢測合併產品 2026 預期成長逾 25%（原話："grow over 25% in calendar 2026, we are encouraged"）
- 2026-07-28｜CFO｜guidance：服務業務長期目標成長 13-15%，今年在區間底部，預期明年朝高端（原話："This year, we're right now at the bottom of that range."）
- 2026-07-28｜CFO｜guidance：管理層估計 backlog/RPO 約 $125 億，且預期持續成長（原話："backlog would be at about $12.5 billion"）
- 2026-07-28｜CFO｜guidance：半導體製程控制業務預期成長比公司整體快至少數個百分點（原話："it will grow at least a few points"）
- 2026-07-28｜CFO｜margin：Q 毛利率 62.4%，主因較有利的服務組合與製造規模，抵銷記憶體價格與關稅（原話："Gross margin was 62.4%."）
- 2026-07-28｜CFO｜margin：本季增量營業利益率 59%（原話："Incremental operating margin in the quarter was 59%."）
- 2026-07-28｜CFO｜margin：記憶體採購價格造成的毛利率逆風（原話："headwinds as related to memory pricing."）
- 2026-07-28｜CFO｜margin：管理層表示記憶體逆風影響可能略多於 100bp（原話："It's probably a little bit more than that."）
- 2026-07-28｜CFO｜margin：2026 全年毛利率原指引 62% 上下，本次稱將高於此（原話："gross margins likely being in the 62%, plus or minus"）
- 2026-07-28｜CFO｜margin：長期毛利率模型為 63.5% ±500bp，並稱增量毛利率 60-65%（原話："63.5%, plus or minus 500 basis point view"）
- 2026-07-28｜CFO｜margin：九月季營業費用約 $690M，之後數季每季增 $15-20M（原話："grow by roughly $15 million to $20 million sequentially"）
- 2026-07-28｜CFO｜margin：長期增量營業利益率模型 40-50%（原話："deliver 40% to 50% incremental operating margin leverage"）
- 2026-07-28｜CFO｜margin：記憶體逆風預期延續至明年，之後定價有望由逆風轉為順風（原話："memory headwinds we're experiencing today likely continues"）
- 2026-07-28｜CFO｜margin：承上，預期定價正常化（原話："start to see some normalization on the pricing front"）
- 2026-07-28｜CFO｜margin：服務收入約 80% 為合約型（原話："80% of revenue is contract-based"）
- 2026-07-28｜CEO｜commitment：新產品推出時才做新定價決定；既有產品以其他方式分享價值（原話："that's when new pricing decisions get made."）
- 2026-07-28｜CFO｜commitment：對 Arcuri 追問：已接單後難以改價，漲價主要靠新產品（原話："hard to go back to your customers after you've taken orders"）
- 2026-07-28｜CEO｜commitment：管理層稱正增加產能以支應預期需求（原話："we are adding capacity to support expected demand"）
- 2026-07-28｜CFO｜commitment：願意承擔為維持產能彈性的成本（原話："we will take the cost of that flexibility"）
- 2026-07-28｜CFO｜commitment：願意在特定產品類型押注庫存（原話："I'm willing to make bets from an inventory point of view"）
- 2026-07-28｜CFO｜commitment：與關鍵供應商洽談 2029 年以後的產能協議（原話："our needs, we believe, in the 2029 and beyond time frame."）
- 2026-07-28｜CFO｜commitment：2030 目標模型：KLA 市占較 2025 增加 150bp ±25bp（原話："150 basis points, plus or minus 25 basis points"）
- 2026-07-28｜CEO｜commitment：若市場遠高於模型假設，管理層稱公司將超越 2030 模型（原話："then we would exceed the model that we laid"）
- 2026-07-28｜CEO｜commitment：管理層稱目前不會重設 2030 目標（原話："we're in no position to reset anything as it pertains to"）
- 2026-07-28｜CFO｜risk：2026 上半年曾遇長交期物料供應短缺（原話："some supply chain shortages as it relates to some of our"）
- 2026-07-28｜CFO｜risk：光學元件等長交期項目擴產需 12-24 個月（原話："it can take 12 to 24 months to"）
- 2026-07-28｜CFO｜risk：晶圓廠空間受限（原話："fab space limitations, we continue to see the market"）
- 2026-07-28｜CFO｜risk：部分產品交期可達 18-24 個月（原話："it can be closer to 18 to 24 months."）
- 2026-07-28｜CFO｜risk：整體交期約 12 個月（原話："are in about the 12-month range, but on certain"）
- 2026-07-28｜CEO｜competition：製程控制為高混合低量市場，管理層稱公平競爭下表現佳（原話："we're allowed to compete, we do quite well"）
- 2026-07-28｜CEO｜competition：管理層否認競爭環境有變，稱為淨市占增加者（原話："we're anything but net share gainers"）
- 2026-07-28｜CFO｜competition：競爭對手能出貨進中國晶圓廠而 KLA 不能（原話："China that we haven't been able to ship into."）
- 2026-07-28｜CEO｜competition：e-beam 等原市占較低市場出現正向動能（原話："We're definitely seeing positive momentum in markets"）
- 2026-07-28｜CFO｜product：HBM 部分產品的製程控制強度可媲美先進邏輯（原話："intensity levels that are rivaling what we see in advanced"）
- 2026-07-28｜CFO｜product：先進封裝市場成長預期由年初約 20% 升至 30% 中高段（原話："the market is kind of a mid- to high 30s growth"）
- 2026-07-28｜CFO｜product：Orbotech 相關業務長期 CAGR 中段約個位數高段（原話："somewhere in the high single-digit range"）
- 2026-07-28｜CFO｜customer：九月季半導體客戶中晶圓代工/邏輯占比預計約 73%（原話："forecasted to increase to approximately 73%"）
- 2026-07-28｜CFO｜customer：2026 全年晶圓代工/邏輯占系統營收約 65% 上下（低至中 60%）（原話："closer to 65-ish percent, so call it kind of low"）
- 2026-07-28｜CEO｜customer：本季服務營收 $820M（原話："KLA Services delivered $820 million revenue"）
- 2026-07-28｜CFO｜capital_allocation：本季回饋股東 $876M（原話："KLA returned $876 million to shareholders"）
- 2026-07-28｜CFO｜capital_allocation：過去 12 個月資本回饋總額 $3.3B（原話："total capital returns were $3.3 billion"）
- 2026-07-28｜CFO｜capital_allocation：已投資營運資金與設施以支應成長（原話："meaningful investments in our working capital and facilities"）

### KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 重申 3 月季度財測：營收 33.5 億美元、non-GAAP EPS 9.08 美元。（原話："revenue at $3.35 billion, non-GAAP diluted EPS of $9.08"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說明 WFE（含先進封裝）預期 1,350–1,400 億美元，並提到先前的「30 多%中段」輪廓。（原話："$135 billion to $140 billion. We talked about a mid-30s"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說 2026 全公司營收年增預期落在高個位數以上的「高十幾%」。（原話："somewhere in the high teens in terms of year-over-year"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說半導體製程控制系統成長會比全公司快。（原話："process control systems growth should be faster than that"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：Q&A 中 CFO 補充 Semi PC 2026 成長將接近 20%。（原話："Semi PC will be closer to 20%"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 說客戶對 2027 的能見度很高，並表示可看 12–24 個月。（原話："visibility 12 to 24 months out is really uncommon"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 表示 2027 產業 WFE 年增率預期與 2026 相近或更高。（原話："perhaps even higher than what we're seeing in 2026"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 在開場說暫不談上下半年的拆分，等 6 月季度再說。（原話："really want to get into it at this point"）
- 2026-03-12｜Richard Wallace (CEO)｜guidance：2030 目標：營收 260 億美元，區間正負 25 億。（原話："$26 billion in 2030 revenue, plus or minus $2.5 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：2030 目標 non-GAAP EPS 84 美元，並持續產生強勁自由現金流。（原話："EPS of $84 and should continue to drive strong free cash"）
- 2026-03-12｜Richard Wallace (CEO)｜guidance：2030 模型假設的市場口徑：WFE 加封裝規模 2,150 億美元。（原話："We're showing $215 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 拆解 2030 模型：半導體營收年增 11%，WFE 約 12%。（原話："semiconductor revenue is growing 11%, that WFE will grow"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：CFO 拆解 2030 模型：半導體製程控制系統年複合成長 16.5%，對比產業 12%。（原話："semi PC systems, 16.5% CAGR against"）
- 2026-03-12｜Brian Lorig (Service)｜guidance：服務業務成長率目標由 12–14% 上調至 13–15%。（原話："from 12% to 14% to 13% to 15%, which means at the upper"）
- 2026-03-12｜Brian Lorig (Service)｜guidance：服務營收目標：區間上緣下 2030 年接近 60 億美元。（原話："revenue to nearly $6 billion and at the upper end of the"）
- 2026-03-12｜Bren Higgins (CFO)｜guidance：2030 模型假設：晶圓代工/邏輯占比 60% 以上（下緣）。（原話："We expect foundry logic to be 60% plus"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 目標毛利率 63.5%，區間正負 50 bps。（原話："63.5% gross margin, plus or minus 50 basis points"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：CFO 說 2030 模型已吸收約 50 bps 的關稅逆風。（原話："basis point headwind related to tariffs"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 營業利益率目標 45–47%（中位 46%，對比目前中位 42%）。（原話："translates into 45% to 47%, so 46% at the midpoint"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2030 費用率假設：R&D 約 11%（上一版計畫為 13%）。（原話："we think the R&D stays about 11%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：SG&A 費用率目標由約 8.5–9% 降到約 7%。（原話："SG&A basically comes down from where we were around 8.5%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2025 營業利益率 43.6%，高於當時 41–43% 的目標區間。（原話："We said our target range was 41% to 43%"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：2022–2025 增量營業利益率 51%，略高於模型上緣。（原話："incremental operating margins at 51%, so slightly ahead"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：增量毛利率相對 2022–2025 基準預期再改善約 1.3 個百分點。（原話："1.3 points of improvement in incremental gross margins"）
- 2026-03-12｜Bren Higgins (CFO)｜margin：CFO 指出服務毛利率較低，但隨系統成長與增量改善，對整體毛利的拖累會減輕。（原話："Service carries a lower gross margin."）
- 2026-03-12｜Ahmad Khan (Systems)｜margin：2025 全公司毛利率 62.8%，CFO/系統總裁以此作為產品差異化指標。（原話："62.8% overall KLA gross margin"）
- 2026-03-12｜Richard Wallace (CEO)｜margin：CEO 說明管理市占率時以毛利率設限。（原話："but we constrain market share by gross margin"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：宣布第 17 年連續調升股利，季配息由 1.90 美元升到 2.30 美元（+21%）。（原話："a 21% increase to $2.30 per quarter from"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：新增 70 億美元庫藏股授權，加上既有餘額合計約 110 億美元。（原話："additional share repurchase authorization of $7 billion"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2030 資本回饋目標：占自由現金流 90% 以上（先前 85% 以上）。（原話："greater than 90% of the free cash flow we'll generate"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：股利政策：每年配息占自由現金流 25–30%。（原話："consistent cadence of 25% to 30% of the free cash flow we"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2026–2030 的資本運用以庫藏股為主。（原話："repurchases as we deploy that cash"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：槓桿目標：總槓桿 1.5–2 倍，目前約 1 倍；營運所需現金 40–50 億美元。（原話："target at 1.5 to 2x gross leverage, we're about 1x today"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：2022 以來流通股數下降約 18%。（原話："drove our shares outstanding down about 18%"）
- 2026-03-12｜Bren Higgins (CFO)｜capital_allocation：已投入約 2.5 億美元擴充供應商產能。（原話："invested about $250 million over the last couple of years"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 表示現任管理層曾承諾 2019 年投資人日目標並達成。（原話："committed to our 2019 Investor Day and hit it"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO 回顧上一版目標：市占提升目標 100 bps，實際超過 150 bps。（原話："We improved it by over 150"）
- 2026-03-12｜Ahmad Khan (Systems)｜commitment：系統總裁：2030 製程控制占 WFE 比重由 7.4% 升至約 9%。（原話："by 2030, we're assuming that it's going to get to around 9%"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO：2030 計畫再取得 150 bps 的市占。（原話："We're going to gain another 150 basis points of share"）
- 2026-03-12｜Bren Higgins (CFO)｜commitment：CFO 稱對外計畫與內部計畫與激勵機制一致。（原話："There's no daylight between the external plans"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 稱管理層激勵以相對自由現金流衡量。（原話："It's on relative free cash flow"）
- 2026-03-12｜Richard Wallace (CEO)｜commitment：CEO 形容 2030 目標設定偏保守，並說這次不是「不同」而是規模更大。（原話："We're generally pretty conservative"）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 稱製程控制市占為最近競爭對手的 6.5 倍（7 年前為 4 倍）。（原話："we're now 6.5x our nearest"）
- 2026-03-12｜Ahmad Khan (Systems)｜competition：系統總裁給出市占口徑：製程控制市占 56.5%，自 2021 年起上升 2 個百分點。（原話："We are now at 56.5% share, up 2% since 2021."）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 說競爭對手無法像 KLA 在每個子系統做客製化。（原話："Our competitors do not. They can't afford it."）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 回應光罩檢測 DUV/e-beam/actinic 路線之爭：稱市占軌跡與競爭對手宣稱難以對上。（原話："it would be hard to reconcile the two"）
- 2026-03-12｜Richard Wallace (CEO)｜competition：CEO 對光學與 e-beam 何者勝出的辯論表示從未定論；去年 Gen 4 出貨多於 Gen 5。（原話："Last year, we sold more Gen 4 than Gen 5."）
- 2026-03-12｜Bren Higgins (CFO)｜competition：CFO 指出先進封裝市場中，傳統前段設備廠都在瞄準此機會。（原話："all the traditional front-end players are targeting"）
- 2026-03-12｜Ahmad Khan (Systems)｜competition：系統總裁說明光罩檢測需偵測 100% 缺陷，因此需組合多種系統。（原話："it's very critical that you detect 100% of the defects"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：e-beam 業務由 7,500 萬–1 億美元成長至約 4 億美元（不含光罩 e-beam）。（原話："Today, we are at $400 million"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：2025 先進封裝營收 9.5 億美元，並稱製程控制市占第一。（原話："$950 million in advanced packaging revenue in 2025"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：資料分析軟體業務目前規模約 2.5 億美元。（原話："$250 million, software business that is doing quite well"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：DRAM 設備市場成長 2 倍，KLA DRAM 營收成長 3 倍；2025 增量強度貢獻 4.5 億美元。（原話："DRAM wafer equipment market went up by 2x"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：系統總裁說 KLA 正在開發 actinic 光罩檢測系統。（原話："we're developing actinic inspection also"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：系統總裁說目前沒有 DUV 與 e-beam 抓不到的缺陷類型問題。（原話："Currently, we don't have a type of defect problem"）
- 2026-03-12｜Ahmad Khan (Systems)｜product：Q&A 中系統總裁量化良率價值：良率每提升 1% 對應客戶至少 1.5 億美元利潤。（原話："could lead to at least $150 million in profit"）
- 2026-03-12｜Brian Lorig (Service)｜product：服務業務：設備中位退役年限由 10 年升至 24 年以上。（原話："increased from 10 years to more than 24 years"）
- 2026-03-12｜Brian Lorig (Service)｜product：服務合約占服務營收比重由 2005 年約 60% 升至 80% 以上。（原話："Today, we're more than 80%"）
- 2026-03-12｜Brian Lorig (Service)｜product：裝機基礎中個別機台兩年期間有營收的經常性比率。（原話："individual tools over a 2-year period recurs in revenue"）
- 2026-03-12｜Ahmad Khan (Systems)｜customer：系統總裁指新型光罩電子束檢測機是與 TSMC 合作開發。（原話："is TSMC because we have published a paper recently"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 稱客戶結構轉向超大規模雲端業者，設計案數量大增。（原話："another hyperscaler that announced 4 new designs"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 轉述前段客戶要求把 KLA 產品線改成可用於封裝，並稱不會因封裝打折。（原話："we definitely need you to take your portfolio"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 稱客戶的客戶也因供給受限而感到挫折。（原話："they're all frustrated that they're supply constrained"）
- 2026-03-12｜Richard Wallace (CEO)｜customer：CEO 說 AI 贏家是誰不影響 KLA。（原話："KLA wins no matter who wins"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：開場提到出口管制對服務業務有影響。（原話："despite some of the export control effects on service"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說上一輪服務成長在目標區間內，但受進廠限制干擾。（原話："had some disruption related to access to fabs"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：供應鏈：材料採購到出貨的自然時間柵約 60 週。（原話："the natural time fence is almost 60 weeks"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說明上半年產能受限於前置時間，下半年彈性較大。（原話："we have a lot more flexibility and capacity"）
- 2026-03-12｜Richard Wallace (CEO)｜risk：被問及中東局勢是否造成供應中斷，CEO 回答目前沒有。（原話："Not currently any disruption."）
- 2026-03-12｜Bren Higgins (CFO)｜risk：CFO 說明產業結構轉向後，傳統（legacy）投資將占 WFE 的 25–30%。（原話："the legacy business will be 25% to 30% of overall WFE"）
- 2026-03-12｜Richard Wallace (CEO)｜product：敘事變化：CEO 針對「KLA 不是記憶體玩家」的看法表示不再成立（HBM）。（原話："think KLA is not a memory player, it's not true"）
- 2026-03-12｜Bren Higgins (CFO)｜customer：敘事變化：CFO 說先進封裝上一輪投資人日沒有談過。（原話："We didn't talk about it before"）
- 2026-03-12｜Bren Higgins (CFO)｜risk：敘事變化：記憶體占比上升後，CFO 稱業務對產品組合的敏感度降低。（原話："it moves from that into the low 60 range"）
- 2026-03-12｜Bren Higgins (CFO)｜customer：敘事變化：記憶體與封裝客戶過去的「計費」服務心態正在改變。（原話："started to change the service mindset"）

### 問答異常語氣（迴避／改口／保留）
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Arcuri：為何不能漲價抵銷記憶體成本（ASML 都在漲 EUV 價）｜答法：未正面回答為何做不到，改談新產品時才調價、已接單難改價，並說 'pretty comfortable with our view'
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Arcuri：12 月季隱含毛利率是否同樣持平｜答法：未給數字，稱看產品組合、'could be a little bit higher, too'，回到長期 60-65% 區間
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Krish：是否漲價、何時生效、對毛利影響｜答法：Rick 稱有討論分享價值，未給漲價幅度或生效時間
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Rasgon：按最樂觀情境擴產是什麼意思｜答法：Rick 稱前述說法 'maybe it was a little unclear'，重新澄清為僅支撐產業能支撐的情境
- KLAC_Q4_2026_Earnings_Call_20260728.md｜問：Malik：是否參與 SpaceX/Terafab 專案｜答法：拒答具體客戶合作，僅稱創新者都會找上 KLA
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Rasgon：2026 受無塵室限制，為何 2027 WFE 成長不會更快？KLA 2027 是否會超越 WFE？｜答法：CFO 回到「至少一樣快」，改談動能與客戶參與、未給 2027 數字，說「等到那時再看」。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Rasgon：2026 高十幾% 是否意味下半年對上半年約成長 20%？｜答法：CFO 先說等季度結束與 6 月財測，再表示下半年相當強、Semi PC 約 20%，並加上「看客戶動能是否改變」的保留語氣，沒有給半年對半年數字。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Muse：2030 市占再增 150 bps 中有多少來自先進封裝？客戶是否願意為封裝付更高價？｜答法：CEO 與系統總裁以客戶要求的軼事和技術論述回答；CFO 明說不會給具體市占數字，也未直接回答封裝 ASP 溢價問題。
- KLAC_Analyst_Investor_Day_KLA_Corporation_20260312.md｜問：Arya：若記憶體占比擴大，對 KLA 市占成長潛力的影響？｜答法：CFO 說「敏感度降低」，改談產業效率、legacy 占比與 R&D 圖，未量化記憶體占比上升對市占的影響。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：KLA distribution channel disruption OR shift 2026；KLAC KLA business model transition subscription OR platform 2026 services revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260729","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"製程控制份額守住或擴張，且服務業務維持 13-15% 複合成長（結構性假設：KLA 是產業複雜化的收租者）"},{"id":"H2","text":"設備支出上行延續至 2028，FY2027/FY2028 EPS 路徑兌現（成長兌現的操作性假設）"},{"id":"H3","text":"入場倍數自 37x 向 30x 以下正常化——這是進場條件，不是業務假設（估值修復的市場假設）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"設備支出在 2028 進入消化期，且市場提前 2-4 季反應。SEMI 2026 年中預測 WFE 2026 +23.1%、2027 +21.8%、2028 +14.1%——三年累計成長逾 70%，屆時的絕對基數（約 $200B）已接近管理層 2030 模型假設的 $215B，等於整輪循環被提前三年跑完。獨立研究亦指出 2028-2029 存在實質過剩情境（Samsung／SK 海力士新廠 2027 下半年才量產、Micron 愛達荷廠 2027 年中投產，供給集中在 2028 落地）。"},{"id":"R2","text":"出口管制與關稅升級。已知量化影響：華虹禁運等管制未來 5 季減少 $300-350M 營收；Section 232 對特定先進半導體品項 25% 關稅（2026-01-15 生效）已列入毛利率逆風。未知風險是管制範圍自先進節點外溢至成熟節點——中國仍占營收 26%。"},{"id":"R3","text":"虛擬量測與客戶自建檢測能力的長期侵蝕。晶圓廠與大型設備商推進以製程機台感測資料 ＋ AI 模型取代部分實體量測步驟；同時 Applied Materials 在本季度被分析師點名「談製程控制的著力增加」。這是慢變數，不會在一兩季顯形，但會逐年壓縮 KLA 在成熟節點與非關鍵層的可服務市場。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY27共識本益比≤34x（約$175）分批starter；≤30x（約$154）加碼；或FY27/FY28共識3個月上修≥10%使同價位倍數下修","irr_base_pct":6.2,"ev5y_pct":35.6,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":3.3,"ev5y_pct":35.6,"irr_base_pct":6.2,"max_dd_pct":-60.0,"bull_5y_price":366.0,"bear_5y_price":119.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"FY27共識本益比≤34x（約$175）分批starter；≤30x（約$154）加碼；或FY27/FY28共識3個月上修≥10%使同價位倍數下修","price_at_dd":190.8,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"KLAC","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"KLA Corporation"},"oneliner":"製程控制龍頭基本面還在加速：12 月季營收指引 47 億美元、2027 年 WFE 上看 2000 億美元以上，股價卻比前份低 17%，FY1 本益比降到 27.5 倍。估值回到合理，但 2027 年記憶體約占業務六成、循環已到後段，FY1、FY2 獲利本身就是多空爭點；先觀望，首批等 1 月法說確認 2027 年 WFE 與 3 月季指引再建。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/KLAC_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺晶圓廠良率的錢：先進製程與記憶體新廠每提升 1% 良率，客戶至少多賺 1.5 億美元，KLA 用檢測量測機台和合約型服務分走其中一塊；錢卡在先進邏輯、HBM／DRAM 與先進封裝的量測節點。","reasoning":"營收結構：FY2026（至 2026-06）營收 135.8 億美元、年增 11.7%；半導體製程控制段年增 12%（晶圓代工／邏輯與記憶體先進製程、先進封裝、服務帶動），PCB 與元件檢測段年增 21%，特殊半導體製程段年減 1%（中國較弱）。最新一季（2026-09 季）營收 41.4 億、季增 13%、年增 29%；毛利率 62.7%，non-GAAP 營益率 46.1%（史上首次破 46%），GAAP 營益率 45.0%，自由現金流 13.4 億；服務 8.5 億、年增 14%，約占營收兩成，其中約八成是合約型。12 月季指引營收 47 億±2 億、毛利率 62.5%±1pp、non-GAAP EPS 1.44±0.11。客戶結構：12 月季半導體系統營收晶圓代工／邏輯約 60%、記憶體約 40%（DRAM 占記憶體 84%），2027 年記憶體預期升到約六成。產業時鐘判擴張期（II）：WFE 2026 年上修到約 1550 億、2027 年預期超過 2000 億，交期約 12 個月且在拉長，KLA 全年供不應求；已出現客戶要求出貨但廠房未完工的過熱前兆，但沒有價格戰或庫存過剩。供需持久性：邏輯與封裝段偏結構性持久（AI 帶動量測強度上升、SEMI 預測 300mm 設備支出 2029 年前每年雙位數成長），記憶體段屬週期性、2028 年後有反轉風險（Bernstein 估 DRAM 設備 2027 年 +53%、2028 年 +37%）。議價權：錢卡在 KLA 這一節點，製程控制份額 56.5%、為最近對手 6.5 倍；上游光學元件單一或少數供應，KLA 需出資擴產；下游最大客戶（TSMC）連兩年約占營收 19%，屬單點依賴但未到必須拆列的程度。產業態勢三軸：競爭面靜態（Onto 只在封裝點狀挑戰）、結構面轉好（量測強度上升、利潤池往量測移）、其他結構變數惡化（出口管制、Section 232、關聯方規則），合判雙向拉鋸。通路與商業模式轉移這一軸沒有找到證據（經銷通路、訂閱或平台化兩組查詢都沒有相關結果）；服務約八成已是合約型，這一軸屬尾部風險，缺口不改變本次結論。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_margi","f_kpi2_gaap_operating_margin","f_kpi3_free_cash_flow","f_kpi5_guidance_q2_fy2027_reven","f_kpi6_non_gaap_diluted_eps","f_earnings_recency"],"verdict_values":{"revenue_quality":"系統約八成、服務約兩成；服務約 80% 為合約型，機台中位退役年限拉長到 24 年以上，裝機基礎帶來經常性收入；系統端有約 125 億美元 backlog（7 月口徑）與約 12 個月交期，未來三到四季能見度高，但系統營收仍隨 WFE 循環","unit_econ_note":"良率每 1% 值客戶至少 1.5 億美元利潤（投資人日），KLA 依良率價值分潤；長期增量營益率 40–50%，最近一季營益率季增 240bp 到 46.1%；記憶體元件漲價壓毛利超過 100bp，既有合約難轉嫁","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"寡占製程控制加合約型服務，毛利率 61.5% 高於全部設備同業，但系統營收隨 WFE 循環；2027 年記憶體占比升到約六成，循環屬性變重"},"industry":{"clock_phase":"II","sd_verdict_source":"邏輯與封裝段結構性持久、記憶體段週期性將反轉：SEMI 300mm 展望（2026-10）預測設備支出 2029 年前每年雙位數成長，但 Bernstein 估 DRAM 設備 2027 年 +53%、2028 年 +37%，SEMI 也指出期末將面臨永續性考驗","bargaining":{"up":"光學等長交期關鍵零件只有單一或少數供應商，擴產要 12–24 個月，KLA 已出資約 2.5 億美元擴充供應商產能；記憶體元件漲價直接壓 KLA 毛利","down":"客戶高度集中，單一客戶（TSMC）FY2025、FY2026 各約占營收 19%；但量測是良率關鍵，管理層稱以毛利率為份額設限，議價權偏在 KLA 一側","geo":"國際營收約占 87%；中國 2026 年約 27–29%、2027 年預期 20% 出頭；製造據點在美國、新加坡、以色列、中國與歐洲"},"profit_pool_dir":"利潤池往量測移：製程控制占 WFE 比重由 2025 年約 7.5% 往 2030 年約 9% 走（投資人日），DRAM 部分產品量測強度已接近先進邏輯","tam_table":[{"item":"WFE（含先進封裝）2026 年","value":"約 1550 億美元（10 月由 7 月的 1500 億出頭上修）"},{"item":"WFE 2027 年","value":"超過 2000 億美元（管理層 10 月）；賣方 1930–2230 億，Morgan Stanley 稱買方預期約 2300 億以上"},{"item":"KLA 占 WFE 比重","value":"2025 年約 7.5%，2030 年目標約 9%"},{"item":"製程控制份額","value":"56.5%（2021 年起 +2pp），為最近對手 6.5 倍"},{"item":"先進封裝製程控制系統","value":"2026 年約 11 億美元、年增逾 70%"},{"item":"服務","value":"單季 8.5 億美元、年增 14%，2030 年目標近 60 億美元"},{"item":"營業利益池占比 5 年前到現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河擴大中：執行力擴大（份額 56.5%、為最近對手 6.5 倍，DRAM 與封裝量測強度上升），定價力穩定（毛利率 61.5% 高於全部同業，但記憶體成本無法即時轉嫁）。","reasoning":"機制：良率經濟加上配方綁定。每個子系統客製、多代產品並存（去年 Gen 4 出貨多於 Gen 5），機台綁在客戶製程配方與良率資料上，換供應商要重新認證該製程層；CEO 稱對手無力在每個子系統做客製。方向證據：同業 ROIC 事實表未涵蓋，改用營益率差當可比軸——KLA TTM 營益率 42.6%，比 ASML 高 4.1pp、Lam 高 5.7pp、AMAT 高 11.6pp、東京威力高 16.3pp；毛利率 61.5% 甚至高於 ASML 的 54.3%。同業只有一期 TTM，利差擴大或持平無法直接驗證，以 KLA 自身營益率 FY2023→FY2026 由 38.1% 升到 41.7%、製程控制份額 2021 年起升 2pp 到 56.5%（對最近對手由 4 倍拉到 6.5 倍）作為利差未收窄的替代證據，執行力與定價力各給 9 分。定價力的上限：既有合約與 backlog 難漲價，記憶體成本只能靠新產品與減少用量消化，毛利率回到 63–64% 要等 2027 年中後段。反向證據：2026 年占 WFE 份額約降 20bp（供貨不足、backlog 同時成長）、Onto 封裝檢測季增 30%、中國客戶在管制下改買對手，皆屬點對點威脅，不扣分。當期 ROIC：稅後營業利益率約 36%（42.6%×0.855），投入資本事實表未涵蓋、周轉率無法驗證，推定為高利益率×高周轉。持續期：需求基礎值、決策層級 🟢；價值鏈分配、社會容忍度 🟡。再投資報酬（代理值）：稅後營業利益＝營業利益×（1−14.5%）。FY2023 營收 104.96 億美元×38.06%＝39.95 億，稅後 34.16 億；FY2026 135.79 億×41.69%＝56.61 億，稅後 48.40 億，三年增 14.25 億。同期再投資以稅後營業利益減自由現金流近似：FY2024 0.77 億、FY2025 5.41 億、FY2026 10.73 億，合計 16.91 億。增量報酬約 14.25÷16.91≈84%；FY2026 再投資率約 10.73÷48.40≈22%；內生成長上限約 84%×22%≈18.7%（用三年平均再投資率 13.8% 則約 11.6%）。這組數字偏向高估增量報酬：分子含 FY2024 谷底後的循環回升，分母沒算費用化的研發。含意：新增資本報酬極高但能投進去的錢不多，成長主要靠產業擴張與營運槓桿，多餘現金配回股東是對的做法。","fact_refs":["f_peer_klac_gross_margin_pct","f_peer_klac_operating_margin_pct","f_peer_klac_fcf_margin_pct","f_peer_asml_gross_margin_pct","f_peer_asml_operating_margin_pct","f_peer_asml_fcf_margin_pct","f_peer_amat_operating_margin_pct","f_peer_lrcx_operating_margin_pct","f_peer_8035_t_operating_margin_pct","f_peer_8035_t_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"良率經濟加配方綁定：機台綁在客戶製程配方與良率資料上，換供應商要重新認證該製程層；每個子系統客製、多代產品並存，對手難以全面跟進研發","execution":9,"pricing":9,"grade":"A","trend":"↑","trend_evidence":"執行力擴大：製程控制份額 2021 年起升 2pp 到 56.5%、對最近對手由 4 倍拉到 6.5 倍；BofA 晶圓檢測份額 81.9%、年增 83bp；DRAM 部分產品量測強度接近先進邏輯；先進封裝製程控制 2026 年增逾 70%、約為封裝市場成長兩倍。定價力穩定：毛利率 62.7%，12 月季指引 62.5%，回到 63–64% 要等 2027 年中後段。反向：2026 年占 WFE 份額約降 20bp，歸因供貨不足","competitor_notes":[{"name":"ASML","strategy_note":"毛利率 54.3%、營益率 38.6%，皆低於 KLA；FCF 利潤率 53.2% 遠高，反映預收款結構而非定價力；10-K 點名的對手之一，但主業微影，與 KLA 互補多於正面交鋒"},{"name":"AMAT","strategy_note":"營益率 31.1%，比 KLA 低 11.6pp；全線設備商最有條件捆綁低價銷售量測機台，前份已記分析師點名其加重製程控制，是捆綁風險的主要來源"},{"name":"LRCX","strategy_note":"營益率 37.0%，以蝕刻沉積為主，不是量測直接對手；其稱 2027 年成長由 DRAM 帶頭，是記憶體循環風險的旁證"},{"name":"8035.T","strategy_note":"營益率 26.3%、FCF 利潤率 6.5%，利潤池遠小於 KLA；非量測主要對手，作為設備商利潤率的下緣參照"},{"name":"Onto Innovation","strategy_note":"先進封裝檢測量測最直接的對手，Dragonfly 檢測 2026 年第二季季增 30%；混合鍵合要求 100 奈米級靈敏度後，KLA 高階系統的優勢較明顯，目前屬點對點競爭"}],"threats":[{"level":"🟡","text":"Onto 在先進封裝檢測量測正面挑戰，Dragonfly 季增 30%；高靈敏度混合鍵合檢測是下一個戰場","p":"30%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"全線設備商捆綁、以明顯低於 KLA 的價格銷售量測機台；新興小公司切局部市場","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"AI 與虛擬量測可能取代部分實體量測步驟；10-K 自述無法預測 AI 對供應鏈的衝擊、可能跟不上技術變化","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"出口管制下 KLA 不能出貨的中國晶圓廠改買對手，中國份額被動流失","p":"40%","evidence_refs":["reg_tariff_export#0","geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推定；投入資本事實表未涵蓋，周轉率無法驗證）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是製程與良率工程師、決策者是晶圓廠資本支出委員會、付款者是晶圓廠，三者都在同一本良率帳上：良率每 1% 值至少 1.5 億美元。先進製程與 HBM 不量測就不能量產，屬需要不是想要；延後購買的代價是新廠良率爬坡變慢。急迫性（交期 12 個月、客戶要求優先出貨）不等於持久性，持久性來自每一代缺陷更小、量測步驟更多（Yole：量測強度持續上升）"},{"item":"決策層級","level":"🟢","text":"替代性要在單一製程層的檢測配方衡量，不在設備品類：機台綁在配方與良率資料，換供應商要重新認證；製程控制份額 56.5%、為最近對手 6.5 倍，機台中位退役年限由 10 年拉長到 24 年以上，服務合約占服務營收八成以上。成熟製程與先進封裝較易切換（Onto），是此項的弱點"},{"item":"價值鏈分配","level":"🟡","text":"製程控制只占 WFE 約 7.5%，卻決定良率，KLA 營益率 42.6% 高於全部同業；但上游光學元件單一或少數供應、需 KLA 出資擴產，記憶體元件漲價時既有合約難轉嫁，毛利率被兩端分走；下游單一客戶約占營收 19%，客戶集中但沒有自建量測的跡象"},{"item":"社會容忍度","level":"🟡","text":"客戶是企業不是消費者，漲價的社會敏感度低；真正的天花板是政策：美國出口管制讓 KLA 不能出貨的中國晶圓廠改買對手，Section 232 調查結果未明、關聯方規則暫停期 2026-11 屆滿。優勢本身不靠監管授權，但市場範圍受政策限縮"}],"roiic":84,"reinvest_rate":22,"endo_ceiling":18.7,"formula_note":"單位 %；增量報酬＝FY2023→FY2026 稅後營業利益增量 14.25 億美元 ÷ FY2024–FY2026（稅後營業利益−自由現金流）合計 16.91 億；再投資率取 FY2026 的 10.73÷48.40；稅率用管理層規劃稅率 14.5%；投入資本事實表未涵蓋，屬代理值"}}}},"q3_growth":{"verdict":"成長跑道中等：量測強度上升與先進封裝讓成長快過 WFE，但這些是同一市場內的新應用，還算不上第二條曲線；共識三年 EPS 年複合約 31.9%，大半靠循環上行與利潤率擴張，不是再投資可複製的成長。","reasoning":"成長來源：以量為主（WFE 擴張、DRAM 與封裝量測強度上升、服務隨裝機基礎成長 13–15%），價為輔（只有新產品能重新定價），每年淨回購約 1–1.5% 股數，沒有併購。三年共識：FY2026 實際 GAAP 稀釋 EPS 3.66，FY2029E 8.40，年複合約 31.9%（Koyfin 共識；營收共識 FY1 23 位、FY2 21 位分析師，EPS 家數事實表未涵蓋）。內生上限約 18.7%（見護城河段再投資推算），缺口約 13pp，歸因：營益率由 41.7% 擴到約 47%，每年貢獻約 4pp；淨回購約 1.3pp；基期 GAAP 對共識 non-GAAP 的口徑差約 1pp；剩下約 7pp 來自 2027 年 WFE 約三成的循環上行，無法以再投資歸因，長期信心上限為中。跑道：製程控制份額已 56.5%，落在 35–70% 區間；先進封裝製程控制 2026 年約 11 億美元、年增逾 70%，e-beam 由約 1 億美元做到約 4 億美元，都是既有市場內的延伸，不算獨立的下一條成長曲線，故判中等，跑道約 5–9 年。衰退信號亮 2 個：2026 年占 WFE 份額小降、EPS 成長比營收快約 10pp，長期成長性與陷阱風險都判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q2_fy2027_reven"],"verdict_values":{"growth":{"driver_mix":"量為主（WFE 擴張與量測強度上升），價為輔（只有新產品重新定價），淨回購每年約 1–1.5% 股數，無併購","runway_years":7,"runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 84% × FY2026 再投資率約 22% ≈ 18.7%（FY2023→FY2026 年度財報代理值，投入資本事實表未涵蓋）；共識三年 EPS 年複合約 31.9%，超出約 13pp","segments":[{"item":"半導體製程控制（FY2026）","value":"年增 12%，先進製程、先進封裝與服務帶動"},{"item":"PCB 與元件檢測（FY2026）","value":"年增 21%，毛利率低於公司平均，拉低組合"},{"item":"特殊半導體製程（FY2026）","value":"年減 1%，中國較弱"},{"item":"系統營收客戶結構（12 月季）","value":"晶圓代工／邏輯約 60%、記憶體約 40%，DRAM 占記憶體 84%"},{"item":"2027 年記憶體占比","value":"約 60%（管理層），循環曝險上升"},{"item":"服務","value":"單季 8.5 億美元、年增 14%，2027 年預期在 13–15% 目標區間高端"},{"item":"中國占比","value":"2026 年 27–29%，2027 年降到 20% 出頭"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"年度毛利率 FY2023→FY2026 由 59.8% 升到 61.3%，TTM 61.5%；季度年比事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"2026 年占 WFE 份額約降 20bp（分析師提問、管理層未否認，歸因供貨不足）；製程控制份額長期仍在升"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"管理層稱既有合約難漲價、新產品才調價，沒有提價後量縮的證據"},{"signal":"EPS 成長顯著快於營收","lit":true,"note":"共識 FY2026→FY2028 EPS 年複合約 38.7%、營收約 28.4%，差約 10pp，來自營運槓桿與口徑差"},{"signal":"FCF/淨利連兩年低於 0.75","lit":false,"note":"FY2026 0.78、FY2025 0.92，接近警戒"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"SBC 占營收 2.0%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"WFE 2026 年約 1550 億、2027 年超過 2000 億，量測強度上升"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數序列事實表未涵蓋；KLA trailing 本益比落在四個年度端點中段"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"資本支出約營收 2–3%，最新一季 1.95 億對自由現金流 13.36 億"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"各廠都在擴產，印度購地建新園區"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"股東回饋紀律好（自由現金流九成以上回饋、2022 年以來股數減約 18%、稀釋低），但回購價格偏貴，回購收益率不及格。","reasoning":"現金轉換：FCF/淨利 FY2023 0.98、FY2024 1.10、FY2025 0.92、FY2026 0.78，最新一季自由現金流 13.36 億美元對 GAAP 淨利 15.5 億約 0.86；下滑來自擴產資本支出與為供貨押庫存，尚未破 0.75。SBC 8,410 萬美元，占營收 2.0%、占 GAAP 營業利益 4.5%，稀釋低。現金去向：股利占自由現金流 25–30%，2030 年目標總回饋占自由現金流 90% 以上；過去 12 個月回饋 33 億美元（7 月口徑），約為 FY2026 自由現金流 37.7 億的 88%；3 月新增 70 億回購授權、合計約 110 億；資本支出將升到每年 6–8 億美元；近 12 個月無併購。完整的四分去向逐年金額事實表未涵蓋。資產負債：現金 47 億、債務約 59.5 億，淨負債 12.5 億，槓桿約 1 倍、低於目標 1.5–2 倍，三大評等皆投資級。計分：併購報酬不適用；回購收益率不及格——現價盈餘殖利率約 2.5%、自由現金流殖利率約 2.0%，要過門檻需 10 年期公債殖利率低於 0.5%（公債殖利率本身事實表未涵蓋）；SBC 淨稀釋為負，及格。","fact_refs":["f_kpi4_sbc_gaap","f_kpi3_free_cash_flow","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_pe_current","f_ps_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購項目；上一筆大型併購的已實現報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"現價盈餘殖利率約 2.5%（1÷39.58 倍 trailing 本益比）、自由現金流殖利率約 2.0%；回購均價事實表未涵蓋，過門檻需 10 年期公債殖利率低於 0.5%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 2.0%；2022 年以來流通股數減約 18%，稀釋股數由 13.11 億股降到指引 13.06 億股"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐（近 12 個月無併購），回饋以回購與股利為主，金額與比例已寫在說明"}}}},"q5_valuation":{"verdict":"現價 157.91 元要求 FY2029 共識 EPS 8.40 兌現、之後再以約一成成長兩年，才換得約 10% 年報酬；我只信一半——FY2029 正好落在記憶體綠地新廠投產後的消化窗口，所以估值判合理，不判便宜。","reasoning":"現價 157.91 元：FY1（2027-06 止）本益比 27.5 倍、FY2 22.4 倍、trailing 39.6 倍（四個年度端點分位 46.2，不是五年連續分位）、P/S 14.2 倍、前瞻 EV/S 11.0 倍。現價要求什麼：以終端 22 倍、每年股息加淨回購約 1.8% 計，要拿到 10% 年報酬，FY2031 EPS 需約 10.4，等於 FY2029 共識 8.40 兌現後再以約一成成長兩年。我只信一半：FY2029 正好落在記憶體綠地新廠投產後的消化窗口，所以基本情境把 FY2029 放在 7.9（低於共識約 6%）。PEG：以 FY2026→FY2029 共識年複合 31.9% 算約 0.86，以 FY1→FY3 的 21% 算約 1.3，前者被循環高成長墊高，不當便宜證據。結論：估值合理，不便宜；12 個月上檔約 6%（FY2028 EPS 7.0×24 倍），五年基本情境上檔約 32%。前份在 190.8 元時判偏貴，這次改判合理，主因是價格下跌 17%，其次是 FY1 共識三個月上修 4.9%；26 週報酬 −8.3%、RSI 40、股價低於 52 週均線 169.8 元，動能偏弱、沒有過熱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_w52"],"verdict_values":{"valuation":{"basis":"FY1／FY2 本益比與 PEG","tier":"半導體設備寡占龍頭","peers":{"expanded":false,"reason":"事實表同業對照只有毛利率、營益率、FCF 利潤率、研發密度，沒有同業本益比；終端倍數改用 KLA 自身 trailing 39.6 倍（四個年度端點中段）與現價 FY2 本益比 22.4 倍作錨"},"fwd_pe":27.51,"peg":0.86,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 27.5 倍、FY2 22.4 倍；trailing 39.6 倍落在四個年度端點中段（分位 46.2，非五年連續分位，五年分位事實表未涵蓋）；PEG 約 0.86（以 FY2026→FY2029 共識年複合 31.9% 計）、以 FY1→FY3 年複合 21% 計約 1.3；基本情境年報酬約 8%，分母又是循環爭點，判合理而非便宜","upside_short_pct":6.4,"upside_mid_pct":32.4,"denominator_disputed":true,"denominator_note":"FY1／FY2 EPS 建立在 2027 年 WFE 超過 2000 億美元、記憶體約占 KLA 業務六成的循環高點；若 2028–29 進入消化期，FY2029 EPS 可能低於 FY2028。分母本身就是多空爭點，所以不拿 27.5 倍、22.4 倍作便宜論證，只作合理區間判斷"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把記憶體帶頭的 2027 年利潤率當成常態，以及低估出口管制擴大到中國成熟製程的機率。","reasoning":"最強空方數字：FY2029 共識 EPS 8.40 已等於管理層 2030 年 EPS 目標（投資人日 84 美元，按十比一分割換算為 8.40），2027 年記憶體約占業務六成，是這家公司近年最高的循環曝險；FY2026 FCF/淨利已降到 0.78。法說迴避：7 月被問為何不能漲價抵銷記憶體成本、漲價幅度與生效時間，管理層都沒正面回答，只說新產品才重新定價，代表短期定價力有上限。壓力測試三項過兩項：①上一輪下行重演（FY2024 營收 −6.5%、營益率 37%、EPS −16%），自由現金流仍正、淨負債只有 12.5 億美元，過；②中國成熟製程管制擴大、中國營收減半（約全公司 −10～−15%），EPS 約 −15～−20%，過，但估值會先壓縮；③記憶體消化與管制同時發生，空頭低點 EPS 4.8×16 倍約 77 元、跌約 51%，不過。歷史最大回撤事實表未涵蓋，回撤範圍改用路徑推估。陷阱判中等：衰退信號亮 2 個，利潤率高點外推是主要陷阱。","fact_refs":["f_week26_return_pct","f_consensus_eps_fy2","f_consensus_eps_fy3","f_net_debt_m","f_kpi3_free_cash_flow"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高點利潤率外推"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.74,"pe":27.51,"basis":"FY1（2027 年 6 月止財年）共識 EPS 5.74，現價 157.91 元；終端倍數同樣是該財年 EPS 的本益比，與起點同口徑"},"eps":{"bull":[5.95,7.6,9.3,10.8,12.3],"base":[5.74,7.0,7.9,8.6,9.5],"bear":[5.6,5.9,4.8,5.3,6.0]},"pe":{"bull":26,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.53,"net_buyback":1.3},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"max_dd":{"lo":-55,"hi":-35,"basis":"歷史最大回撤事實表未涵蓋，改用路徑推估：①空頭終點約 96 元，跌 39%；②下行時倍數先壓、EPS 後落：FY1 本益比由 27.5 倍壓到 16 倍、EPS 落到空頭低點 4.8，約 77 元，跌 51%；③上一輪 FY2024 營收只減 6.5%、EPS 減 16%，跌幅主要來自倍數。範圍取 −35%～−55%；前份 −60% 從 190.8 元起算，價格已回落 17%，吸收了一部分壓縮","trigger_time":null},"basis":{"bull":"AI 與 HBM 讓設備支出延續到 2029 年，無塵室瓶頸拉長而非截斷週期；KLA 占 WFE 比重如期升向 9%，毛利率 2027 下半年回到 63–64%，FY2031 EPS 約 12.3，終端 26 倍","base":"FY2027–28 照共識兌現，FY2029 記憶體消化使成長放緩到約 13%（低於共識 8.40 約 6%），之後回到約一成成長；營益率 46–47%、每年淨回購約 1.3%；終端 22 倍，與現價 FY2 本益比 22.4 倍相當","bear":"2027 年有客戶因廠房延誤推遲拉貨，FY2028 只到 5.9；2028–29 記憶體消化使 FY2029 EPS 較前一年回落約 19%（上一輪 FY2024 EPS 減 16%），疊加中國管制擴大；終端 16 倍＝成長熄火到一成時的本益比錨"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層預期 2027 年記憶體約占 KLA 業務六成；Bernstein 估 DRAM 設備 2027 年 +53%、2028 年 +37%；SEMI 指出期末將面臨永續性考驗；Morgan Stanley 稱買方預期已接近飽和","assumption":"量測強度上升與服務合約能讓 KLA 下行跌幅小於設備總體，像 FY2024 只減 6.5%","consequence":"五年後虧 50% 的故事：2027 年記憶體綠地新廠集中投產，2028–29 DRAM 供過於求、記憶體客戶砍設備支出，同時出口管制擴大到中國成熟製程；KLA EPS 由高點回落兩到三成，市場以 16 倍谷底倍數定價，股價落到 77–96 元","ruling":"部分採納：空頭機率給 30%（高於多數品質股的 25%），回撤區間放到 −55%；不給更高，因為上一輪下行營收只減 6.5%、營益率守 37%，服務約八成為合約型。本條與唯一致命點（中國管制）部分重疊，已在空頭路徑把兩者疊加","watch":"季營收指引中點是否低於前季實際、FY2028 共識三個月變化、1 月法說 2027 年記憶體占比","evidence_refs":["supply_demand_durability#4","reg_tariff_export#0"],"fact_refs":["f_consensus_eps_fy2","f_consensus_eps_fy3"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 FCF/淨利 0.78（FY2025 為 0.92）；資本支出將升到每年 6–8 億美元、各廠擴產、印度購地；為擴產願意承擔庫存與彈性成本；記憶體元件漲價壓毛利超過 100bp；光學元件單一或少數供應；過去兩年回購多在 30 倍以上本益比買進","assumption":"營收成長帶來的營運槓桿能抵銷成本上升，新產品能把價格調上去","consequence":"份額與營收都照劇本走，但毛利率卡在 62–63%、自由現金流轉換率掉到 0.75 以下，回購在高倍數買進，每股價值成長慢於 EPS","ruling":"部分採納：轉換率下降有擴產與營運資金的合理解釋，尚未破 0.75；回購收益率不及格是實情，已反映在資本配置判斷","watch":"FCF/淨利連兩年低於 0.75；毛利率連兩季低於 61.5%；資本支出超過營收 4%","evidence_refs":["geo_supply_chain#1"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_pe_current"]},{"view":"價格已反映太多","evidence":"FY1 本益比 27.5 倍、trailing 39.6 倍，是在 46% 的史上最高營益率上算的；FY2029 共識 EPS 8.40 已等於管理層 2030 年 EPS 目標","assumption":"市場給的倍數是給長期成長，而不是給循環高點","consequence":"即使 EPS 照共識走，倍數由 27.5 倍收斂到 22 倍，五年價格報酬只剩三成上下","ruling":"部分反駁：價格已比前份低 17%、FY2 本益比 22.4 倍，倍數壓縮已走了一段；但基本情境年報酬約 8%，只支持首批，不支持重倉","watch":"FY2 共識本益比是否跌破 20 倍、共識是否開始下修","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 190.8 → 本次 157.91（-17.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=190.8","side_b":"本次 price_at_dd=157.91","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 190.8 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 190.8 美元：Bull 價 366、Bear 價 119，五年期望值 +35.6%，基準年化 6.2%，不對稱比 3.3","side_b":"本次情境、股價仍用 190.8 美元：Bull 價 319.8、Bear 價 96，五年期望值 +6.3%，基準年化 1.8%，不對稱比 1.13","ruling":"先換情境、股價不動：五年期望值少 29.3 個百分點，基準年化少 4.4 個百分點。不對稱比由 3.3 變為 1.13。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 190.8 美元：五年期望值 +6.3%，基準年化 1.8%，不對稱比 1.13","side_b":"本次情境、股價 157.91 美元：五年期望值 +28.4%，基準年化 5.8%，不對稱比 2.18","ruling":"再換股價、情境不動：起點價下跌 17.2%，五年期望值多 22.1 個百分點，基準年化多 3.9 個百分點，不對稱比由 1.13 升到 2.18。合計五年期望值比前份少 7.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面加速對股價降評","cause":"新證據","prior_field":null,"side_a":"管理層（10 月法說）：12 月季營收指引 47 億美元、2027 年 WFE 超過 2000 億、backlog 與銷售漏斗能見度前所未有、未來數季逐季成長；FY1 共識三個月上修 4.9%","side_b":"市場：股價由前份 190.8 元跌到 157.91 元、26 週 −8.3%，FY1 本益比由約 35 倍壓到 27.5 倍；Morgan Stanley 稱買方預期約 2300 億以上、接近飽和；2027 年成長由 DRAM 帶頭","ruling":"不可調和（方向相反），裁定基本面一側較有據，但不足以現在建倉：①上一輪 FY2024 營收只減 6.5%、營益率守 37%；②無塵室與電力瓶頸把擴產分散到更多年（CEO）；③價格下跌而 EPS 上修，屬跌但基本面無損。現在就賣的最強論證：FY2029 共識 8.40 已等於 2030 年 EPS 目標，記憶體占 2027 年業務約六成是這家公司近年最高的循環曝險，週線已跌破 52 週均線。FY1、FY2 獲利本身就是多空爭點，所以先觀望，首批等 1 月法說確認 2027 年 WFE 與 3 月季指引再建","evidence_level":"一手（法說、新聞稿）對二手（賣方彙整）","settle_metric":"1 月法說的 2027 年 WFE 分項與 3 月季營收指引","if_then":["若 1 月法說維持 2027 年 WFE 2000 億美元以上且 3 月季指引逐季成長，建首批三分之一；週收盤再站回 52 週均線，加第二批至目標倉位三分之二","若 2027 年 WFE 下修到 1900 億以下或 3 月季指引低於 12 月季實際，不建倉，維持追蹤","若股價先漲到 52 週均線上方 10% 而 1 月證據未到，不追"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"估值結論與裁決：價格回落","cause":"價格變動","prior_field":["val","signal","max_dd_pct"],"side_a":"前份 2026-07-29：股價 190.8 元，估值判偏貴，最大回撤估 −60%","side_b":"本次：股價 157.91 元（−17%），FY1 本益比 27.5 倍、FY2 22.4 倍，估值改判合理；最大回撤估 −35%～−55%；整體評級不變","ruling":"估值由偏貴改為合理，主因是價格下跌 17%，次因是 FY1 共識上修 4.9%；回撤區間收窄是因為起算價已低；裁決與角色由矩陣依新輸入重算","if_then":[],"evidence_refs":[]},{"axis":"循環位置：中循環改為晚循環","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：中循環","side_b":"本次：晚循環。10 月法說：2027 年記憶體約占業務六成、DRAM 綠地新廠帶頭；2027 年 WFE 由 7 月約 1900 億上修到 2000 億以上；交期約 12 個月且在拉長；有客戶要求出貨但廠房未完工、機台暫緩","ruling":"採晚循環：記憶體帶頭、客戶拉貨超前廠房進度是循環後段的典型跡象；但 SEMI 預測 2029 年前仍雙位數成長、瓶頸拉長週期，故不判過熱頂部","settle_metric":"季營收指引是否維持逐季成長","if_then":["若 3 月季與 6 月季指引都逐季成長且記憶體占比未超過六成，維持晚循環不升級為頂部"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"情境機率：多頭 30% 改 25%、空頭 25% 改 30%","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：多頭 30%、空頭 25%","side_b":"本次：多頭 25%、基本 45%、空頭 30%","ruling":"共識三年 EPS 年複合約 31.9%，超過再投資推得的內生上限約 18.7%，依規空頭機率不得低於 30%；多頭下調是因循環已到後段、FY2029 共識已等於 2030 年目標","if_then":[],"evidence_refs":[]},{"axis":"護城河方向：2026 年份額小降對長期擴張","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：擴大","side_b":"本次 10 月法說：分析師指出 2026 年 KLA 占 WFE 份額只降約 20bp，管理層未否認並歸因供貨不足；Onto 封裝檢測季增 30%","ruling":"維持擴大：份額小降發生在供貨受限而 backlog 同時成長的年份，屬遞延不是流失；投資人日份額 56.5%、為最近對手 6.5 倍（7 年前 4 倍），DRAM 量測強度接近先進邏輯","settle_metric":"2027 年 KLA 營收成長對 WFE 成長","if_then":["若 2027 年供貨改善後 KLA 營收成長仍低於 WFE，護城河方向改判穩定並停止加碼"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"成長跑道、陷阱風險與公司類型：維持","cause":"新證據","prior_field":["runway_post_y5","trap","archetype"],"side_a":"前份：跑道中等、陷阱風險中等、品質複利成長","side_b":"本次新增：先進封裝製程控制 2026 年約 11 億美元、年增逾 70%；服務年增 14%；但 2027 年記憶體占比約六成、FCF/淨利由 0.92 降到 0.78","ruling":"三欄都不變：封裝與 e-beam 是同一市場內的新應用，不足以算第二條成長曲線；衰退信號亮 2 個，陷阱風險維持中等；記憶體曝險上升讓公司類型的信心降為中，但主類型不變","if_then":[],"evidence_refs":[]},{"axis":"進場與加碼門檻變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"FY27共識本益比≤34x（約$175）分批starter；≤30x（約$154）加碼；或FY27/FY28共識3個月上修≥10%使同價位倍數下修","side_b":"加碼需 1 月法說維持 2027 年 WFE ≥2000 億美元且週收盤站回 52 週均線（約 170 元），或 FY2 本益比 ≤20 倍（約 141 元）且共識未下修逾 5%","ruling":"前份兩條本益比門檻都已碰到（FY1 本益比 27.5 倍），照前份觸發器原本要建首批；本次不建、改列觀望：2027 年記憶體約占業務六成的新證據讓 FY1、FY2 獲利本身成為多空爭點，FY1 本益比不再是可靠的錨。首批改綁 1 月法說確認（2027 年 WFE ≥2000 億美元且 3 月季營收指引中點高於 12 月季實際），第二批再加週收盤站回 52 週均線，第三批限首批建立後、FY2 本益比 ≤20 倍（約 141 元）且共識未下修逾 5%","if_then":["若 1 月法說維持 2027 年 WFE ≥2000 億美元且 3 月季營收指引中點高於 12 月季實際，建首批三分之一","若首批建立後週收盤站回 52 週均線，加碼第二批","若首批建立後價格到約 141 元且共識未下修逾 5%，加碼第三批"],"evidence_refs":[]},{"axis":"Single Thing 由未設定改為出口管制擴大到成熟製程","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（null）","side_b":"美國把對中國的設備出口管制擴大到成熟製程，或關聯方規則在 2026-11 暫停期滿後恢復執行且無豁免","ruling":"前份把出口管制放在風險清單，沒挑出唯一致命點；本次比較各項單一事件的 EPS 衝擊，中國成熟製程管制（EPS 約 −15～−20%）大於關稅（毛利率 100bp 約 EPS −2%），且關聯方規則暫停期 2026-11 屆滿、時點最近；觸發即減碼至首批的一半","if_then":["若規則生效且無豁免，減碼至首批的一半並重算空頭路徑"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"停損指標由無到有","cause":"方法變動","prior_field":null,"side_a":"前份未設定停損指標（null）","side_b":"本次五條：占 WFE 比重連兩年下降則清倉；毛利率連兩季低於 61.5% 停止加碼；中國占比單季低於 18% 減碼；FY2028 共識三個月下修逾 10% 減碼一半；季營收指引中點低於前季實際停止加碼","ruling":"前份只有進場門檻、沒有出場門檻；本次補齊，每條都綁具體動作與資料來源","if_then":[],"evidence_refs":[]},{"axis":"管理層說法前後對照","cause":"新證據","prior_field":null,"side_a":"7 月法說：9 月季營收指引 40 億±2 億、EPS 1.16±0.10；下半年較上半年成長約 20%；2027 年 WFE 約 1900 億；3 月投資人日稱 2030 年目標偏保守，7 月稱目前不會重設","side_b":"10 月：9 月季營收 41.4 億、EPS 1.22，皆高於中點；下半年成長改為約 25%；2027 年 WFE 上修到 2000 億以上；CEO 改稱 2030 模型的假設會在 2030 年前被超越；但毛利率回到 63–64% 目標的時間推到 2027 年中後段至 2028","ruling":"交付紀錄加分、可信度高；但提前超越 2030 模型等於把循環往前拉，和 FY2029 共識已等於 2030 年 EPS 目標是同一件事，已寫入第一條風險；毛利率延後寫入第四條風險","if_then":["若 12 月季毛利率低於 61.5%，停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"12 月季營收落在指引區間內（45–49 億美元）","type":"假設驗證","maps_to":"H2","metric":"12 月季營收","threshold":"低於 45 億美元","action":"停止加碼，首批持有不動","source_freq":"季報／每季","date":"2027-01"},{"n":2,"text":"1 月法說維持 2027 年 WFE 2000 億美元以上，且週收盤站回 52 週均線","type":"加碼","maps_to":"H2","metric":"2027 年 WFE 展望與週收盤對 52 週均線","threshold":"WFE ≥2000 億美元 且 週收盤 >52 週均線（約 170 元）","action":"加碼第二批至目標倉位三分之二","source_freq":"法說／每季；週線／每週","date":"2027-01"},{"n":3,"text":"價格回到 FY2 本益比 20 倍且共識沒有下修","type":"估值rearm","maps_to":"H2","metric":"FY2 共識本益比","threshold":"≤20 倍（以 7.04 計約 141 元），FY2 共識三個月下修不超過 5%","action":"分批反買第三批","source_freq":"Koyfin 共識／每月；股價／每日","date":null},{"n":4,"text":"FY2028 共識大幅下修","type":"減碼","maps_to":"R1","metric":"FY2028 共識 EPS 三個月變化","threshold":"下修超過 10%（低於約 6.3）","action":"減碼一半","source_freq":"Koyfin 共識／每月","date":null,"evidence_refs":["supply_demand_durability#4"]},{"n":5,"text":"對中國出口管制擴大到成熟製程，或關聯方規則恢復執行","type":"Single Thing","maps_to":"R2","metric":"BIS 規則狀態與中國營收占比","threshold":"規則生效且無豁免，或中國占比單季跌破 18%","action":"減碼至首批的一半","source_freq":"BIS 公告／即時；季報／每季","date":"2026-11","evidence_refs":["reg_tariff_export#1","reg_tariff_export#0"]},{"n":6,"text":"毛利率連兩季跌破指引下緣","type":"風險","maps_to":"R4","metric":"季度毛利率","threshold":"連兩季低於 61.5%","action":"停止加碼","source_freq":"季報／每季","date":null},{"n":7,"text":"Section 232 對半導體設備加徵關稅且無法轉嫁","type":"風險","maps_to":"R2","metric":"毛利率指引","threshold":"關稅公告後毛利率指引較前季下修超過 100bp","action":"減碼三分之一","source_freq":"商務部公告／即時；季報／每季","date":null,"evidence_refs":["regulatory_antitrust#1","reg_tariff_export#2"]},{"n":8,"text":"份額論點破裂","type":"清倉","maps_to":"H1","metric":"KLA 占 WFE 比重與製程控制份額","threshold":"占 WFE 比重連兩年下降 且 製程控制份額低於 55%","action":"清倉","source_freq":"1 月法說／每年","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":9,"text":"1 月法說後全面複審","type":"複審日期","maps_to":null,"metric":"2027 年分項展望","threshold":null,"action":"重跑整份判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"KLA 占 WFE 比重（管理層年度口徑）","bear_threshold":"連續兩年下降；或 2027 年營收成長低於 WFE 成長","window":"每年 1 月法說","source":"KLA 法說會與投資人日","last_status":"warning"},{"metric":"季度毛利率","bear_threshold":"連兩季低於 61.5%（12 月季指引下緣）","window":"每季","source":"KLA 季報新聞稿","last_status":"ok"},{"metric":"中國營收占比","bear_threshold":"單季跌破 18%，且不是其他地區放量造成","window":"每季","source":"KLA 股東信地區營收拆分","last_status":"ok"},{"metric":"FY2028 共識 EPS","bear_threshold":"三個月下修超過 10%（低於約 6.3）","window":"三個月滾動","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"下一季營收指引中點對前季實際營收","bear_threshold":"指引中點低於前季實際（逐季成長中斷）","window":"每季","source":"KLA 季報新聞稿","last_status":"ok"}],"action_conditions":{"rearm_trigger":"加碼需 1 月法說維持 2027 年 WFE ≥2000 億美元且週收盤站回 52 週均線（約 170 元），或 FY2 本益比 ≤20 倍（約 141 元）且共識未下修逾 5%","exec_line":"目前觀望、不建倉：FY1、FY2 獲利建在 2027 年記憶體帶頭的循環高點，現價 157.91 元不買。首批三分之一目標倉位等 1 月法說維持 2027 年 WFE 2000 億美元以上、且 3 月季營收指引中點高於 12 月季實際，再分兩筆買進；之後週收盤站回 52 週均線（約 170 元），加第二批到目標倉位三分之二；第三批限首批建立後、股價到約 141 元（FY2 本益比 20 倍）且 FY2 共識三個月下修不超過 5%；股價先漲過 52 週均線 10% 而證據未到則不追","holding_cap":"單一個股上限 5%，循環後段首年先不超過 3%；需有跌 35–55% 的心理準備，跌但基本面無損不停損"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2027 年當循環頂先行降評（FY1 本益比由約 35 倍壓到 27.5 倍，同期共識上修 4.9%），但上一輪下行 FY2024 營收只減 6.5%、營益率守 37%，且無塵室與電力瓶頸把擴產分散到更多年，下行時 EPS 回落可能比股價隱含的小","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":"1 月法說維持 2027 年 WFE 2000 億美元以上，且 3 月季營收指引中點高於 12 月季實際營收，兩項都成立才建首批三分之一目標倉位；等的是證據不是價格，股價先跌到約 141 元也等法說再建"},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2027 年當循環頂先行降評（FY1 本益比由約 35 倍壓到 27.5 倍，同期共識上修 4.9%），但上一輪下行 FY2024 營收只減 6.5%、營益率守 37%，且無塵室與電力瓶頸把擴產分散到更多年，下行時 EPS 回落可能比股價隱含的小"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=-8.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"製程控制份額守住或擴張：KLA 占 WFE 比重由 2025 年約 7.5% 往 2030 年約 9% 走，2027 年營收成長快過 WFE","2y":null,"5y":"占 WFE 比重 2030 年達 8.5% 以上、製程控制份額不低於 56%","10y":null,"threshold":"占 WFE 比重連續兩年下降，或製程控制份額跌破 55%","source":"KLA 每年 1 月法說與投資人日揭露的份額口徑；賣方晶圓檢測份額資料","drift_rule":"五年期論點：滾動四季營收成長對 WFE 成長的差，連 4 季落後 5% 以上為削弱，連 6 季落後 10% 以上為反轉"},{"id":"H2","text":"2027 年 WFE 超過 2000 億美元、KLA 季營收逐季成長，FY2028 EPS 走到 7.0 附近","2y":"FY2027 EPS 約 5.7、FY2028 約 7.0，12 月季營收落在 45–49 億美元","5y":null,"10y":null,"threshold":"FY2028 共識 EPS 較 7.04 下修超過 10%，或任一季營收低於指引下緣","source":"季報新聞稿與法說；Koyfin 共識快照（每月）","drift_rule":"兩年期論點：滾動四季 EPS 對路徑連 2 季偏低 5% 以上為削弱，連 3 季偏低 10% 以上為反轉"},{"id":"H3","text":"下一次 WFE 消化期，KLA 營收跌幅控制在上一輪的兩倍以內，營益率守在 35% 以上；靠服務約兩成營收、八成合約型與量測強度上升撐住","2y":null,"5y":"下行年營收跌幅不超過 15%、營益率不低於 35%","10y":null,"threshold":"任一下行年營收年減超過 15% 或營益率低於 35%","source":"KLA 年報與季報","drift_rule":"五年期論點：營收連 4 季年減 5% 以上為削弱，連 6 季年減 10% 以上為反轉"}],"R":[{"id":"R1","text":"記憶體帶頭的 2027 年設備支出在 2028–29 年進入消化期，市場提前 2–4 季反應：管理層預期 2027 年記憶體約占 KLA 業務六成，Bernstein 估 DRAM 設備 2027 年 +53%、2028 年 +37%，SEMI 也指出期末將面臨永續性考驗","h_ref":"H2","clock":"🔥","threshold":"季營收指引中點低於前季實際（逐季成長中斷），或 1 月法說把 2027 年 WFE 下修到 1900 億美元以下","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"出口管制與關稅升級：關聯方規則暫停期 2026-11 屆滿；Section 232 半導體設備調查結果未明；2026-02 最高法院裁定 IEEPA 關稅無授權後，退款與新關稅不確定；2026-04 BIS 更新被報導為 FY2026 營收逆風（二手來源）；出口管制估計至 2026 年累計減少營收 3–3.5 億美元；中國 2026 年約占營收 27–29%","h_ref":"H1","clock":"🔥","threshold":"中國營收占比單季跌破 18%，或關稅使毛利率指引較前季下修超過 100bp","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3","regulatory_antitrust#1","geo_supply_chain#2"]},{"id":"R3","text":"競爭與替代技術：Onto 在先進封裝檢測量測正面挑戰（Dragonfly 季增 30%）；全線設備商可能捆綁低價；AI 與虛擬量測可能減少部分實體量測步驟，10-K 自述可能跟不上技術變化","h_ref":"H1","clock":"🐢","threshold":"先進封裝製程控制營收成長低於封裝市場成長，或 KLA 占 WFE 比重連兩年下降","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"記憶體成本壓毛利、既有合約難漲價：12 月季營收季增約 14%，毛利率指引卻只有 62.5%，沒有槓桿；3 月投資人日目標 63–64%，10 月改口要到 2027 年中後段至 2028 才回到目標","h_ref":"H2","clock":"⚡","threshold":"毛利率連兩季低於 61.5%（指引下緣）","evidence_refs":[]},{"id":"R5","text":"集中度：單一客戶（TSMC）FY2025、FY2026 各約占營收 19%（FY2024 約 13%）；光學等關鍵零件只有單一或少數供應商，斷供即延誤出貨","h_ref":"H3","clock":"🐢","threshold":"單一客戶占比升到 25% 以上，或管理層再度因零件短缺下修季營收","evidence_refs":["customer_concentration_credit#0","geo_supply_chain#1"]}],"single_thing":{"description":"美國把對中國的設備出口管制擴大到成熟製程，或關聯方規則（持股 50% 以上關聯方納入）在 2026-11 暫停期滿後恢復執行且無豁免","why_fatal":"中國 2026 年約占營收 27–29%、2027 年預期 20% 出頭，且以成熟製程為主；若成熟製程也被擋，推估失去中國營收一半以上，約全公司營收 10–15%，以高增量利潤率換算 EPS 約減 15–20%，而且是永久性的市場流失、由對手補位。這是所有單一事件中 EPS 衝擊最大的一項，關稅（毛利率 100bp）只約 EPS −2%","if_happens":"減碼至首批的一半並重算空頭路徑；若同時遇到記憶體消化期，清倉等下一輪","how_monitor":"BIS 公告與實體清單更新、KLA 每季地區營收拆分（中國占比）、法說對出口管制影響金額的更新","probability":"約 20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.43,"peg_fy2":1.07,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":3.66,"FY2027E":5.74,"FY2028E":7.04,"FY2029E":8.4},"fy_end_month":6,"eps_basis":"FY2026A 用年度財報 GAAP 稀釋 EPS 3.66（已調整 2026-06 十比一分割）；FY2027E–FY2029E 為 Koyfin 共識（2026-10-31 快照），應屬 non-GAAP；最新一季 non-GAAP 1.22 對 GAAP 1.18，口徑差約 3%，使三年年複合高估約 1pp。財年 6 月底結束；營收共識 FY1 23 位、FY2 21 位分析師，EPS 家數事實表未涵蓋"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"12 月季財報與 2027 年 WFE 分項展望（管理層說 1 月底再談）","impact":"高","watch":"2027 年 WFE 是否維持 2000 億美元以上、記憶體占比、3 月季營收指引是否逐季成長"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"出口管制關聯方規則一年暫停期屆滿","impact":"中","watch":"恢復執行、延長暫停或改版；KLA 對中國營收影響的更新"},{"date":null,"date_precision":null,"type":"regulatory","event":"Section 232 半導體與設備進口調查結果","impact":"中","watch":"設備關稅稅率、是否有豁免、毛利率指引變化"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"FY2027 年度財報與 FY2028 展望","impact":"中","watch":"毛利率回到 63% 以上的進度、資本支出水準、FCF/淨利是否回升"}]}
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
