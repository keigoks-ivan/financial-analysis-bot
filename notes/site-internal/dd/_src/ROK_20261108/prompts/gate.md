你是 DD 管線 v20 的判斷層閘（gate），標的 ROK（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝2332 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（SEC 轉載公司 IR 新聞稿）（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi1_enterprise_operating_pro`（q1_business）｜企業營業利益（enterprise operating profit，公司口徑；新聞稿未列 GAAP operating income）／利益率＝24.5 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜稅前利益（GAAP）／利益率＝18.6 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi3_segment_operating_margin`（q1_business）｜總部門營業利益率（segment operating margin，三部門加總，依新聞稿數字自算；公司未列總計）＝24.3 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：部門盈餘 588M ÷ 部門銷售 2,417M；公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi4_adjusted_eps_non_gaap`（q1_business）｜Adjusted EPS（non-GAAP）＝3.88 USD｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_kpi6_fy2027`（q1_business）｜管理層 FY2027 指引（全年）＝Adjusted EPS 14.50–15.50；GAAP 稀釋 EPS 13.78–14.78；報告營收成長 4.5%–7.5%；有機成長 6%–9% USD／%｜期間與口徑：公告於 2026-11-05（FY2027 全年指引）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[6]，as_of 公告於 2026-11-05（FY2027 全年指引））
  - 註記：EPS 中值 15.00；FY1 共識 EPS 於財報後由 13.24 升至 14.92（見 consensus_revision，dd_numbers_extra.py）
