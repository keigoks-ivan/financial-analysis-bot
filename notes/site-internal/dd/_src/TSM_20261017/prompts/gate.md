你是 DD 管線 v20 的判斷層閘（gate），標的 TSM（20261017）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝40.2 US$ billion｜期間與口徑：Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.tsmc.com 2Q26 Earnings Release（https://investor.tsmc.com/english/quarterly-results/2026/q2；同文件 SEC 6-K https://www.sec.gov/Archives/edgar/data/0001046179/000104617926000451/a2q26e_withguidancexfinal.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季度結束 2026-06-30，公告於 2026-07-16））
  - 註記：consensus 約 US$39.5–40.04B（來源：web_search 綜合媒體報導，非單一權威資料庫），實際 $40.20B 落在自結指引上緣、beat consensus 約 1.4%
- `f_kpi1_tsm_taiwan_ifrs_gaap_non`（q1_business）｜營業利益率（TSM 採 Taiwan-IFRS 單一口徑，未如美股公司分列 GAAP／Non-GAAP——此為結構性差異，不強行拆成兩筆數字）＝60.3 %｜期間與口徑：Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 2Q26 Earnings Release（同上 URL），創歷史新高（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季度結束 2026-06-30，公告於 2026-07-16））
  - 註記：毛利率 consensus 67.1% vs 實際 67.7%（beat）；營業利益率未查到明確 sell-side consensus 數字
- `f_kpi4_guidance_q3_2026_2026`（q1_business）｜管理層 guidance（下一季 Q3 2026 ＋ 全年 2026）＝Q3'26 營收 $44.6–45.8B／毛利率 65–67%／營業利益率 56–58%；FY26 營收成長上修至「40%以上」YoY（前次為 30%以上）；FY26 capex 上修至 $60–64B（另加碼美國亞利桑那 $100B 投資） guidance range（text）｜期間與口徑：公告於 2026-07-16 法說會／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 2Q26 Earnings Release ＋ 法說會逐字稿（web_search 綜合多家媒體轉引，非官方逐字稿原文）（numbers.latest_quarter_kpis.items[4]，as_of 公告於 2026-07-16 法說會）
  - 註記：N/A
