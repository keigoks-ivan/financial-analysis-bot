你是 DD 管線 v20 的判斷層閘（gate），標的 3037.TW（20261019）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（30 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP 合併）＝42.89 十億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（Total Revenue 42,889.8M）；setn 法說報導 YoY +32%、QoQ +14.5%（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：查無 Q2 共識
- `f_kpi1_gaap`（q1_business）｜GAAP 毛利率＝24.8 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance 毛利 10,638M ÷ 營收 42,890M；與 setn／uanalyze 報導 24.8% 一致（uanalyze 寫 24.08% 屬筆誤）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／營業利益率＝6.65 十億 TWD（營益率 15.5%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance Operating Income 6,651M；營益率 6,651÷42,890＝15.51%，與媒體報導一致（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：查無
- `f_kpi3_eps`（q1_business）｜稅後淨利（歸屬母公司）／EPS＝13.11 十億 TWD；EPS 8.45 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance Net Income 13,115M；媒體報導 EPS 8.45。業外收益約 8.9 十億（利息收入、轉投資與金融資產評價轉盈、深圳聯能處分利益），淨利品質低於營業利益（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：查無
- `f_kpi6_q3_2026`（q1_business）｜管理層指引（Q3 2026／全年）＝營收與毛利率續季增；AI 伺服器營收占比目標 >60%；無數字區間 定性｜期間與口徑：Q2 2026 法說（2026-07-28／29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：setn 法說報導 https://www.setn.com/news/1881053；管理層未給產能利用率與價格的數字指引。券商估 Q3 營收約 49.78 十億（QoQ +16%）、毛利率約 28%（外部估計，非公司指引）。2026 資本支出預算由 34 十億上調至 53.7 十億，長交期設備採購上調至 31.6 十億；Guangfu Fab 1 三期 Q3 量產、Fab 2 於 2027 Q2 量產（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 法說（2026-07-28／29））
  - 註記：n/a