- `f_peer_rok_gross_margin_pct`（q2_moat）｜ROK 毛利率＝49.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_rok_operating_margin_pct`（q2_moat）｜ROK 營業利益率＝19.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_emr_gross_margin_pct`（q2_moat）｜EMR 毛利率＝53.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_emr_operating_margin_pct`（q2_moat）｜EMR 營業利益率＝20.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ph_gross_margin_pct`（q2_moat）｜PH 毛利率＝37.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ph_operating_margin_pct`（q2_moat）｜PH 營業利益率＝21.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hon_gross_margin_pct`（q2_moat）｜HON 毛利率＝38.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hon_operating_margin_pct`（q2_moat）｜HON 營業利益率＝16.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝14.92 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝16.67 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝18.48 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝9575.33 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝10131.83 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_fcf`（q4_capital）｜自由現金流（FCF）＝602 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Q4 FY26 8-K Ex.99（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未取得
- `f_peer_rok_fcf_margin_pct`（q2_moat）｜ROK FCF 利潤率＝16.51 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3119.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 3552.0、現金 433.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝111.27 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.469 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝375.86 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝25.19 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 14.92，分子＝快照價 375.86｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝29.97 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝31.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝31.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝98.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝12.69 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（13.24 → 14.92）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝12.86 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 13.22 → 14.92（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-16.68 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.86｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w250`（q5_valuation）｜250 週均線＝299.56 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：若無法達成目標可能流失業務或價格受侵蝕；預期競爭水準維持高檔，可能限制維持或提高市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-12）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Citi 2026 會議上 CEO 回應 AI 顛覆疑慮，Siemens/NVIDIA 工業 AI 作業系統被視為較具威脅的競爭問題。
  - 來源：Fintool: Rockwell Citi conference AI disruption（as_of 2026-02-28）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：FY26 Q4 Lifecycle Services 衰退 9%，Software and Control 有機成長 15%、Intelligent Devices 5%；先前一季 book-to-bill 0.97、ARR 成長 6% 導致全年 ARR 指引下調
  - 來源：finsee.ai ROK Q4 2026 earnings review（搜尋摘要）（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美、墨、加、中等貿易政策變動與關稅可能推升成本，轉嫁價格能力受競爭與合約限制。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：Section 232 機器人與工業機械調查：公告認定進口構成國安威脅，目前未課關稅（搜尋摘要，日期未核）。
  - 來源：White & Case, Section 232 investigation on robotics and industrial machinery（as_of 2026-01-01）｜affects：thesis.R、triggers
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：10-K風險因素為一般性供應商依賴：仰賴外部供應商與分包商提供設備、電子零件與大宗商品，短缺或漲價會影響製造效率與準時交貨；未見具名單一來源或特定地區集中。
  - 來源：Rockwell Automation FY2025 10-K 之搜尋摘要（as_of 2025-11-06）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Lifecycle Services FY2026 sales $2,071M, -6%; Q4 $519M, -9% (organic +2%, divestitures -11% per search summary)
  - 來源：Rockwell Automation FY2026 Q4 earnings release (8-K Ex.99)（as_of 2026-11-05）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：若未能預判並推出回應客戶偏好與新興技術趨勢（含 AI 採用與整合）的產品，產品需求可能下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-12）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Schneider Electric 專欄稱開放式自動化把軟體與硬體脫鉤、採 IEC 61499 等開放標準。
  - 來源：Creamer Media newsletter: Open automation is breaking legacy chains in 2026（as_of 2026-03-02）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":744.8,"bear_5y_price":272.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":35.4,"ev5y_pct":32.2,"irr_base_pct":6.2,"asym_ratio":3.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.42,"pe":28.01,"basis":"FY2026 實際 Non-GAAP EPS 13.42 美元（TTM，含 0.11 美元關稅退款淨利益），與終端倍數的 trailing 分母同口徑。"},"eps":{"bull":[15.5,18.0,20.8,23.7,26.6],"base":[14.9,16.4,18.0,19.6,21.2],"bear":[14.2,12.8,13.6,14.9,16.0]},"pe":{"bull":28,"base":24,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.469,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ROK_Q3_2026_Earnings_Call_20260804.md
- 2026-08-04｜Blake Moret｜guidance：FY26 reported and organic sales growth guidance raised to 7.5%-9.5%（原話："7.5% to 9.5% range for the year."）
- 2026-08-04｜Christian Rothe｜guidance：Adjusted EPS guide raised to $13-$13.30, midpoint up $0.35（原話："adjusted EPS guidance range to $13 to $13.30."）
- 2026-08-04｜Blake Moret｜guidance：FY26 enterprise operating margin and FCF conversion guide maintained（原話："operating margin to be 21.5%, up 260 basis points"）
- 2026-08-04｜Christian Rothe｜guidance：Guidance excludes any IEEPA refunds or claims（原話："impact from expected IEEPA refunds or claims resulting from"）
- 2026-08-04｜Christian Rothe｜guidance：Q4 guide: sales up low single digits sequentially, enterprise margin about flat vs Q3, citing inflation and mix（原話："up low single digits sequentially with approximately flat"）
- 2026-08-04｜Christian Rothe｜guidance：Q4 Software & Control segment margin expected lower sequentially on flat sales, memory inflation（原話："margin in Software & Control to be lower sequentially"）
- 2026-08-04｜Christian Rothe｜guidance：FY26 segment guide: Intelligent Devices low double-digit growth, margin ~20%（原話："Devices reported revenue to grow in the low double digits"）
- 2026-08-04｜Christian Rothe｜guidance：FY26 Lifecycle Services revenue to decline about $150M due to Sensia and longer-cycle headwinds（原話："revenue to decline about $150 million year-over-year"）
- 2026-08-04｜Christian Rothe｜guidance：Modeling items: buybacks ~$850M for the year, diluted shares ~112.2M（原話："million in repurchases for the year."）
- 2026-08-04｜Christian Rothe｜margin：Q3 enterprise margin expansion drivers and Sensia contribution（原話："positive impact of about 40 basis points on enterprise"）
- 2026-08-04｜Christian Rothe｜margin：Intelligent Devices Q3 margin was below management's expectation（原話："120 basis points year-over-year, lower than we expected."）
- 2026-08-04｜Christian Rothe｜margin：Q3 core price/cost unfavorable; price increase implemented late Q3 to be realized in Q4（原話："reflecting rising costs and the timing of price increases."）
- 2026-08-04｜Christian Rothe｜margin：Incremental margin disclosed on reported and organic basis, fourth straight quarter above 40%（原話："an as-reported basis and over 40% on an organic basis."）
- 2026-08-04｜Christian Rothe｜margin：Price breakdown: Q3 tariff price 1%, underlying near 0; tariff price intended for EPS neutrality, not incremental（原話："really there to create EPS neutrality around tariff-based"）
- 2026-08-04｜Christian Rothe｜margin：Q3 EPS walk: tax was a $0.20 headwind, largely BEPS Pillar Two（原話："Tax was a $0.20 headwind, largely due to BEPS"）
- 2026-08-04｜Christian Rothe｜margin：On 2027 S&C margin, CFO says price alone is hard to deliver expansion against inflation; volume should help（原話："get margin expansion off of the price alone"）
- 2026-08-04｜Christian Rothe｜margin：Clarified Q4 S&C margin expectation as roughly 33%, not high 20s（原話："we're not looking at it to be in the 20s in Q4."）
- 2026-08-04｜Christian Rothe｜risk：Inflation headwind escalating across quarters (single-digit M, double-digit M, now higher double-digit M for 2H)（原話："So it is, in fact, increasing."）
- 2026-08-04｜Christian Rothe｜risk：CFO does not expect inflation to stabilize soon, memory biggest driver tied to data center demand（原話："it's not one of those that we're expecting to stabilize"）
- 2026-08-04｜Blake Moret｜risk：Organic ARR growth of 6% was below expectations, services recurring softer（原話："grew 6% in the quarter, below our expectations."）
- 2026-08-04｜Blake Moret｜risk：Lifecycle Services down 2% organic, constrained by lack of F&B and process capex recovery（原話："organic sales were down 2% versus prior year"）
- 2026-08-04｜Blake Moret｜risk：Expects continued tariff volatility and geopolitical uncertainty heading into FY27（原話："continue to expect tariff volatility, hope for the best,"）
- 2026-08-04｜Blake Moret｜customer：Strong demand verticals vs. no capex pickup in F&B and parts of process（原話："not yet seeing a pickup in CapEx across Food & Beverage"）
- 2026-08-04｜Blake Moret｜customer：E-commerce & Warehouse Automation sales up 30% year over year（原話："Automation sales were up 30% year-over-year"）
- 2026-08-04｜Blake Moret｜customer：Organic growth ex-data center would still have been 8%（原話："took everything out that was related to data center"）
- 2026-08-04｜Blake Moret｜customer：Automotive: renewed project activity but management not calling it a broad opening（原話："I'm not ready to call that the flood gates are open,"）
- 2026-08-04｜Blake Moret｜customer：Customer reasons for project delays: cautious capital deployment, funding constraints, terms and conditions（原話："Overall, it's a cautious approach to deploying capital."）
- 2026-08-04｜Christian Rothe｜customer：Book-to-bill inside normal corridor in Q3 (previously slightly above)（原話："Q3 was inside of that corridor."）
- 2026-08-04｜Blake Moret｜competition：Management says it is gaining share in controllers（原話："we're gaining market share in controllers."）
- 2026-08-04｜Blake Moret｜competition：Logix being standardized by hyperscalers over traditional DDC units in data center central utility plant（原話："standardization on those units by the hyperscalers"）
- 2026-08-04｜Blake Moret｜competition：Competitive wins in drug substance MES in Life Sciences（原話："increasing competitive wins in drug substance"）
- 2026-08-04｜Blake Moret｜product：New products cited as driving results（原話："excited about the accelerated pace of new product launches"）
- 2026-08-04｜Blake Moret｜product：Software & Control organic +18%, driven by Logix（原話："Software & Control organic sales were up 18%"）
- 2026-08-04｜Blake Moret｜product：Plex: software ARR at high single digits, new logos, agentic AI embedded（原話："Yes, feeling good about Plex."）
- 2026-08-04｜Blake Moret｜commitment：Management expects Clearpath (AMR) to be profitable in Q4（原話："we'll be profitable in Clearpath in the fourth quarter."）
- 2026-08-04｜Christian Rothe｜commitment：Expects positive price/cost for full year and Q4（原話："positive price/cost both for the full year and in Q4."）
- 2026-08-04｜Christian Rothe｜commitment：Tariffs to be EPS neutral in FY26（原話："We remain on track for tariffs to be EPS neutral in"）
- 2026-08-04｜Christian Rothe｜commitment：FY27 initial outlook to be given next quarter（原話："a quarter from now, we'll give that initial outlook."）
- 2026-08-04｜Christian Rothe｜capital_allocation：FY27 capex to exceed FY26 (~3% of sales), around 4%, New Berlin greenfield（原話："we're going to be spending more CapEx than this year."）
- 2026-08-04｜Christian Rothe｜capital_allocation：CFO says ROIC has recovered and higher investment should stay accretive（原話："ROIC for us has actually recovered nicely."）
- 2026-08-04｜Christian Rothe｜capital_allocation：Q3 free cash flow $654M; FY FCF conversion 100% maintained（原話："Q3 of $654 million was above our expectations."）

### 問答異常語氣（迴避／改口／保留）
- ROK_Q3_2026_Earnings_Call_20260804.md｜問：Jeff Sprague asked for the size of the Q3 price/cost headwind and Q4 jump-off into 2027｜答法：CFO declined to quantify ("probably not going to dimensionalize exactly what the numbers were"), only ranked volume/mix/price-cost qualitatively
- ROK_Q3_2026_Earnings_Call_20260804.md｜問：Andrew Buscaglia asked how to set up Software & Control margins for 2027 against tough comps｜答法：No 2027 numbers; said it is early and outlook comes next quarter, while noting price alone cannot expand margin against inflation
- ROK_Q3_2026_Earnings_Call_20260804.md｜問：Andrew Obin asked what gets better on inflation over 6-12 months｜答法：CFO did not offer an improvement timeline; said inflation is increasing and not expected to stabilize soon, pivoting to pricing/productivity levers

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：ROK Rockwell Automation antitrust OR monopoly investigation 2026；Rockwell Automation regulation OR regulatory scrutiny Specialty Industrial Machinery 2026；ROK Rockwell Automation DOJ OR FTC OR EU competition 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260620","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"工業短週期復甦延續 + reshoring 結構需求：organic growth 持續","columns":{"具體數字門檻（sourced floor）":"FY26 organic ≥ +7%（midpoint guide）連 4 季；訂單成長維持雙位數；FY27 organic ≥ +5%","信息來源":"ROK Q2 FY26 法說（organic +9%、上修 7% guide）｜BofA reshoring 8% organic note｜Reshoring Initiative 244k jobs","漂移觸發條件（連 2 季 / QC-34）":"連 2 季 organic &lt; +5%（TTM 計）；或訂單成長轉負"}},{"id":"H2","text":"margin 擴張兌現：Enterprise OM 站穩 21%+ 並向 22-23% 邁進","columns":{"具體數字門檻（sourced floor）":"FY26 Enterprise OM ≥ 21.5%（上修 guide）；incremental margin 維持 ~40%+；FY28 OM ≥ 22%","信息來源":"Q2 FY26 OM 22.5% +350bps、上修至 21.5% guide｜incremental margin low-50s","漂移觸發條件（連 2 季 / QC-34）":"連 2 季 Enterprise OM &lt; 20%（從 22.5% 回落 = 復甦獲利兌現失利）"}},{"id":"H3","text":"市場願維持 FPE 28-35x（vs peer 20x 溢價合理）；不 derate 至 22x 以下","columns":{"具體數字門檻（sourced floor）":"FY27 FPE 維持 28-35x；reshoring 溢價持續","信息來源":"5Y FPE history (~20-35x)｜共識均標 $462｜EMR/Siemens peer 20x","漂移觸發條件（連 2 季 / QC-34）":"連 4 季 FPE 漂移至 &lt; 25x = re-rating；或現價持續 &gt; 共識均標 = 透支"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"短週期復甦熄火（reshoring 訂單兌現慢 / 全球 capex 放緩）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"organic growth、訂單成長","警戒閾值":"organic 連 2 季 &lt; +5%"}},{"id":"R2","text":"競爭加劇：Siemens/Schneider/ABB/中國廠在 NA 或全球壓價搶份額","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期結構（2+ 年）","監測指標":"ROK NA 市佔、price/cost、GM 趨勢","警戒閾值":"GM 連 2 季 YoY 下滑 + 市佔流失"}},{"id":"R3","text":"估值 derate：市場不再給 reshoring 溢價，FPE 向 peer 20x 收斂","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"FY27 FPE、現價 vs 共識均標","警戒閾值":"連 1-2 季 FPE 漂移至 &lt; 25x"}},{"id":"R4","text":"OT/IT 融合 / 開放式軟體定義 PLC 長期侵蝕硬體鎖定","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期結構（2+ 年）","監測指標":"開放式 PLC 採用率、ROK 硬體 vs 軟體 mix","警戒閾值":"硬體段份額結構性下滑"}},{"id":"R5","text":"margin 擴張不可持續（comp cost / mix 反轉）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Enterprise OM、incremental margin","警戒閾值":"OM 連 2 季 &lt; 20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":473.79,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ROK","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Rockwell Automation"},"oneliner":"ROK 的控制平台與利潤率兌現良好，但現價約 25 倍 FY2027 EPS，共識三年路徑沒有下行年，基準情境年化不到 8%，等 340 美元以下再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ROK_20261108/scenario.json","answers":{"q1_business":{"verdict":"ROK 賺的是工廠把控制標準定在 Logix 之後的持續採購，錢卡在控制器與軟體這一節點。Software & Control 占 FY2026 部門營收約 31%，第四季貢獻約 44% 的部門盈餘。","reasoning":"FY2026 部門營收：Intelligent Devices 4,185 百萬美元（約 46%，+11%）、Software & Control 2,818 百萬美元（約 31%，+18%）、Lifecycle Services 2,071 百萬美元（約 23%，−6%，主要因 Sensia 合資解散）。第四季部門利益率依序為 21.6%、34%、16.4%，三部門盈餘 588 百萬美元，Software & Control 約 256 百萬美元。TTM 毛利率 49.35%。第四季 Enterprise 營業利益率 24.5%，其中 1.3 個百分點來自關稅退款、0.5 個百分點來自 Sensia，剔除後約 22.7%，不能拿 24.5% 當常態。產業位於擴張期：第四季核心成長 7%、離散產業 +20%、美國新產能投資創新高，但管理層明說指引沒有假設資本支出全面回升，採礦專案仍在延後，食品飲料資本支出偏弱。單點依賴在通路：約 65% 銷售經獨立經銷商，前兩大經銷商約占 20%（FY2025 10-K），這既是觸及客戶的優勢，也是集中度風險；單一終端客戶占比事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi1_enterprise_operating_pro","f_kpi2_gaap","f_kpi3_segment_operating_margin","f_kpi4_adjusted_eps_non_gaap","f_kpi6_fy2027","f_peer_rok_gross_margin_pct"],"verdict_values":{"revenue_quality":"約 65% 經獨立經銷商銷售；第四季有機成長含約 2.5 個百分點價格；有機 ARR 成長 5%，ARR 絕對規模事實表未涵蓋。","unit_econ_note":"FY2026 增量利益率：Software & Control 在 50% 高段，Intelligent Devices 在 30% 高段；全公司剔除關稅退款約 50%，FY2027 指引降到 30% 高段。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利控制平台，獲利隨工業資本支出循環波動，FY2024 營收 −8.77%。"},"industry":{"clock_phase":"II","sd_verdict_source":"偏週期、結構為輔：資料中心與半導體約占營收 10%、FY2027 指引中十位數成長，屬結構性；其餘多數垂直仍看資本支出循環，事實表也沒有能區分再工業化結構性與週期性的 2027 至 2028 預測。","bargaining":{"up":"記憶體與 PCB 供應商議價力上升，Rothe 2026-11-05 說通膨未消退、PCB 供應偏緊。","down":"下游分散，但約 65% 經獨立經銷商，前兩大約占 20%。","geo":"北美是最快成長區，美國 FY2026 有機成長逾 12%；對墨西哥、加拿大、中國的進口受關稅政策影響。"},"profit_pool_dir":"公司內部利潤向控制器與軟體集中；產業層級的利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池占比，無法展開；這項缺口限制了跑道判斷，不代表不重要。"}}}},"q2_moat":{"verdict":"護城河方向穩定。Logix 控制平台的標準地位仍在賺錢，但份額上升只有管理層自述，外部份額與同業 ROIC 都沒有資料，不足以判定擴大。","reasoning":"機制是工廠、機器製造商與工程人員把控制系統標準化在 Logix 與其軟體工具上，換系統要重寫程式、重新認證、重訓人員。可證方向：QTS、Stryker 的標準化案，Logix 第四季 +25%，控制器出貨量已高於疫情前（2026-11-05，Moret）；2026-08-04 Moret 也說在控制器取得份額。反向證據是這些都來自管理層，事實表沒有第三方份額。執行力判擴大：FY2026 Enterprise 營業利益率 +330 個基點，其中營運改善 270 個基點。定價權判穩定：FY2027 規劃約 3 個百分點價格，但 Rothe 2026-08-04 說單靠漲價難擴張利潤率，第三季 price/cost 也一度為負。同業比較：ROK TTM 毛利率 49.35%，高於 HON、PH、ETN，低於 EMR 的 53.61%；營業利益率 19.74%，低於 EMR 與 PH。ROIC 20.4%（CFO，TTM），同業 ROIC 事實表未涵蓋，所以評等不上到 A。當期報酬屬高利益率×低周轉，用 FY2026 Enterprise 營業利益率 22.2%、稅率 19.6% 倒推周轉約 1.1 倍。","fact_refs":["f_peer_rok_gross_margin_pct","f_peer_rok_operating_margin_pct","f_peer_emr_gross_margin_pct","f_peer_emr_operating_margin_pct","f_peer_ph_gross_margin_pct","f_peer_ph_operating_margin_pct","f_peer_hon_gross_margin_pct","f_peer_hon_operating_margin_pct","f_peer_etn_gross_margin_pct","f_peer_etn_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"工廠與機器製造商把控制系統標準化在 Logix 與其軟體工具上，轉換成本來自重寫程式、重新認證與重訓人員，再由約 65% 銷售所經的獨立經銷網放大。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行力擴大，定價權穩定，合併為方向穩定。沒有出現最大客戶份額下滑的具名證據，也沒有第三方份額佐證上升。","competitor_notes":[{"name":"EMR","strategy_note":"最接近的利潤率對照，毛利率與營業利益率都略高於 ROK，說明 ROK 的毛利優勢並非同業第一。"},{"name":"PH","strategy_note":"毛利率低很多但營業利益率高於 ROK，營運效率是值得對照的標竿。"},{"name":"HON","strategy_note":"毛利率與營業利益率都低於 ROK，FCF 利潤率 4.95% 偏低，原因事實表未涵蓋，不宜直接比較現金品質。"},{"name":"ETN","strategy_note":"毛利率明顯低於 ROK，產品重疊主要在電力，直接競爭控制平台的證據事實表未涵蓋。"},{"name":"Siemens","strategy_note":"事實表沒有財務數字；10-K 列為主要對手，與 NVIDIA 的工業 AI 作業系統是目前最值得防的生態攻擊。"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 事實表未涵蓋，改用毛利率與營業利益率比較，無法證明報酬差距擴大。","threats":[{"level":"🔴","text":"Siemens 與 NVIDIA 的工業 AI 作業系統試圖把決策層移到控制器之上，屬生態攻擊；ROK 也與 NVIDIA 合作，但主導權不在自己手上，AI 淨增量 ARR 也未揭露。攻擊者投入資本量級事實表未涵蓋。","p":"30%","evidence_refs":["competitive_share_entrants#3","substitute_technology#0"]},{"level":"🟡","text":"開放式自動化把軟體與硬體脫鉤；來源是 Schneider 自家專欄，採用率事實表未涵蓋，ROK 已把 Logix 放上開放運算平台應對。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"10-K 預期競爭維持高強度，可能限制份額與獲利，屬點對點競爭常態。","p":"常態存在","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是控制工程師，決策者是廠方與機器製造商的標準制定者，付款者是資本支出預算。工廠提升生產力與韌性的問題長期存在，但購買可以延後：2026-11-05 Moret 說採礦等產業專案被延後而非取消，FY2024 營收 −8.77%。"},{"item":"決策層級","level":"🟢","text":"替代要以整座工廠或整個機型的控制標準為單位衡量，不是單顆控制器。QTS、Stryker、Vale 都是平台標準化案，換掉要重寫程式、重新認證與重訓。代理讀數只有 Logix 第四季 +25% 與管理層稱續約強勁，續約率與流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"約 65% 銷售經獨立經銷商，前兩大約占 20%，下游分潤穩定。上游的記憶體與 PCB 正在多拿：Rothe 2026-11-05 說通膨未消退、第一季最難，PCB 供應偏緊。AI 層若由運算平台主導，長期也會分走價值。"},{"item":"社會容忍度","level":"🟢","text":"產品賣給企業，不是民生必需品，也不靠監管授權，沒有政治定價上限。關稅退款後公司主動提列 85 百萬美元退給客戶，屬客戶關係管理，不是社會壓力。"}],"roiic":"20.4%（以 TTM ROIC 代理；投入資本逐年值事實表未涵蓋，真實增量報酬無法計算）","reinvest_rate":"≤21.9%（FY2027 資本支出約 383 百萬美元 ÷ NOPAT 約 1,752 百萬美元；折舊與營運資金事實表未涵蓋）","endo_ceiling":4.5,"formula_note":"單位為百分比。資本支出＝共識營收 9,575 百萬美元×指引 4%；NOPAT＝15.00 美元×110.4 百萬股＋利息 120 百萬美元×（1−20%）。內生上限＝20.4%×21.9%≈4.5%。把全部資本支出當成長性投入是刻意取高，FY2027 指引 FCF 轉換率 100% 也顯示淨再投資很少。可能看錯的方向：若增量報酬高於平均（Software & Control 增量利益率逾 50% 暗示有此可能），上限會被低估。"}}}},"q3_growth":{"verdict":"五年後的跑道中等：資料中心與半導體約占營收 10%、FY2027 指引中十位數成長，但 TAM 與滲透率事實表未涵蓋，不足以確認第二條成長曲線。","reasoning":"三年共識 EPS CAGR 11.25%（13.42 到 18.48 美元，2026-11-07 Koyfin 快照，家數事實表未涵蓋）；基期剔除 0.11 美元關稅退款後為 11.6%。內生上限 4.5%，缺口約 6.75 個百分點。歸因：FY2026 營收約 8,989 百萬美元（部門合計 9,074 減客戶退款 85）到 FY2028 共識 10,132 百萬美元，CAGR 約 6.2%，高於內生上限的部分主要是約 3 個百分點的漲價，不需資本；同期 EPS CAGR 約 11.45%，與營收差約 5.3 個百分點，其中淨回購約 1.5 個百分點，其餘約 3.8 個百分點來自利潤率擴張。缺口可歸因於利潤率與淨回購，不依賴倍數重估，但表示成長品質低於靠再投資複利的公司。FY2027 有機指引 6% 至 9% 含 1 個百分點關稅退款基期效應，中值的真實成長是 6.5%，低於 FY2026 核心 9%。美國新產能 Moret 形容約在第四局，屬管理層自述。","fact_refs":["f_kpi6_fy2027","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"FY2027 有機 6% 至 9%：價格約 3 個百分點，關稅退款基期 1 個百分點，其餘為量；無併購，回購貢獻 EPS 0.20 美元。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"沿用報酬持續期欄位：TTM ROIC 20.4%×再投資率上限 21.9%≈4.5%，是取高的上限。","segments":[{"item":"Intelligent Devices","value":"FY2026 營收 4,185 百萬美元，+11%；全年利益率 20%；FY2027 指引中個位數成長，利益率約 +100 個基點。"},{"item":"Software & Control","value":"FY2026 營收 2,818 百萬美元，+18%；全年利益率 33.8%；FY2027 指引高個位數成長，利益率小幅上升。"},{"item":"Lifecycle Services","value":"FY2026 營收 2,071 百萬美元，−6%，主因 Sensia；第四季有機 +2%、訂單出貨比 0.97；FY2027 指引有機低個位數成長，利益率約 +100 個基點。"}],"decay_signals":["亮燈：EPS CAGR 高於營收 CAGR 超過 5 個百分點（FY2026 至 FY2028 約 11.45% 對 6.2%）。","未亮：FCF／淨利連 2 年低於 0.75（FY2025 約 156%，FY2026 公司口徑 113%）。","資料缺口：毛利率季度同比、市占、SBC、維護性資本支出、產業倍數三年變化，事實表未涵蓋。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置尚可：股數確實在減、槓桿低於 2 倍，但以現價回購的盈餘殖利率只有約 4%，回購不算便宜。","reasoning":"FY2026 FCF 轉換率 113%，含關稅退款 6 個百分點，剔除後約 107%；第四季 FCF 602 百萬美元，轉換率 139%，退款貢獻約 21 個百分點；FY2027 指引回到 100%。全年回饋股東約 19 億美元，以股息約 6 億美元估算回購約 13 億美元，FY2027 只規劃約 6 億美元。資本支出由營收約 3% 升到約 4%，用於美國綠地新廠與數位基礎設施。淨負債 3,119 百萬美元，信評 A-／A3／A。近 12 個月沒有併購。資料差異：公司口徑全年 FCF 按 13.42 美元×約 112 百萬股×113% 約 17 億美元，yfinance TTM FCF 利潤率 16.51% 換算約 14.8 億美元，差異原因事實表未涵蓋，本輪不以 FCF 絕對額做承重判斷。現金去向四分與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi5_fcf","f_peer_rok_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_consensus_eps_fy1","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 沒有併購完成項目；歷史併購投入與回報事實表未涵蓋，無法計算。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以現價算 FY2027 盈餘殖利率 3.97%（14.92÷375.86）；10Y 殖利率與回購均價事實表未涵蓋，但只有 10Y 低於 1.97% 才會過關，故判不過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 金額事實表未涵蓋；目前股數 111.27 百萬股，FY2027 回購 6 億美元按現價約減 1.6 百萬股，年均約 0.8 百萬，與指引平均稀釋股數 110.4 百萬股相符，隱含淨發行接近零，低於 1.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，且現金去向四分事實表未涵蓋，主要數字已寫在本題理由。"}}}},"q5_valuation":{"verdict":"現價要求 FY2031 EPS 約 21 美元、終端仍有 24 倍，才有年化約 7.7%。這個假設我相信，但報酬不夠厚，跌到 340 美元以下才有約 10% 年化。","reasoning":"現價 375.86 美元，FY2027 共識 EPS 14.92 美元，前瞻本益比 25.19 倍；三年 CAGR 11.25%，PEG 2.24，屬偏貴。基準情境 FY2031 EPS 21.2 美元乘 24 倍得 508.8 美元，價格年化約 6.2%，加股息約 7.7%，其中 EPS 複利約 9.6%、倍數下降約 −3.0%、股息約 1.5%，沒有靠倍數重估。敏感度：FY2031 EPS 少 10%，目標價少約 51 美元；終端倍數少 2 倍，少約 42 美元；FY2031 利潤率少 1 個百分點，少約 22 美元。成長熄火對照：三年後成長降到 15%／10%／5%，前瞻本益比約 26／21／17 倍，較現值 +3%／−17%／−33%。市場可能錯的只有一點，就是共識沒有循環，這對現價是壞事不是好事，所以本次比共識保守，不主張市場低估。賣方目標價 406.67 美元（2026-04-07）與約 421 美元（無日期）都早於這次財報，只作弱參考。五年分位無資料：事實表只有 3 個年度端點，trailing P/E 分位 31.4、P/S 分位 98.5，兩者方向相反，是利潤率上升造成的。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_percentile","f_dividend_yield_ttm","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG，Non-GAAP EPS 口徑","tier":"高品質工業自動化","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數；前份記載 EMR／Siemens 約 20 倍（2026-06-20）已過時，不足以展開。"},"fwd_pe":25.19,"peg":2.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比 25.19 倍、PEG 2.24 偏貴，但基準情境已假設倍數由 28.0 倍降到 24 倍，仍有約 7.7% 年化，多空不對稱約 3 倍，結論為合理偏貴。五年分位事實表未涵蓋，不用年度端點代替。","upside_short_pct":7.8,"upside_mid_pct":22.6,"denominator_disputed":false,"denominator_note":"FY2027 共識 14.92 美元不含關稅退款淨利益，分母可用；FY2026 的 13.42 美元含 0.11 美元退款。上行幅度以基準 EPS 乘 trailing 倍數計算，倍數由 28.0 倍線性降到 24 倍，一年後 14.9×27.2，三年後 18.0×25.6。帳面共識上修 12% 至 13% 是財年換年，同一財年 FY2027 前後都是 14.92 美元，不能當上修證據。"}}},"q6_how_wrong":{"verdict":"最可能看錯在循環：共識三年路徑沒有下行年，而 FY2024 才剛出現營收 −8.77%、GAAP 稀釋 EPS 約 −31%。","reasoning":"衰退信號亮一項，價值陷阱風險中等，依據見反證紀錄。反方向也可能看錯：若投資人日上修長期利潤率目標，且美國新產能真的還在早中段，本次 FY2028 起低於共識的基準情境會偏保守，340 美元可能等不到。歷史最大回撤事實表未涵蓋，回撤範圍改由空頭情境推導。2026-08-04 法說有三題未正面回答：Rothe 未量化第三季 price/cost 逆風、未給 2027 年 Software & Control 利潤率、未給通膨改善時間表。2026-11-05 已部分回答，Software & Control 利潤率小幅上升、通膨變化速度放緩，但 price/cost 金額仍未量化。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長靠漲價、利潤率與回購，再投資貢獻小"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.42,"pe":28.01,"basis":"FY2026 實際 Non-GAAP EPS 13.42 美元（TTM，含 0.11 美元關稅退款淨利益），與終端倍數的 trailing 分母同口徑。"},"eps":{"bull":[15.5,18.0,20.8,23.7,26.6],"base":[14.9,16.4,18.0,19.6,21.2],"bear":[14.2,12.8,13.6,14.9,16.0]},"pe":{"bull":28,"base":24,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.47,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-45,"hi":-30,"basis":"歷史最大回撤事實表未涵蓋，改由空頭情境推導：FY2028 EPS 12.8 美元乘 17 至 20 倍得 218 至 256 美元，較現價跌 32% 至 42%，上下各留緩衝。","trigger_time":null},"basis":{"bull":"資本支出全面回升、資料中心與半導體維持中十位數成長，營收 CAGR 約 8.5%，FY2031 Enterprise 營業利益率約 26%；FY2027 取指引上緣 15.5 美元。","base":"FY2027 略低於指引中值，FY2028 起低於共識，因共識沒有下行年；營收 CAGR 約 6%、FY2031 Enterprise 營業利益率約 24%、股數每年約減 1.5%。EPS 路徑已含回購，不另計殖利率以免重複。終端 24 倍 trailing 約等於 22 倍前瞻，高於前份記載的 EMR／Siemens 約 20 倍（2026-06-20，本輪事實表無更新）。","bear":"FY2027 低於指引下緣，FY2028 循環下行約 10%，比 FY2024 的 GAAP EPS −31% 溫和；FY2031 營業利益率約 21.5%。終端 17 倍對應成長熄火到 5% 的倍數。機率 30% 依據為共識成長超過內生上限，且事實表無法證明需求屬結構性。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2024 營收 −8.77%、GAAP 稀釋 EPS 由 11.95 降到 8.28 美元；FY2027 指引明說未假設資本支出全面回升，Lifecycle Services 第四季有機僅 +2%、訂單出貨比 0.97。","assumption":"共識 FY2027 至 FY2029 每年 EPS 成長 10% 以上，沒有下行年。","consequence":"FY2028 EPS 落到約 12.8 美元、倍數降到 17 至 20 倍，股價約 218 至 256 美元，較現價跌 32% 至 42%；若同時發生架構替代，五年虧 50% 才會成立。","ruling":"採納為最大風險，與唯一致命點同源，不另設第二個致命點；機率放進空頭情境 30%。FY2024 下行時公司仍賺錢且 FCF 為正，屬可守的循環，採波動保護紀律。","watch":"每季核心有機成長、Lifecycle Services 訂單出貨比。","evidence_refs":["supply_demand_durability#1","end_markets#2"],"fact_refs":["f_price_at_dd"]},{"view":"論點失敗","evidence":"Siemens／NVIDIA 工業 AI 作業系統被視為較具威脅的問題，10-K 也把 AI 採用列為需求風險，Schneider 專欄主張以開放標準脫鉤軟硬體。","assumption":"控制層仍是工廠自動化的價值匯集點。","consequence":"若決策與編排層移到控制器之上，Software & Control 34% 的利益率會先受壓，影響最大的是終端倍數。","ruling":"部分採納。FactoryTalk Conductor 長在自有工具鏈，Logix 也能在開放運算平台上跑，屬強化型回應；但 AI 淨增量 ARR 未揭露，無法證明攻守已分，分界年暫訂 2028。","watch":"Software & Control 相對 Intelligent Devices 的有機成長差、毛利率。","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"],"fact_refs":["f_peer_rok_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY2027 資本支出升到營收約 4%（FY2026 約 3%），新廠最大投資 FY2027 結束後才投入使用；回購由 FY2026 估算約 13 億美元降到 6 億美元；Software & Control 利益率 FY2027 只小幅上升，Rothe 2026-08-04 已說單靠漲價難擴張利潤率。","assumption":"新廠與資料中心訂單的報酬不低於目前 20.4% 的 ROIC。","consequence":"營收與 Logix 論點都成立，但折舊從 FY2028 起墊高、回購托底減少，EPS 成長低於簡單外推；基準 FY2029 EPS 因此低於共識約 2.6%。","ruling":"採納。基準情境 FY2028 起低於共識，不給新廠額外報酬。","watch":"FY2028 折舊與 ROIC；公司口徑 ROIC 低於 18% 即視為再投資報酬變差。","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"],"fact_refs":["f_rev_consensus_fy1_m","f_consensus_eps_fy3"]},{"view":"價格已反映太多","evidence":"前瞻本益比 25.19 倍、PEG 2.24；帳面共識上修實為財年換年；賣方目標價 407 至 421 美元都早於這次財報，全距 215 至 536 美元接近 2.5 倍。","assumption":"市場願意為一段沒有下行年的路徑付 25 倍。","consequence":"基準情境即使 EPS 年增約 10%，年化也只有約 7.7%。","ruling":"採納，結論是現價不追。較前份下跌 20.7% 主要是倍數修正，不等於安全邊際。","watch":"前瞻本益比與同財年共識 EPS。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_fy1_pct","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 473.79 → 本次 375.86（-20.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=473.79","side_b":"本次 price_at_dd=375.86","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 473.79 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 473.79 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 473.79 美元：Bull 價 744.8、Bear 價 272，五年期望值 +4.8%，基準年化 1.4%，不對稱比 1.12","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.12。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 473.79 美元：五年期望值 +4.8%，基準年化 1.4%，不對稱比 1.12","side_b":"本次情境、股價 375.86 美元：五年期望值 +32.2%，基準年化 6.2%，不對稱比 2.96","ruling":"再換股價、情境不動：起點價下跌 20.7%，五年期望值多 27.3 個百分點，基準年化多 4.8 個百分點，不對稱比由 1.12 升到 2.96。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值區間假設","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 473.79 美元，假設市場維持 28 到 35 倍前瞻本益比，估值結論偏貴。","side_b":"本次股價 375.86 美元、前瞻本益比 25.19 倍，估值結論降一級到合理偏貴。","ruling":"前份對倍數的假設已失效，本次不再把倍數維持當論點，基準情境改用倍數下降計算。跌幅不等於安全邊際，PEG 仍有 2.24。","evidence_level":"高","settle_metric":"前瞻本益比與基準年化報酬","if_then":[],"evidence_refs":[]},{"axis":"品質評級與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B，價值陷阱風險中等。","side_b":"本次兩者不變，但依據換成 FY2026 利潤率達標、ARR 連兩季不及預期，以及 EPS 成長明顯快於營收。","ruling":"維持原結論。利潤率兌現是正面新證據，ARR 落後與成長品質是負面新證據，兩者相抵。","evidence_level":"中","settle_metric":"FY2027 上半年 ARR 與 Enterprise 營業利益率","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"本次首次給值的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位為空。","side_b":"本次依新格式首次給值：護城河方向穩定、跑道中等、品質複利型兼具循環性、循環位置中段、機率 25／45／30、最大回撤 −30% 至 −45%。","ruling":"不是判斷轉向，沒有可比較的前值。","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份無重新進場條件（原文為空）。","side_b":"收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS），且 FY2027 共識 EPS 不低於 14.50 美元。","ruling":"唯一約束是價格。共識下限只用來確認分母沒壞，不是第二個等待理由。340 美元對應基準年化約 10%。","evidence_level":"中","settle_metric":"收盤價與 FY2027 共識 EPS","if_then":["若收盤價 ≤ 340 美元且共識不低於 14.50 美元，重跑研究後分批反買。","若共識跌破 14.50 美元，即使價格到位也不買，改看唯一致命點是否發生。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"organic 連 2 季 < +5%；OM 連 2 季 < 20%；連 1-2 季 FPE 漂移至 < 25x；前份未列獨立的清倉清單。","side_b":"核心有機成長連 2 季低於 5% 減碼三分之一；剔除關稅退款的 Enterprise 營業利益率連 2 季低於 22% 減碼三分之一；有機 ARR 連 2 季低於 5% 停止加碼；Software & Control 有機成長連 4 季為負且毛利率連 2 季同比下滑則清倉。","ruling":"成長門檻數字不變，但改用剔除關稅退款的口徑。利潤率門檻由 20% 升到 22%，因 FY2026 已達 22.2%。前瞻本益比低於 25 倍不再是減碼理由，因為現價已接近 25 倍且本次基準已假設倍數下降。","evidence_level":"中","settle_metric":"每季核心有機成長與 Enterprise 營業利益率","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份無唯一致命點（原文為空）。","side_b":"FY2028 之前出現連續兩季有機營收同比轉負的循環下行。","ruling":"新增，因為這是 EPS 與倍數同時受影響的最大單一敏感項。","evidence_level":"中","settle_metric":"每季有機營收同比","if_then":[],"evidence_refs":[]},{"axis":"共識上修是否真實","cause":null,"prior_field":null,"side_a":"事實表顯示 FY1 共識上修 12.69%、近 3 個月上修 12.86%。","side_b":"舊值 13.24／14.92／16.67 與新值 14.92／16.67／18.48 恰好平移一年，是財年換年，同一財年 FY2027 前後都是 14.92 美元。","ruling":"採後者，不把這些數字當上修動能。同財年修正約為零，FY2026 實際 13.42 美元高於三個月前共識 13.22 美元才是真正的超越。可能看錯之處：2026-07 Zacks 的 FY2027 估值為 13.90 美元，表示不同來源的舊值不一致。","evidence_level":"高","settle_metric":"同一財年的共識 EPS 逐週比較","if_then":["若投資人日後 FY2027 共識 EPS 高於 15.00 美元，才算真上修。","若跌破 14.50 美元，停止加碼。"],"evidence_refs":[]},{"axis":"FY2027 有機成長品質","cause":null,"prior_field":null,"side_a":"指引有機成長 6% 至 9%，中值 7.5%。","side_b":"中值含 1 個百分點客戶關稅退款的基期效應，真實成長 6.5%，低於 FY2026 核心 9% 與第四季核心 7%。","ruling":"採後者。Moret 說指引有保留，但目前只能確認成長放緩；若資本支出全面回升才會走向區間上緣。","evidence_level":"高","settle_metric":"FY2027 上半年核心有機成長","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"ARR 指引可信度","cause":null,"prior_field":null,"side_a":"Moret 2026-11-05：FY2027 ARR 成長 7%，軟體與服務都會改善。","side_b":"Moret 2026-08-04：第三季 ARR 成長 6% 低於預期；2026-11-05：第四季 5% 仍低於預期。Lifecycle Services 第四季報告 −9% 主要是 Sensia，有機 +2%。","ruling":"管理層把落後歸因於專案延後與 IT 設備漲價，未證，先監測。基準情境假設 ARR 約 6%。若 FY2027 上半年連兩季低於 6%，視為歸因證偽。","evidence_level":"中","settle_metric":"FY2027 第一、二季有機 ARR 成長","if_then":["若連兩季低於 6%，下修軟體第二曲線的權重，停止加碼。","若連兩季達到 7% 以上，跑道判斷重新檢視。"],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"Logix 是真需求還是提前拉貨","cause":null,"prior_field":null,"side_a":"Moret 2026-11-05：Logix 第四季 +25%，沒有補庫存或提前購買。","side_b":"FY2027 指引 Software & Control 降到高個位數，Logix 相近；PCB 供應偏緊，缺料期常見重複下單。通路庫存事實表未涵蓋。","ruling":"不可裁決至 FY2027 第二季財報。決勝數據未揭露，不採信也不否定管理層說法。","evidence_level":"低","settle_metric":"Software & Control 第一季指引 10% 的達成情況與第二季增速","if_then":["若第二季 Software & Control 有機成長低於 5%，視為有拉貨成分，下修 FY2028 EPS 假設。","若維持 10% 以上，上修基準情境。"],"evidence_refs":[]},{"axis":"通膨說法改變","cause":null,"prior_field":null,"side_a":"Rothe 2026-08-04：通膨在升高，不預期短期穩定。","side_b":"Rothe 2026-11-05：變化速度放緩、供應商調價通知減少，但第一季更難，PCB 供應偏緊。","ruling":"語氣轉好，尚未證實。第一季增量利益率指引 30% 中段，低於全年 30% 高段。損益層的吸收失敗以 price/cost 連兩季轉負為準。","evidence_level":"中","settle_metric":"price/cost 與第一季增量利益率","if_then":["若 price/cost 連兩季轉負，減碼三分之一。"],"evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：資料中心與半導體約占營收 10%，美國新產能投資創新高，Logix 獲超大規模資料中心採用。","side_b":"競爭與其他結構變數：Siemens／NVIDIA 工業 AI、開放式自動化，以及 Section 232 機器人與工業機械調查。","ruling":"雙向拉鋸。正面已反映在營收，負面尚未反映在數字，故護城河方向維持穩定。","evidence_level":"中","settle_metric":"Software & Control 有機成長差與 Section 232 結果","if_then":[],"evidence_refs":["competitive_share_entrants#3","reg_tariff_export#3","substitute_technology#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"RSI 28.86，股價較前份低 20.7%，FY2026 EPS 比最初指引中值高 1.72 美元，投資人日將更新長期利潤率目標，多頭情境年化逾 15%。","side_b":"基準年化不到 8%，共識沒有下行年，ARR 未達預期，前瞻本益比仍有 25 倍。","ruling":"不買。超賣與財報表現都是事實，但基準報酬不足以補償循環風險；代價是投資人日若大幅上修目標，可能買不到 340 美元。","evidence_level":"中","settle_metric":"收盤價、投資人日長期目標、同財年共識","if_then":["若股價先反彈到 420 美元以上而同財年共識沒有上修，不追。","若股價跌到 340 美元以下且基本面無損，分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 剔除關稅退款的核心有機成長要達到指引中值。","type":"假設驗證","maps_to":"H1","metric":"核心有機成長（剔除關稅退款與 Sensia）","threshold":"全年 ≥ 6.5%，第一季 ≥ 4%","action":"未達不加碼","source_freq":"季報與法說，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"Enterprise 營業利益率要達到 FY2027 指引。","type":"假設驗證","maps_to":"H2","metric":"Enterprise 營業利益率（剔除關稅退款）","threshold":"FY2027 ≥ 23%","action":"未達不加碼","source_freq":"季報與法說，每季","date":"2027-11","evidence_refs":[]},{"n":3,"text":"有機 ARR 成長要由 5% 回升到指引 7%。","type":"假設驗證","maps_to":"H3","metric":"有機 ARR 成長","threshold":"FY2027 ≥ 7%，上半年任一季 ≥ 6%","action":"上半年連兩季低於 6% 停止加碼","source_freq":"季報與法說，每季","date":"2027-05","evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"工業資本支出循環回落，核心有機成長熄火。","type":"風險","maps_to":"R1","metric":"核心有機成長","threshold":"連 2 季低於 5%","action":"減碼三分之一","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"n":5,"text":"電子料通膨吃掉漲價。","type":"風險","maps_to":"R2","metric":"price/cost、Enterprise 營業利益率（剔除關稅退款）","threshold":"price/cost 連 2 季轉負，或營業利益率連 2 季低於 22%","action":"減碼三分之一","source_freq":"季報與法說，每季","date":null,"evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"n":6,"text":"Section 232 關稅落地且無法轉嫁。","type":"風險","maps_to":"R5","metric":"Section 232 結果與當季 price/cost","threshold":"關稅落地且當季 price/cost 轉負","action":"停止加碼","source_freq":"政府公告與季報","date":null,"evidence_refs":["reg_tariff_export#3"]},{"n":7,"text":"控制平台優勢被 AI 作業系統或開放式架構削弱。","type":"風險","maps_to":"R3","metric":"Software & Control 減 Intelligent Devices 的有機成長差、毛利率","threshold":"成長差連 2 季為負且毛利率同比下滑","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"n":8,"text":"循環下行成真。","type":"Single Thing","maps_to":"Single Thing","metric":"有機營收同比","threshold":"連 2 季轉負","action":"第一季轉負停止加碼，第二季確認後減碼至半倉","source_freq":"季報，每季","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":9,"text":"價格回到足以補償循環風險的水準。","type":"估值rearm","maps_to":"現價","metric":"收盤價、FY2027 共識 EPS","threshold":"收盤價 ≤ 340 美元且共識 ≥ 14.50 美元","action":"重跑研究後分兩批建倉","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":10,"text":"跌到 250 週均線附近且基本面無損。","type":"加碼","maps_to":"現價","metric":"收盤價、FY2027 共識 EPS","threshold":"收盤價 ≤ 300 美元且共識 ≥ 14.50 美元","action":"分批反買","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":11,"text":"估值回到前份偏貴區間。","type":"減碼","maps_to":"現價","metric":"前瞻本益比","threshold":"≥ 32 倍（以 14.92 美元計約 477 美元）","action":"減碼三分之一","source_freq":"每日股價、每週共識","date":null,"evidence_refs":[]},{"n":12,"text":"控制平台地位出現實質流失。","type":"清倉","maps_to":"R3","metric":"Software & Control 有機成長、毛利率","threshold":"有機成長連 4 季為負且毛利率連 2 季同比下滑","action":"清倉","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":13,"text":"投資人日後複審長期目標與同財年共識。","type":"複審日期","maps_to":"H2","metric":"長期利潤率目標、FY2027 共識 EPS","threshold":"投資人日結束後一週內","action":"更新情境，不因目標上修直接追價","source_freq":"一次性","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"核心有機成長（剔除關稅退款與 Sensia）","bear_threshold":"連 2 季低於 5%","window":"連 2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"Enterprise 營業利益率（剔除關稅退款）","bear_threshold":"連 2 季低於 22%","window":"連 2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"有機 ARR 成長","bear_threshold":"連 2 季低於 5%","window":"連 2 季","source":"公司季報與法說","last_status":"warning"},{"metric":"Software & Control 減 Intelligent Devices 的有機成長差","bear_threshold":"連 2 季為負","window":"連 2 季","source":"公司季報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS），且 FY2027 共識 EPS 不低於 14.50 美元","exec_line":"現價不追。收盤價 ≤ 340 美元且 FY2027 共識 EPS 不低於 14.50 美元時，重跑研究後分兩批建倉；投資人日若上修長期利潤率目標，只更新情境，不因此追價。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS，基準年化約 10%），且 FY2027 共識 EPS 不低於 14.50 美元。"},"thesis":{"H":[{"id":"H1","text":"工業自動化需求延續，FY2027 剔除關稅退款後的核心有機成長站穩中高個位數。","2y":"FY2027 核心有機成長 ≥ 6.5%，FY2028 ≥ 5%","5y":null,"10y":null,"threshold":"FY2027 核心有機成長 ≥ 6.5%；FY2028 ≥ 5%；資料中心加半導體 FY2027 達中十位數成長","source":"2026-11-05 法說（Moret、Rothe）與公司季報；口徑為報告有機成長扣掉 1 個百分點的客戶關稅退款基期效應","drift_rule":"TTM 連 2 季偏離門檻 ≥ 5% 為削弱，連 3 季偏離 ≥ 10% 為反轉"},{"id":"H2","text":"利潤率擴張來自生產力與產品組合，FY2031 Enterprise 營業利益率站上 24%。","2y":null,"5y":"FY2031 Enterprise 營業利益率 ≥ 24%","10y":null,"threshold":"FY2027 ≥ 23%（指引）；FY2029 ≥ 23.5%；FY2031 ≥ 24%；price/cost 全年為正","source":"公司季報與法說；投資人日將更新長期目標","drift_rule":"TTM 連 4 季偏離門檻 ≥ 5% 為削弱，連 6 季偏離 ≥ 10% 為反轉"},{"id":"H3","text":"Logix 的工廠控制標準地位十年內不被架構替代，軟體與 ARR 補上較穩定的收入。","2y":null,"5y":null,"10y":"Software & Control 利益率維持 30% 以上，Logix 仍是主要客戶的控制標準","threshold":"FY2027 有機 ARR 成長 ≥ 7%（指引）；Software & Control 利益率 ≥ 32%；有機成長不低於 Intelligent Devices","source":"公司季報、法說、年度 10-K 競爭段落；第三方份額事實表未涵蓋","drift_rule":"跨 2 個年度低於門檻為削弱，跨 3 個年度低於門檻為反轉"}],"R":[{"id":"R1","text":"工業資本支出循環回落或專案繼續延後，核心有機成長熄火。","h_ref":"H1","clock":"🔥","threshold":"核心有機成長連 2 季低於 5%","evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"id":"R2","text":"記憶體與 PCB 等電子料通膨，加上缺料，吃掉約 3 個百分點的漲價。","h_ref":"H2","clock":"⚡","threshold":"price/cost 連 2 季轉負，或剔除關稅退款後 Enterprise 營業利益率連 2 季低於 22%","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"id":"R3","text":"Siemens／NVIDIA 工業 AI 作業系統與開放式自動化削弱 Logix 鎖定。","h_ref":"H3","clock":"🐢","threshold":"Software & Control 有機成長連 2 季低於 Intelligent Devices 且毛利率同比下滑","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"ARR 連續不及預期，軟體與服務的穩定收入沒有出現。","h_ref":"H3","clock":"🔥","threshold":"有機 ARR 成長連 2 季低於 5%","evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"id":"R5","text":"Section 232 機器人與工業機械關稅落地，轉嫁受競爭與合約限制。","h_ref":"H2","clock":"🔥","threshold":"關稅落地且當季 price/cost 轉負","evidence_refs":["reg_tariff_export#3","reg_tariff_export#1"]},{"id":"R6","text":"資料中心與半導體投資降溫，約 10% 營收的成長主題退潮。","h_ref":"H1","clock":"🔥","threshold":"合併垂直 FY2027 成長低於 10%","evidence_refs":[]}],"single_thing":{"description":"FY2028 之前出現連續兩季有機營收同比轉負的循環下行。","why_fatal":"這是數學上最大的單一敏感項。共識三年路徑沒有下行年；一旦發生，FY2028 EPS 由共識 16.67 美元落到約 12.8 美元，倍數同時降到 17 至 20 倍，股價約 218 至 256 美元。","if_happens":"第一季轉負先停止加碼，第二季確認後減碼至半倉，到 17 至 20 倍區間再分批買回；控制平台未受損就不清倉。","how_monitor":"每季有機成長、Lifecycle Services 訂單出貨比、管理層對機器製造商訂單的說法。","probability":"12 至 24 個月約 25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":22.55,"peg_fy2":2.0,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":13.42,"FY2027E":14.92,"FY2028E":16.67,"FY2029E":18.48},"fy_end_month":9,"eps_basis":"Non-GAAP Adjusted EPS。FY2026A 為公司實際值，含 0.11 美元關稅退款淨利益；三年共識來自 2026-11-07 Koyfin 快照，EPS 家數事實表未涵蓋。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日更新長期利潤率目標","impact":"高","watch":"Enterprise 營業利益率目標是否高於 FY2027 的 23%，以及 ARR 目標。"},{"date":"2026-11","date_precision":"month","type":"product","event":"Automation Fair 展示軟體定義 Logix 與 FactoryTalk Conductor","impact":"中","watch":"客戶採用案例與 AI 收入是否有量化揭露。"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"FY2027 第一季財報","impact":"高","watch":"有機成長是否達中個位數、EPS 約 3 美元、Software & Control 成長 10%、ARR 是否回升。"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"美國綠地新廠的主要投資開始投入使用","impact":"中","watch":"折舊增幅與 ROIC 是否低於 18%。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-16.68, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等收盤價 ≤ 340 美元（約 22.8 倍 FY2027 共識 EPS，基準年化約 10%），且 FY2027 共識 EPS 不低於 14.50 美元。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：regulatory_antitrust（法規／反壟斷）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
