你是 DD 管線 v20 的判斷層閘（gate），標的 MP（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
- `f_kpi0_gaap_ppa_income`（q1_business）｜營收（GAAP，不含 PPA Income）＝147.7 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 investors.mpmaterials.com Q3 2026 results（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得單季共識
- `f_kpi1_ppa_income`（q1_business）｜營收＋PPA Income＝155.8 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi2_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未揭露 Non-GAAP 營業利益，以此代）＝41.1 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益（損失）＝-22.1 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi7_ndpr`（q1_business）｜NdPr 產量／銷量＝1018 MT（銷量 1,020 MT）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_peer_mp_gross_margin_pct`（q2_moat）｜MP 毛利率＝-16.15 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MP.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-05 date｜期間與口徑：2026-11-05／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-05）
- `f_peer_mp_operating_margin_pct`（q2_moat）｜MP 營業利益率＝-34.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MP.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mp_fcf_margin_pct`（q2_moat）｜MP FCF 利潤率＝-165.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_alb_operating_margin_pct`（q2_moat）｜ALB 營業利益率＝16.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_usar_operating_margin_pct`（q2_moat）｜USAR 營業利益率＝-946.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.USAR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uuuu_operating_margin_pct`（q2_moat）｜UUUU 營業利益率＝-62.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UUUU.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝-0.01 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝0.74 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.31 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝453.16 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝786.15 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi8`（q1_business）｜期末現金與短期投資＝1337.9 USD m｜期間與口徑：Q3 2026（2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_kpi4_gaap_eps`（q4_capital）｜GAAP 淨損／稀釋 EPS＝-20.7 USD m（EPS -0.12；Adjusted EPS 0.04）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi5`（q4_capital）｜自由現金流（單季，由九個月累計減上半年推算）＝-125.2 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：推算：九個月 OCF -7.8、capex 420.3（Q3 新聞稿）減上半年 OCF +4.9、capex 307.7（Q2 8-K 2026-08-06）；公司未直接報 FCF（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi6_sbc`（q4_capital）｜SBC 占營收＝7.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Q3 2026 results（SBC 11.3m ÷ 營收 147.7m；營業利益為負故不以營業利益為分母）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-354.29 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 983.62、現金 1337.91（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝35.41 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝5957.01 USD m｜期間與口徑：2026-11-08／市值 6311.3 ＋ 淨負債 -354.29｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝13.15 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（0.74 → 0.74）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝11.49 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝2.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝2.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝12.17 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝7.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝7.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝178.23 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-47.49 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝3830.0 x｜期間與口徑：2026-10-22／分母＝FY1 EPS 0.01，分子＝快照價 38.3｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-22）
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.19｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 35.41 / W52 54.95 / W104 46.82 / W250 34.12 / W250 13週斜率 -0.28%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝34.12 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.28 %｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（27 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子明言新進入者可能透過併購、合作進入市場，且產業整併可能使對手具更強產品或定價彈性。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：USA Rare Earth 在奧克拉荷馬州 Stillwater 磁鐵廠調機，目標 2026 Q4 達 600 MT/年，為美國本土磁鐵直接新進入者。
  - 來源：Motley Fool: MP Materials vs USA Rare Earth（as_of 2026-02-14）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：報導稱 Stillwater 磁鐵廠出現主要競爭對手。
  - 來源：OK Energy Today: Major rival emerges for Stillwater rare earth magnet firm（as_of 2026-02-01）｜affects：moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025：客戶 A（材料）30%、B（材料）23%、C（主要磁材）31%，前三大合計約84%；2024 年 B 78%、A 20%；2023 年 B 96%。
  - 來源：SEC EDGAR 10-K FY2025 Item 8 Concentration of Customer Risk（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：公司稱預期 DoW 可能成為最大磁材客戶，且高度依賴 DoW 資金撥款（需國會撥款）；撥款延遲或受限可能需另尋融資。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 Q3 10-Q：客戶A（材料）單季33%／前九月37%，客戶B（材料）23%／26%，客戶C（磁材）12%／16%。
  - 來源：SEC EDGAR 10-Q Q3 2026 Note 2 Concentration of Customer Risk（as_of 2026-11-06）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：IDTechEx 預期全球稀土磁體產能擴張將大幅超過需求成長，2037 年全球產能利用率降至 59%
  - 來源：IDTechEx (經 Skillings/搜尋摘要引用)（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：美國磁體產能擴張時程：USA Rare Earth 奧克拉荷馬廠 2027 年達 1,200 噸/年、南卡廠 2028-04 首產 6,400 噸/年；JS Link 喬治亞廠 3,000 噸/年預計 2027 年底商業生產
  - 來源：搜尋摘要（Skillings／SMM／ProjectBlue）（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K風險因素指出，因DoW交易協議，公司可能面臨更嚴格審查、政府稽核／調查、國會關注及司法部執法（含False Claims Act）等；未見反壟斷調查之陳述。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：公司在全球銷售，美國關稅政策、出口管制或其他貿易限制的變動難以預測，可能對公司造成重大不利影響；現任政府已對中國、加拿大、墨西哥進口品加稅。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：中國商務部 2026-06-22 將 MP Materials 與 USA Rare Earth 等美國實體列入出口管制清單，禁止向其出口兩用物項
  - 來源：Mining Weekly: China places two US rare earths producers on export control list（as_of 2026-06-22）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：中國商務部於 2026-06-22 將 MP Materials 與 USA Rare Earth 列入出口管制清單，禁止中國原產雙用途物項轉移給這些公司
  - 來源：Mining Weekly: China places two US rare earths producers on export control list（as_of 2026-06-22）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：稀土精礦營收因 2025 年 7 月起停止對中國銷售，預期未來期間將大幅偏低。
  - 來源：MP Materials 10-Q Q3 2026 (SEC)（as_of 2026-11-06）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：MP 在 FY2025 10-K 風險因子自陳：若下游產業採用不需稀土或 NdFeB 磁鐵的新技術，或出現合適替代品，需求會下降並對業務造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：IDTechEx 預測 2035 年近 30% 電動車市場將使用無稀土馬達（含外激磁同步馬達）。
  - 來源：IDTechEx via electricvehiclesresearch.com（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Chartmill（2026-10 資料）：EPS 預估 23 位分析師；下一財年 EPS 預估 1 個月降 17.56%、3 個月降 57.21%；Q3 2026 共識 EPS -$0.01、營收約 $120.18M，預定 2026-11-05 公布（未查到實際結果）。原文未核。
  - 來源：Chartmill MP estimates page（as_of 2026-10-18）｜affects：valuation、triggers、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露與一家營建總包商的仲裁爭議，已估列損失；若不利結果可能對財報有重大影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-26）｜affects：decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Argus Media 2026-09 報導：美國至少有 56,000 噸新稀土磁鐵產能在開發中（同業擴產，未見紀律性克制的證據）
  - 來源：Argus Media market insight paper: US rare earth magnet capacity（as_of 2026-09-09）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：USA Rare Earth Stillwater Phase 1a 磁鐵線 2026-03 投產，目標 2026 年底 600 mtpa、2027 Q1 Phase 1b 後合計 1,200 mtpa
  - 來源：Barchart / Metal.com (SMM) USAR 報導（as_of 2026-03-30）｜affects：moat_trend、thesis.R
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Evolution Metals & Technologies：13 台 ULVAC 燒結磁鐵設備預計 2026-11 交機安裝，完成後韓國浦項年磁鐵產能逾 10,000 噸（約 6,000 噸高性能燒結）；FY2027 營收指引 $400–460mm 為公司自述
  - 來源：Investegate / FinanceWire EMAT press release（as_of 2026-10-01）｜affects：moat_trend、thesis.R
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：JS Link America 投資約 $223M 在喬治亞州 Columbus 建稀土磁鐵廠，預計 2027 開始營運
  - 來源：Mining.com（as_of 2026-06-01）｜affects：moat_trend
