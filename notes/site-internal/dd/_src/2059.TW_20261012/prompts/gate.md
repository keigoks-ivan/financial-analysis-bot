你是 DD 管線 v20 的判斷層閘（gate），標的 2059.TW（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝10830.04 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（TWD，與公司公告 Q2 營收108.3億、營益率82.1%相符）；財報日來自 numbers.earnings_recency；公開資訊觀測站正式公告 URL 未取得（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_kpi1`（q1_business）｜毛利率＝87.4 %｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（TWD，與公司公告 Q2 營收108.3億、營益率82.1%相符）；財報日來自 numbers.earnings_recency；公開資訊觀測站正式公告 URL 未取得；fugle 法說摘要（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝8901.5 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（TWD，與公司公告 Q2 營收108.3億、營益率82.1%相符）；財報日來自 numbers.earnings_recency；公開資訊觀測站正式公告 URL 未取得（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益率＝82.1 %｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：fugle 法說摘要 https://blog.fugle.tw/post/earnings-call-2059-2026-08-07（yfinance 計算 82.2%）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_kpi6`（q1_business）｜產能利用率＝70–80%（接近90%） %｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）；7月維持70–80%以上／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：fugle 法說摘要（AI 整理，未核對簡報）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）；7月維持70–80%以上）
- `f_kpi7`（q1_business）｜管理層指引＝下半年營收 HoH 成長『可期待』；毛利率維持80%以上，全年往去年±2%區間上緣；研發費用1–2%營收；不預測單月營收 文字｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：fugle 法說摘要（AI 整理，未核對簡報）（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_kpi8`（q1_business）｜資本支出／擴產＝川益三、五期總投資約100億TWD，預計2026年底動工；美國休士頓廠2026年9月量產 文字｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：fugle 法說摘要（numbers.latest_quarter_kpis.items[8]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_peer_2059_tw_gross_margin_pct`（q2_moat）｜2059.TW 毛利率＝81.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2059.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2059_tw_operating_margin_pct`（q2_moat）｜2059.TW 營業利益率＝74.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2059.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2059_tw_fcf_margin_pct`（q2_moat）｜2059.TW FCF 利潤率＝41.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2059.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3533_tw_operating_margin_pct`（q2_moat）｜3533.TW 營業利益率＝27.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3533.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3017_tw_operating_margin_pct`（q2_moat）｜3017.TW 營業利益率＝23.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3017.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2383_tw_operating_margin_pct`（q2_moat）｜2383.TW 營業利益率＝23.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2383.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2383_tw_fcf_margin_pct`（q2_moat）｜2383.TW FCF 利潤率＝-2.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2383.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi5_ocf_capex`（q4_capital）｜自由現金流（OCF−Capex）＝2371.6 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 2,697.4；Capex 325.7）（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝349.76 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝495.27 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝572.82 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝51968.08 TWD m｜期間與口徑：2026-10-12／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝75062.27 TWD m｜期間與口徑：2026-10-12／yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_eps`（q4_capital）｜稅後淨利／稀釋EPS＝7088.1 百萬TWD；EPS 74.38（媒體／法說，yfinance 稀釋 73.22）｜期間與口徑：Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（TWD，與公司公告 Q2 營收108.3億、營益率82.1%相符）；財報日來自 numbers.earnings_recency；公開資訊觀測站正式公告 URL 未取得（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，財報公告於 2026-08-06，法說 2026-08-07））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-27861.33 TWD m｜期間與口徑：2026-10-12／yfinance 最新一季：總債務 1546.28、現金 29407.61（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.482 %｜期間與口徑：2026-10-12／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-12）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝95.3 m shares｜期間與口徑：2026-10-12／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝10580.0 TWD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝30.35 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 349.76，分子＝快照價 10615.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝59.85 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝218.36 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.79｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝18.87 x｜期間與口徑：2026-10-12／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（4 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Daiwa Securities 預期川湖在 Nvidia 系統滑軌套件的供應份額明年可能降至約 75%，因 Nvidia 擴大供應商基礎（搜尋摘要轉述，未見原文）
  - 來源：Taipei Times 2026-07-07（經搜尋摘要轉述）（as_of 2026-07-07）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：南俊國際 2026 Q1 合併營收 NT$8.7 億、年增 73.5%，伺服器滑軌占營收 74%；僅為營收數據，非市占（搜尋摘要轉述）
  - 來源：搜尋摘要（Nan Juen Q1 2026）（as_of 2026-05-31）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Daiwa Securities 預期 King Slide 供應 Nvidia 系統滑軌套件的份額明年可能降至約 75%，因 Nvidia 擴大供應商基礎；新製造商通過認證後，資料中心營運商亦可用競爭壓價。
  - 來源：Forklog, Taiwan's richest person emerges from AI demand surge (citing Daiwa Securities)（as_of 2026-08-25）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：財經分析稱川湖生產基地目前集中在台灣，並提出是否需在北美或東南亞設廠（未找到官方產地揭露；未找到中國／越南設廠或關稅衝擊的川湖專屬報導）
  - 來源：搜尋摘要（vocus.cc 財經分析文章，日期未確認）（as_of 2025-03-23）｜affects：decision_inputs.bear、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2059.TW_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":24960,"bear_5y_price":4200,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":13.4,"ev5y_pct":21.9,"irr_base_pct":2.6,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":349.76,"pe":30.25,"basis":"FY1（FY2026E）共識EPS，與終端年以當年度EPS計倍數同口徑"},"eps":{"bull":[560,680,790,880,960],"base":[480,545,560,575,600],"bear":[430,380,300,280,300]},"pe":{"bull":26,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.482,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | none | 0 | 3 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | none | 0 | 5 |