- `f_kpi5_archetype`（q1_business）｜產能利用率（archetype=硬體/設備 追加項；定性描述，公司未揭露具體利用率百分比）＝— qualitative｜期間與口徑：Q2 2026 法說會（2026-07-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：web_search 法說會逐字稿摘要：管理層表示毛利率 QoQ +150bp 部分來自成本改善與「整體產能利用率提高」，未給出具體利用率數字（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026 法說會（2026-07-16））
  - 註記：N/A
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-15 date｜期間與口徑：2026-10-15／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-15）
- `f_peer_tsm_gross_margin_pct`（q2_moat）｜TSM 毛利率＝64.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsm_operating_margin_pct`（q2_moat）｜TSM 營業利益率＝56.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tsm_fcf_margin_pct`（q2_moat）｜TSM FCF 利潤率＝25.33 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TSM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvda_gross_margin_pct`（q2_moat）｜NVDA 毛利率＝74.67 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_fcf_margin_pct`（q2_moat）｜AVGO FCF 利潤率＝44.22 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amd_operating_margin_pct`（q2_moat）｜AMD 營業利益率＝15.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mu_operating_margin_pct`（q2_moat）｜MU 營業利益率＝65.67 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝16.95 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝22.65 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝28.9 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；已依 data/adr_ratios.json 換算為 adr-usd (koyfin ordinary ×5)｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5561413.97 TWD m｜期間與口徑：2026-10-17／yfinance revenue_estimate 0y 平均（41 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-17）
  - 註記：財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7647456.61 TWD m｜期間與口徑：2026-10-17／yfinance revenue_estimate +1y 平均（41 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-17）
  - 註記：財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.67 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（22.5 → 22.65）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝1.05 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（28.6 → 28.9）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_kpi2_fcf`（q4_capital）｜自由現金流（FCF）＝287.36 NT$ billion｜期間與口徑：Q2 2026（季度結束 2026-06-30，公告於 2026-07-16）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：web_search 綜合法說會揭露：營運現金流 NT$783B － 資本支出 NT$496B（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季度結束 2026-06-30，公告於 2026-07-16））
  - 註記：無明確 sell-side FCF consensus 可查
- `f_kpi3_tsm_sbc_sbc`（q4_capital）｜員工酬勞性現金紅利占營收%（TSM 依台灣公司法走員工利潤分配現金紅利，非美式股權 SBC，口徑不同、不可直接類比美股公司 SBC%）＝2.93 %｜期間與口徑：H1 2026 累計（非單季，查無單季拆分數字）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：web_search／SEC 6-K：H1 2026 員工酬勞金 NT$70.35B（YoY +54.3%）÷ H1 2026 營收 NT$2,404.48B（numbers.latest_quarter_kpis.items[3]，as_of H1 2026 累計（非單季，查無單季拆分數字））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3198600.09 TWD m｜期間與口徑：2026-10-17／yfinance 最新一季：總債務 818380.01、現金 4016980.1（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-17）
  - 註記：財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.934 %｜期間與口徑：2026-10-17／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-17）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝5186.47 m shares｜期間與口徑：2026-10-17／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-17）
  - 註記：財報幣別 TWD ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 TWD，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝412.61 USD｜期間與口徑：2026-10-16（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-16（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.74 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 16.95，分子＝快照價 453.31｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝26.74 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-16（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.43 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-16（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝-0.21 x｜期間與口徑：2026-10-16（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-16（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝7.96 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 15.7 → 16.95（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.3｜期間與口徑：2026-10-16（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-16（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝11.93 %｜期間與口徑：2026-10-16（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-16（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：華爾街日報於 2026 年 5 月報導，Apple 與 Intel Foundry Services 已達成初步協議，Apple 將以 Intel 18A 製程（電晶體密度與電性可比台積電 2nm 級製程）生產部分 Apple Silicon 晶片，可能結束 Apple 近乎完全依賴台積電代工的局面；Apple 仍自行設計晶片，Intel 僅負責製造。
  - 來源：Investing.com, "Apple-Intel Chip Manufacturing Deal Reshapes Foundry Race", https://www.investing.com/analysis/appleintel-chip-manufacturing-deal-reshapes-foundry-race-200682398（as_of 2026-06-18）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Apple(蘋果，TSM 長期最大單一客戶)正探索讓部分低階處理器改由 TSMC 以外廠商生產，與 Intel、Samsung 進行早期洽談；Intel 18A-P 製程(預計 2026 年底量產)被視為 2016 年 Apple 離開 Samsung 以來第一個理論上可行的替代方案，但分析師認為 Intel 短期內較可能是策略備援或低量次要供應商，而非主力代工廠。
  - 來源：MacRumors, 'Apple May Break a 10-Year Chip Strategy' (引述 Wall Street Journal 報導)（as_of 2026-02-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：TSMC's ten largest customers accounted for 78% of FY2025 net revenue, up from 76% in FY2024; the single largest customer accounted for roughly 19% of FY2025 revenue (up from 12% in FY2024).
  - 來源：TSMC 2025 Annual Report (20-F) customer concentration disclosure, summarized by StockTitan (https://www.stocktitan.net/sec-filings/TSM/20-f-taiwan-semiconductor-manufacturing-co-ltd-files-annual-report-fo-e7792df70159.html) and ExploreSemis (https://exploresemis.substack.com/p/tsmcs-top-10203040-customers-who)（as_of 2025-12-31）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：台灣政府於 2026 年 6 月研議收緊 AI 晶片對中國出口管制，擬將限制範圍從僅涵蓋華為等受制裁對象擴大至所有中國客戶，並首度賦予刑事追訴權；若定案將限縮 TSMC 對中國先進製程客戶的銷售，尚未拍板。
  - 來源：Bloomberg, 'Taiwan Weighs Tighter AI Chip Export Controls Targeting China to Align with US'; UPI, 'Taiwan weighs tighter rules for AI chip exports to China'（as_of 2026-06-09）｜affects：thesis.R、decision_inputs.bear、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：台灣生產全球約92%的最先進邏輯晶片（5奈米以下），台積電先進製程產能高度集中在台灣本島，海外廠（美國亞利桑那、日本、歐洲）尚無法承接同等先進製程規模。
  - 來源：Simply Wall St News, 'Blockade Risk Puts TSMC's Taiwan Hub And Tech Supply Chain In Focus'（as_of 2026-05-20）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：台積電亞利桑那廠在2027年前是其海外唯一具備先進邏輯製程（5奈米以下）量產能力的據點，海外產能達到有意義規模預計要到2028年以後才會出現，短中期地緣風險仍高度集中於台灣。
  - 來源：Simply Wall St News（彙整報導，同上主題）（as_of 2026-05-20）｜affects：thesis.R、triggers
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：晶片製造耗電量約占台灣全國總發電量18%，台灣本地電力供應若不穩定，可能直接影響在製晶圓批次良率與交期，成為供應鏈單點失效的具體傳導管道之一。
  - 來源：Simply Wall St News, 'Taiwan Semiconductor Puts Global Tech Supply Chains Under Geopolitical Scrutiny'（as_of 2026-05-20）｜affects：thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：路透2025-04報導：TSMC 因一顆晶片流入華為 AI 處理器（涉 Sophgo），可能面臨 US$10 億以上的美國出口管制罰款；消息來自匿名人士。TSMC 表示自2020年9月中旬起未供貨華為並配合商務部。搜尋未找到 2026 年後續（無正式指控或罰款）。發布日早於近12個月窗口，列為仍未結案的監管事項。
  - 來源：Reuters via SCMP/Yahoo Finance/Business Today：TSMC could face $1b or more fine in US export control probe（as_of 2025-04-09）｜affects：decision_inputs.bear、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2025-08 TSMC 表示已對涉及潛在營業秘密外洩的員工啟動法律程序並採取懲處（二手來源摘要，未取得原文）。
  - 來源：搜尋摘要（Nasdaq／二手站）（as_of 2025-08-01）｜affects：moat_trend

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1144.0,"bear_5y_price":273.0,"p_bull_pct":28,"p_bear_pct":30,"upside_5y_pct":86.7,"ev5y_pct":75.9,"irr_base_pct":13.3,"asym_ratio":4.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":16.95,"pe":24.34,"basis":"FY2026E 共識 EPS（每 ADR 美元，當年度），終端倍數同樣套在終端年當年度 EPS"},"eps":{"bull":[24.5,32.5,39.0,45.5,52.0],"base":[22.65,28.9,33.5,38.2,42.8],"bear":[20.0,17.5,18.0,19.5,21.0]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":28,"base":42,"bear":30},"yield_pct":{"dividend":0.934,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TSM_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜CFO｜guidance：CFO 給第三季營收指引區間（446–458 億美元，中點季增 12%）（原話："our third quarter revenue to be between USD 44.6 billion"）
- 2026-07-16｜CFO｜guidance：第三季毛利率與營業利益率指引（匯率假設 32）（原話："gross margin is expected to be between 65% and 67%"）
- 2026-07-16｜CEO｜guidance：CEO 上調 2026 全年美元營收成長預期（原話："slightly above 40% year-over-"）
- 2026-07-16｜CFO｜margin：第二季毛利率季增 150bp 至 67.7% 的原因（原話："primarily due to cost"）
- 2026-07-16｜CFO｜margin：管理層說明 2 奈米陡峭放量對毛利率的稀釋幅度（約 3–4 個百分點）（原話："dilute our gross margin by about 3 to 4"）
- 2026-07-16｜CFO｜margin：海外晶圓廠毛利率稀釋的區間口徑（初期 2–3%、後期 3–4%）（原話："to be 2% to 3% in the early stages"）
- 2026-07-16｜CFO｜capital_allocation：全年資本支出上調至 600–640 億美元（原話："raise our full year 2026 capital budget to be between USD 60"）
- 2026-07-16｜CFO｜capital_allocation：資本支出分配比例（原話："About 70% to 80% of the 2026 capital budget will be"）
- 2026-07-16｜CFO｜commitment：管理層重申股利承諾：2026 每股 24 元、2027 持續增加（原話："we expect a continued and increasing cash dividends"）
- 2026-07-16｜CFO｜commitment：未來三年資本支出相對過去三年的說法升級（先前為「明顯高於」）（原話："the CapEx in the next 3 years will be even more"）
- 2026-07-16｜CEO｜capital_allocation：宣布亞利桑那再增 1000 億美元投資（原話："we would like to announce an additional USD 100 billion"）
- 2026-07-16｜CEO｜capital_allocation：被問及亞利桑那時程，CEO 稱視市況而定，並說明新增約 4 座廠（含前後段）（原話："the schedule will depend on the market situation."）
- 2026-07-16｜CEO｜risk：消費性與價格敏感市場受零組件漲價與總經不確定性挑戰，公司規劃趨於審慎（原話："consumer and price-sensitive end market segments are being"）
- 2026-07-16｜CEO｜customer：CEO 指雲端服務商給出強烈正向訊號，對多年 AI 趨勢信心很高（原話："our conviction in the multi-year AI"）
- 2026-07-16｜CEO｜product：Agentic AI 使 CPU 在 AI 資料中心角色回升，CEO 稱各種 CPU 架構幾乎都是客戶（原話："they are almost all"）
- 2026-07-16｜CEO｜product：A14 進度：2027 試產、2028 量產（原話："Pre-production will start in 2027 and volume production"）
- 2026-07-16｜CEO｜product：A13、A12 為 A14 延伸，預定 2029 量產（原話："Both A13 and A12 are scheduled for"）
- 2026-07-16｜CEO｜product：N3 擴產：台灣、亞利桑那、日本各一座新廠，並轉換 5 奈米機台（原話："we continue to convert 5-nanometer tools"）
- 2026-07-16｜CEO｜product：成熟製程策略：高附加價值領域增加而非減少產能，其他商品化領域需求不強（原話："mature node demand in other commodity area is not that"）
- 2026-07-16｜CEO｜competition：回應三星／英特爾競爭：強調技術、製造與客戶信任三項基本功（原話："the technology, manufacturing, and customer"）
- 2026-07-16｜CEO｜competition：CEO 表示先進封裝產能吃緊，歡迎 EMIB-T 等替代方案分擔（原話："our packaging capacity is so tight that now it's limited by"）
- 2026-07-16｜CEO｜competition：CEO 區分前段晶圓與後段封裝為兩種不同業務（原話："The front-end's wafer business and the back-end's business"）
- 2026-07-16｜CEO｜guidance：被問 AI 半導體五年 CAGR 更新，CEO 不給數字，只稱比先前說法更強（原話："but stronger than what we said before."）
- 2026-07-16｜CEO｜risk：CEO 談需求預測方法：各客戶說法加總未必是真相，需自行判斷（原話："You put all the truths"）
- 2026-07-16｜CEO｜risk：被問供給不足會否持續，CEO 稱需求強勁至約 2029–2030，但不確定中間是否有回檔（原話："Whether in between there's a dip or not, I'm not very"）
- 2026-07-16｜CEO｜margin：定價哲學：不大幅漲價以免擠壓客戶，毛利以支撐長期擴張為目標（原話："I don't want to squeeze them out from the market."）
- 2026-07-16｜CEO｜customer：被問前五大客戶集中度風險，CEO 稱不是顧慮（原話："No, that's not our concern."）
- 2026-07-16｜CEO｜capital_allocation：CEO 表示公司目前不做對客戶的客戶提供融資或投資（原話："So far, no, TSMC don't do this kind of financial arrangement"）
- 2026-07-16｜CEO｜product：COUPE 已開始生產，預期未來幾年重要性提升（未給時程數字）（原話："We start the production right now, and it will be ramped up."）
- 2026-07-16｜CEO｜product：玻璃基板等替代方案仍在建置試產線，約再一年成熟（原話："it takes about another 1 year to be mature"）
- 2026-07-16｜CEO｜capital_allocation：資本支出上調原因之二：設備價格通膨（之一為客戶需求持續增加）（原話："The second reason is inflation."）
- 2026-07-16｜CEO｜customer：成熟製程僅與 AI 相關者短缺（電源管理 IC、感測器），消費性需求不強（原話："Only the one which related to AI is in"）
- 2026-07-16｜CEO｜risk：被問先進製程需求超出供給的幅度，CEO 不給數字，只稱缺口很大（原話："the gap is very big."）

### 問答異常語氣（迴避／改口／保留）
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：是否提供未來三年資本支出指引（比照 2021 年做法）｜答法：CFO 明說沒有數字可提供，改以定性說法（未來三年資本支出會更顯著高於過去三年）回應
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：是否上調 AI 半導體五年營收 CAGR（1 月為中高 50% 區間）｜答法：CEO 拒絕給數字，只說「越來越強」、比先前說法更強
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：亞利桑那新增 1000 億美元的投入時程｜答法：CEO 稱有計畫但視市況與客戶需求，拒絕給確定時程
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：未來幾年營收成長是否可量化｜答法：CEO 只答「接下來幾年對台積電會是很好的生意」，未給數字
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：3 奈米以下無限制需求超出供給的比例是否遠高於 30–50%｜答法：CEO 不給數字，僅稱缺口「很大」，並提及不想評論記憶體
- TSM_Q2_2026_Earnings_Call_20260716.md｜問：先進封裝資本支出可否單獨拆出、佔比多少｜答法：CEO 稱前後段彈性調度無法具體拆分，維持 10–20% 區間

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | none | 0 | 3 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）（沿用 TSM_20260916，31d）：TSMC antitrust OR monopoly investigation 2026；TSMC DOJ OR FTC OR EU competition investigation chip manufacturing 2026；TSMC European Commission FTC investigation market power exclude rivals date
- **substitute_technology**（none）（沿用 TSM_20260916，31d）：TSMC advanced packaging chiplet threat alternative technology 2026；semiconductor foundry alternative technology disruption 2026 2027 gate-all-around backside power；TSMC technology obsolescence risk silicon photonics chiplet bypass foundry 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260916","verdict":"進場","role":"核心","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","irr_base_pct":13.0,"ev5y_pct":81.4,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":6.3,"ev5y_pct":81.4,"irr_base_pct":13.0,"max_dd_pct":-50,"bull_5y_price":1222.0,"bear_5y_price":294.0,"p_bull_pct":28,"p_bear_pct":30,"rearm_trigger":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","price_at_dd":413.75,"archetype":"品質複利成長","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TSM","date":"2026-10-17","schema":"v15.2","contract":"v19","company_name":"Taiwan Semiconductor Manufacturing Company Limited"},"oneliner":"全球晶圓代工市占 72.5% 的製程龍頭。第三季營收高於指引上緣，全年成長上修到約 44%；現價約 FY2027E 共識 EPS 的 18 倍。基本面沒變，股價卻回落；主要風險在資本支出強度、Apple 引進第二家代工廠，以及台灣產能集中。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TSM_20261017/scenario.json","answers":{"q1_business":{"verdict":"公司賺的是全球 AI 與高階運算晶片設計公司的製造費，獲利集中在先進製程和先進封裝兩個產能瓶頸。第二季營收 402 億美元、營益率 60.3%；第三季（2026-10-15 法說）營收 467 億美元，高於指引上緣，毛利率 66.4%、營益率 58.7%。","reasoning":"收費方式是按晶圓片計價，先進封裝另外收費。最新一季逐字稿（2026-10-15，CFO）顯示：HPC 占營收 68%、季增 22%，智慧型手機占 21%，7 奈米以下占晶圓營收 79%（2 奈米 8%、3 奈米 33%、5 奈米 28%、7 奈米 10%）。第四季指引 523–543 億美元，中點年增 58%，全年成長由 7 月的「略高於 40%」上修到約 44%。產業時鐘在擴張期：CEO 說需求仍遠高於供給、缺口很大；存貨天數減少 5 天到 82 天，還看不到庫存堆積。供需持久度判為結構性持久，依據是新廠要 2–3 年、擴產再 1–2 年，CoWoS 2026 年需求約 100 萬片，供給只有 60–70 萬片。單點依賴：前十大客戶占 FY2025 營收 78%，最大客戶（Nvidia）約 19%；因為代工市占 72.5%，客戶在先進製程沒有同量級的替代廠，所以集中度目前反而是議價優勢。產業態勢是雙向拉鋸。轉好的一面：市占創新高、CoWoS 到 2026 年底已售罄。競爭的一面：Apple 與英特爾 18A 達成初步協議。其他結構變數：台灣研議收緊對中國的 AI 晶片出口；美國對先進邏輯晶片課 232 關稅，但在美新建產能可豁免。","fact_refs":["f_kpi0_gaap","f_kpi1_tsm_taiwan_ifrs_gaap_non","f_kpi4_guidance_q3_2026_2026","f_kpi5_archetype","f_earnings_recency"],"verdict_values":{"revenue_quality":"品質高：HPC 占 68%、7 奈米以下占晶圓營收 79%，收入來自按片計價的經常性製造合約，沒有一次性收入。要留意美元營收含匯率效果，第三季台幣季增 17.6%，美元季增 16.2%。","unit_econ_note":"晶圓按片收費，先進封裝另計。第三季毛利率 66.4%，2 奈米初期放量稀釋 130bp，第四季指引中點 66%。海外廠稀釋 2026 年約 2pp，五年後段擴大到 3–4pp；靠規模與降本部分抵銷。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高利潤率、重資本、單一產業市占過七成，獲利隨 AI 與半導體景氣起伏"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：CEO 稱 AI 晶片短缺延續到 2027 年以後，新廠需 2–3 年、擴產再 1–2 年；CoWoS 2026 年需求約 100 萬片，供給 60–70 萬片；第三季法說再說需求仍遠高於供給。","bargaining":{"up":"設備商議價力上升：管理層承認設備、材料與人工通膨是真的，高數值孔徑曝光機要到 2030 年才導入。","down":"客戶集中但缺乏替代：前十大占營收 78%，Nvidia 鎖住 2026–2027 年 CoWoS 擴產一半以上；不過 2 奈米以下只有三家量產，三星市占 5.9%。","geo":"5 奈米以下先進邏輯產能約九成在台灣；美國 232 關稅以在美設廠豁免，逼產能外移，海外廠稀釋毛利率 3–4pp。"},"profit_pool_dir":"利潤池往設計端與製造瓶頸兩端集中。公司毛利率由 2023 年 54.4% 升到 2026 年第二季 67.7%，在價值鏈中分到的份額上升，但仍低於最大客戶 Nvidia 的 74.7%。","tam_table":{"expanded":false,"reason":"事實表沒有代工總市場、滲透率與利潤池占比的五年序列，只有市占 72.5% 單點與 CoWoS 供需估計，無法做五年前對照，以免自行推估。"}}}},"q2_moat":{"verdict":"護城河擴大中（↑）。機制是製程領先、規模成本，加上設計導入造成的轉換成本；份額與定價兩軸都在往上走。","reasoning":"可證的方向用份額軸：2026 年第二季全球代工市占 72.5%（第一季 72.3%），與第二名三星的差距擴大到 12.3 倍。定價軸：毛利率 2023 年 54.4%、2025 年 59.9%、2026 年第二季 67.7%，第三季在 2 奈米稀釋下仍有 66.4%。執行面：2 奈米良率佳，2027 年產能翻倍以上；A14 洽談客戶比 2 奈米同期多，CEO 預期會是更大的節點；5 倍光罩尺寸的先進封裝已量產，CEO 稱目前只有台積電做得到。執行力評 10、定價權評 8。定價權扣分的理由：CEO 明言不擠壓客戶，毛利率仍低於最大客戶，且海外廠稀釋會擴大到 3–4pp。同業投入資本報酬事實表未涵蓋（同業表列的是客戶），所以改用份額軸證明方向。威脅都屬點對點：Apple 用英特爾 18A 生產部分晶片的初步協議、三星與英特爾承接溢出需求、先進封裝被外包與替代。目前看不到生態攻擊或架構替代。報酬持續期：當期營益率 TTM 56.1%、第三季年化 ROE 45.5%（法說揭露），屬高利益率、低周轉的重資本型。增量報酬約 45%、再投資率約 42%，內生成長上界約 19%。","fact_refs":["f_peer_tsm_gross_margin_pct","f_peer_tsm_operating_margin_pct","f_peer_tsm_fcf_margin_pct","f_peer_nvda_gross_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_avgo_fcf_margin_pct","f_peer_amd_operating_margin_pct","f_peer_mu_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"製程領先、規模成本、設計導入轉換成本三者疊加。先進製程從設計階段就綁定製程設計套件，換廠要重新流片與驗證；72.5% 市占帶來的規模，讓管理層有底氣說公司在每個營運地區都是成本最低的製造者。","execution":10,"pricing":8,"grade":"A","trend":"↑","trend_evidence":"份額：代工市占 72.3% → 72.5%，與第二名差距 12.3 倍。定價：年度毛利率 54.4%（2023）→ 56.1%（2024）→ 59.9%（2025），2026 年第二季 67.7%。領先度：A14 客戶洽談熱度高於 2 奈米同期。最大客戶 Nvidia 沒有出現轉單跡象；Apple 只在低階處理器評估第二來源，尚未量產。","competitor_notes":[{"name":"NVDA","strategy_note":"最大客戶，不是對手。毛利率 74.7% 高於公司的 64.2%，代表設計端在價值鏈分得更多，也是公司漲價空間的上限參考。"},{"name":"AVGO","strategy_note":"客製 AI 晶片客戶。FCF 利潤率 44.2% 高於公司的 25.3%，差距來自公司的重資本支出，不是定價弱。"},{"name":"AMD","strategy_note":"客戶。營益率 15.7%，議價力遠弱於公司，CoWoS 配額仰賴公司。"},{"name":"MU","strategy_note":"同屬重資本製造業的對照。營益率 65.7% 正處記憶體景氣高點，提醒公司目前的利潤率也帶有週期成分。"},{"name":"三星晶圓代工","strategy_note":"市占 5.9%，2 奈米已量產但 3 奈米落後。主要機會是承接公司產能不足的溢出需求，不必搶客戶。"},{"name":"英特爾代工","strategy_note":"18A 與 Apple 有初步協議、EMIB-T 封裝可替代，是最具體的第二來源威脅；分析師評估短期仍屬策略備援量級。"}],"spread_notes":null,"peer_na_reason":"同業表列的是客戶（NVDA、AVGO、AMD）與記憶體廠（MU），不是代工對手；三星晶圓代工與英特爾代工的投入資本報酬事實表未涵蓋，所以改用市占與毛利率兩條可比軸證明方向。","threats":[{"level":"🟡","text":"Apple 與英特爾就 18A 生產部分 Apple 自研晶片達成初步協議，Apple 同時評估讓低階處理器改由其他廠生產；分析師認為英特爾短期是低量備援。","p":"35%","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"先進製程需求達公司產能的 110–120%，三星與英特爾不用搶客戶就能承接溢出單，累積量產經驗、縮小差距。","p":"40%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"先進封裝獨占性下降：CoWoS 部分委外給封測廠、向 GlobalFoundries 採購中介層，英特爾 EMIB-T 成為替代方案。","p":"30%","evidence_refs":["channel_business_model_shift#0","channel_business_model_shift#1"]},{"level":"🟡","text":"營業秘密外洩的員工法律程序。目前只有二手摘要，沒有涉案製程與損失金額。","p":"10%","evidence_refs":["major_events#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（雲端與 AI 模型公司）、決策者（晶片設計公司）、付款者（設計公司下單）三個角色都成立。CEO 派團隊實地查美國資料中心與電力進度，結論是「目前順利」。例外是消費性與價格敏感終端轉弱。"},{"item":"決策層級","level":"🟢","text":"替代性要在單一晶片專案層級衡量：先進製程換廠要重做設計套件與驗證，2 奈米以下只有三家量產，CEO 也不准客戶轉租產能。不過 Apple 已在低階處理器層級評估英特爾，代表低階產品上替代性存在。"},{"item":"價值鏈分配","level":"🟡","text":"公司毛利率 64.2% 低於最大客戶 Nvidia 的 74.7%。上游設備通膨擠壓成本；前三大客戶控制 85% 以上的 CoWoS 產能，買方集中。公司在價值鏈的份額雖在上升，但 CEO 明言不把價格推到上限。"},{"item":"社會容忍度","level":"🟡","text":"美國用 232 關稅與在地設廠豁免要求產能移轉，台灣研議收緊對中國出口。晶片製造用電約占台灣發電量 18%，電力分配的社會容忍度是隱性上限。目前是政策壓力，還沒到限制定價。"}],"roiic":"約 45%。代理算法：2022→2025 年淨利增加 7,047 億台幣，除以 2023–2025 年「淨利減自由現金流」的累計淨再投資約 1.57 兆台幣。折舊與投入資本事實表未涵蓋，屬近似值；基期 2022 年是景氣高點，算法偏保守。","reinvest_rate":"約 42%。FY2025 淨利 1.698 兆減自由現金流 0.992 兆，再除以淨利。2026 年資本支出上修到 600–640 億美元，往後再投資率可能更高。","endo_ceiling":19,"formula_note":"內生成長率＝增量報酬約 45% × 再投資率約 42% ≈ 19%；淨再投資以「淨利減自由現金流」代理。"}}}},"q3_growth":{"verdict":"成長跑道寬（🟢）：代工市占已過七成，但下一條曲線有來源可查，包括先進封裝平台與 A14。","reasoning":"成長來源是量價齊揚，沒有併購也沒有回購。量：近 20 座廠同時進行，其中台灣 13 座先進製程與封裝廠、海外 5–6 座；2 奈米產能 2027 年翻倍以上。價：先進製程漲價，加上 2 奈米組合提升。共識 EPS（每 ADR 美元）FY2026E 16.95、FY2027E 22.65、FY2028E 28.9，兩年年化約 30.6%。內生上界約 19%，缺口約 11.6pp，可歸因於毛利率擴張與漲價：年度毛利率 2025 年 59.9%，2026 年第三季 66.4%。不是靠回購或併購，所以不屬於依賴重新評價的成長。跑道判斷不看市占：代工市占 72.5% 已無多少空間，成長要靠先進製程矽含量增加，以及封裝從 CoWoS 擴到 SoIC 與晶圓級系統。滲透率序列事實表未涵蓋，無法算出達 30% 滲透率要幾年。十類衰退信號亮一項：自由現金流對淨利連兩年低於 0.75（FY2024 0.74、FY2025 0.58），原因是資本支出擴張，所以價值陷阱風險評為中度。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量價齊揚。量：先進製程與 CoWoS 擴產，2 奈米產能 2027 年翻倍以上。價：先進製程漲價與 2 奈米組合。無併購、無回購。","runway_years":"事實表未涵蓋滲透率序列，無法計算","runway_post_y5":"🟢","endo_ceiling_basis":"報酬持續期檢核的內生上界約 19%（增量報酬約 45% × 再投資率約 42%）。共識 FY2026→FY2028 EPS 年化約 30.6%，缺口約 11.6pp，歸因於毛利率擴張（2025 年 59.9% → 2026 年第三季 66.4%）與漲價。","segments":[{"item":"HPC","value":"第三季占營收 68%，季增 22%"},{"item":"智慧型手機","value":"占 21%，季增 10%"},{"item":"物聯網","value":"占 4%，季增 5%"},{"item":"車用","value":"占 4%，季增 23%"},{"item":"消費性電子","value":"占 1%，季減 12%"},{"item":"製程組合","value":"2 奈米 8%、3 奈米 33%、5 奈米 28%、7 奈米 10%；7 奈米以下合計 79%"}],"decay_signals":["自由現金流對淨利連兩年低於 0.75（FY2024 0.74、FY2025 0.58），原因是資本支出擴張"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置有紀律，但再投資負擔正在加重：盈餘近半投回產能，股東回報以穩定增加的現金股利為主。","reasoning":"自由現金流對淨利：FY2023 0.34、FY2024 0.74、FY2025 0.58。第三季（法說揭露）營業現金流約 9,200 億台幣，資本支出 4,430 億（約 48%），發放股利 1,560 億（約 17%），其餘留成現金。期末現金與有價證券約 4 兆台幣（1,260 億美元），淨現金約 3.2 兆台幣。員工酬勞是現金紅利，2026 上半年占營收 2.93%，不發股權，所以股數淨稀釋近零。沒有回購，也沒有重大併購。管理層承諾每股股利逐季、逐年增加，並重申只要執行得好，營收成長會快於資本支出成長；但 2026–2028 年資本支出會「更顯著高於」過去三年，這個承諾是接下來的檢驗點。","fact_refs":["f_kpi2_fcf","f_kpi3_tsm_sbc_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年沒有重大併購；併購金額事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"公司以現金股利為主，未見回購計畫；回購資料事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"員工酬勞以現金紅利發放（2026 上半年占營收 2.93%），不發股權，股數淨稀釋近零"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐。股東回報只有現金股利，殖利率 0.93%，管理層承諾每股股利逐年增加，沒有回購可展開。"}}}},"q5_valuation":{"verdict":"現價要求 2027–2028 年 EPS 大致照共識兌現，且毛利率守在 60% 以上；這一點我相信。估值落在合理區，不算便宜到可以忽略利潤率風險。","reasoning":"現價 412.61 美元，對 FY2026E 共識 EPS 16.95 是 24.3 倍，對 FY2027E 22.65 是 18.2 倍，對 FY2028E 28.9 是 14.3 倍。FY2026E 共識是 10/8 財報前的快照；之後第三季營收高於指引上緣、第四季指引年增 58%，分母偏保守。近三個月 FY1 共識上修 7.96%。短期上檔：FY2027E 22.65 × 20 倍 ≈ 453 美元，約 +9.8%。中期上檔：FY2028E 28.9 × 19 倍 ≈ 549 美元，約 +33.1%。事實表的市銷率 0.43 倍與 EV/S −0.21 倍，是拿台幣營收對美元市值、沒有換算的結果，數值失真，不採用。trailing 本益比 26.74 與快照 forward 本益比數值完全相同，疑為同一欄位重用，也不採用。年報端點分位只有 4 個年度點，不是五年分位。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E 共識 EPS 16.95 美元／ADR）搭配 PEG。市銷率與 EV/S 因台幣營收對美元股價沒有換算，不採用。","tier":"大型半導體製造龍頭","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業本益比；而且列的是客戶與記憶體廠，不是同層級的代工對手，不能當倍數錨。"},"fwd_pe":24.34,"peg":0.8,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026E 24.3 倍、FY2027E 18.2 倍；FY2026→FY2028 共識 EPS 年化 30.6%，PEG 約 0.8，落在便宜區。不過年報端點本益比分位 100%（只有 4 個年度點），且共識建立在接近歷史高點的毛利率上；便宜與否取決於利潤率守不守得住，所以判為合理。","upside_short_pct":9.8,"upside_mid_pct":33.1,"denominator_disputed":false,"denominator_note":"FY2026E 共識 16.95 在第三季財報前取得，分母偏保守而非虛胖。事實表 trailing 本益比 26.74 與 10/8 快照 forward 本益比相同，疑為欄位重用，不作為估值依據。"}}},"q6_how_wrong":{"verdict":"最可能看錯的有三處：2028 年 AI 資本支出進入消化期而公司正好大量投產；資本密集度上升，侵蝕每股經濟價值；台灣產能集中的尾端事件。","reasoning":"第一，失敗路徑：近 20 座新廠在 2027–2028 年陸續投產，若 AI 需求進入消化期，三星與英特爾又承接了溢出單，EPS 可能比照 2023 年回落（當年營收 −4.5%、營益率由 49.5% 降到 42.6%），倍數壓到 12–13 倍。第二，股東經濟：自由現金流對淨利已降到 0.58，海外稀釋擴大到 3–4pp，設備通膨也是真的，營收成長可能不會等比例轉成每股價值。第三，價格面：年報端點本益比在 4 點中最高，共識隱含利潤率接近高點。股價自 10/8 的 453 美元跌到 412.61 美元，RSI 34.3，26 週報酬 11.9%，沒有過熱。三個視角的詳細裁定見反證紀錄。","fact_refs":["f_rsi14","f_week26_return_pct","f_price_at_dd","f_pe_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"資本密集度上升中的高品質龍頭"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":16.95,"pe":24.34,"basis":"FY2026E 共識 EPS（每 ADR 美元，當年度），終端倍數同樣套在終端年當年度 EPS"},"valuation_basis":"eps_pe","eps":{"bull":[24.5,32.5,39.0,45.5,52.0],"base":[22.65,28.9,33.5,38.2,42.8],"bear":[20.0,17.5,18.0,19.5,21.0]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":28,"base":42,"bear":30},"yield_pct":{"dividend":0.93,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-55,"hi":-40,"basis":"Bear 終點跌幅約 −34%（13 倍 × 21 美元 ≈ 273 美元）。路徑中 2028 年 EPS 回落到 17.5 美元、倍數壓到 12–13 倍時，價格約 210–228 美元，即 −45% 到 −49%。再疊加台海或出口管制事件的尾端，下緣取 −55%，上緣 −40%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"AI 需求缺口延續到 2029 年、A14 成為比 2 奈米更大的節點，漲價抵銷海外稀釋，毛利率守在 66% 以上；終端 22 倍。","base":"2027–2028 年照共識，之後成長逐年放緩到 12%；海外稀釋 3–4pp 由規模與漲價部分吸收；終端 18 倍，低於現價的 FY2026E 24.3 倍。同業倍數事實表未涵蓋，以自身 FY2027E 18.2 倍對照。","bear":"2028 年 AI 資本支出消化，新廠投產造成產能過剩，英特爾與三星分走溢出單；EPS 回落後緩升，終端 13 倍。13 倍介於成長熄火情境的 15 倍（成長降到 10%）與 12 倍（降到 5%）之間。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"公司同時推進近 20 座新廠，2 奈米產能 2027 年翻倍；先進製程需求達公司產能 110–120% 的溢出單由三星與英特爾承接；Apple 與英特爾 18A 有初步協議。","assumption":"AI 加速器需求到 2027 年後仍高於供給（CEO 說法），且各客戶預測加總不會高估真實需求。","consequence":"若 2028 年需求進入消化期，產能剛好大量開出，稼動率與價格同時下滑；EPS 可比照 2023 年回落，倍數壓到 12–13 倍，股價約 210–230 美元。","ruling":"部分採納。這是五年內最可能虧掉一半的故事，已放進 30% 的 Bear 機率；但存貨天數下降、CoWoS 售罄至 2026 年底，目前看不到過剩證據。","watch":"第四季營收是否達 523 億美元下緣、2027 年成長指引、存貨天數、CoWoS 交期","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"],"fact_refs":["f_kpi4_guidance_q3_2026_2026","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"台灣生產全球約 92% 的 5 奈米以下邏輯晶片；亞利桑那在 2027 年前是唯一的海外先進據點，有意義的海外規模要到 2028 年後；晶片製造用電約占台灣發電量 18%。","assumption":"台海維持現狀，台灣電力與能源進口穩定。","consequence":"一旦封鎖或檢疫，沒有替代產能，盈利與資產價值同時受損；這也是唯一致命點。","ruling":"採納為尾端風險，與唯一致命點一致；機率低，不放進情境機率，改用事件出場處理。","watch":"解放軍演習規模與禁航區、台灣能源進口、海外先進產能進度","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流對淨利 FY2024 0.74、FY2025 0.58；2026–2028 年資本支出更顯著高於過去三年；設備通膨屬實；海外廠稀釋擴大到 3–4pp；前十大客戶占營收 78%，最大客戶毛利率 74.7% 高於公司。","assumption":"增量報酬約 45% 能延續，營收成長快於資本支出成長（管理層承諾）。","consequence":"營收照 AI 需求成長，但每股自由現金流落後；股息殖利率只有 0.93%，4 兆台幣現金報酬低，股東實拿的經濟價值落後營收。","ruling":"部分採納。價值陷阱風險因此評為中度，並設資本支出對營收、自由現金流對淨利的出場指標。目前反駁的依據是毛利率仍在上升、增量報酬約 45%。","watch":"FY2027 資本支出年增率對營收年增率、自由現金流對淨利是否跌破 0.5","evidence_refs":["customer_concentration_credit#0"],"fact_refs":["f_kpi2_fcf","f_peer_tsm_fcf_margin_pct","f_peer_nvda_gross_margin_pct"]},{"view":"價格已反映太多","evidence":"年報端點本益比分位 100%（4 個年度點）；共識 FY2026→FY2028 EPS 年化 30.6%，建立在接近歷史高點的 66–67% 毛利率上。","assumption":"市場用 24 倍 FY2026E 定價，等於預設高利潤率可以延續。","consequence":"若毛利率回到 60% 附近，EPS 下修疊加倍數壓縮，下行雙殺。","ruling":"反駁。現價對 FY2027E 只有 18.2 倍、PEG 約 0.8；Base 終端 18 倍低於現價倍數，Base 報酬來自 EPS 複利而非重新評價；而且財報後股價已從 453 美元回落到 412.61 美元。","watch":"毛利率是否守住 60%、FY2027E 共識是否續升","evidence_refs":[],"fact_refs":["f_pe_percentile","f_consensus_eps_fy2","f_consensus_eps_fy3","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 413.75 → 本次 412.61（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=413.75","side_b":"本次 price_at_dd=412.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 413.75 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 413.75 美元：Bull 價 1,222、Bear 價 294，五年期望值 +81.4%，基準年化 13.0%，不對稱比 6.3","side_b":"本次情境、股價仍用 413.75 美元：Bull 價 1,144、Bear 價 273，五年期望值 +75.4%，基準年化 13.2%，不對稱比 4.84","ruling":"先換情境、股價不動：五年期望值少 6.0 個百分點，基準年化多 0.2 個百分點。不對稱比由 6.3 變為 4.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 413.75 美元：五年期望值 +75.4%，基準年化 13.2%，不對稱比 4.84","side_b":"本次情境、股價 412.61 美元：五年期望值 +75.9%，基準年化 13.3%，不對稱比 4.89","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.5 個百分點，基準年化多 0.1 個百分點，不對稱比由 4.84 升到 4.89。合計五年期望值比前份少 5.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份基本面判斷延續","cause":"新證據","prior_field":["signal","val","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-09-16）：品質 A、估值合理、護城河擴大、成長跑道寬、品質複利成長型、中循環、進場","side_b":"本次：同樣結論。第三季營收 467 億美元高於指引上緣，全年成長上修到約 44%，市占 72.5% 創新高；股價 412.61 美元與前份 413.75 美元幾乎相同，FY2027E 共識 22.55 → 22.65","ruling":"一致判斷，不改。新證據強化原論點，估值條件因股價與共識都幾乎沒動而不變。","evidence_level":"公司財報與法說（2026-10-15）","settle_metric":"第四季營收對指引、2027 年全年指引","if_then":["若第四季營收達指引且 2027 年成長指引 ≥20%，維持原判斷"],"evidence_refs":["competitive_share_entrants#0","capital_markets_pricing#0"]},{"axis":"價值陷阱風險由低改為中度","cause":"方法變動","prior_field":["trap"],"side_a":"前份：價值陷阱風險低（🟢）","side_b":"本次：十類衰退信號逐項比對，自由現金流對淨利連兩年低於 0.75（FY2024 0.74、FY2025 0.58），亮一項，改為中度（🟡）","ruling":"這筆資料前份就已存在，變的是本次嚴格逐項比對，屬方法變動，不是基本面惡化。","evidence_level":"年度財報","settle_metric":"FY2026 自由現金流對淨利","if_then":["若 FY2026 自由現金流對淨利回到 0.75 以上，恢復低風險","若跌破 0.5 且資本支出增速高於營收，減碼至半倉"],"evidence_refs":[]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 28%、Bear 30%，最大回撤單點 −50%","side_b":"本次：Bull 28%、Base 42%、Bear 30% 不變；最大回撤改填範圍 −55% 到 −40%","ruling":"機率不變。最大回撤由單點改為範圍，屬方法變動；下緣加深 5pp，用來反映台海與出口管制的尾端。","evidence_level":"情境推導","settle_metric":"不適用","if_then":[],"evidence_refs":[]},{"axis":"加碼條件改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"FY2027 共識 EPS 22.55 × 16x ≈ $361 以下，或 250 週均線斜率回到 +3% 以上且毛利率連兩季 ≥66%","side_b":"股價跌至 FY2027 共識 EPS 22.65 × 16x ≈ $362 以下分批加碼；或 2027 年營收成長指引 ≥20% 且第四季營收達指引下緣 $52.3B","ruling":"加碼門檻的價格只隨共識更新（22.55 → 22.65），幾乎不變。第二條改寫有兩個原因：毛利率連兩季 ≥66% 已成立（第二季 67.7%、第三季 66.4%），不再有區辨力；均線斜率由程式另算，改用基本面事件。前份價格條件 $361 沒有觸發；均線斜率那半事實表未涵蓋，所以整條未確認觸發，延續前份判斷。","evidence_level":"共識快照與公司財報","settle_metric":"股價、2027 年全年指引","if_then":["若股價 ≤$362 且第四季營收達指引，加碼一批","若 2027 年成長指引 <20%，停止加碼"],"evidence_refs":[]},{"axis":"出場指標由無到有","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場指標","side_b":"本次新設：年度毛利率 <58% 減碼、資本支出增速高於營收且自由現金流對淨利 <0.5 減碼、Apple 占營收 <12% 減碼、市占連兩季 <68% 減碼、台海封鎖清倉","ruling":"前份是空白，本次補上，屬方法變動。","evidence_level":"不適用","settle_metric":"見出場指標清單","if_then":["任一減碼指標觸發，減碼至半倉","封鎖事件發生，清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未記錄唯一致命點","side_b":"Single Thing：台海封鎖或海上檢疫，使台灣晶圓廠的設備、原料或能源進口中斷；發生即清倉","ruling":"前份空白，本次補上。選它的理由是數學上敏感度最大：先進邏輯產能約九成在台灣，2028 年前沒有替代。","evidence_level":"產業報導","settle_metric":"台海航運與能源進口","if_then":["封鎖或檢疫實際限制航運 ≥7 天，清倉"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"增量資本報酬：擴產創造價值或稀釋報酬","cause":null,"prior_field":null,"side_a":"價值創造：2022→2025 年淨利增加 7,047 億台幣，對應淨再投資約 1.57 兆，增量報酬約 45%；毛利率在擴產期一路升到 66–67%；管理層重申營收成長快於資本支出成長","side_b":"報酬稀釋：2026–2028 年資本支出更顯著高於過去三年，設備通膨屬實，海外廠稀釋擴大到 3–4pp，自由現金流對淨利降到 0.58","ruling":"不可調和（方向相反），裁定站價值創造這邊。依據是硬數據：擴產期間毛利率與營益率都在上升，不是下降。","evidence_level":"年度財報＋兩季法說","settle_metric":"FY2027 資本支出年增率對營收年增率、年度毛利率","if_then":["若 FY2027 資本支出年增率高於營收年增率且全年毛利率 <60%，減碼至半倉","反向條件：若 FY2027 營收年增 ≥25% 且毛利率 ≥62%，維持並在 $362 以下加碼"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"營收超預期與股價回落","cause":null,"prior_field":null,"side_a":"第三季營收 467 億美元高於指引上緣，第四季指引中點年增 58%，全年成長上修到約 44%","side_b":"股價自 10/8 的 453 美元跌到 412.61 美元，RSI 34.3；市場擔心資本支出強度、AI 資金與電力瓶頸","ruling":"可調和，屬程度差異：股價先跌，基本面沒有受損。依股價跌但基本面無損的處理原則，分批買回，不停損。","evidence_level":"公司財報、市場價格","settle_metric":"FY2026E 共識是否上修","if_then":["若股價續跌但第四季營收達指引，分批反買","若股價續漲而 2027 年指引尚未公布，不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層前後說法對照（7 月 → 10 月）","cause":null,"prior_field":null,"side_a":"2026-07-16 法說：第三季營收指引 446–458 億美元、毛利率 65–67%；全年成長略高於 40%；海外稀釋初期 2–3%、後期 3–4%；CEO 稱不大幅漲價以免擠壓客戶","side_b":"2026-10-15 法說：第三季 467 億美元超過上緣、毛利率 66.4%；全年上修到約 44%；2026 年海外稀釋接近 2%、後段 3–4% 不變；CEO 改稱定價要讓價值被認可、給股東最大價值","ruling":"說到做到，財測連兩季超標。唯一的口徑轉變在定價，由「不擠壓客戶」轉向「讓價值被認可」，與市場傳出漲價一致，屬程度差異。","evidence_level":"兩季法說逐字稿","settle_metric":"2027 年毛利率指引","if_then":["若 2027 年毛利率指引中點 ≥64%，視為漲價落地"],"evidence_refs":[]},{"axis":"Steelman：現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方論點：毛利率接近歷史高點；資本支出加速；Apple 引進第二來源；英特爾 EMIB-T 與 18A 成熟；台灣出口管制與美方罰款未結；消費性終端轉弱，管理層對 2027 年轉審慎","side_b":"持有論點：市占創新高、需求高於供給的說法有 CoWoS 售罄佐證，FY2027E 只有 18.2 倍，Base 報酬不靠重新評價","ruling":"維持持有。賣方論點都是 1–3 年後才會驗證的風險，已分別設出場門檻，目前沒有一項觸發。","evidence_level":"綜合","settle_metric":"出場指標清單","if_then":["任一出場指標觸發，照該指標的動作減碼或清倉"],"evidence_refs":["reg_tariff_export#2","major_events#0"]}],"triggers":[{"n":1,"text":"第四季營收是否達指引下緣","type":"假設驗證","maps_to":"H1","metric":"第四季美元營收","threshold":"≥523 億美元","action":"未達則停止加碼","source_freq":"季度財報","date":"2027-01","evidence_refs":[]},{"n":2,"text":"2027 年全年營收成長指引","type":"假設驗證","maps_to":"H1","metric":"2027 年美元營收成長指引","threshold":"≥20%","action":"低於 20% 則停止加碼，並把 Bear 機率上調到 35%","source_freq":"年度指引","date":"2027-01","evidence_refs":[]},{"n":3,"text":"Apple 轉單英特爾的實質化","type":"風險","maps_to":"R2","metric":"年報 Apple 占營收比重，或英特爾量產公告","threshold":"<12%，或公告量產先進製程","action":"減碼至半倉","source_freq":"年報、公司公告","date":null,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"n":4,"text":"出口管制事項定案","type":"風險","maps_to":"R5","metric":"美方罰款金額、台灣對中國出口新規定","threshold":"罰款 ≥10 億美元並附營運限制，或新規定把所有中國客戶納入","action":"單純一次性罰款不動作；附營運限制則減碼一級","source_freq":"監管公告","date":null,"evidence_refs":["reg_tariff_export#2","major_events#0"]},{"n":5,"text":"台海封鎖或檢疫","type":"Single Thing","maps_to":"Single Thing","metric":"台灣港口航運與能源進口","threshold":"實際限制 ≥7 天","action":"清倉","source_freq":"即時新聞","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":6,"text":"股價回到加碼區","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤362 美元（FY2027E 22.65 × 16 倍）","action":"分批加碼一批","source_freq":"每日","date":null,"evidence_refs":[]},{"n":7,"text":"資本密集度失控","type":"減碼","maps_to":"R3","metric":"FY2027 資本支出年增率對營收年增率、自由現金流對淨利","threshold":"資本支出增速高於營收，且自由現金流對淨利 <0.5","action":"減碼至半倉","source_freq":"年報","date":"2028-01","evidence_refs":["customer_concentration_credit#0"]},{"n":8,"text":"第四季財報複審","type":"複審日期","maps_to":null,"metric":"全份複審","threshold":"財報發布","action":"重跑判斷","source_freq":"季度","date":"2027-01-15","evidence_refs":[]}],"kill_metrics":[{"metric":"年度毛利率","bear_threshold":"全年 <58%，扣掉海外稀釋 3–4pp 後仍守不住","window":"FY2027–FY2028 年報","source":"公司季度財報與年報","last_status":"ok"},{"metric":"資本支出年增率對營收年增率，與自由現金流對淨利","bear_threshold":"資本支出增速高於營收，且自由現金流對淨利 <0.5","window":"FY2027–FY2028","source":"年報現金流量表","last_status":"warning"},{"metric":"Apple 占營收比重","bear_threshold":"<12%，或英特爾公告為 Apple 量產先進製程","window":"FY2026–FY2027 年報","source":"年報客戶集中度揭露、公司公告","last_status":"ok"},{"metric":"全球晶圓代工市占","bear_threshold":"連兩季 <68%","window":"每季","source":"TrendForce 季度排名","last_status":"ok"},{"metric":"台海封鎖或檢疫","bear_threshold":"實際限制航運或能源進口 ≥7 天","window":"持續","source":"官方公告、主要通訊社","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價跌至 FY2027 共識 EPS 22.65 × 16x ≈ $362 以下分批加碼；或 2027 年營收成長指引 ≥20% 且第四季營收達指引下緣 $52.3B","exec_line":"現價 412.61 美元依目標倉位分批，首批不超過目標的一半；$362 以下補第二批。第四季營收低於 523 億美元或 2027 年指引 <20% 時停止加碼；任一出場指標觸發，照該指標動作執行。"}},"decision_inputs":{"signal":"A","ma":"✅","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場在財報前後把股價從 453 美元壓到 412.61 美元，擔心資本支出強度、AI 資金與電力瓶頸。但第三季營收高於指引上緣、第四季指引年增 58%，財報前的 FY2026E 共識還沒反映，股價先走，證據還沒跟上。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":null,"prior_verdict":"進場","prior_role":"核心"},"decision_out":{"verdict":"進場","role":"核心","row_hit":"10","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場在財報前後把股價從 453 美元壓到 412.61 美元，擔心資本支出強度、AI 資金與電力瓶頸。但第三季營收高於指引上緣、第四季指引年增 58%，財報前的 FY2026E 共識還沒反映，股價先走，證據還沒跟上。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='↑', week26=11.93, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='A', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='A', val='🟡', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":true,"basis":"signal='A', val='🟡', ma='✅'"},{"row":"10-verdict","condition":"命中 row10 → 進場","hit":true,"basis":"row_hit=10"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 加速器與先進製程需求在 2027 年仍高於供給，美元營收維持高成長","2y":"FY2027 美元營收年增 ≥25%，HPC 占營收 ≥65%","5y":null,"10y":null,"threshold":"FY2027 美元營收年增 ≥25%；HPC 平台占營收 ≥65%","source":"公司季度財報的平台別營收、2027 年 1 月全年指引","drift_rule":"TTM 營收低於上述路徑：連兩季 ≥5% 為削弱，連三季 ≥10% 為反轉"},{"id":"H2","text":"定價權足以吸收 2 奈米放量與海外廠 3–4pp 稀釋，毛利率長期守在 60% 以上","2y":null,"5y":"FY2027–FY2030 年度毛利率皆 ≥60%、營益率 ≥50%","10y":null,"threshold":"年度毛利率 ≥60%，營益率 ≥50%","source":"公司年報與季度財報","drift_rule":"TTM 毛利率連四季低於 57% 為削弱，連六季低於 54% 為反轉"},{"id":"H3","text":"製程領先延續到 A14 之後，全球代工市占守在 65% 以上","2y":null,"5y":null,"10y":"2035 年前每代新節點量產不落後對手，代工市占 ≥65%，7 奈米以下占晶圓營收 ≥75%","threshold":"代工市占 ≥65%；7 奈米以下占晶圓營收 ≥75%","source":"TrendForce 季度市占、公司製程別營收","drift_rule":"跨兩個年度低於門檻為削弱，跨三個年度為反轉"}],"R":[{"id":"R1","text":"消費性與價格敏感終端轉弱，CEO 在 7 月與 10 月兩次法說都說 2027 年規劃轉審慎","h_ref":"H1","clock":"⚡","threshold":"第四季營收低於 523 億美元，或 2027 年成長指引 <20%","evidence_refs":[]},{"id":"R2","text":"Apple 引進英特爾 18A 作第二來源，從低階處理器開始分流","h_ref":"H3","clock":"🔥","threshold":"年報 Apple 占營收 <12%，或英特爾公告為 Apple 量產先進製程","evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"id":"R3","text":"資本支出強度上升與海外稀釋擴大，管理層「營收成長快於資本支出成長」的承諾可能失守","h_ref":"H2","clock":"🔥","threshold":"FY2027 資本支出增速高於營收，且自由現金流對淨利 <0.5","evidence_refs":[]},{"id":"R4","text":"先進產能高度集中在台灣，海外規模要到 2028 年後；台灣電力供應是單點失效的傳導管道","h_ref":"H3","clock":"🐢","threshold":"台灣電力事件造成單季指引下修，或 2028 年後海外先進產能仍不具規模","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"出口管制雙邊收緊：美方可能罰款 10 億美元以上，台灣研議把對中國 AI 晶片出口限制擴大到所有中國客戶","h_ref":"H1","clock":"🔥","threshold":"罰款 ≥10 億美元並附營運限制，或新規定定案；受影響營收事實表未涵蓋，以公司揭露為準","evidence_refs":["reg_tariff_export#2","major_events#0"]},{"id":"R6","text":"客戶集中度上升：前十大客戶占營收 78%，最大客戶由 12% 升到 19%","h_ref":"H2","clock":"🐢","threshold":"前十大占營收 >85%，或單一客戶 >25%","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"台海封鎖或海上檢疫，使台灣晶圓廠的設備、原料或能源進口中斷","why_fatal":"5 奈米以下先進邏輯產能約九成在台灣；亞利桑那在 2027 年前是唯一的海外先進據點，2028 年後才有規模。台灣停擺時沒有替代產能，盈利與資產價值同時受損。","if_happens":"清倉，不等基本面數字確認","how_monitor":"解放軍演習規模與是否劃設禁航區、台灣能源進口與港口航運、公司月營收與海外產能進度","probability":"12–24 個月約 3–5%（主觀估計，事實表未涵蓋機率來源）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"高","fpe_fy2":18.22,"peg_fy2":0.6,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":16.95,"FY2027E":22.65,"FY2028E":28.9},"fy_end_month":12,"eps_basis":"每 ADR 美元（Koyfin 普通股共識 ×5）。FY2025A 的美元口徑事實表未涵蓋，只有台幣每 ADR 331.25，不自行換匯，所以留空；三年成長改用 FY2026E→FY2028E 年化 30.6%。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年全年營收、毛利率指引","impact":"高","watch":"成長指引是否 ≥20%、毛利率指引中點是否 ≥64%"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"台南新 3 奈米廠上半年量產","impact":"中","watch":"3 奈米供給缺口是否收斂"},{"date":"2027-07","date_precision":"quarter","type":"capacity","event":"亞利桑那第二廠 3 奈米第三季量產（略早於原時程）","impact":"中","watch":"海外稀釋是否超過 3%"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"A14 風險試產","impact":"中","watch":"客戶數與量產時程是否維持 2028 年"},{"date":null,"date_precision":null,"type":"regulatory","event":"台灣對中國 AI 晶片出口管制定案、美方出口管制罰款結果","impact":"中","watch":"受影響營收與營運限制"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