- `f_peer_3037_tw_gross_margin_pct`（q2_moat）｜3037.TW 毛利率＝19.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_operating_margin_pct`（q2_moat）｜3037.TW 營業利益率＝10.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_fcf_margin_pct`（q2_moat）｜3037.TW FCF 利潤率＝-0.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3189_tw_gross_margin_pct`（q2_moat）｜3189.TW 毛利率＝23.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3189_tw_operating_margin_pct`（q2_moat）｜3189.TW 營業利益率＝10.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3189_tw_fcf_margin_pct`（q2_moat）｜3189.TW FCF 利潤率＝7.37 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8046_tw_gross_margin_pct`（q2_moat）｜8046.TW 毛利率＝16.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_8046_tw_operating_margin_pct`（q2_moat）｜8046.TW 營業利益率＝12.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_8046_tw_fcf_margin_pct`（q2_moat）｜8046.TW FCF 利潤率＝7.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.7 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝38.22 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝62.74 TWD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.8483 @ 2026-10-08)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝185831.18 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate 0y 平均（19 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝271148.92 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1640.39 m shares｜期間與口徑：2026-10-19／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝1.16 十億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow：營業現金流 7,491M − 資本支出 6,333M（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：n/a
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝0.5 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance Stock Based Compensation 32.4M ÷ 營業利益 6,651M；金額小，非稀釋風險（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-42934.21 TWD m｜期間與口徑：2026-10-19／yfinance 最新一季：總債務 50188.16、現金 93122.37（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1120.0 TWD｜期間與口徑：2026-10-19（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝73.15 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝12.33 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.04 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-19（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝61.35 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 20.7，分子＝快照價 1270.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝65.53 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-19（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：2026 年 9 月法人分析：客戶對公司治理疑慮升高，可能認證更多供應商分散風險，相關競爭者含景碩、南電、IBIDEN、SEMCO、Toppan、AT&S；但欣興 ABF 高階產品比重高、訂單移轉難度大。另有 9/6 報導指市場擔心高層涉案觸發美系大廠供應鏈合規條款，關注訂單是否轉向日本大廠、南電或景碩（皆為市場疑慮，非已發生之轉單）
  - 來源：中時 wantrich 2026-09-02／2026-09-06 報導（as_of 2026-09-06）｜affects：moat_trend、decision_inputs.bear、triggers
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：桃園地檢署於2026年8月下旬搜索欣興總部（龜山）與中壢廠，懷疑將中國製PCB運回台灣更換產地標示；涉嫌法條為刑法偽造私文書、妨害農工商罪（產地標示），非反壟斷。14名主管員工被詢問，一名PCB事業部總經理以1500萬元交保，尚未公布起訴。公司表示全力配合調查。
  - 來源：Focus Taiwan／Taiwan Plus 報導（Unimicron suspected of relabeling China-made products）（as_of 2026-08-29）｜affects：thesis.R、decision_inputs.bear、triggers
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年 8～9 月檢調搜索欣興，指其大陸廠 PCB 涉嫌洗產地；有本土法人認為列入美國實體清單機率偏低，需留意美國海關扣貨、補稅與客戶重新稽核供應鏈（搜尋摘要轉述，未開原頁核對）
  - 來源：中時 wantrich.chinatimes.com 2026-09-10 報導（搜尋結果）（as_of 2026-09-10）｜affects：decision_inputs.bear、triggers、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：PCB 大廠欣興涉嫌將中國製產品標示為台灣製造，遭檢方搜索，屬地緣政治下的原產地合規風險
  - 來源：科技新報 technews：PCB 大廠欣興電子涉嫌將中國製產品標示為台灣製造（as_of 2026-09-05）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：分析稱最壞情境為未達實質轉型標準時，美國海關扣貨、補稅與客戶重新稽核產地文件；調查集中在 PCB 而非載板
  - 來源：Wistock 分析 blog.wistock.ai（搜尋結果摘要）（as_of 2026-09-06）｜affects：thesis.R、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：部分外資關注 HDI 獲利與執行風險；一家美系外資指初期良率偏低使 AI HDI/PCB 毛利率展望偏弱（共識與公司樂觀展望有落差之處）
  - 來源：工商時報 wantrich（搜尋摘要）（as_of 2026-07-30）｜affects：decision_inputs.bear、thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-08-28 桃園地檢署指揮市調處至欣興搜索，涉嫌妨害農工商罪（產地標示爭議）；公司稱爭議產品主要是PCB而非載板，將配合調查，認為對財務業務無重大影響
  - 來源：技術新報 search and investigation；uanalyze 欣興指今遭檢調調查對財務及業務並沒有重大影響（as_of 2026-08-28）｜affects：decision_inputs.bear、thesis.R、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-10-13 楊梅一廠發生工安意外，勞檢處依法課以部分停工處分；公司稱目前不影響生產營運，罰鍰金額未定
  - 來源：自由時報 焦點股》欣興：桃園一廠因工安意外部分停工 衝擊股價回測月線（as_of 2026-10-13）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年第一季欣興營收265.66億元、毛利率20.56%，年減11.75個百分點；2023年第二季營收252.35億元，為8個季度以來新低（搜尋摘要轉述，未取得逐字原文）
  - 來源：鉅亨網／搜尋摘要（欣興2023年Q1、Q2財報報導）（as_of 2023-08-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年第三季毛利率19.7%，低於市場預期；外資歸因於產能利用率偏低與產品組合不佳，BT基板因稼動率太低而虧損（搜尋摘要轉述）
  - 來源：鉅亨網／搜尋摘要（欣興2023Q3毛利率報導）（as_of 2023-11-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024年第二季營收278.77億元（6季新高），但毛利率降至13.21%，季減3.05個百分點；公司稱PCB產線調整、學習曲線較長，載板折舊逐季上升（搜尋摘要轉述）
  - 來源：中央社 2024-07-31 欣興法說報導（as_of 2024-07-31）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-08-28 桃園地檢署刑事搜索（妨害農工商罪、產地標示），屬刑事調查而非民事／團體訴訟；未見投保中心團體訴訟或專利訴訟
  - 來源：技術新報 search and investigation（as_of 2026-08-28）｜affects：decision_inputs.bear、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261019/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1936,"bear_5y_price":330,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-17.9,"ev5y_pct":-18.2,"irr_base_pct":-3.9,"asym_ratio":0.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.7,"pe":54.1,"basis":"FY2026E 共識 EPS（含 Q2 業外一次性收益約89億元）；終端倍數以終端年當年 EPS 為分母，同屬當年度預估口徑"},"eps":{"bull":[40,66,76,82,88],"base":[35,52,48,42,46],"bear":[30,33,24,18,22]},"pe":{"bull":22,"base":20,"bear":15},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.177,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 4 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 7 | 5 |