| channel_business_model_shift | none | 0 | 4 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | none | 0 | 6 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_concentration_credit**（none）：川湖科技 2059 主要客戶 營收比重 客戶集中度；King Slide Works 2059.TW customer concentration risk top customer revenue；川湖 前十大客戶 占營收 信用風險 2026
- **regulatory_antitrust**（none）：2059.TW King Slide Works antitrust OR monopoly investigation 2026；King Slide Works regulation OR regulatory scrutiny 2026 川湖科技 公平會 OR 監管；2059.TW King Slide Works DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）：King Slide Works product substitute technology threat 2026；川湖科技 2059 伺服器滑軌 替代 技術 競爭 2026；server rack rail-less tool-less chassis design GB300 slide rail alternative King Slide competitor；King Slide Works 川湖科技 product substitute technology threat 2026；川湖 滑軌 液冷 伺服器 替代技術 風險 2026
- **channel_business_model_shift**（none）：King Slide Works distribution channel disruption OR shift 2026；2059.TW King Slide Works business model transition subscription OR platform 2026；Furnishings, Fixtures & Appliances channel disintermediation D2C 2026；King Slide Works go-to-market change 2026
- **major_events**（none）：2059.TW King Slide Works acquisition merger 2025 2026；2059.TW King Slide Works class action lawsuit securities fraud；2059.TW King Slide Works product recall warning letter investigation restatement；2059.TW King Slide Works clinical trial FDA approval 2025 2026；2059.TW King Slide Works product launch recall warning letter；2059.TW King Slide Works SEC investigation restatement

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2059.TW","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"川湖科技（King Slide Works）"},"oneliner":"AI伺服器滑軌龍頭，Q2毛利率87.4%、份額約七到八成；現價已計入共識兩年EPS高成長，但大和預告輝達份額降至約75%。現價不追，等回檔或毛利率守住的證據再進。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2059.TW_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2059.TW_20261012/scenario.json","answers":{"q1_business":{"verdict":"川湖賺的是AI機櫃組裝方（輝達平台與大型雲端業者）的重載滑軌錢。錢卡在機櫃設計認證這一節點，滑軌又只占機櫃成本不到1%，所以收得到87%毛利。","reasoning":"Q2營收108.3億元，年增156%；毛利率87.4%，營益率82.1%，稅後淨利70.9億元。年度毛利率從2022年57.3%一路升到2025年76.1%，今年再上一層。管理層指引下半年營收較上半年成長，全年毛利率80%以上。產能利用率七到八成，逼近九成。休士頓廠2026年9月量產，川益三、五期約100億元預計年底動工。分部與客戶占比事實表未涵蓋，只能從媒體得知主要客戶為輝達與大型雲端業者，單點依賴集中在輝達機櫃平台。產業時鐘判在過熱段，依據是供給端而非股價：營收年增三位數、毛利率創歷史新高，對手（南俊伺服器滑軌占營收74%、Q1年增73.5%）與新供應商同步擴產。供需持久性：AI伺服器超過70公斤，重載規格門檻是結構性提高；但出貨量跟著雲端資本支出走，2023年營收曾年減26%，週期反轉風險偏高。產業態勢屬雙向拉鋸：需求結構轉好（重載與單價提升），競爭面惡化中（輝達擴大供應商基礎）。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_gaap","f_kpi3_gaap","f_kpi6","f_kpi7","f_kpi8"],"verdict_values":{"revenue_quality":"高毛利、高集中、高週期：營收集中在AI伺服器機櫃滑軌，年增156%由量與單價同步推升。分部與客戶占比事實表未涵蓋","unit_econ_note":"法人稱滑軌占AI機櫃成本不到1%，客戶重品質輕價格；法人預估VR機櫃滑軌單價較GB300再升一成以上（非公司指引）","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"毛利率87%、營益率82%、淨現金約279億元、26週漲218%、份額七到八成、2023年營收曾年減26%"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉風險偏高：需求規格因機櫃重量結構性提高（Taipei Times／Counterpoint），但量隨雲端資本支出波動（2023年營收年減26%，yfinance年度財報），且對手與新供應商同步擴產","bargaining":{"up":"上游為鋼材等通用原料，供應商議價力低；採購集中度事實表未涵蓋","down":"客戶為輝達與大型雲端業者，買方高度集中；但滑軌占機櫃成本不到1%，價格敏感度低","geo":"產能集中台灣，休士頓廠2026年9月量產開始分散地緣與關稅風險"},"profit_pool_dir":"利潤池目前流向川湖（毛利率57%→87%）；輝達擴大供應商後，部分利潤將外溢給第二供應商與買方","tam_table":{"expanded":false,"reason":"事實表沒有滑軌市場規模與滲透率數據，只有份額估計；份額變化已放在護城河威脅與反證處理"}}}},"q2_moat":{"verdict":"護城河持平。設計專利與機櫃認證帶來的定價力仍在擴大，毛利率由57%升到87%；但最大客戶正在引入第二供應商，兩股力量相抵。","reasoning":"機制：3,808件專利加上機櫃共同設計與認證，客戶換供應商要重新認證；滑軌成本占比低，客戶不值得為省錢冒品質風險。執行力給8分：產能快速擴充、休士頓廠如期量產；扣分在Q2自由現金流只有淨利的三成三，產地仍集中台灣。定價力給8分：營益率TTM 74.7%，同業表三家只有23%～28%；扣分在大和指出新供應商通過認證後，客戶可拿來壓價。同業表三家都是AI伺服器零組件鄰業，不是滑軌直接競品，只能用利潤率代替報酬率差；投入資本口徑事實表未涵蓋，無法算報酬率差。份額下滑目前是券商預估、尚未實現，所以趨勢判持平而非向下；若法人調查確認份額跌破七成，趨勢改判向下。","fact_refs":["f_peer_2059_tw_gross_margin_pct","f_peer_2059_tw_operating_margin_pct","f_peer_2059_tw_fcf_margin_pct","f_peer_3533_tw_operating_margin_pct","f_peer_3017_tw_operating_margin_pct","f_peer_2383_tw_operating_margin_pct","f_peer_2383_tw_fcf_margin_pct","f_kpi1","f_kpi5_ocf_capex"],"verdict_values":{"moat":{"mechanism":"重載滑軌設計專利（3,808件）＋機櫃共同設計與重新認證成本；滑軌占機櫃成本不到1%，客戶重品質輕價格","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價力擴大：年度毛利率2022年57.3%→2025年76.1%→Q2 87.4%，營益率TTM 74.7%對同業23%～28%。份額轉弱：大和預估輝達份額明年降至約75%（預估，尚未實現）。兩者相抵判持平","competitor_notes":[{"name":"南俊國際","strategy_note":"直接競品，伺服器滑軌占營收74%、Q1年增73.5%，是份額外流最可能的承接者；不在同業財務表內"},{"name":"3533.TW","strategy_note":"連接器廠，毛利率49%、營益率28%；屬AI伺服器零組件鄰業，只作利潤率對照，沒有份額競爭"},{"name":"3017.TW","strategy_note":"散熱模組廠，營益率24%、自由現金流利潤率24%；同吃AI機櫃順風，與滑軌無重疊"},{"name":"2383.TW","strategy_note":"基板材料廠，營益率23%、自由現金流為負，擴產吃現金；對照出川湖輕資本的現金轉換"}],"spread_notes":null,"peer_na_reason":"同業表三家是AI伺服器零組件鄰業，非滑軌直接競品；直接競品南俊國際不在表內，且投入資本口徑缺，無法算報酬率差","threats":[{"level":"🔴","text":"輝達擴大滑軌供應商基礎，大和預估川湖明年份額降至約75%；新供應商認證後，客戶可用來壓價","p":"60%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"level":"🟡","text":"南俊伺服器滑軌營收快速放量（占營收74%、Q1年增73.5%），屬點對點競爭","p":"40%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"同業抄襲專利並拿川湖研發成果宣傳，公司已表態走法律途徑","p":"30%","evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋；營益率TTM 74.7%）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運商，決策者是輝達與代工廠的機櫃設計，付款者是雲端業者。AI伺服器超過70公斤，重載滑軌是必需品；但出貨量跟雲端資本支出走，2023年營收年減26%，急迫性不等於持久性"},{"item":"決策層級","level":"🟡","text":"替代性在機櫃設計認證這一層決定，換供應商要重新認證，形成轉換成本；但最大買方輝達正主動擴大供應商基礎，降低對單一來源的依賴"},{"item":"價值鏈分配","level":"🟡","text":"滑軌占機櫃成本不到1%，客戶重品質輕價格，川湖拿到87%毛利；但買方高度集中，新供應商認證後可被拿來壓價，價值有回流買方的壓力"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，沒有民生或政治敏感性；產地集中台灣屬關稅與地緣議題，休士頓廠2026年9月量產已在分散"}],"roiic":"事實表未涵蓋（缺投入資本、折舊與營運資金）","reinvest_rate":"事實表未涵蓋；已知擴產為川益三、五期約100億元（2026年底動工）＋休士頓廠，約為FY2026E淨利（約333億元）的三成，分數年投入","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率；兩項輸入皆缺，不推估數字"}}}},"q3_growth":{"verdict":"五年後跑道中等。份額已七到八成，再成長只能靠AI機櫃市場本身擴大，未見有來源的第二條成長曲線。","reasoning":"成長以量為主（AI機櫃出貨），單價為輔（法人預估VR機櫃滑軌單價再升一成），毛利率擴張貢獻很大；沒有併購，也沒有回購。共識EPS由FY2025實際100.7元到FY2028E 572.82元，三年年化約78.5%；FY1到FY3兩年年化約28%（Koyfin快照，美元換算）。內生天花板無法計算，因為投入資本與折舊事實表未涵蓋。但資本支出強度低（Q2資本支出3.26億元，對營收108億元），即使增量報酬極高，靠再投資撐得住的成長也遠低於78.5%。缺口來自毛利率擴張（57%→87%）與產能利用率拉升的營運槓桿，屬週期性來源，不能外推，所以情境樹的Bear機率提高到30%。衰退信號亮一個：共識EPS成長明顯高於營收成長（FY2025→FY2027 EPS年化約122%，營收年化約107%）。另有預警：Q2自由現金流只有淨利的三成三。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_ocf_capex","f_kpi6","f_kpi8"],"verdict_values":{"growth":{"driver_mix":"量（AI機櫃出貨）為主、價（VR滑軌單價）為輔，毛利率擴張貢獻大；無併購、無回購","runway_years":"事實表未涵蓋（無滑軌市場滲透率）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬與再投資率皆缺，天花板不給數字；已知資本支出強度低，共識三年EPS年化78.5%明顯超出再投資能支撐的範圍，缺口歸因於毛利率擴張與產能利用率","segments":{"expanded":false,"reason":"事實表沒有分部與客戶營收占比；主力營收已確定是AI伺服器滑軌，家具與一般伺服器滑軌比重未知"},"decay_signals":[{"signal":"EPS成長顯著高於營收成長","status":"亮","note":"共識FY2025→FY2027 EPS年化約122%，營收約107%，差約15個百分點，靠毛利率擴張"},{"signal":"核心市占近12個月縮減","status":"預警","note":"大和預估輝達份額降至約75%，屬預估，尚未實現"},{"signal":"自由現金流÷淨利連2年低於0.75","status":"預警","note":"2025年為1.06，未亮；Q2單季0.33"},{"signal":"毛利率連2季年減","status":"未亮","note":"Q2毛利率87.4%，創新高"}]}}},"q4_capital":{"verdict":"資本配置以保留現金為主。淨現金約279億元，沒有併購也沒有回購，股息殖利率0.48%；三項計分中兩項不適用，股權稀釋事實表未涵蓋。","reasoning":"自由現金流÷淨利：2022年0.77、2023年1.07、2024年0.78、2025年1.06，長期現金轉換良好。Q2單季只有0.33（營業現金流27.0億元、資本支出3.3億元，對淨利70.9億元），推測是營收季增98.7%時應收與存貨先墊款，但營運資金明細事實表未涵蓋。現金去向四分事實表未涵蓋，已知用途是川益三、五期約100億元與休士頓廠。營運槓桿為正：營益率由2022年48.2%升到TTM 74.7%，沒有利益率壓縮。","fact_refs":["f_kpi4_eps","f_kpi5_ocf_capex","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_kpi8"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表未見併購紀錄"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未見回購資料"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"股權酬勞與稀釋率事實表未涵蓋；目前股數9,530萬股"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長未依賴併購；現金去向四分事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求FY2027、FY2028共識EPS（495元、573元）兌現，之後還要有雙位數成長，等於假設87%毛利率與八成份額都能維持。份額這一段我不信，基準情境的五年年化報酬只有低個位數。","reasoning":"前瞻本益比30.35倍。對FY2共識EPS約21.4倍，對FY3約18.5倍。落後本益比59.85倍，位於四個年度端點最高。賣方目標價12,000～17,500元（Investing.com均值約14,897元），另一聚合站7,022元，日期不明、應已過時，不採用。賣方目標建立在高峰毛利率延續上。成長熄火壓力測試以FY2028共識573元為基：三年後成長降到15%、給20倍，約11,460元；降到10%、給15倍，約8,595元；降到5%、給12倍，約6,876元。三情境只有一個不虧，Bear本益比錨定在14倍。現在就買的最強論證：對FY2共識只有21倍，淨現金約279億元，RSI已回到35.8，7月單月營收64億元若延續，FY2027可能超越共識。我判斷這些都依賴分母不被份額與價格侵蝕，因此不追。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct","f_rsi14","f_net_debt_m","f_ev_s_fwd","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1共識EPS 349.76元）","tier":"AI伺服器零組件高毛利龍頭","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有同業倍數；直接競品南俊也不在表內，終端倍數改以自身FY3隱含18.5倍與成長熄火測試錨定"},"fwd_pe":30.35,"peg":1.09,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"前瞻30.35倍÷FY1→FY3共識EPS兩年年化約28%＝約1.09；以FY2025實際為基期的三年年化78.5%受基期低點扭曲，不採用。分位100是四個年度端點內的位置，不是連續五年分位。分母建立在87%高峰毛利率與七到八成份額上，大和已預告份額下滑，便宜論證不成立；成長熄火三情境只有一個不虧→偏貴","upside_short_pct":-0.2,"upside_mid_pct":5.9,"denominator_disputed":true,"denominator_note":"FY1到FY3共識EPS建立在87%毛利率與約八成份額上；大和預估輝達份額降至約75%，新供應商可壓價，分母本身就是爭點。短期上檔＝Base FY2027 EPS 480元×22倍≈10,560元；中期上檔＝Base FY2029 EPS 560元×20倍≈11,200元"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是把高峰毛利率當常態；反過來，若AI機櫃需求與份額同時延續，本判斷會錯過上漲。","reasoning":"往下看錯：雲端資本支出進入消化期，加上輝達第二供應商放量，EPS可能回到300元上下，本益比壓到14倍。往上看錯：VR機櫃單價提升、休士頓廠擴產順利，份額維持八成，FY2027 EPS超越共識。兩邊的決勝數據都是未來兩季的毛利率與法人份額調查。","fact_refs":["f_week26_return_pct","f_pe_percentile","f_kpi1"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰利潤率外推風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":349.76,"pe":30.25,"basis":"FY1（FY2026E）共識EPS，與終端年以當年度EPS計倍數同口徑"},"eps":{"bull":[560,680,790,880,960],"base":[480,545,560,575,600],"bear":[430,380,300,280,300]},"pe":{"bull":26,"base":20,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.48,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-65,"hi":-45,"basis":"2023年營收曾年減26%；26週漲218%之後估值回吐空間大；Bear終點約4,200元（300元×14倍，−60%），本益比由30倍壓縮途中可能超跌，範圍取−45%～−65%","trigger_time":null},"basis":{"bull":"份額維持八成、VR單價再升一成、休士頓廠擴產順利，毛利率守在85%以上","base":"份額降到約75%，毛利率緩降至八成上下，FY2027–28較共識低3%～5%，之後隨AI機櫃市場個位數成長","bear":"2028年起雲端資本支出消化，加上第二供應商放量，份額落到六成、毛利率回到六成多，EPS回落到300元上下"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023年營收年減26%；大和預告輝達份額明年降至約75%，新供應商認證後客戶可壓價","assumption":"AI機櫃需求與高峰毛利率至少延續到2028年","consequence":"2028年若進入雲端資本支出消化期，且份額落到六成，EPS回到300元上下、本益比壓到14倍，股價約4,200元（−60%）","ruling":"採納。Bear機率給30%；這條與唯一致命點（份額跌破六成）部分重疊，已補進觸發器","watch":"月營收年增率、法人份額調查","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"南俊伺服器滑軌占營收74%、Q1年增73.5%；Q2自由現金流23.7億元，只有淨利70.9億元的三成三；擴產約100億元","assumption":"出貨量成長就等於股東報酬成長","consequence":"出貨量照樣成長，但價格被對手與第二供應商壓低，營運資金與擴產吃掉現金，每股自由現金流成長遠低於EPS","ruling":"部分採納。Base路徑較共識低3%～5%，終端倍數壓到20倍","watch":"單季毛利率、自由現金流÷淨利","evidence_refs":["competitive_share_entrants#3"],"fact_refs":["f_kpi5_ocf_capex","f_kpi4_eps"]},{"view":"價格已反映太多","evidence":"26週漲218%；落後本益比59.85倍，位於四個年度端點最高；前瞻30.35倍","assumption":"市場會繼續用30倍給高峰EPS定價","consequence":"即使EPS照共識兌現，本益比回到20倍左右，五年年化報酬只剩約3%","ruling":"採納。現價不追，設價格與毛利率雙條件才進場","watch":"股價對FY2共識倍數","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_pe_current","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 10580.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=10580.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"輝達平台份額","cause":null,"prior_field":null,"side_a":"媒體與本土券商：新世代平台份額七到八成以上，客製機櫃更高","side_b":"大和：輝達擴大供應商，明年份額降至約75%","ruling":"可調和，屬程度差異。兩邊都同意川湖目前領先，差在下滑幅度。Base採75%；份額跌破六成另列為唯一致命點","evidence_level":"二手轉述，大和原文未見","settle_metric":"2027年上半年法人供應鏈調查、南俊與川湖營收增速對照","if_then":["若南俊伺服器滑軌營收連2季增速高於川湖→減碼","若2027年上半年份額仍確認≥75%且毛利率≥80%→維持Base，不下調"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#0","competitive_share_entrants#1"]},{"axis":"估值與賣方目標價","cause":null,"prior_field":null,"side_a":"賣方目標價12,000～17,500元（Investing.com均值約14,897元），隱含較現價上漲約13%～65%","side_b":"本判斷Base：五年後約12,000元，年化報酬約3%","ruling":"⚖選本判斷這一側。依據：賣方目標是FY2027–28共識EPS乘20～30倍，等於延續高峰毛利率與份額；硬數據點是大和的75%份額預估，以及Q2自由現金流只有淨利三成三。現在就買的最強論證：對FY2共識只有21倍，淨現金約279億元，RSI已回到35.8。執行：不追，等價格或證據","evidence_level":"賣方報告二手轉述","settle_metric":"Q3、Q4單季毛利率與法人份額調查","if_then":["若股價≤8,500元且最近一季毛利率≥80%→分批反買首倉","反向：若Q3與Q4毛利率都≥85%且法人確認份額≥80%→上修Base，等價線上移至9,500元"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"獲利品質","cause":null,"prior_field":null,"side_a":"Q2淨利70.9億元","side_b":"Q2自由現金流23.7億元（營業現金流27.0億元、資本支出3.3億元）","ruling":"可調和。營收季增98.7%時，應收與存貨先墊款，2025全年自由現金流為淨利的1.06倍；但若Q3仍低於0.5，代表收款條件或庫存出問題","evidence_level":"財報數字，營運資金明細事實表未涵蓋","settle_metric":"Q3、Q4自由現金流÷淨利","if_then":["若Q3、Q4自由現金流÷淨利都低於0.5→停止加碼並下調品質分","若Q3回到0.8以上→移除此疑慮"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q3財報單季毛利率是否守住80%以上","type":"假設驗證","maps_to":"H1","metric":"單季毛利率","threshold":"≥80%","action":"守住則維持觀望、等價格；低於75%則停止加碼","source_freq":"公司季報，每季","date":"2026-11"},{"n":2,"text":"輝達新平台滑軌份額跌破六成","type":"Single Thing","maps_to":"Single Thing","metric":"輝達平台滑軌供應份額（法人調查或公司揭露）","threshold":"<60%","action":"清倉；未持有則不建倉","source_freq":"法人報告與法說，每季","date":"2027-12","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"n":3,"text":"股價回到FY2共識EPS約17倍以下，且毛利率守住","type":"估值rearm","maps_to":"H1","metric":"股價與最近一季毛利率","threshold":"股價≤8,500元且毛利率≥80%","action":"重跑研究後分批反買首倉","source_freq":"每日股價、每季財報","date":null},{"n":4,"text":"南俊伺服器滑軌營收成長連2季快於川湖","type":"風險","maps_to":"R2","metric":"南俊與川湖季營收年增率差","threshold":"南俊高於川湖連2季","action":"減碼","source_freq":"月營收公告，每月","date":null,"evidence_refs":["competitive_share_entrants#3"]},{"n":5,"text":"月營收年增率轉負","type":"風險","maps_to":"R3","metric":"月合併營收年增率","threshold":"連3個月<0%","action":"減碼","source_freq":"公開資訊觀測站，每月10日前","date":null},{"n":6,"text":"自由現金流跟不上淨利","type":"風險","maps_to":"H2","metric":"單季自由現金流÷淨利","threshold":"<0.5連2季（Q2為0.33）","action":"停止加碼","source_freq":"公司季報，每季","date":"2026-11"},{"n":7,"text":"美國對台灣製伺服器零組件加徵關稅，毛利率未能吸收","type":"風險","maps_to":"R4","metric":"單季毛利率","threshold":"關稅生效後毛利率<75%","action":"減碼","source_freq":"公司季報，每季","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":8,"text":"FY2026年報與2027年展望","type":"複審日期","maps_to":null,"metric":"全年EPS對共識349.76元","threshold":"偏離≥10%","action":"重跑研究","source_freq":"年報","date":"2027-03"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<75%連2季","window":"2026Q3至2027Q4","source":"公司季報與法說","last_status":"ok"},{"metric":"輝達平台滑軌份額","bear_threshold":"<60%","window":"12～24個月","source":"法人供應鏈調查、法說","last_status":"warning"},{"metric":"月合併營收年增率","bear_threshold":"連3個月<0%","window":"2026-10至2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"單季自由現金流÷淨利","bear_threshold":"<0.5連2季","window":"2026Q3至2027Q2","source":"公司季報現金流量表","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤8,500元（約FY2共識EPS 17倍）且最近一季毛利率≥80%，重跑研究後才建首倉","exec_line":"現價不追。跌到8,500元以下且Q3或Q4毛利率≥80%，分兩筆分批反買；份額跌破60%，或毛利率連2季低於75%，則不建倉","holding_cap":"首倉≤2%，上限3%（深回撤風險）"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方用FY2027–28共識EPS給12,000～17,500元目標價，等於假設87%毛利率與八成份額延續；大和已預告輝達份額降至約75%，新供應商認證後客戶可壓價，共識尚未反映","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤8,500元（約FY2共識EPS 17倍），且Q3財報毛利率≥80%","qc48_result":null,"qc48_note":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方用FY2027–28共識EPS給12,000～17,500元目標價，等於假設87%毛利率與八成份額延續；大和已預告輝達份額降至約75%，新供應商認證後客戶可壓價，共識尚未反映"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=218.36, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"高毛利延續：AI機櫃滑軌單季毛利率維持80%以上","2y":"單季毛利率≥80%","5y":null,"10y":null,"threshold":"單季毛利率≥80%（Q2為87.4%）","source":"公司季報與法說","drift_rule":"低於門檻5個百分點以上連2季＝削弱；低於10個百分點以上連3季＝反轉"},{"id":"H2","text":"獲利跟上基準路徑：FY2027 EPS達480元以上","2y":"FY2027 EPS≥480元","5y":null,"10y":null,"threshold":"近四季EPS對基準路徑偏離不超過5%","source":"公司季報、月營收","drift_rule":"近四季EPS低於基準路徑5%以上連2季＝削弱；10%以上連3季＝反轉"},{"id":"H3","text":"份額守住：輝達與雲端業者的AI機櫃滑軌份額維持七成以上","2y":null,"5y":"份額≥70%","10y":null,"threshold":"份額≥70%","source":"法人供應鏈調查、法說、南俊營收對照","drift_rule":"份額估計低於70%連4季＝削弱；低於60%連6季＝反轉"}],"R":[{"id":"R1","text":"輝達擴大供應商，份額降到約75%甚至更低，新供應商被拿來壓價","h_ref":"H3","clock":"⚡","threshold":"份額<70%","evidence_refs":["competitive_share_entrants#0","customer_second_source#0"]},{"id":"R2","text":"南俊等對手產能放量，壓低價格，毛利率回落","h_ref":"H1","clock":"🔥","threshold":"單季毛利率<75%","evidence_refs":["competitive_share_entrants#3"]},{"id":"R3","text":"AI資本支出進入消化期，營收重演2023年的下滑","h_ref":"H2","clock":"🔥","threshold":"月營收年增率連3個月<0%","evidence_refs":[]},{"id":"R4","text":"生產集中台灣，美國關稅或地緣事件侵蝕毛利率","h_ref":"H1","clock":"🐢","threshold":"關稅生效後單季毛利率<75%","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"輝達新一代機櫃平台滑軌認證中，川湖分配到的份額跌破60%","why_fatal":"87%毛利與30倍本益比都建立在近乎獨家供應上。份額跌破六成，代表買方已有可信替代來源，價格壓力會擴散到所有客戶，毛利率可能回到六成多，EPS下修四成以上","if_happens":"清倉；未持有則不建倉","how_monitor":"法人供應鏈調查、公司法說、南俊伺服器滑軌營收增速","probability":"約20%（大和預估已降到75%，再降15個百分點需要新平台大幅分配給第二供應商）"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.36,"peg_fy2":1.36,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":100.7,"FY2026E":349.76,"FY2027E":495.27,"FY2028E":572.82},"fy_end_month":12,"eps_basis":"新台幣；FY2025A為yfinance稀釋EPS，共識來自Koyfin快照（美元依2026-10-09匯率換算）"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3財報與法說，驗證毛利率與下半年營收","impact":"高","watch":"單季毛利率是否≥80%、自由現金流÷淨利"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"休士頓廠量產爬坡，川益三、五期動工","impact":"中","watch":"美國廠出貨占比、產能利用率"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026年報與2027年展望","impact":"高","watch":"全年EPS對共識349.76元"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