- `cyclical_supply_discipline_capacity#5`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Energy Fuels 整合平台目標年產約 15,700 噸磁鐵，並有 $725M 美國有條件融資（20 年貸款，待盡調與正式協議）
  - 來源：Pulse2: Energy Fuels mine-to-magnet platform（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `cyclical_supply_discipline_capacity#6`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Lynas FY2026 Q3（至 2026-03-31）NdPr 產量 1,996 噸、年增 32%，2026-03 首次產出氧化釤，預期重稀土初期年產約 400 噸並待新增分離產能
  - 來源：Zacks / Metal.com 彙整 Lynas（as_of 2026-04-30）｜affects：moat_trend、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：MP FY2023 10-K：2023年稀土精礦營收年減51%，實現價格每REO公噸年減43%；定價高峰在2022年2月；全年調整後EBITDA margin約40%。
  - 來源：MP Materials Form 10-K FY2023 / Q4 2023 8-K（as_of 2024-02-29）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：MP Q1 2024：營收年增20%至$62.9M，REO實現價年減23%，調整後EBITDA為$(11.2)M（年減$26.7M），為上輪下行期EBITDA轉負。
  - 來源：MP Materials Q1 2024 earnings 8-K（經搜尋摘要）（as_of 2024-05-09）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：SMM 報導：PrNd氧化物2022上半年約81萬至110萬人民幣/噸；2024年5月下旬約37.5萬至37.7萬人民幣/噸，自高點下跌約三分之二、歷時約兩年（跌幅為搜尋摘要所算，未見單一來源明載谷底日）。
  - 來源：SMM metal.com / SunSirs 價格報導（as_of 2024-05-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Ex-China NdPr價格跌破MP與DoD協議的$110/kg底價，約$95,000/噸
  - 來源：Benchmark Source（as_of 2026-08-21）｜affects：thesis.R、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":84.0,"bear_5y_price":10.9,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":17.8,"ev5y_pct":15.6,"irr_base_pct":3.3,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","valuation_basis":"sales_multiple","start":{"rev":453.16,"ev_s":13.15,"basis":"起點用 FY2026E 共識營收，EV/S 為目前 EV÷當年度營收；終端同為 FY2031 當年度營收。事實表未標明共識是否含 PPA，路徑一律按不含 PPA 的營收估。"},"rev":{"bull":[800,1200,1600,2050,2400],"base":[690,950,1180,1400,1550],"bear":[550,680,760,830,900]},"ev_s":{"bull":6.5,"base":5.0,"bear":3.0},"net_debt_y5":{"bull":-1200,"base":-800,"bear":250},"shares_y5":{"bull":200,"base":205,"bear":225},"net_debt_now":-354.29,"shares_now":178.23,"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":null,"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MP_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Michael Rosenthal｜guidance：Q3 NdPr 產量預期超過 1,000 公噸（原話："I expect Q3 NdPr production to exceed 1,000"）
- 2026-08-06｜Ryan Corbett｜guidance：Q3 NdPr 氧化物實現價格預期在每公斤 90 多元高段，PPA 收入約每公斤 10 元（原話："will be in the high 90s per kilogram, leaving PPA income"）
- 2026-08-06｜Ryan Corbett｜guidance：Q3 材料部門銷量預期持平（原話："sales volumes in the Materials segment to be flattish"）
- 2026-08-06｜Ryan Corbett｜guidance：全年 CapEx 預期維持 5 到 6 億美元（原話："CapEx spend to be in the $500 million to $600 million range."）
- 2026-08-06｜Ryan Corbett｜guidance：上半年累計 CapEx 為 3.08 億美元（原話："year-to-date spend to $308 million as of June 30."）
- 2026-08-06｜James Litinsky｜guidance：磁鐵商業出貨預計在第四季開始，之後穩定爬坡（原話："expect to begin commercial shipments in the fourth quarter"）
- 2026-08-06｜Ryan Corbett｜guidance：磁鐵銷量為小幅爬坡，且不會線性（原話："There'll be a modest ramp of volume over time."）
- 2026-08-06｜Ryan Corbett｜guidance：預付款約 4,600 萬美元的前驅物營收將在未來 3 到 4 季認列（原話："$46 million of prepaid revenue to be earned for magnetic"）
- 2026-08-06｜James Litinsky｜margin：材料部門營收加 PPA 收入 1.132 億美元、調整後 EBITDA 3,250 萬美元（原話："$113.2 million of revenue plus PPA income and $32.5 million"）
- 2026-08-06｜Ryan Corbett｜margin：合併營收加 PPA 收入 1.261 億美元（原話："$126.1 million of revenue and PPA income, more than doubling"）
- 2026-08-06｜James Litinsky｜margin：前驅物產品調整後 EBITDA 利潤率超過 40%（原話："Precursor production generated adjusted EBITDA margins"）
- 2026-08-06｜Ryan Corbett｜margin：磁鐵部門營收小降，因成本更多歸入磁鐵量產起步而非前驅物（原話："much higher proportion of costs being attributable to the"）
- 2026-08-06｜Ryan Corbett｜margin：降成本的前提是穩定在目標產量運轉（固定成本攤提）（原話："we need to be operating consistently at our target"）
- 2026-08-06｜Ryan Corbett｜margin：氯鹼等降本效益預計到 2027 年逐步堆疊（原話："we expect those benefits to build progressively through '27"）
- 2026-08-06｜Michael Rosenthal｜margin：新試劑直接成本略高於舊產品，管理層認為整體效益較大（原話："The direct cost of the reagent is somewhat higher than our"）
- 2026-08-06｜Michael Rosenthal｜commitment：Dy/Tb 分離線預計今年稍後產出鋱與鏑（原話："we remain on track to produce terbium and dysprosium"）
- 2026-08-06｜Michael Rosenthal｜commitment：釤計畫預計 2028 年首度生產（原話："planning first production in 2028."）
- 2026-08-06｜Michael Rosenthal｜commitment：預浮選製程預計 2028 年前規模化導入（原話："pre-flot process that we now anticipate implementing"）
- 2026-08-06｜Ryan Corbett｜commitment：不急於為宣布而宣布合約，只在準備好時才公布（原話："We are in no rush to announce a deal to announce a deal."）
- 2026-08-06｜James Litinsky｜customer：7 月簽下對美國航太國防廠商的釓氧化物長約，預期多年累計 9 位數美元（原話："9-figure deal in total over multiple years"）
- 2026-08-06｜Ryan Corbett｜customer：釓合約經濟條件已鎖定，不受現貨價影響（原話："we've locked in economics on this contract."）
- 2026-08-06｜James Litinsky｜customer：Independence 已被 GM 與 Apple 訂滿，可能再塞一兩家客戶（原話："sold out between GM and Apple, it's possible that we'll"）
- 2026-08-06｜James Litinsky｜customer：10X 目前 100% 由戰爭部合約涵蓋，之後預期多數轉給產業客戶（原話："is 100% contracted with the Department of War."）
- 2026-08-06｜James Litinsky｜customer：Project Swarm 用來彙整並標準化未來無人機磁鐵需求（原話："initiative designed to aggregate and standardize future"）
- 2026-08-06｜Michael Rosenthal｜product：持續降低產品的重稀土用量（原話："aggregate and standardize future magnet demand"）
- 2026-08-06｜James Litinsky｜product：預期 10X 開出時大多數產能為無重稀土或極少重稀土的磁鐵（原話："the vast majority of that facility will be no"）
- 2026-08-06｜James Litinsky｜competition：管理層稱 NdPr 是可預見未來的限制性資源（原話："But I remain convicted in the view that NdPr is the"）
- 2026-08-06｜James Litinsky｜competition：管理層描述目前為「管制性稀缺」體制（中國出口管制）（原話："And we are in a regime right now of controlled scarcity."）
- 2026-08-06｜Ryan Corbett｜risk：中國出口禁令對試劑與成本預期影響極小（原話："we expect minimal impact given everything you know about us"）
- 2026-08-06｜Michael Rosenthal｜risk：Mountain Pass 停機被與計畫無關的專案延長（原話："Unrelated projects extended the downtime"）
- 2026-08-06｜Ryan Corbett｜capital_allocation：現金 14.5 億美元，稱可完全支應長期資本計畫（原話："This fully funds our long-term capital plan and"）
- 2026-08-06｜Michael Rosenthal｜capital_allocation：回收業務目前主力為自家製程廢料與 Apple，規模依市況擴張（原話："but we are looking at scaling that business in line"）