| substitute_technology | found | 1 | 3 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 6 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 5 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：欣興 大客戶 第二供應商 OR 轉單 2026；欣興 客戶 自製 OR 分散供應商；3037.TW Unimicron Technology largest customer second source OR in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3037.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"欣興電子"},"oneliner":"欣興是 AI 高階 ABF 載板龍頭，供需缺口推升報價與毛利率；但現價已按高於2022前高的利潤率定價，又有產地標示刑案與2027年起同業擴產兩道風險，報酬風險比偏差，等回檔。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261019/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261019/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 加速器晶片商的錢：ABF 載板占營收52%，錢卡在高階載板產能這一節點，現在是賣方市場。","reasoning":"Q2 2026 營收428.9億元，年增32%；毛利率24.8%，營益率15.5%。分部組成為 ABF 載板52%（年增51%）、HDI 22%（年增29%）、BT 載板9%、PCB 9%。上半年載板與 PCB 的 AI 產品占比都超過六成，公司預期下半年分別升到70%與65～70%。歸屬母公司淨利131億元裡，約89億元是業外收益，來源包括利息、轉投資評價與處分深圳聯能，所以本業獲利品質低於 EPS 8.45元看起來的樣子。產業位置在擴張期，依據有兩項：法人估 ABF 缺口2027年約21～25%、2028年約36～42%；客戶用3～7年長約加預付款鎖量。供需屬週期性、會反轉，供給可逆性高：景碩2027年、IBIDEN 2027下半年、南電2029上半年都有新產能開出，欣興自己2027年光復二廠的 ABF 產能也會增加三成以上。單點依賴方面，據報導欣興在美系 AI ASIC 載板市占超過70%，這是護城河的證據，同時也是集中度風險；客戶別占比事實表未涵蓋。產業態勢屬雙向拉鋸：供需缺口擴大是結構轉好；產地標示刑案帶來客戶合規風險；2027年起同業擴產則是競爭惡化。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_eps","f_kpi6_q3_2026"],"verdict_values":{"revenue_quality":"中：本業營收量價齊揚，可信度高；但 Q2 淨利約三分之二來自業外，EPS 品質低於營收品質","unit_econ_note":"載板屬重資產：2026年資本支出537億元，約占全年共識營收29%；2024年折舊上升曾把毛利率壓到13～14%","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"毛利率高低點擺動超過20個百分點（2022年35.9%→2025年13.9%），資本支出占營收結構性高於15%"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：法人估 ABF 缺口2027年約21～25%、2028年約36～42%，但同業新產能2027下半年到2029年陸續開出，供給可逆性高","bargaining":{"up":"上游 T-glass、銅箔、鑽針短缺，材料商議價力上升","down":"賣方市場；客戶簽3～7年長約並預付款","geo":"ABF 產能全部在台灣；PCB 有中國四個廠加泰國新廠，產地標示爭議集中在 PCB"},"profit_pool_dir":"現階段利潤往載板廠移動","tam_table":{"expanded":false,"reason":"事實表未涵蓋 ABF 市場規模與欣興份額時間序列；供需缺口只有第三方估計，已寫在成長題"}}}},"q2_moat":{"verdict":"護城河方向持平：定價力正在擴大，治理與執行面卻在侵蝕客戶黏著，兩者相抵。","reasoning":"護城河機制是高階 ABF 載板的製程良率加上客戶認證週期。據報導欣興在 AI ASIC 載板的市占超過70%，客戶簽3～7年長約並預付款，可見轉換成本真實存在。同業 ROIC 事實表未涵蓋，改用利潤率比較：TTM 毛利率19.85%，低於3189.TW的23.26%、高於8046.TW的16.04%；營益率10.24%，與3189.TW的10.12%相當、低於8046.TW的12.27%；自由現金流利潤率−0.4%，兩家同業約7.4～7.7%。換句話說，目前的優勢主要表現在定價，資本效率還沒顯現。執行力給6分：刑案搜索、AI HDI 良率偏低、工安部分停工。定價力給8分：多次漲價、長約預付。綜合約7分。","fact_refs":["f_peer_3037_tw_gross_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_3037_tw_fcf_margin_pct","f_peer_3189_tw_gross_margin_pct","f_peer_3189_tw_operating_margin_pct","f_peer_3189_tw_fcf_margin_pct","f_peer_8046_tw_gross_margin_pct","f_peer_8046_tw_operating_margin_pct","f_peer_8046_tw_fcf_margin_pct","f_kpi1_gaap"],"verdict_values":{"moat":{"mechanism":"高階 ABF 載板良率加客戶認證週期，配合3～7年長約與預付款鎖量","execution":6,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價力在擴大：2026年多次調漲、下半年再漲，法人估漲幅10～15%，Q2 毛利率由17.96%升到24.8%。執行面在縮減：2026年8月產地標示刑案；法人指客戶可能認證更多供應商；美系外資指 AI HDI 初期良率偏低；10月13日楊梅一廠工安意外部分停工。兩軸相抵，判持平。目前沒有已經發生轉單的證據，所以不判下降。","competitor_notes":[{"name":"3189.TW（景碩）","strategy_note":"楊梅六廠擴產，ABF 產能增加25%到5,000萬顆，2027年陸續開出；TTM 毛利率與自由現金流都優於欣興"},{"name":"8046.TW（南電）","strategy_note":"嘉義新廠投資468億元，最快2029上半年才貢獻營收，2027–2028年只靠去瓶頸；營益率略高於欣興"},{"name":"4062.T（IBIDEN）","strategy_note":"日系龍頭，新產能多半在2027下半年開出；事實表營收欄缺失，無法比較利潤率"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用毛利率、營益率與自由現金流利潤率對照","threats":[{"level":"🟡","text":"主要客戶因治理疑慮認證第二供應商，可能的對象包括景碩、南電、IBIDEN、SEMCO、Toppan、AT&S；目前仍是市場疑慮，尚未發生轉單","p":"25%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"同業與欣興自身的 ABF 新產能集中在2027下半年至2029年開出，賣方市場可能提前結束","p":"40%","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"EMIB-T 等先進封裝基板世代轉換，首階良率目標只有50%，良率爬坡不如預期會讓份額讓給對手","p":"20%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低周轉；利益率由低轉中（TTM 營益率10.24%，最新一季15.5%）。投入資本事實表未涵蓋，ROIC 無法精算","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"AI 加速器與伺服器 CPU 都需要 ABF 載板，屬於需要而非想要；載板與 PCB 的 AI 產品占比上半年已超過六成，晶片設計商是決策者也是付款者"},{"item":"決策層級","level":"🟡","text":"替代要經過晶片設計商重新認證，而且有3～7年長約，轉換成本高；但治理疑慮已讓法人提出客戶可能多認證供應商，替代性正在上升"},{"item":"價值鏈分配","level":"🟡","text":"現在載板廠拿到較大份額（漲價、預付款），但上游 T-glass、銅箔短缺也在分走利潤；2023–2024年供過於求時毛利率曾跌到13～14%，分配比例會隨循環擺動"},{"item":"社會容忍度","level":"🟡","text":"屬企業間交易，沒有社會性價格天花板；限制來自地緣與原產地合規，產地標示刑案顯示監管容忍度是實際約束"}],"roiic":"事實表未涵蓋投入資本與折舊，增量 ROIC 無法計算","reinvest_rate":"明顯高於100%：2026年資本支出預算537億元，TTM 營業利益約153億元（營益率10.24%乘以 TTM 營收約1,490億元）","endo_ceiling":null,"formula_note":"TTM 營收的推法：2026上半年803.36億元年增28.42%，回推2025上半年約625.6億元；2025全年1,312.4億元減去上半年，得下半年約686.8億元；兩段相加約1,490億元。投入資本缺值，內生成長上界留空"}}}},"q3_growth":{"verdict":"成長跑道中等：供需缺口估計撐到2028年，之後同業與自身產能開出，第二條成長曲線還沒有來源佐證。","reasoning":"成長來自量價齊揚，沒有併購，也沒有回購。三年共識 EPS 從 FY2025 實際4.34元到 FY2028 的62.74元，年複合約143%；若以 FY2026 的20.7元為起點，年複合也有約74%。共識與內生能力之間的缺口，主要來自毛利率擴張（2025年13.94%→Q2 2026 24.8%）與漲價，不是再投資報酬。投入資本事實表未涵蓋，內生天花板算不出來；這段成長要靠利潤率回到並超過前高，所以信心上限為中。FY2027 共識淨利率約23%（38.22元×16.4億股÷2,711億元），已經高於2022年高峰約21%。衰退信號亮兩個：自由現金流連兩年為負；EPS 成長遠高於營收成長。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"量價齊揚：AI 載板出貨量增加，加上2026年多次漲價（法人估漲幅10～15%）；無併購、無回購","runway_years":"約3年（供需缺口估計延續到2028年）","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板無法計算（缺投入資本）；共識三年 EPS 年複合約143%，靠毛利率擴張與漲價，不是靠再投資報酬","segments":[{"item":"ABF 載板","value":"Q2 2026 營收占52%，季增22%、年增51%；2026年資本支出的80～85%投入"},{"item":"HDI","value":"營收占22%，季增14%、年增29%；美系外資指 AI HDI 初期良率偏低"},{"item":"BT 載板","value":"營收占9%；2023年第三季曾因稼動率低而虧損"},{"item":"PCB","value":"營收占9%；產地標示爭議集中在此業務"}],"decay_signals":["自由現金流相對淨利連兩年低於0.75：2024年與2025年自由現金流分別約−164億元與−111億元（亮）","EPS 成長顯著高於營收成長：FY2027 共識 EPS 年增約85%，營收年增約46%（亮）","毛利率連兩季年減：未亮，Q2 2026 毛利率24.8%為近年高點","核心市占縮減：未亮，客戶分散供應目前仍是市場疑慮"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：重押擴產換成長，自由現金流還沒轉正，而且是發行新股而不是買回股票。","reasoning":"Q2 2026 營業現金流74.9億元，減去資本支出63.3億元，自由現金流11.6億元，相對歸屬淨利131億元的轉換率不到一成。TTM 自由現金流利潤率−0.4%，同業約7.4～7.7%。2026年資本支出預算由340億元上調到537億元，其中80～85%投入 ABF。SBC 只占營業利益0.5%，不是稀釋來源；但2026年6月董事會決議現金增資發行海外存託憑證，子公司蘇州群策也申請港股上市，股本方向是擴張。淨現金約429億元，資產負債表撐得住擴產。現金去向四分事實表未涵蓋。","fact_refs":["f_kpi4","f_kpi5_sbc","f_peer_3037_tw_fcf_margin_pct","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購；子公司赴港上市屬分拆籌資，不算併購"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"無回購；2026年6月董事會決議現金增資發行海外存託憑證，方向是發行新股"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占 Q2 營業利益0.5%，金額小"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能而非併購；近三年現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 FY2027–2028 的利潤率站上並長期停在前一循環高點以上才划算，我不相信它能維持到終端年。","reasoning":"現價1,120元，相當於 FY2026 共識 EPS 的54倍、FY2027 的約29倍、FY2028 的約18倍。trailing 本益比73倍、P/S 12.3倍、EV/S 12倍，三項都落在四個年度端點的最高處。FY2026 的分母含 Q2 約89億元業外收益，換算約每股5.4元；FY2027–2028 的分母則建立在高於2022前高的淨利率上，所以分母本身就是爭點。用前瞻 PEG 說便宜（以四年低基期算約0.38）不成立。循環股高峰盈餘給18～29倍並不便宜。外資目標價區間1,200～1,500元，高於現價，代表賣方仍採結構性看法，與本判斷方向相反。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi3_eps"],"verdict_values":{"valuation":{"basis":"Fwd P/E，以 FY2027 共識為主錨（FY2026 含 Q2 業外一次性收益）","tier":"台灣 ABF 載板三雄","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業 Fwd P/E 與目標價"},"fwd_pe":54.1,"peg":0.38,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"現價1,120元，相當於 FY2026 共識54倍、FY2027約29倍、FY2028約18倍。分位用四個年度端點代理，非連續五年序列：本益比、P/S、EV/S 都在端點最高。FY2027 共識淨利率約23%，已高於2022高峰約21%，循環高峰盈餘配這個倍數偏貴；但外資目標價仍高於現價，所以未到極貴。","upside_short_pct":-16,"upside_mid_pct":-18,"denominator_disputed":true,"denominator_note":"FY2026 EPS 含 Q2 約89億元業外收益（利息、轉投資評價、處分深圳聯能）；FY2027–2028 EPS 要靠高於前一循環高點的淨利率，以前瞻倍數論證便宜不成立"}}},"q6_how_wrong":{"verdict":"最可能看錯的有兩處：供需缺口比我估的更久，漲價延續到2029年；或者產地標示案升級，導致高階客戶轉單。","reasoning":"第一處會讓 Base 情境過度保守，見反證紀錄中的價格與利潤率矛盾。第二處會讓 Bear 情境來得比預期早，見治理矛盾與風險一。衰退信號亮兩個，價值陷阱風險為中。","fact_refs":["f_kpi4","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高點估值，自由現金流連年為負"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.7,"pe":54.1,"basis":"FY2026E 共識 EPS（含 Q2 業外一次性收益約89億元）；終端倍數以終端年當年 EPS 為分母，同屬當年度預估口徑"},"eps":{"bull":[40,66,76,82,88],"base":[35,52,48,42,46],"bear":[30,33,24,18,22]},"pe":{"bull":22,"base":20,"bear":15},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.18,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-78,"hi":-60,"basis":"Bear 終點約−70%（22元×15倍＝330元）。2023年營收年減26%，毛利率由35.9%掉到19.5%，循環反轉時盈餘腰斬以上。現價又在四個年度端點的最高倍數，倍數與盈餘雙殺下，回撤落在−60%到−78%","trigger_time":null},"basis":{"bull":"缺口延續到2029年，長約鎖住高價，淨利率維持25%以上，AI 產品占比持續提高；終端倍數22倍（同業 Fwd P/E 事實表未涵蓋，以自身2022高峰後的倍數區間對照）","base":"缺口撐到2028年，2029–2030年同業產能開出後利潤率回落，再隨 AI 量增回升；FY2028 EPS 52元，低於共識62.74元","bear":"2027下半年起產能集中開出，碰上 AI 資本支出放緩或客戶因合規轉單，利潤率回到上一輪谷底附近，終端倍數15倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023年營收年減26%，毛利率由35.9%掉到19.5%；2023年第三季 BT 載板因稼動率低而虧損","assumption":"同業與欣興自身在2027下半年至2029年新增的 ABF 產能，碰上 AI 資本支出放緩","consequence":"2029–2030年 EPS 回到20元上下，倍數15倍，五年後約−70%","ruling":"採納：寫進 Bear 情境並給35%機率。與唯一致命點（報價首次季減）部分重疊，致命點就是這段故事的起點","watch":"每季毛利率與 ABF 報價方向；同業擴產時程","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"],"fact_refs":["f_kpi1_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026年資本支出537億元；2024–2025年自由現金流合計約−275億元；2026年6月決議發行海外存託憑證","assumption":"需求如預期，但長約把價格鎖住，擴產又吃掉現金並稀釋股本","consequence":"營收翻倍，每股自由現金流仍偏低，股東拿不到漲價紅利","ruling":"部分採納：長約加預付款保護了量，但可能壓低漲價上限，長約價格條款事實表未涵蓋。以 FY2027 自由現金流是否轉正來驗證","watch":"FY2027 自由現金流與股本變動","evidence_refs":["major_events#2"],"fact_refs":["f_kpi4","f_peer_3037_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"現價1,120元，相當於 FY2026 共識54倍、FY2027約29倍；trailing 本益比、P/S、EV/S 都在四個年度端點最高；26週上漲65.5%","assumption":"市場已經把 FY2027 約23%的淨利率（高於2022前高）當成常態","consequence":"利潤率只要回到前高附近，倍數與盈餘就會雙殺","ruling":"採納：Base 情境五年報酬為負，等回檔","watch":"股價相對 FY2027 共識 EPS 是否回到20倍以下","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1120.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1120.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"治理疑慮與訂單黏著","cause":null,"prior_field":null,"side_a":"法人指客戶對公司治理疑慮升高，可能認證更多供應商；市場擔心高層涉案觸發美系大廠的供應鏈合規條款，分析指最壞情況是美國海關扣貨、補稅、客戶重新稽核","side_b":"高階 ABF 比重高，訂單移轉不易；ABF 產能全部在台灣，爭議產品是 PCB 而非載板；9月營收年增64.7%，看不到轉單","ruling":"目前偏向後者：月營收沒有轉單跡象，爭議集中在 PCB。但起訴與否、2027年長約續簽要到2026年底至2027年才知道，在那之前不能說風險已解除，所以 Bear 機率維持35%","evidence_level":"中：轉單疑慮是市場推測，營收數字是公司實際公告","settle_metric":"是否起訴公司法人；任一美系客戶是否公告第二供應商；月營收年增率","if_then":["若檢方起訴公司法人，或任一主要美系客戶公開導入第二供應商，持有者清倉，未持有者不建倉","反向條件：若調查只停在個人責任、不擴及載板，且月營收年增維持30%以上直到2027年第一季，此風險移出 Bear 情境加權，Bear 機率調降到30%"],"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0"]},{"axis":"共識盈餘路徑與前一循環利潤率上限","cause":null,"prior_field":null,"side_a":"FY2027 共識淨利率約23%，已高於2022高峰約21%；同業與欣興自身2027下半年起擴產；2023年循環反轉時，毛利率一年內掉了16個百分點","side_b":"現在就買的最強論證：法人估 ABF 缺口2027年約21～25%、2028年約36～42%；客戶用3～7年長約加預付款鎖量；現價只有 FY2028 共識的約18倍","ruling":"選前者。缺口估計來自賣方與二手轉述，沒有原報告可驗證；長約的價格條款事實表未涵蓋，無法證明利潤率鎖得住。Base 情境 FY2028 EPS 取52元，低於共識的62.74元","evidence_level":"中：前者是公司實際財報，後者是第三方估計","settle_metric":"2027年各季毛利率是否守在24%以上","if_then":["若2027上半年兩季毛利率都在28%以上，且月營收年增40%以上，Bull 機率由20%調升到30%，價格合理時小倉起步","若任一季毛利率季減3個百分點以上，Bear 機率調升到45%，不建倉"],"evidence_refs":["cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#5","end_markets#5"]}],"triggers":[{"n":1,"text":"單季毛利率連兩季跌破22%，代表漲價循環提前結束","type":"假設驗證","maps_to":"H1","metric":"單季毛利率","threshold":"<22%，連2季","action":"不建倉；已持有者減碼一半","source_freq":"每季財報","date":"2027-01"},{"n":2,"text":"產地標示刑案升級：檢方起訴公司法人，或任一主要美系客戶公開導入第二供應商","type":"風險","maps_to":"R1","metric":"起訴或客戶第二來源公告","threshold":"任一發生","action":"清倉","source_freq":"事件，公開資訊觀測站重大訊息與新聞","date":null,"evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#1"]},{"n":3,"text":"高階 ABF 載板報價出現首次季減","type":"Single Thing","maps_to":"Single Thing","metric":"ABF 報價季變動，依法說會與產業報價","threshold":"首次季減","action":"清倉","source_freq":"每季法說會","date":null},{"n":4,"text":"股價回到約 FY2027 共識 EPS 的20倍以下，而且毛利率沒有破線，就重跑研究","type":"估值rearm","maps_to":null,"metric":"股價相對 FY2027 共識 EPS","threshold":"股價≤765元，且最近一季毛利率≥24%","action":"重跑研究，通過後小倉起步","source_freq":"每日股價與每季財報","date":null},{"n":5,"text":"同業新產能開出後，月營收年增率明顯放緩","type":"風險","maps_to":"R2","metric":"月營收年增率","threshold":"<10%，連3個月","action":"減碼","source_freq":"每月10日前營收公告","date":"2027-07","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":6,"text":"良率或停工拖累毛利率","type":"風險","maps_to":"R3","metric":"單季毛利率季變動","threshold":"季減3個百分點以上，且公司歸因於良率或停工","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["capital_markets_pricing#2","major_events#1","cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"Q3 2026 法說會後複審","type":"複審日期","maps_to":null,"metric":"Q3 毛利率與 Q4 展望","threshold":"毛利率是否優於24.8%","action":"更新情境機率","source_freq":"一次","date":"2026-10"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<20%，連2季","window":"2027Q1–2028Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"<10%，連3個月","window":"2027全年","source":"公開資訊觀測站月營收公告","last_status":"ok"},{"metric":"產地標示刑案進展","bear_threshold":"起訴公司法人，或客戶公告第二來源","window":"2026Q4–2027Q4","source":"檢方發布與公司重大訊息","last_status":"warning"},{"metric":"年度自由現金流","bear_threshold":"FY2027 自由現金流<0","window":"FY2027","source":"年報現金流量表","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","exec_line":"不追；股價回到765元以下且毛利率未破24%，才重跑研究，首倉以小倉起步","holding_cap":"≤3%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2028 共識 EPS 約18倍定價，等於把高於2022前高的淨利率當成常態；2027下半年起同業與欣興自身擴產開出後，載板利潤率歷史上會回落，2023年毛利率一年掉了約16個百分點","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤765元，且最近一季毛利率≥24%","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2028 共識 EPS 約18倍定價，等於把高於2022前高的淨利率當成常態；2027下半年起同業與欣興自身擴產開出後，載板利潤率歷史上會回落，2023年毛利率一年掉了約16個百分點"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=65.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":["QC-50"]},"thesis":{"H":[{"id":"H1","text":"ABF 供需缺口延續到2027年，報價續漲，毛利率守住新高區","2y":"2027年底前單季毛利率維持24%以上","5y":null,"10y":null,"threshold":"單季毛利率≥24%（Q2 2026 為24.8%）","source":"公司季報、法說會","drift_rule":"單季毛利率連2季低於22%為削弱；連3季低於20%為反轉"},{"id":"H2","text":"AI 產品占比提升，讓這一輪循環的谷底利潤率高於上一輪","2y":null,"5y":"2029–2031年年度營益率谷底≥12%（上一輪谷底為2024年的4.43%）","10y":null,"threshold":"年度營益率谷底≥12%；AI 產品營收占比≥65%","source":"年報、法說會 AI 營收占比","drift_rule":"TTM 營益率連4季低於門檻5%以上為削弱；連6季低於門檻10%以上為反轉"},{"id":"H3","text":"537億元擴產能在兩年內回收，轉為正自由現金流","2y":"FY2027 自由現金流轉正，利潤率≥5%","5y":null,"10y":null,"threshold":"FY2027 自由現金流利潤率≥5%（TTM 為−0.4%）","source":"年報與季報現金流量表","drift_rule":"TTM 自由現金流利潤率連2季低於5%為削弱；連3季為負為反轉"}],"R":[{"id":"R1","text":"產地標示刑案升級為起訴、美國海關扣貨或客戶啟動合規條款，高階客戶轉向第二供應商","h_ref":"H1","clock":"⚡","threshold":"起訴公司法人，或任一主要美系客戶公開導入第二供應商","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#1"]},{"id":"R2","text":"同業與欣興自身的新產能在2027下半年至2029年集中開出，供需反轉，重演2023年的毛利率下滑","h_ref":"H2","clock":"🔥","threshold":"單季毛利率季減3個百分點以上連2季，或報價季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","competitive_share_entrants#2","cyclical_supply_discipline_capacity#2"]},{"id":"R3","text":"執行面失誤：AI HDI 良率偏低、折舊上升、工安停工拖累毛利率，重演2024年第二季的情況","h_ref":"H3","clock":"🔥","threshold":"單季毛利率低於24.8%，且公司歸因於良率、停工或折舊","evidence_refs":["capital_markets_pricing#2","major_events#1","cyclical_prior_downcycle_behavior#2"]}],"single_thing":{"description":"高階 ABF 載板報價出現首次季減，宣告這一輪漲價循環結束","why_fatal":"共識 FY2027–2028 EPS 要靠高於2022前高的淨利率；上一輪循環反轉時，營收一年減26%、毛利率掉16個百分點。報價是盈餘最大的單一敏感項，倍數也會跟著壓縮","if_happens":"清倉，等循環位置回到深谷或早循環再重跑研究","how_monitor":"每季法說會的報價說法與毛利率；月營收年增率；景碩、IBIDEN 2027下半年新產能的開出進度","probability":"20%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":29.3,"peg_fy2":0.4,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.34,"FY2026E":20.7,"FY2027E":38.22,"FY2028E":62.74},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；共識取 Koyfin 美元值，依2026-10-08匯率換算為新台幣"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"Q3 2026 法說會：毛利率是否優於 Q2 的24.8%，以及2027年資本支出","impact":"高","watch":"毛利率與漲價是否延續"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"光復二廠後續產能於2027年第二季開出","impact":"中","watch":"新產能稼動率與價格"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"景碩、IBIDEN 新增 ABF 產能於2027下半年開出","impact":"高","watch":"報價是否轉弱"},{"date":null,"date_precision":null,"type":"regulatory","event":"產地標示刑案偵查結果，是否起訴","impact":"高","watch":"是否擴及公司法人或載板產品"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