### 問答異常語氣（迴避／改口／保留）
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Garchitorena 問下半年成本能改善多少、Dy/Tb 調機是否增加成本｜答法：未給下半年數字，改談存貨資本化與成本效益到 2027 年逐步出現
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Peterson 要求 GBD/低重稀土磁鐵與傳統磁鐵的績效數據｜答法：未提供比較數據，只說符合並超過客戶規格
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Summerville 問 2027 磁鐵爬坡到 1,000 噸/年的節奏與下半年磁鐵營收/EBITDA 組成｜答法：只說會不規則、非線性，2027 節奏留待年底再說，未給數字
- MP_Q2_2026_Earnings_Call_20260806.md｜問：Ma 問為何磁鐵新合約沒有加速｜答法：質疑問題前提，改稱已訂滿且不急於簽約
- MP_Q2_2026_Earnings_Call_20260806.md｜問：de Alba 問 GM 資格驗證的早期回饋｜答法：只談驗證流程，說結果「極鼓舞」，未給 GM 具體反饋

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 7 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 7 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"NdPr 商品價格維持 $110+ 且 DOD floor 可信（最關鍵的結構性假設）","columns":{"2Y 驗證點":"2026-2027 NdPr 季均價 ≥ $110","5Y 驗證點":"2028-2030 五年均價 ≥ $115（不含 floor 補貼）","10Y 驗證點":"2035 全球 ex-China 供給達 30% market share，價格可獨立形成","具體數字門檻":"NdPr ≥ $110/kg（CRU + Argus weekly）+ DOD floor 撥款 trigger（Pentagon FY 預算 line item ≥ $200M for MP offtake）","信息來源":"CRU Group / Argus Media / DOD FY2026 budget","漂移觸發條件":"連 2 季 TTM 均價偏離"}},{"id":"H2","text":"10X facility 按時 ramp + Magnetics 段 GM 轉正（成長兌現的操作性假設）","columns":{"2Y 驗證點":"2027 末 Magnetics 段年化營收 ≥ $200M，GM 由負轉 0","5Y 驗證點":"2030 達 10,000 MT 磁鐵年產能、Magnetics GM ≥ 20%（規模經濟）","10Y 驗證點":"2035 magnetics segment 達 50% 公司 OI","具體數字門檻":"季度報出 magnet 出貨量（MT/quarter）+ Magnetics revenue/MT 單價","信息來源":"MP 季報 + 8-K 公告","漂移觸發條件":"連 2 季 magnet 出貨量"}},{"id":"H3","text":"估值倍數收斂至成長股區間（normalized PE 35x）（估值修復的市場假設）","columns":{"2Y 驗證點":"FY 2027 EPS 共識穩定 ≥ $1.10，Forward PE 收斂至 50-55x","5Y 驗證點":"FY 2030 EPS ≥ $2.50，PE 收斂至 30-35x","10Y 驗證點":"FY 2035 EPS ≥ $4，PE 25-30x","具體數字門檻":"EPS 共識穩定（90d trend 標準差","信息來源":"yfinance EPS estimate + analyst rating distribution","漂移觸發條件":"FY 2027 EPS 共識 90d trend 連 2 季下修 > 15% → 削弱；連 4 季下修 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NdPr spot 連續走弱（China 反向補貼出口或全球需求疲軟）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期","監測指標":"NdPr 月均價（CRU/Argus）+ China REE 出口量","警戒閾值":"連 2 月均價"}},{"id":"R2","text":"10X facility ramp 失敗（成本超支或良率不達標）","columns":{"對應假設":"H2","時間尺度":"🔥 中期","監測指標":"季度 magnet shipment + Magnetics 段 GM","警戒閾值":"連 4 季 magnet 出貨量"}},{"id":"R3","text":"政治結構變化（2028 大選後 DOD 預算重排或中美和解）","columns":{"對應假設":"H1+H3","時間尺度":"🐢 長期","監測指標":"DOD FY 預算 line item for MP + 中美關係溫度（CSIS / RAND 評估）","警戒閾值":"2028-2029 DOD MP 撥款"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":64.46,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MP","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"MP Materials Corp."},"oneliner":"股價半年腰斬後，MP 的礦、資金與政府合約都還在，但第三季營收有 21% 來自一次性賣庫存，磁鐵要到 2028 年才看得出獲利；基本情境五年只賺約 18%，先等 2027 下半年的磁鐵與成本數字。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MP_20261108/scenario.json","answers":{"q1_business":{"verdict":"MP 賺的是美國與盟友為了擺脫中國供應而願意多付的錢，錢現在卡在 Mountain Pass 的 NdPr 產量與單位成本，2028 年後卡在磁鐵廠的良率與合約單價。","reasoning":"Materials 賣 NdPr 氧化物與金屬給日本經銷商和美國大型工業客戶，Magnetics 目前主要認列前驅物收入，政府用 PPA 補足 $110/kg 底價的差額。第三季營收 1.477 億美元，Materials 1.335 億、Magnetics 1,860 萬，部門間沖銷約 440 萬；營業利益 −2,210 萬，營益率 −15.0%，最新單季毛利率事實表未涵蓋，只有截至 6 月的 TTM −16.15%。Materials 營收裡有 3,160 萬是一次性 SEG+ 銷售，占合併營收 21%，扣除後 1.161 億，低於會前約 1.2018 億的共識（該共識原文未核，也無法確認是否含這筆）。調整後 EBITDA 4,110 萬同樣被這筆銷售墊高，而管理層在 2026-11-05 拒絕揭露成本，底層獲利無法還原。客戶集中：第三季客戶 A 33%、B 23%、C 12%，前九月 37%、26%、16%，A、B 都在 Materials；公司預期 DoW 會成為最大磁鐵客戶，集中度只是換對象。","fact_refs":["f_kpi0_gaap_ppa_income","f_kpi1_ppa_income","f_kpi2_adjusted_ebitda_non_gaap","f_kpi3_gaap","f_kpi7_ndpr","f_peer_mp_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"中低：21% 為一次性銷售；PPA 收入 810 萬不計入營收，卻占調整後 EBITDA 約 20%；Magnetics 收入幾乎等於前驅物遞延收入轉列。","unit_econ_note":"第三季 NdPr 氧化物與金屬營收 1.01 億÷1,020 噸＝約 $99/kg，PPA 約 $7.9/kg，合計約 $107/kg，低於 $110 的標題底價。單位成本事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":"未獲利高成長","confidence":"中","fingerprint":"FY2022 毛利率 79.04%，FY2024 −32.76%；GAAP 連兩年虧損，營收受 NdPr 價格驅動；磁鐵合約段屬於另一種生意。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高：非中國供應的溢價來自出口管制，2025-11 美中協議已顯示管制可以暫停；Benchmark 在 2026-08 報 Ex-China NdPr 跌破 $110 且供給轉寬。產業仍在擴張投資期，判斷依據是量與資本形成，不是股價。","bargaining":{"up":"自有礦，對外依賴主要是試劑；管理層稱試劑占成本比重高，氯鹼廠 2027 年第一階段啟用後依賴下降。","down":"客戶議價力強：前兩大客戶占第三季營收 56%，DoW 包銷 10X 全部產量，合約條款鎖定獲利區間。","geo":"中國 2026-06-22 把 MP 列入出口管制清單；精礦自 2025-07 起停售中國；管理層 2026-08-06 稱對試劑與成本影響極小，這點尚未獨立驗證。"},"profit_pool_dir":"政策把部分利潤從中國分離與磁材環節移往受保護的美國供應鏈，方向明確，金額與占比事實表未涵蓋。","tam_table":[{"item":"全球 NdFeB 磁鐵市場","value":"約 25 萬噸／年，中國占 90% 以上（Litinsky，2026-11-05 法說）"},{"item":"MP 規劃磁鐵產能占比","value":"Independence 約 3,000 噸＋10X 7,000 噸＝10,000 噸，約全球 4%"},{"item":"美國開發中磁鐵產能","value":"至少 56,000 噸（Argus，2026-09）"},{"item":"全球產能利用率預測","value":"2037 年降至 59%（IDTechEx）"},{"item":"利潤池 5 年前後占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"→：執行面在擴大（GM 認證完成、重稀土分離開機、降重稀土配方），定價面在收縮（Ex-China NdPr 跌破底價、美國新產能排隊），兩者抵銷，方向穩定。","reasoning":"機制是三件事疊加：美國本土從礦到磁鐵的整合、DoW 合約的價格與包銷保護、長達數年的車規認證。執行面：GM 認證完成，第四季開始出貨，Dy/Tb 分離線開機，第三季 1,018 噸符合 8 月「超過 1,000 噸」的指引。定價面：NdPr 是受保護的價格接受者，Ex-China 價格在 2026-08 跌破 $110，第三季補貼約 $7.9/kg，低於 8 月所說的約 $10/kg；磁鐵高毛利目前只是管理層口徑，RFQ 沒有具名客戶或單價。對手面：中國以外的大型整合商只有 Lynas 一家，新進者多半卡在資金與原料，但 56,000 噸開發中產能足以壓縮 2030 年後的議價。ROIC 差距無法計算，事實表只有同業利潤率；MP TTM 營益率 −34.06%，低於 ALB 的 16.27%，高於 UUUU 的 −62.09% 與 USAR 的 −946.09%。反例：若 USAR 或其他對手在 2028 年前通過車規認證並取得獨立原料，執行面的領先會快速縮小，方向應改為向下。","fact_refs":["f_peer_mp_gross_margin_pct","f_peer_mp_operating_margin_pct","f_peer_mp_fcf_margin_pct","f_peer_alb_operating_margin_pct","f_peer_usar_operating_margin_pct","f_peer_uuuu_operating_margin_pct","f_kpi7_ndpr"],"verdict_values":{"moat":{"mechanism":"美國唯一從礦到磁鐵的整合供應鏈，加上 DoW 底價與包銷合約，以及 2021 年做到 2026 年才完成的車規認證門檻。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：GM 認證完成，2026 Q4 開始出貨。定價面收縮：Ex-China NdPr 約 $95/kg，低於 $110，美國開發中磁鐵產能至少 56,000 噸。沒有資料顯示最大客戶流失，客戶 C 比重下降來自前驅物收入遞減。","competitor_notes":[{"name":"LYC.AX","strategy_note":"中國以外唯一已量產的大型整合分離商，至 2026-03 的單季 NdPr 1,996 噸、年增 32%，約為 MP 第三季的兩倍；財報資料事實表缺，利潤率無法比較。"},{"name":"ALB","strategy_note":"同屬政策敏感的礦業商品，TTM 營益率 16.27%、FCF 率 23.47%，只用來對照商品礦業的正常利潤，不是直接對手。"},{"name":"USAR","strategy_note":"直接對手，Stillwater 目標 2027 年 1,200 噸，TTM FCF 率 −1,865.38%，資金與原料都弱於 MP；MP 已對其提出營業秘密訴訟。"},{"name":"UUUU","strategy_note":"目標年產約 15,700 噸磁鐵，有 7.25 億美元有條件融資但尚待正式協議；TTM 營益率 −62.09%，產能目標遠大於目前現金流所能支撐。"}],"peer_na_reason":"最接近的 Lynas 無財報資料，其他同業沒有投入資本資料，ROIC 差距無法計算。","threats":[{"level":"🔴","text":"美國與亞洲磁鐵新產能排隊，USAR、JS Link、Energy Fuels、EMAT 與 Lynas 同時擴張，壓縮 10X 轉單給商業客戶時的議價力。","p":"40%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","competitive_share_entrants#3","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4","cyclical_supply_discipline_capacity#5","cyclical_supply_discipline_capacity#6"]},{"level":"🟡","text":"無稀土馬達替代，IDTechEx 估 2035 年近 30% 電動車採用；影響電動車部分，不影響 DoW 包銷。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"中國把 MP 列入出口管制清單，影響設備、試劑與兩用物項取得；管理層稱影響極小，尚未獨立驗證。","p":"已發生，實質衝擊機率 20%","evidence_refs":["reg_tariff_export#3","geo_supply_chain#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉：TTM 營益率 −34.06%，投入資本周轉率事實表未涵蓋，當期 ROIC 為負。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（GM、Apple）、決策者（DoW、車廠採購）與付款者都已具體存在，但 GM 要先用完既有供應，機器人需求仍停在未具名 RFQ，SMM 估 2027 年新能源車 NdFeB 只成長 3.74%。"},{"item":"決策層級","level":"🟢","text":"認證要審到每台設備與作業指導書，MP 從 2021 年做到 2026 年才通過，單一車型計畫的更換成本高。代理讀數：GM 按專案與工廠逐步切換。"},{"item":"價值鏈分配","level":"🟡","text":"DoW 包銷 10X，並分走 $110 以上 30% 的利益，買方與政府都有議價力；若 10X 能轉給機器人客戶，分配會改善，但沒有單價證據。"},{"item":"社會容忍度","level":"🟡","text":"優勢依賴 DoW 協議與年度撥款，FY26 DPA 請求 2.66 億美元；以 6,000 噸計，NdPr 要跌到約 $66/kg，年付款才會超過這個額度，目前差額約 $10/kg，還沒有壓力。10-K 已列出稽核、國會關注與 False Claims Act 風險。"}],"roiic":"實績為負：FY2022 到 FY2025 營業利益由正轉負，投入資本持續增加。前瞻假設：Base 到 FY2031 增量稅後利益約 3.6 億美元÷增量投入約 17 億美元＝約 21%，本檔自估，尚未證實。","reinvest_rate":"TTM 無法計算，稅後營業利益為負；FY2026 資本支出指引 5～6 億美元，相當於 FY2026E 共識營收的 110%～132%。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；稅後營業利益為負時公式無解，因此留空，並視為共識成長超過內生能力。"}}}},"q3_growth":{"verdict":"🟢：以全球 25 萬噸市場看，MP 滿產只占 4%，還有重稀土與機器人兩條尚未兌現的新曲線；但 5 年內的成長大多是已簽約產能，5 年後的成長要看原料與新合約。","reasoning":"成長由量帶動：NdPr 2027 年目標 5,000 噸以上，磁鐵從零開始爬坡，價格被底價與 30% 分潤截斷，併購為零、回購未計。共識 EPS 由 FY2026E −0.01 到 FY2028E 1.31，基期為負，三年 CAGR 不能算；FY2027E 到 FY2028E 年增 77%。TTM 稅後營業利益為負，內生上界無法用實績算出，前瞻約 21% 的增量報酬只是假設。共識與內生能力的缺口，來源是固定成本攤提與 PPA 帶來的利潤率擴張，不是回購或併購。本檔 FY2027E 營收 6.9 億，低於共識 7.86 億 12%，因為 CFO 在 2026-11-05 說 2027 年磁鐵貢獻仍小、2028 年才看得見，而 S&P 9 月引用的 2027 年 Magnetics 營收 2.08 億是在這段話之前的數字。反例：若 GM 導入比預期快、Apple 提前放量，FY2027 可能接近共識。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8"],"verdict_values":{"growth":{"driver_mix":"量為主；價格被底價與分潤截斷；併購為零；回購未計。","runway_years":"10 年以上（滿產占全球約 4%，距 30% 滲透率很遠；實際上限是原料與合約）","runway_post_y5":"🟢","endo_ceiling_basis":"TTM 稅後營業利益為負，內生上界無法計算；成長資金來自 13.38 億美元現金與 Apple、DoW 的合約資金，不是自身盈餘。","segments":[{"item":"Materials","value":"第三季營收 1.335 億、調整後 EBITDA 4,780 萬（含一次性 SEG+）；Base FY2031 外銷 NdPr 約 4.3 億＋重稀土等 1.5 億"},{"item":"Magnetics","value":"第三季營收 1,860 萬、調整後 EBITDA 530 萬，幾乎等於前驅物遞延收入轉列；Base FY2031 約 9.7 億，含 10X 約六成開工"},{"item":"PPA 收入","value":"第三季 810 萬，不計入營收；第四季指引約 $8/kg"}],"decay_signals":[{"item":"毛利率連 2 季年減","status":"未亮","note":"單季毛利率事實表未涵蓋，TTM −16.15% 優於 FY2025 的 −25.67%"},{"item":"核心市占縮減","status":"資料缺口","note":"事實表沒有 NdPr 份額時間序列"},{"item":"提價後銷量下滑","status":"未亮","note":"銷量年增 94%"},{"item":"EPS CAGR 高於營收 CAGR 超過 5pp","status":"資料缺口","note":"EPS 基期為負"},{"item":"FCF 對淨利轉換偏低連 2 年","status":"亮燈","note":"FCF 連三年為負，累計 −7.0 億美元"},{"item":"SBC 占營收超過 5% 且逐年上升","status":"資料缺口","note":"第三季 7.7%，趨勢事實表未涵蓋"},{"item":"TAM 被替代技術壓縮","status":"亮燈","note":"IDTechEx 估 2035 年近 30% 電動車用無稀土馬達"},{"item":"產業倍數系統性下移","status":"資料缺口","note":"事實表沒有同業倍數序列"},{"item":"維護性資本支出占 FCF 過高","status":"不適用","note":"FCF 為負"},{"item":"停止投資新產能且收入下滑","status":"未亮","note":"仍在擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置目前還算穩健：13.38 億美元現金足以支應建設期，但新資本的報酬還沒有實績。","reasoning":"單季 FCF −1.252 億、GAAP 淨損 2,070 萬，FCF 對淨利的轉換沒有意義；FY2023 至 FY2025 FCF 連三年為負，累計 −7.0 億。SBC 占營收 7.7%，年化 4,520 萬÷市值 63.1 億＝0.72%，未含 DoW 股權工具與歷次增資，完整條款事實表未涵蓋。現金去向只有資本支出可追：九個月約 4.14 億至 4.20 億（法說與新聞稿口徑差約 650 萬），約六成投入磁鐵；併購、回購金額事實表未涵蓋，2024 年回購只見分析師口頭提及。Litinsky 在 2026-11-05 表示已收緊支出，並提到未來要趁亂「清理垃圾」，這是併購機會，也代表新資本可能投向尚未驗證的資產。","fact_refs":["f_kpi4_gaap_eps","f_kpi5","f_kpi6_sbc","f_kpi8","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"未見併購實績，沙烏地合資尚未產生報酬"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"2024 年回購的金額與均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"單季 SBC 1,130 萬，年化÷市值＝0.72%／年，低於 1.5%；未含 DoW 股權工具與增資"}]},"governance":{"capital_returns":{"expanded":false,"reason":"公司無股利，回購金額事實表未涵蓋，成長也不靠併購，這張表沒有可用數字。"}}}},"q5_valuation":{"verdict":"現價要賺到 12% 年化，FY2031 營收必須到約 24 億美元（等於 Bull），或 15.5 億營收配 7.7 倍 EV/S；我不把這當基本情境。","reasoning":"現價 $35.41，EV 59.57 億，FY2026E EV/S 13.15 倍，FY2027E 本益比 47.85 倍，FY2028E 27.03 倍。Base 終值 $41.71，五年多 17.8%；Bull $84.00，Bear $10.89。12% 年化需要五年後股價約 $62，在 2.05 億股與 8 億淨現金下，EV 約 120 億。12 個月參考價：FY2027E 營收 6.9 億×10 倍，淨現金約 0，÷1.85 億股＝$37.3（+5.3%）。兩年參考價：FY2028E 9.5 億×8.5 倍＋淨現金約 0.7 億，÷1.9 億股＝$42.9（+21.1%）。終端倍數找不到同業現值對照，因為事實表同業只有利潤率沒有倍數，改用隱含 EBITDA 倍數判斷：Base 約 12 倍、Bear 約 10 倍、Bull 約 16 倍；ALB TTM 營益率 16.27% 只能對照利潤水準。賣方平均目標 $76～78（2026-08、09，區間 $60～100，高低比 1.67）明顯高於本檔 Base，這些目標多在最近一輪下跌與第三季法說之前，Koyfin 最近兩份快照修正為 0，可能尚未反映 2027 年磁鐵貢獻仍小。26 週跌 47.49% 不是安全邊際：前份 FY2027 EPS 門檻 $1.10，現共識 0.74，以此計算的本益比只由 58.6 倍降到 47.85 倍。","fact_refs":["f_price_at_dd","f_ev_m","f_ev_s_fwd","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_ev_s_current","f_ev_s_percentile","f_ps_current","f_ps_percentile","f_net_debt_m","f_shares_diluted_m","f_week26_return_pct","f_fwd_pe_latest"],"verdict_values":{"valuation":{"basis":"EV/S（FY1 共識為虧損，改用銷售倍數），另以隱含 EBITDA 倍數檢查","peers":{"expanded":false,"reason":"事實表同業只有毛利率、營益率、FCF 率與研發密度，沒有倍數，無法建立同業倍數表。"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價對應 FY2026E EV/S 13.15 倍、FY2027E 本益比 47.85 倍、FY2028E 本益比 27.03 倍。Bull 20%、Base 50%、Bear 30% 加權後五年價值約 $40.9，年化約 2.9%，以 10% 折現的現值約 $25，現價高出約四成，所以判斷偏貴。五年分位與 PEG 都無法計算：事實表只有 4 個年度端點，EPS 基期為負。反例：若以本檔估的 FY2028 EBITDA 約 4.3 億計，EV/EBITDA 約 13.9 倍，對高成長期不算離譜，倍數並非明顯泡沫。","upside_short_pct":5.3,"upside_mid_pct":21.1,"denominator_disputed":true,"denominator_note":"EV/S 分母有三個問題：FY2026E 含 3,160 萬一次性 SEG+，扣除後前瞻 EV/S 為 14.13 倍；PPA 收入不計營收卻計入 EPS，營收口徑低估底價保護下的獲利；trailing EV/S 11.49 倍低於前瞻 13.15 倍，但營收正在高成長，trailing 分母隱含約 5.18 億美元，與 FY2026E 共識 4.53 億矛盾，所以 2.5 和 7.7 的年度端點分位不當作便宜的依據。3,830 倍的前瞻本益比分母只有 0.01，同樣不使用。"}}},"q6_how_wrong":{"verdict":"最可能看錯的不是礦和合約，而是磁鐵到底賺多少錢；2028 年前沒有數字能驗證，現在的每個判斷都帶著未決風險。","reasoning":"第一，Magnetics 第三季營收 1,860 萬，而前驅物遞延收入由 8 月的 4,600 萬降到 2,800 萬，減少 1,800 萬，這季部門收入幾乎全是遞延收入轉列（本檔推算，公司未揭露），不能拿來外推磁鐵獲利。第二，8 月被問的五題（下半年成本、低重稀土磁鐵績效、2027 磁鐵節奏、新合約、GM 回饋），到 11 月只有 GM 認證有明確結果；2028 年是否達 3,000 噸、SEG+ 成本、GM 與另一供應商的爭議，11 月都未作答。第三，五項壓力測試過三項：現金撐過 10X 建設、NdPr 跌到 $60 而底價照付、磁鐵延後一年仍有流動性，這三項過；PPA 中止，以及管制解除、價格回到上輪低點並疊加磁鐵延遲，這兩項不過。歷史最大回撤幅度事實表未涵蓋。商品段缺乏穿越循環的獲利紀錄，適用循環交易紀律，不適用長抱抗波動的紀律。","fact_refs":["f_kpi5","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"現金流仍負的未證實成長，不是便宜陷阱，但倍數跌得沒有股價多"}}}},"scenario_inputs":{"valuation_basis":"sales_multiple","terminal_label":"FY2031E","start":{"rev":453.16,"ev_s":13.15,"basis":"起點用 FY2026E 共識營收，EV/S 為目前 EV÷當年度營收；終端同為 FY2031 當年度營收。事實表未標明共識是否含 PPA，路徑一律按不含 PPA 的營收估。"},"rev":{"bull":[800,1200,1600,2050,2400],"base":[690,950,1180,1400,1550],"bear":[550,680,760,830,900]},"ev_s":{"bull":6.5,"base":5.0,"bear":3.0},"net_debt_y5":{"bull":-1200,"base":-800,"bear":250},"shares_y5":{"bull":200,"base":205,"bear":225},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"max_dd":{"lo":-75,"hi":-55,"basis":"從現價 $35.41 起算。下緣 −75% 略深於 Bear 終點 −69.2%；上緣 −55% 參考 26 週已跌 47.49%，以及 NdPr 上輪下行由高點跌約三分之二的經驗。股價歷史高低點事實表未涵蓋，以情境終點和同段跌幅推估。","trigger_time":null},"basis":{"bull":"10X 於 2031 年滿載並有高毛利機器人訂單，NdPr 高於 $110，重稀土穩定獲利，營收 24 億，EBITDA 率約 40%，EV/S 6.5 倍約等於 16 倍 EBITDA。","base":"NdPr 約 $100～105 加底價補足，2027 年 5,000 噸、2031 年 6,500 噸，Independence 滿載、10X 約六成開工，營收 15.5 億，EBITDA 約 6.6 億（含不計營收的 PPA），EV/S 5 倍約等於 12 倍 EBITDA；股數含 SBC 與 DoW 等工具約 15% 稀釋，完整條款事實表未涵蓋。","bear":"NdPr 停在 $85 以下、新產能壓價，10X 延後一年且只拿最低保障，營收 9 億，EBITDA 約 2.8 億，EV/S 3 倍約等於 10 倍 EBITDA；合約仍有效，失效時另看唯一致命點。機率 30%，依據是上輪下行營收減半、EBITDA 轉負，以及內生成長能力尚未建立。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"第三季 Magnetics 營收 1,860 萬，遞延收入同期減少約 1,800 萬，真實磁鐵獲利尚未出現；FY2023 營收減半、2024 Q1 調整後 EBITDA −1,120 萬，顯示 NdPr 下行時舊業務沒有抗跌力。","assumption":"假設磁鐵毛利足以讓約 17 億美元新增投入賺到超過資金成本的報酬。","consequence":"Bear 路徑 FY2031 營收 9 億、EV/S 3 倍，股價約 $10.89，五年跌 69%。","ruling":"採納，Bear 機率 30%。與唯一致命點部分重疊，這裡補上合約照付但磁鐵賺不到錢的路徑。","watch":"2027 Q4 Magnetics 單季營收與 EBITDA 率；2028 年全年部門利潤率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","end_markets#1"],"fact_refs":["f_kpi5","f_peer_mp_operating_margin_pct"]},{"view":"論點失敗","evidence":"2025-11 中國同意暫停擴大管制，顯示管制可用政策解除；PrNd 氧化物 2022～2024 年跌約三分之二；但中國 2026-06 又把 MP 列管，方向並不單一。","assumption":"假設中國的管制和價格壓力是長期結構。","consequence":"管制解除會壓低 NdPr 與稀缺溢價，政府也較難持續撥款。","ruling":"部分採納，放在 Bear 內，不另加機率。","watch":"中國出口管制公告；DPA 撥款。","evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"view":"論點成功但股東經濟變差","evidence":"NdPr 高於 $110 時政府分走 30%；10X 由 DoW 包銷並保證 EBITDA 至少 1.4 億美元，保底之外的獲利要靠轉單給商業客戶；股本可能因 DoW 工具與 SBC 增加，完整條款事實表未涵蓋。","assumption":"假設營收與產量達標，利益會全部留給普通股東。","consequence":"Base 股數由 1.7823 億升到 2.05 億，終端 EV/S 5 倍；營收增加三倍多，每股價值只多 18%。","ruling":"採納，已反映在 Base 的股數與倍數；商業轉單的高毛利在證據出現前不計入。","watch":"具名商業合約與單價；每季股數變化。","evidence_refs":["customer_concentration_credit#1","regulatory_antitrust#0"],"fact_refs":["f_shares_diluted_m"]},{"view":"論點成功但股東經濟變差","evidence":"FY2025 10-K 揭露與營建總包商的仲裁，已估列損失，金額與裁決時點事實表未涵蓋。","assumption":"假設仲裁不影響資本計畫。","consequence":"不利結果會增加建設成本，影響範圍無法量化。","ruling":"列入監測，金額與時點是資料缺口，不納入情境。","watch":"10-Q 或爭議附註的金額更新。","evidence_refs":["major_events#2"]},{"view":"價格已反映太多","evidence":"FY2026E EV/S 13.15 倍、FY2028E 本益比 27.03 倍；下一財年 EPS 共識 3 個月下修 57.21%（Chartmill，原文未核），Koyfin 最近快照修正為 0；11 月法說的 2027 磁鐵偏弱可能還沒進入共識。","assumption":"假設跌 47.49% 後已反映壞消息。","consequence":"共識再下修時，Base $41.71 這個錨也會往下。","ruling":"採納。現價約為合約保底價值 $16～18 的兩倍，仍在為未驗證的成長付費；利空進入賣方模型前凍結加碼。","watch":"2027-02 法說後的 FY2027E 共識 EPS 與營收。","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ev_s_fwd","f_consensus_rev_fy2_pct","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 64.46 → 本次 35.41（-45.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=64.46","side_b":"本次 price_at_dd=35.41","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 64.46 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 64.46 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 64.46 美元：Bull 價 84、Bear 價 10.89，五年期望值 −36.5%，基準年化 −8.3%，不對稱比 0.24","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.24。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 64.46 美元：五年期望值 −36.5%，基準年化 −8.3%，不對稱比 0.24","side_b":"本次情境、股價 35.41 美元：五年期望值 +15.6%，基準年化 3.3%，不對稱比 1.32","ruling":"再換股價、情境不動：起點價下跌 45.1%，五年期望值多 52.1 個百分點，基準年化多 11.7 個百分點，不對稱比由 0.24 升到 1.32。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"NdPr 是長期瓶頸，還是供過於求","cause":null,"prior_field":null,"side_a":"管理層（Litinsky，2026-08-06 與 2026-11-05）：NdPr 是限制性資源，RFQ 已明顯超過 10X 產能。","side_b":"Benchmark 2026-08 報 Ex-China NdPr 約 $95/kg，跌破 $110 且供給轉寬；IDTechEx 預期 2037 年全球磁鐵產能利用率 59%；Argus 統計美國開發中產能至少 56,000 噸。","ruling":"不可調和，選 B 側作為 2031 年前的現貨判斷，依據是 B 側有報價與產能清單，A 側只有未具名 RFQ。合約磁鐵需求不受影響，所以這項裁決只影響 NdPr 外銷與 10X 轉單定價，不推翻 Base。","evidence_level":"A 側為管理層陳述，B 側為第三方報價與預測","settle_metric":"Ex-China NdPr 季均價；10X 具名商業合約數與單價","if_then":["若 2028 年底前簽下至少 1 份具名商業 10X 合約且單價高於 DoW 條件，重跑研究，Base 終端 EV/S 上調至 6 倍，首倉上限 3%。","反向：若 Ex-China NdPr 連 2 季低於 $85/kg 且仍無具名合約，不追；已持有者減碼至 1%。","股價續漲但上述證據未到，不追；股價下跌而產量與磁鐵營收達標，分批反買。"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#2","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#0"]},{"axis":"第三季是實力，還是一次性撐高","cause":null,"prior_field":null,"side_a":"營收年增 176%，調整後 EBITDA 年增 5,370 萬；Corbett 稱 SEG+ 代表資產負債表上未被理解的內含價值。","side_b":"扣除 3,160 萬 SEG+ 後營收 1.161 億，低於約 1.2018 億共識；Corbett 同時稱這是一次性銷售，並拒絕揭露成本。","ruling":"可調和。NdPr 量價進步是真的，SEG+ 的經常性未證實，不採信也不否定。Base 不計 SEG+ 再現；若之後連 4 季沒有非磁鐵重稀土外銷，就認定為一次性。","evidence_level":"公司財報與法說，共識原文未核","settle_metric":"未來 4 季重稀土與中間產品外銷收入及毛利揭露","if_then":["若 2027 Q3 前再出現 2,000 萬美元以上外銷且揭露毛利，Base 其他產品營收上調，但不追高。","反向：若連 4 季沒有外銷，維持一次性認定，不追。"],"evidence_refs":[]},{"axis":"底價是否足額補差","cause":null,"prior_field":null,"side_a":"協議底價 $110/kg，低於即由政府補差；Corbett 2026-08-06 指引第三季 PPA 約 $10/kg。","side_b":"第三季 PPA 810 萬÷1,020 噸＝約 $7.9/kg，實現價約 $99，合計約 $107；第四季指引約 $8/kg，且庫存精礦不認列。","ruling":"可調和。差額來自產品組合與計價口徑，管理層未拆解。Base 以約 $107/kg 的實得金額計算，不用 $110。","evidence_level":"公司財報與兩次法說","settle_metric":"每季 PPA 收入÷銷量，對照當季差額","if_then":["若連 2 季補貼低於差額 40% 以上，下修 Materials EBITDA，不追；持有者減碼一半。","反向：若補貼回到差額的 90% 以上，維持 Base。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"13.38 億現金、淨現金 3.54 億、GM 認證完成、Apple 2027 年開始貢獻、底價到 2035 年、10X 100% 包銷；股價貼近 250 週線 $34.12，賣方平均目標是現價兩倍以上。","side_b":"基本情境五年只多 18%；磁鐵 2028 年才看得見；共識可能未下修；NdPr 已跌破底價。","ruling":"買方論點要成立，合約價值必須足以支撐現價。依合約最低保障估的 FY2031 EBITDA 約 3.8 億，乘 10 倍每股約 $16～18，現價仍為未證實的成長付了一倍溢價，因此不現在買。","evidence_level":"事實表與本檔推算","settle_metric":"2027 Q4 NdPr 產量與 Magnetics 營收","if_then":["若 2027 Q4 前兩項營運條件達成，重跑研究，首倉上限 3%。","若 2027-08 前股價漲過 $55 而磁鐵營收仍未達標，不追。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：DoW 協議、Section 232 關鍵礦物公告、2027-01-01 國防供應鏈禁用中國來源材料。","side_b":"競爭惡化：美國開發中磁鐵產能至少 56,000 噸，Lynas 擴產。其他結構變數：無稀土馬達替代、中國把 MP 列管。","ruling":"雙向拉鋸。政策給的保護到 2035 年，競爭供給的壓力從 2028 年後開始。","evidence_level":"公告、公司文件與第三方報告","settle_metric":"OEM 量產定點名單；NdPr 季均價","if_then":["若對手取得 OEM 量產定點，下調定價評分，不追。","反向：若多家開發案在 2027 年停工，上調定價評分並重跑研究。"],"evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"axis":"商品段的循環位置","cause":null,"prior_field":null,"side_a":"偏買：NdPr 銷量年增 94%、TTM 毛利率 −16.15% 接近自身低點、賣方目標約現價兩倍、26 週跌 47.49%。","side_b":"偏賣：美國開發中產能至少 56,000 噸，公司存貨升至 2.932 億美元，NdPr 約 $95～100 仍接近 2026 年初約 $98～104/kg 的高點。P/B 事實表未涵蓋。","ruling":"訊號互相矛盾，商品段判中循環，不建立循環部位。毛利率低點來自爬坡成本，不是價格谷底，不能當便宜訊號。磁鐵合約段另計，不隨循環賣出。","evidence_level":"第三方價格與公司財報","settle_metric":"Ex-China NdPr 季均價與公司存貨","if_then":["若 NdPr 連 2 季低於 $85/kg 且新產能延後或取消，改判早循環並重跑研究。","若 NdPr 高於 $130/kg 且對手加速投產，改判晚循環，不追。"],"evidence_refs":[]},{"axis":"管理層答覆與實績的落差","cause":null,"prior_field":null,"side_a":"8 月法說有 5 題未正面回答：下半年成本、低重稀土磁鐵績效、2027 磁鐵節奏、新合約、GM 回饋。","side_b":"11 月只有 GM 認證有明確結果；但 8 月的量化承諾（1,000 噸、$90 高段、第四季出貨、Dy/Tb 開機、資本支出 5～6 億）都達成或維持。","ruling":"可調和。進度型承諾可信，獲利型資訊不透明，所以營運進度看管理層說法，獲利要等財報。","evidence_level":"兩次法說對照","settle_metric":"2027-02 法說是否提供 2027 磁鐵量或單位成本","if_then":["若 2027-02 仍不提供磁鐵量或單位成本，維持不追。","反向：若提供且高於 Base，重跑研究。"],"evidence_refs":[]},{"axis":"估值結論與股價","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 $64.46，估值結論偏貴。","side_b":"現價 $35.41，跌 45%，估值結論仍偏貴。","ruling":"價格下跌只改善了一部分：前份 FY2027 EPS 門檻 $1.10，現共識 0.74，低 33%，以此計本益比只由 58.6 倍降到 47.85 倍，2027 年磁鐵指引又偏弱。","evidence_level":"事實表價格與共識","settle_metric":"FY2027E 共識 EPS 與股價","if_then":["若股價跌到約 $28 且營運指標未惡化，分批反買至 1%。","反向：若 FY2027E 共識再下修 20% 以上，$28 這個價位同步下移，不追。"],"evidence_refs":[]},{"axis":"進場訊號與陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份進場訊號 B，陷阱風險中等。","side_b":"本次進場訊號 C，陷阱風險中等。","ruling":"訊號降一級，原因是第三季獲利品質、NdPr 跌破底價，以及前份 FY2027 EPS 門檻未達。陷阱判斷不變，FCF 連三年為負與替代技術兩項亮燈。","evidence_level":"公司財報與第三方報價","settle_metric":"扣除一次性後的部門 EBITDA","if_then":["若 2027 Q4 兩項營運條件達成，訊號回升並重跑研究。","反向：若 FCF 在 10X 主要支出結束後仍為負，陷阱判斷轉差，減碼至 1%。"],"evidence_refs":[]},{"axis":"前份沒有的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空。","side_b":"本次首次填入：護城河方向穩定、後續跑道寬、循環與商品型、中循環、最大回撤 −55%～−75%、Bull 20%、Bear 30%；裁決與角色由程式算出。","ruling":"前份沒有這些欄位，這裡是新增紀錄，不是看法改變。","evidence_level":"方法差異","settle_metric":"下次研究延用同一組欄位","if_then":[],"evidence_refs":[]},{"axis":"重新評估條件與清倉、減碼門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設定重新評估條件與清倉門檻。","side_b":"重新評估：2027 Q4 前 NdPr 單季 1,350 噸且 Magnetics 單季營收 5,000 萬美元、部門 EBITDA 率 20%。清倉：DoW 協議實質打折或現金低於 5 億。減碼：Ex-China NdPr 連 2 季低於 $85/kg。","ruling":"新設門檻，把觀望的約束點明為磁鐵獲利未證實。","evidence_level":"方法差異","settle_metric":"2027 Q4 財報","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 新增","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點。","side_b":"DoW 協議被實質打折：NdPr 底價或 10X 最低 EBITDA 保障因撥款不足、重新議約或稽核爭議而無法足額入帳。","ruling":"Single Thing 設為這一項，因為它是模型最大的單一敏感項，約占 Base FY2031 EBITDA 的三分之二。","evidence_level":"本檔推算","settle_metric":"PPA 每季入帳","if_then":[],"evidence_refs":[]},{"axis":"前份論點門檻調整","cause":"新證據","prior_field":null,"side_a":"前份：NdPr 季均價 ≥ $110；FY2027 EPS 共識 ≥ $1.10，本益比收斂至 50～55 倍。","side_b":"本次：改看產量、扣除一次性後的部門 EBITDA、Magnetics 營收、DoW 履約與商業合約；FY2027 EPS 共識 0.74。","ruling":"前份價格假設已不成立：第三季實現價約 $99，第四季指引約 $100，都低於 $110，但有底價補差。前份 EPS 門檻低於 33%，倍數修復不再作為論點。新門檻直接對應現金流來源。","evidence_level":"公司財報、共識","settle_metric":"FY2027E、FY2028E 共識 EPS","if_then":["若 FY2027 EPS 共識跌破 0.50 或 FY2028 跌破 1.00，下修 Base 營收，不追。","反向：若 FY2028 共識回到 1.50 以上且磁鐵營收達標，重跑研究。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"NdPr 產量驗證","type":"假設驗證","maps_to":"H1","metric":"NdPr 單季產量","threshold":"2027 Q4 ≥ 1,350 噸","action":"與第 2 條同時達標才重跑完整研究，首倉上限 3%；否則不追","source_freq":"公司季報，每季","date":"2028-02"},{"n":2,"text":"磁鐵獲利驗證","type":"假設驗證","maps_to":"H2","metric":"Magnetics 單季營收與部門 EBITDA 率","threshold":"2027 Q4 營收 ≥ 5,000 萬美元，EBITDA 率 ≥ 20%","action":"與第 1 條同時達標才重跑完整研究，首倉上限 3%；否則不追","source_freq":"公司季報，每季","date":"2028-02"},{"n":3,"text":"NdPr 現貨跌破保護帶","type":"風險","maps_to":"R1","metric":"Ex-China NdPr 季均價","threshold":"連 2 季低於 $85/kg","action":"持有者減碼至 1%，未持有者不追","source_freq":"Benchmark、Argus，按季判斷","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#3"]},{"n":4,"text":"DoW 協議被打折","type":"Single Thing","maps_to":"H3","metric":"PPA 入帳、DPA 撥款、最低 EBITDA 條款","threshold":"任一季 PPA 應入未入，或協議重談後保障降低","action":"清倉","source_freq":"每季 10-Q、年度撥款文件","date":null,"evidence_refs":["customer_concentration_credit#1","regulatory_antitrust#0"]},{"n":5,"text":"價格先到、證據未到","type":"估值rearm","maps_to":"H2","metric":"股價與營運指標","threshold":"股價 ≤ $28，且 NdPr 與磁鐵指標未惡化","action":"分批反買至 1%","source_freq":"每日股價、每季報告","date":null},{"n":6,"text":"磁鐵爬坡失敗","type":"減碼","maps_to":"R2","metric":"Magnetics 單季營收","threshold":"2027 Q4 低於 2,500 萬美元","action":"持有者減碼一半，停止加碼","source_freq":"公司季報，每季","date":"2028-02","evidence_refs":["customer_concentration_credit#3"]},{"n":7,"text":"流動性破線","type":"清倉","maps_to":"R2","metric":"期末現金與短期投資","threshold":"10X 完工前低於 5 億美元","action":"清倉","source_freq":"公司季報，每季","date":null},{"n":8,"text":"對手取得車規量產定點","type":"風險","maps_to":"R4","metric":"美國或盟友對手的 OEM 量產定點","threshold":"任一家取得","action":"不追，下調定價評分","source_freq":"公司公告與新聞，不定期","date":null,"evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#1"]},{"n":9,"text":"2026 Q4 財報複審","type":"複審日期","maps_to":"H1","metric":"2027 磁鐵指引與單位成本揭露","threshold":"2027-02 法說","action":"未達重新評估條件則不追","source_freq":"公司法說","date":"2027-02"}],"kill_metrics":[{"metric":"PPA 收入實際入帳","bear_threshold":"現貨低於 $110/kg 時，單季 PPA 為零或遭扣減","window":"任一季","source":"公司 8-K、10-Q","last_status":"ok"},{"metric":"Magnetics 單季營收","bear_threshold":"2027 Q4 低於 2,500 萬美元","window":"2027 Q4","source":"公司季報","last_status":"unknown"},{"metric":"NdPr 單季產量","bear_threshold":"2027 Q4 低於 1,200 噸","window":"2027 Q4","source":"公司季報","last_status":"unknown"},{"metric":"10X 試車時程","bear_threshold":"2028 年底試車延後超過 2 季","window":"至 2029 Q2","source":"公司法說與 8-K","last_status":"ok"},{"metric":"期末現金與短期投資","bear_threshold":"10X 完工前低於 5 億美元","window":"至 10X 完工","source":"公司季報","last_status":"ok"}],"action_conditions":{"rearm_trigger":"2027 Q4 前 NdPr 單季產量達 1,350 噸，且 Magnetics 單季營收達 5,000 萬美元、部門 EBITDA 率達 20%，觸發後重跑研究","exec_line":"現在不建倉；條件達成後重跑研究，首倉上限 3%；若價格先跌到 $28 而兩項營運指標未惡化，可先建 1%。","holding_cap":"首倉不超過 3%"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"wait_for_price":true,"wait_for_price_condition":"等 2027 下半年磁鐵與成本數字；若數字未到而股價先跌到約 $28，且營運指標未惡化，只建 1%。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"Mountain Pass 在 2027 下半年穩定跑到每月 450～500 噸 NdPr，靠固定成本攤提與氯鹼自製降低單位成本，Materials 在底價保護下成為穩定的現金來源。","2y":"FY2028 NdPr 產量 ≥ 5,500 噸，Materials 調整後 EBITDA ≥ 2.5 億美元（不含一次性銷售）","5y":"FY2031 NdPr 產量 ≥ 6,500 噸（含第三方原料），Materials EBITDA ≥ 4 億美元","10y":"2035 年底價到期後，不靠補貼仍有正 EBITDA","threshold":"2027 Q4 單季產量 ≥ 1,350 噸，且扣除一次性銷售後的 Materials 調整後 EBITDA ≥ 5,000 萬美元","source":"公司季度新聞稿與法說","drift_rule":"TTM 產量或部門 EBITDA 連 2 季偏離目標路徑 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"Independence 在 2027 下半年進入量產節奏，Magnetics 在 2028 年靠真實磁鐵出貨賺錢，而不是靠前驅物遞延收入，10X 按時在 2028 年底試車。","2y":"FY2028 Magnetics 營收 ≥ 3 億美元，部門 EBITDA 率 ≥ 25%","5y":"FY2031 磁鐵年出貨 ≥ 8,000 噸，Magnetics 營收 ≥ 9 億美元","10y":null,"threshold":"2027 Q4 單季 Magnetics 營收 ≥ 5,000 萬美元，部門 EBITDA 率 ≥ 20%；10X 2028 年底前試車","source":"公司季度新聞稿、法說與 8-K","drift_rule":"TTM 部門營收連 2 季偏離目標路徑 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"DoW 協議如約履行（底價、10X 包銷、最低 EBITDA），且部分 10X 產能轉給願付更高價格的商業客戶，在合約到期前建立不靠補貼的獲利基礎。","2y":"PPA 每季依差額入帳、無撥款延遲；2028 年底前至少 1 份具名商業客戶承接 10X 產能","5y":"10X 商業客戶占比 ≥ 30%，10X EBITDA 高於 1.4 億美元保障線","10y":"2035 年前完成續約或找到商業替代","threshold":"PPA 單季入帳不中斷；DPA 撥款不低於依當季差額推算的年付款；2028 年底前具名商業合約 ≥ 1 份","source":"10-Q PPA 附註、國防授權與撥款文件、公司 8-K","drift_rule":"連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"NdPr 現貨續弱，Materials 愈來愈靠補貼維持；前一輪下行曾讓營收減半、EBITDA 轉負，精礦外銷也已停止。","h_ref":"H1","clock":"⚡","threshold":"Ex-China NdPr 連 2 季均價低於 $85/kg，或單季 PPA 每公斤低於差額 40% 以上","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3","end_markets#1"]},{"id":"R2","text":"磁鐵爬坡慢於預期，客戶集中使單一計畫延遲直接反映到營收。","h_ref":"H2","clock":"🔥","threshold":"連 4 季 Magnetics 營收低於 Base 路徑 20%，或 10X 試車延後超過 2 季","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3"]},{"id":"R3","text":"政府依賴：PPA 與包銷需要年度撥款，也帶來稽核、調查與貿易政策變動的風險。","h_ref":"H3","clock":"🐢","threshold":"DPA 撥款低於推算的年付款，或出現政府稽核、False Claims Act 調查","evidence_refs":["customer_concentration_credit#1","regulatory_antitrust#0","reg_tariff_export#0"]},{"id":"R4","text":"全球與美國磁鐵新產能超前需求，10X 轉單時的議價力低於管理層描述。","h_ref":"H2","clock":"🐢","threshold":"美國或盟友對手取得 OEM 量產定點，或 2028 年底前 10X 沒有具名商業合約","evidence_refs":["supply_demand_durability#1","supply_demand_durability#2","competitive_share_entrants#1"]}],"single_thing":{"description":"DoW 協議被實質打折：NdPr 底價或 10X 最低 EBITDA 保障因撥款不足、重新議約或稽核爭議而無法足額入帳。","why_fatal":"這是模型裡最大的單一敏感項。假設 NdPr 回到 $60/kg，底價價值約（110−60）×6,000 噸＝3 億美元，加上 10X 最低 EBITDA 1.4 億美元，合計 4.4 億美元，約占 Base FY2031 EBITDA 6.6 億的三分之二。","if_happens":"Base 的 FY2031 EBITDA 跌回約 2.2 億美元，情境改用無保護的 Bear，股價低於 $10，10X 的回收假設也要重估；清倉。","how_monitor":"每季 10-Q 的 PPA 收入與應收款；DPA 撥款與國防授權法案；10-Q 風險因子是否新增稽核或調查字眼。","probability":"8%（2026-11 至 2028-11）。Litinsky 2026-11-05 稱合約具約束力，也有兩黨支持，但撥款仍須國會年度處理。"}},"appendix_a":{"growth_durability":6,"quality_score":4,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":47.85,"peg_fy2":null,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-0.5,"FY2026E":-0.01,"FY2027E":0.74,"FY2028E":1.31},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS，FY2026E～FY2028E 為 Koyfin 共識；基期為負，三年 CAGR 無法計算。分析師家數依 Chartmill 為 23 位（2026-10，原文未核）。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"regulatory","event":"美國國防供應鏈對中國來源材料的禁令生效，政府曾考慮延長部分取用","impact":"中","watch":"是否延期，以及 MP 是否取得新增國防訂單"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報，首批 GM 磁鐵出貨與 2027 年展望","impact":"高","watch":"磁鐵量、單位成本與 2027 指引是否量化"},{"date":"2027-Q1","date_precision":"quarter","type":"capacity","event":"氯鹼廠第一階段啟動，年初成本可能波動","impact":"中","watch":"停機天數與單位成本"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"Apple 磁鐵開始貢獻，GM 放量","impact":"高","watch":"Magnetics 單季營收與部門 EBITDA 率"},{"date":"2028-Q2","date_precision":"quarter","type":"product","event":"釤與釓計畫預計於上半年首度生產","impact":"中","watch":"投產時程與合約毛利"},{"date":"2028-Q4","date_precision":"quarter","type":"capacity","event":"10X 預計試車","impact":"高","watch":"時程、資本支出與具名商業合約"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟢', val='🟠', moat_trend='→', week26=-47.49, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
