你是 DD 管線 v20 的判斷層閘（gate），標的 3037.TW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（43 條）
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
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
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
- `f_peer_4062_t_gross_margin_pct`（q2_moat）｜4062.T 毛利率＝32.01 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4062.T.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_4062_t_operating_margin_pct`（q2_moat）｜4062.T 營業利益率＝16.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4062.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_4062_t_fcf_margin_pct`（q2_moat）｜4062.T FCF 利潤率＝21.01 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4062.T.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝24.43 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝42.01 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝69.69 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝192300.52 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝279430.0 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝1.16 十億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow：營業現金流 7,491M − 資本支出 6,333M（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：n/a
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝0.5 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-07-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance Stock Based Compensation 32.4M ÷ 營業利益 6,651M；金額小，非稀釋風險（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-07-28））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-110968.85 TWD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 48903.5、現金 159872.35（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.2 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1643.01 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝989.0 TWD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝40.48 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 24.43，分子＝快照價 989.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝64.6 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝9.69 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝9.03 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.87 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝21.78 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 20.06 → 24.43（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.77 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（41.69 → 42.01）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝2.88 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（67.74 → 69.69）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝38.16｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝12.23 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝✅｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 989.0 / W52 685.45 / W104 406.71 / W250 262.65 / W250 13週斜率 5.82%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝685.45 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝262.65 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（14 條）
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
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-08-28 公司公告配合檢調單位調查妨害農工商罪；媒體報導案情主要涉及PCB產地標示爭議，8/31 有第二波搜索，調查進行中。
  - 來源：公開資訊觀測站 歷史重大訊息清單（as_of 2026-08-28）｜affects：thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-10-13 楊梅一廠一名員工維修機台時遭夾傷不治，勞檢處依法課以部分停工處分；公司稱目前不影響生產營運，罰鍰與損失尚未確定。
  - 來源：公開資訊觀測站 重大訊息：本公司針對115/10/13工安意外之說明（as_of 2026-10-13）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年第一季欣興營收265.66億元、毛利率20.56%，年減11.75個百分點；2023年第二季營收252.35億元，為8個季度以來新低（搜尋摘要轉述，未取得逐字原文）
  - 來源：鉅亨網／搜尋摘要（欣興2023年Q1、Q2財報報導）（as_of 2023-08-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年第三季毛利率19.7%，低於市場預期；外資歸因於產能利用率偏低與產品組合不佳，BT基板因稼動率太低而虧損（搜尋摘要轉述）
  - 來源：鉅亨網／搜尋摘要（欣興2023Q3毛利率報導）（as_of 2023-11-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2024年第二季營收278.77億元（6季新高），但毛利率降至13.21%，季減3.05個百分點；公司稱PCB產線調整、學習曲線較長，載板折舊逐季上升（搜尋摘要轉述）
  - 來源：中央社 2024-07-31 欣興法說報導（as_of 2024-07-31）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-08-28 公司公告配合檢調調查妨害農工商罪（刑事偵辦，非民事訴訟）；未見投保中心團體訴訟或專利侵權訴訟。
  - 來源：公開資訊觀測站 歷史重大訊息清單（as_of 2026-08-28）｜affects：thesis.R、decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：2026-10-13 楊梅一廠工安死亡意外，勞檢處課以部分停工處分；無產品召回，公司稱不影響生產營運。
  - 來源：公開資訊觀測站 重大訊息：工安意外說明（as_of 2026-10-13）｜affects：thesis.R
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：2026-08-28 檢調搜索，公司公告配合調查；同日應證交所說明媒體新聞內容。未見財報重編或會計師非無保留意見。
  - 來源：公開資訊觀測站 歷史重大訊息清單（as_of 2026-08-28）｜affects：thesis.R、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1980,"bear_5y_price":324,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-19.1,"ev5y_pct":-12.1,"irr_base_pct":-4.2,"asym_ratio":0.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":24.43,"pe":40.48,"basis":"FY2026E 共識 EPS 24.43 元（含業外一次性收益），現價 989 元為 40.5 倍；終端倍數同樣套在終端年度 EPS，路徑 Y1～Y5 為 FY2027～FY2031；同業本益比事實表未涵蓋，以自身 FY2027 共識 23.5 倍作參照"},"eps":{"bull":[45,72,85,88,90],"base":[40,54,50,40,40],"bear":[34,36,26,16,18]},"pe":{"bull":22,"base":20,"bear":18},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.2,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 4 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 7 | 5 |
| substitute_technology | found | 1 | 3 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 3 |
| cyclical_supply_discipline_capacity | found | 6 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 5 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261019","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","irr_base_pct":-3.9,"ev5y_pct":-18.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.6,"ev5y_pct":-18.2,"irr_base_pct":-3.9,"max_dd_pct":-78,"bull_5y_price":1936,"bear_5y_price":330,"p_bull_pct":20,"p_bear_pct":35,"rearm_trigger":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","price_at_dd":1120.0,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3037.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"欣興電子"},"oneliner":"AI 讓 ABF 載板漲價、Q2 毛利率回到 24.8%，但 989 元已在付 2028 年循環高點的獲利，產地標示刑案也未決；等股價 765 元以下、毛利率守 24% 且公司未遭起訴再重啟","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3037.TW_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 晶片商（GPU、ASIC）的載板錢：ABF 載板占 Q2 營收 52%，錢卡在高階 ABF 產能與 T-glass 等關鍵材料這一節點；2026 年是缺貨漲價年，毛利率由 2025 年 13.94% 回到 Q2 24.8%","reasoning":"營收分部（Q2 2026 法說）：ABF 載板 52%（年增 51%）、HDI 22%（年增 29%）、BT 載板 9%、PCB 9%；載板與 PCB 的 AI 相關營收上半年都超過六成，下半年目標分別 70% 與 65～70%。Q2 營收 428.9 億元、毛利率 24.8%、營益率 15.5%，淨利 131.1 億元含約 89 億元業外，本業品質低於帳面。7～9 月營收合計約 526.5 億元（前九月 1,329.86 億元減上半年 803.36 億元），季增約 23%，高於券商估的 497.8 億元；但 10-27 已公布的 Q3 財報不在事實表內，Q3 毛利率是本次最大資料缺口。產業時鐘在擴張期：需求大於供給、報價逐季調漲，同業新產能要到 2027 下半年以後才開出。供需持久性判為週期性將反轉，依據見供需判讀欄。產業態勢三軸是雙向拉鋸：競爭端惡化（景碩 2027 年 ABF 產能增 25%、南電 468 億元新廠、Ibiden 擴產），結構端轉好（客戶簽 3～7 年長約並預付款），其他端變動中（產地標示刑案、美國 232 關稅是否涵蓋載板未確認）。單點依賴：單一客戶占比事實表未涵蓋；美系 ASIC 載板份額約七成既是護城河證據，也是客戶集中風險。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_eps","f_kpi6_q3_2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"中低：Q2 淨利 131.1 億元中約 89 億元來自業外（利息、評價轉盈、深圳聯能處分利益），營業利益只有 66.5 億元；本業正在改善，但帳面 EPS 高估本業","unit_econ_note":"量價齊揚：ABF 2026 年多次漲價、法人估漲幅 10～15%，並以漲價轉嫁材料成本；單價與出貨量的結構化數字事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"2022→2025 年毛利率 35.9%→13.94%，擺動約 22 個百分點；2026 年資本支出 537 億元約占共識營收 28%；營益率在 4.43%～27.17% 之間擺動"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：ABF 缺口預估 2026 下半年約 10%、2027 年 20～25%、2028 年 36～42%（Counterpoint 二手轉述、高盛、本土法人），2027 年續為賣方市場；但欣興 2026 年資本支出三度上修到 537 億元，景碩、Ibiden 2027 下半年、南電 2029 上半年新產能開出，供給可逆性高","bargaining":{"up":"上游 T-glass、銅箔、鑽針短缺，材料商議價力強；公司已為部分關鍵材料建立替代方案並以漲價轉嫁","down":"下游 AI 晶片客戶為保供應簽 3～7 年長約並預付款，短缺期公司議價力強；但客戶可在新專案加認證第二家，治理疑慮給了理由","geo":"ABF 產能全在台灣；中國有深圳、蘇州、昆山、黃石廠，產地標示案涉中國製 PCB；泰國廠第四季小量出貨；2025 年直接出口美國約 2～3%"},"profit_pool_dir":"利潤池往 AI 用高層數、大尺寸 ABF 集中，BT 與一般 PCB 相對弱；長期分配隨供需擺動","tam_table":{"expanded":false,"reason":"事實表未涵蓋 ABF 市場規模、滲透率與利潤池占比，只有供需缺口預估；不以缺口數字代替市場規模"}}}},"q2_moat":{"verdict":"護城河持平：靠 AI 高階 ABF 的良率、客戶認證與長約撐住份額，但獲利率落後 Ibiden，短缺期的定價權來自循環而非結構，等級 C","reasoning":"機制：AI 高層數、大尺寸 ABF 的製程良率與客戶認證，加上 3～7 年長約與預付款。方向證據：對獲利標竿 Ibiden 差距為負——TTM 營益率 10.24% 對 16.13%、毛利率 19.85% 對 32.01%、FCF 利潤率 −0.4% 對 21.01%；對景碩營益率持平（10.12%），對南電落後（12.27%）。份額端：美系 ASIC 載板約七成、Blackwell 三成以上（2025 年底法人看法），但治理疑慮讓客戶有理由分散。執行力 7 分（擴產與 AI 份額到位，扣分在 HDI 良率、工安、合規），定價權 5 分（短缺期漲價 10～15%，但上一輪毛利率由 35.9% 跌到 13.94%，定價權隨循環來去），綜合 C。同業投入資本不在事實表，ROIC 差距以利潤率代替。","fact_refs":["f_peer_3037_tw_gross_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_3037_tw_fcf_margin_pct","f_peer_3189_tw_gross_margin_pct","f_peer_3189_tw_operating_margin_pct","f_peer_3189_tw_fcf_margin_pct","f_peer_8046_tw_gross_margin_pct","f_peer_8046_tw_operating_margin_pct","f_peer_8046_tw_fcf_margin_pct","f_peer_4062_t_gross_margin_pct","f_peer_4062_t_operating_margin_pct","f_peer_4062_t_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"AI 高階 ABF 製程良率與客戶認證，加上 3～7 年長約與預付款形成的轉換成本","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力穩定：美系 ASIC 載板份額約七成、Blackwell 三成以上，客戶簽長約；定價權短期擴大（2026 年多次漲價）但屬循環，上一輪毛利率由 35.9% 跌到 13.94%；負面是治理疑慮可能讓客戶分散，尚未見實際轉單。兩者合計持平","competitor_notes":[{"name":"景碩（3189.TW）","strategy_note":"TTM 毛利率 23.26%、FCF 利潤率 7.37% 都優於欣興；2027 年 ABF 產能擴 25% 到約 5,000 萬顆，是客戶分散供應商時最直接的受益者"},{"name":"南電（8046.TW）","strategy_note":"毛利率 16.04% 較低但營益率 12.27% 較高；嘉義新廠 468 億元最快 2029 上半年才貢獻，2027～2028 年只靠去瓶頸微幅擴量"},{"name":"Ibiden（4062.T）","strategy_note":"毛利率 32.01%、營益率 16.13%、FCF 利潤率 21.01%，是獲利標竿；新產能多在 2027 下半年開出，與欣興正面爭奪 AI 高階份額"}],"peer_na_reason":"事實表未涵蓋同業投入資本，ROIC 差距以毛利率、營益率、FCF 利潤率代替","threats":[{"level":"🟡","text":"客戶因產地標示案的治理疑慮加認證景碩、南電、Ibiden、SEMCO 等供應商，美系 ASIC 載板約七成份額易降難升","p":"30%","evidence_refs":["competitive_share_entrants#1","geo_supply_chain#1","reg_tariff_export#1"]},{"level":"🟡","text":"同業同步擴產：景碩 2027 年 ABF 產能增 25%、Ibiden 2027 下半年、南電 2029 上半年開出，短缺期定價權在 2028 年後退潮","p":"40%","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"新世代封裝基板 EMIB-T 2027 年量產、首階良率目標僅 50%，世代轉換中良率落後會讓出份額","p":"20%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"TTM 屬低利益率×低周轉（營益率 10.24%，資產重），2026 下半年往高利益率×低周轉移動；投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端業者、決策者是 GPU 與 ASIC 設計商、付款者是晶片商或封測廠，三角色都成立；AI 加速器沒有 ABF 以外的量產方案，屬需要而非想要。但急迫性來自 AI 資本支出週期，不等於持久，高盛也點名 PC 需求復甦慢"},{"item":"決策層級","level":"🟡","text":"替代性要看單一晶片專案：新專案要重新認證，合約 3～7 年並有預付款，轉換成本高；但客戶可在下一代專案加認證第二家，治理疑慮正給客戶理由這樣做"},{"item":"價值鏈分配","level":"🟡","text":"AI 晶片價值鏈中載板採購金額占比小，晶片設計與晶圓代工拿走多數；短缺期欣興能漲價 10～15%，但上游 T-glass、銅箔短缺也讓材料商分走一塊；2023～2025 年毛利率跌到 14%，說明分配隨供需擺動"},{"item":"社會容忍度","level":"🟢","text":"工業零組件的企業間交易，沒有社會對漲價的容忍上限；監管風險是產地標示的刑事合規，不是定價授權"}],"roiic":"無法計算：事實表未涵蓋投入資本與折舊。旁證：2022→2025 年營業利益由約 381.7 億元降到約 66.8 億元（營收×營益率），同期自由現金流由正 286 億元轉為負 111 億元，上一輪增量投資在谷底期報酬為負；2026 年回升主要來自報價","reinvest_rate":"扣折舊前約 140%：2026 年資本支出 537 億元÷FY2026 共識淨利約 379 億元（24.43 元×約 15.52 億股）；折舊與營運資金變動事實表未涵蓋，淨再投資率無法精算","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；增量 ROIC 缺投入資本無法計算，天花板留空。共識 FY2026→2028 年 EPS 年複合 69% 幾乎全靠利潤率回升，不是再投資複利，視同超出天花板"}}}},"q3_growth":{"verdict":"五年後成長空間中等：2028 年前靠漲價加擴產，AI 占比已超過六成，之後要看新世代封裝基板能否接棒，而且成長幾乎全靠利潤率回升","reasoning":"成長來源：價（ABF 2026 年多次漲價，法人估漲幅 10～15%）＋量（光復一廠三期 Q3 量產、光復二廠 2027 年擴 30% 以上 ABF 產能、楊梅二廠約 2028 年量產）＋利潤率回升；無併購、無回購。共識 EPS：FY2025A 4.34 元→FY2028E 69.69 元，三年年複合約 152%，分母是谷底，沒有參考意義；FY2026E→FY2028E 年複合約 69%。共識營收 FY2026 1,923 億元（11 位分析師）、FY2027 2,794 億元（20 位），FY2028 營收共識事實表未涵蓋。缺口歸因：幾乎全來自利潤率回升（毛利率由 13.94% 回到 24.8% 並預期續升），屬循環，不是再投資複利。Runway：缺口預估到 2028 年，高確信約 2～3 年；第二條曲線 EPS 只有 EMIB-T 2027 年量產，屬世代轉換而非新市場，判中等。衰退訊號亮兩項，價值陷阱風險與長期成長性都判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_q3_2026"],"verdict_values":{"growth":{"driver_mix":"價＋量＋利潤率回升：ABF 漲價、光復廠擴產、AI 占比提高；無併購、無回購","runway_years":3,"runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 缺投入資本與折舊資料無法計算，天花板留空；再投資率扣折舊前約 140%，代表成長靠大量資本投入。共識年複合 69% 的缺口歸因為利潤率回升（毛利率 13.94%→24.8% 並預期續升），屬循環","segments":[{"item":"ABF 載板","value":"Q2 營收占 52%，年增 51%、季增 22%；2026 年資本支出八成以上投入"},{"item":"HDI","value":"占 22%，年增 29%；外資指 AI HDI 初期良率偏低"},{"item":"BT 載板","value":"占 9%；上一輪 2023 年曾因稼動率低而虧損"},{"item":"PCB","value":"占 9%；產地標示調查集中在此"},{"item":"其他","value":"約 8%，事實表未拆分"}],"decay_signals":["亮：EPS 成長遠高於營收成長——FY2027 共識 EPS 年增約 72%，共識營收年增約 45%","亮：自由現金流÷淨利連兩年低於 0.75——2024、2025 年自由現金流為負 164 億、負 111 億元","未亮：毛利率連兩季年減（Q2 2026 毛利率 24.8%，遠高於 2025 年全年 13.94%）","未亮：核心市占縮減（只有市場疑慮，未見實際轉單）","未亮：SBC 占比偏高（SBC 只占營業利益 0.5%）","資料缺口：維護性資本支出占比事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：賺的錢全投回擴產、自由現金流轉負，靠約 1,110 億元淨現金與客戶預付款撐住，股東回饋極低","reasoning":"現金轉換：2024、2025 年自由現金流 −164 億、−111 億元，對淨利 50.8 億、66.7 億元皆為負；Q2 2026 營業現金流 74.9 億元減資本支出 63.3 億元，自由現金流 11.6 億元，只有淨利的 9%。SBC 只占營業利益 0.5%，不是稀釋來源。現金去向：資本支出為主（2026 年預算 537 億元，八成以上投 ABF）；股息殖利率 0.2%；事實表未涵蓋回購；處分深圳聯能（人民幣 8.8 億元）與日本子公司（意向書階段）屬組合瘦身；無收購。資產負債：總債務約 489 億元、現金約 1,599 億元，淨現金約 1,110 億元，足以支應一年資本支出。股數：以淨利÷EPS 推得的加權股數 2022 年約 15.47 億、2025 年約 15.38 億、Q2 2026 約 15.52 億股，但市值口徑的流通股數 16.43 億股，差距約 6% 原因事實表未涵蓋，終端 EPS 以約 16 億股估算。","fact_refs":["f_kpi4","f_kpi5_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_kpi3_eps","f_peer_3037_tw_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近期無收購，只有處分深圳聯能（人民幣 8.8 億元）與日本子公司意向書，沒有併購報酬可算"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄；股息殖利率 0.2%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營業利益 0.5%；淨利÷EPS 推得的加權股數 2022 年約 15.47 億、2025 年約 15.38 億、Q2 2026 約 15.52 億股，年稀釋遠低於 1.5%；市值口徑流通股數 16.43 億股的差距來源未明"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能而非併購，股息殖利率 0.2%、無回購紀錄，資本回饋不承重"}}}},"q5_valuation":{"verdict":"現價 989 元要求 2028 年共識 EPS 69.69 元兌現，而且被當成常態獲利；那是高於 2022 年循環高點的利潤率，我不信能延續，估值偏貴","reasoning":"股價隱含的預期：989 元＝FY2027 共識 23.5 倍、FY2028 共識 14.2 倍。若 2028 年是循環高點，市場屆時通常只給低倍數；要讓現價合理，需要 2029 年後獲利不回落。FY2027 共識隱含淨利率約 23%（42.01 元×約 15.52 億股÷營收 2,794 億元），已高於 2022 年高點約 21%。共識仍在上修：FY1 三個月上修 21.78%，最近一次 FY2 上修 0.77%、FY3 上修 2.88%。法說後賣方目標價 1,010～1,500 元，全距約 1.5 倍，年初大摩 550 元已過時；現價低於所有法說後目標價，賣方共識反對本次偏貴判斷，分歧在框架：賣方用 2027～2028 年獲利給成長倍數，我用循環高點利潤率打折。週線均線仍是多頭排列，RSI 38 屬回檔，不過熱。循環股優先看股價淨值比，但事實表未涵蓋淨值；同業本益比也未涵蓋，終端倍數只能以自身 FY2027 共識倍數作參照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_ev_s_fwd","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_rsi14","f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w250"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026～FY2028 共識）為主；循環股優先的股價淨值比事實表未涵蓋","tier":"台系 ABF 三雄（欣興、南電、景碩）與日系 Ibiden 同層","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比與股價淨值比，無法做倍數對照"},"fwd_pe":40.48,"peg":0.59,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 989 元＝FY2026 共識 40.5 倍、FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；現值本益比 64.6 倍、股價營收比 9.69 倍、EV／營收 9.03 倍都在四個年度端點最高（連續五年分位事實表未涵蓋，五年分位留空）。2027～2028 年共識獲利隱含利潤率高於 2022 年循環高點，高點年份應給低倍數。一年後：FY2028 Base EPS 54 元×18 倍＝972 元（−1.7%）；五年 Base：40 元×20 倍＝800 元（−19.1%）。PEG 0.59＝40.48 倍÷FY2026→2028 共識 EPS 年複合 69%，偏低只因分母從循環低點起算，不代表便宜。判為偏貴","upside_short_pct":-1.7,"upside_mid_pct":-19.1,"denominator_disputed":true,"denominator_note":"FY2026 共識 EPS 24.43 元含 Q2 約 89 億元業外收益（其中有深圳聯能處分利益），FY2028 共識 69.69 元是循環高點獲利；用哪一年當分母決定便宜或貴，以本益比論便宜不成立"}}},"q6_how_wrong":{"verdict":"最可能看錯在循環長度：若 AI 需求讓短缺延續到 2029 年後、長約讓谷底變淺，偏貴的判斷就錯；往下則是 2027 下半年就見頂，再疊上合規事件","reasoning":"壓力測試五項過兩項：毛利率回到 2025 年 13.94% 仍有獲利（2025 年淨利 66.7 億元）、淨現金約 1,110 億元足以支應一年 537 億元資本支出；未過：自由現金流為負、Bear 下檔約三分之二、產地標示案未決。回撤區間與推導寫在情境假設，反證三視角寫在反證紀錄，這裡不重寫。衰退訊號亮兩項（EPS 成長遠高於營收、自由現金流連兩年為負），價值陷阱判中等。","fact_refs":["f_price_at_dd","f_ma_w250","f_net_debt_m","f_peer_3037_tw_fcf_margin_pct","f_pe_current"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高檔＋自由現金流為負"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":24.43,"pe":40.48,"basis":"FY2026E 共識 EPS 24.43 元（含業外一次性收益），現價 989 元為 40.5 倍；終端倍數同樣套在終端年度 EPS，路徑 Y1～Y5 為 FY2027～FY2031；同業本益比事實表未涵蓋，以自身 FY2027 共識 23.5 倍作參照"},"eps":{"bull":[45,72,85,88,90],"base":[40,54,50,40,40],"bear":[34,36,26,16,18]},"pe":{"bull":22,"base":20,"bear":18},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.2,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-80,"hi":-45,"basis":"Bear 終點 18 元×18 倍＝324 元（−67%）；循環谷底 EPS 16 元×15 倍＝240 元（−76%）；股價回到 250 週均線 262.65 元為 −73%；Base 路徑 2028 年高點約 54 元×23 倍＝1,242 元，2030 年回到 40 元×18 倍＝720 元，高點回落約 42%；上一輪 2022→2024 年營益率由 27.17% 跌到 4.43%。取 −80%～−45%，屬深回撤路徑；論點完整時不因波動砍倉，但倉位上限 3%","trigger_time":null},"basis":{"bull":"Bull 20%：AI 加速器載板用量增速高於全產業產能，缺口照高盛與本土法人預估在 2028 年擴大到 36～42% 並延續到 2030 年，長約鎖價讓利潤率停在 2022 年高點附近，2031 年 EPS 約 90 元、給 22 倍","base":"Base 45%：2027 年 EPS 40 元（略低於共識 42.01 元，折舊與 HDI 良率拖累），2028 年高點 54 元（低於共識 69.69 元），2029～2030 年新產能湧出、報價回落，2031 年 40 元；長約讓谷底比上一輪淺，終端 20 倍","bear":"Bear 35%：2027 下半年起同業產能開出、AI 資本支出消化，加上產地標示案起訴與客戶分散，2030 年毛利率回到 15～18%、EPS 約 16 元。供需缺口預估屬結構性順風但不全採信，因為上一輪高點後兩年營益率掉約 23 個百分點、本輪全產業同步擴產，且共識 2028 年利潤率高於上一輪高點"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪高點後，2023 年 Q1 毛利率年減 11.75 個百分點、Q3 BT 載板因稼動率低而虧損，2024 年 Q2 毛利率 13.21%；本輪欣興資本支出三度上修到 537 億元，八成以上投 ABF","assumption":"AI 需求能吸收 2027 下半年到 2029 年全產業的新產能","consequence":"報價 2028 年轉跌、2030 年毛利率回到 15～18%，EPS 約 16～18 元，乘 18 倍約 300 元，五年虧損約三分之二","ruling":"採納，Bear 機率 35%；與唯一致命點（報價首度季減）是同一件事的前後階段，兩者一致","watch":"季毛利率年增減、ABF 報價口徑、同業新廠進度","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1_gaap","f_kpi6_q3_2026"]},{"view":"論點失敗","evidence":"檢方兩波搜索、14 名主管員工被詢問、PCB 事業部總經理 1,500 萬元交保；法人提醒美國海關扣貨、補稅與客戶重新稽核","assumption":"案件限於 PCB 特定廠房，ABF 產能全在台灣不受影響","consequence":"若起訴公司或客戶啟動合規條款，PCB 與 HDI（合計約 31% 營收）訂單轉出，ABF 新專案也被分散認證","ruling":"部分採納：決勝資料尚不存在，列入重啟條件與風險 R1；營收曝險小於報價轉折，不當唯一致命點","watch":"起訴範圍、美國海關動作、客戶揭露的供應商名單","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","competitive_share_entrants#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"TTM 自由現金流利潤率 −0.4%，2024、2025 年自由現金流 −164 億、−111 億元；2026 年資本支出 537 億元約為 FY2026 共識淨利的 1.4 倍；Ibiden FCF 利潤率 21.01%","assumption":"這一輪高額擴產的增量報酬高於資金成本","consequence":"AI 需求論點成立，但獲利被折舊與下一輪擴產吃掉，股東拿到的現金有限，股息殖利率只有 0.2%","ruling":"採納：資本配置偏弱，長期信心上限中","watch":"自由現金流÷淨利、2027 年資本支出指引","evidence_refs":["cyclical_supply_discipline_capacity#3"],"fact_refs":["f_peer_3037_tw_fcf_margin_pct","f_peer_4062_t_fcf_margin_pct","f_kpi4","f_dividend_yield_ttm"]},{"view":"論點成功但股東經濟變差","evidence":"楊梅一廠工安死亡、勞檢部分停工、罰鍰未定；美系外資指 AI HDI 與 PCB 初期良率偏低","assumption":"停工不影響營運，良率能在 2027 年拉上來","consequence":"營收成長但營益率落後共識，2027 年 EPS 低於 42.01 元","ruling":"部分採納：Base 2027 年 EPS 取 40 元，略低於共識","watch":"月營收月增率、季營益率","evidence_refs":["major_events#1","product_recall_warning#0","capital_markets_pricing#2"],"fact_refs":["f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"現價為 FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；現值本益比 64.6 倍、股價營收比 9.69 倍都在四個年度端點最高；股價是 250 週均線 262.65 元的 3.8 倍","assumption":"2028 年共識獲利是常態而非高點","consequence":"即使 2028 年兌現，市場在高點利潤率年份給低倍數，Base 五年終值 800 元低於現價","ruling":"採納：維持觀望、不追價；反方是賣方目標價與共識續上修，已在矛盾裁定處理","watch":"FY2028 共識修正方向、股價對 FY2027 共識倍數","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4"],"fact_refs":["f_price_at_dd","f_pe_current","f_ps_current","f_ma_w250","f_consensus_eps_fy2","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1120.0 → 本次 989.0（-11.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1120.0","side_b":"本次 price_at_dd=989.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,120 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,120 元：Bull 價 1,936、Bear 價 330，五年期望值 −18.2%，基準年化 −3.9%，不對稱比 0.6","side_b":"本次情境、股價仍用 1,120 元：Bull 價 1,980、Bear 價 324，五年期望值 −22.4%，基準年化 −6.5%，不對稱比 0.62","ruling":"先換情境、股價不動：五年期望值少 4.2 個百分點，基準年化少 2.6 個百分點。不對稱比由 0.6 變為 0.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,120 元：五年期望值 −22.4%，基準年化 −6.5%，不對稱比 0.62","side_b":"本次情境、股價 989 元：五年期望值 −12.1%，基準年化 −4.2%，不對稱比 0.85","ruling":"再換股價、情境不動：起點價下跌 11.7%，五年期望值多 10.3 個百分點，基準年化多 2.4 個百分點，不對稱比由 0.62 升到 0.85。合計五年期望值比前份多 6.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後結論未變","cause":"價格變動","prior_field":["signal","val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份（10-19）股價 1,120 元：觀望、整體評級 C、估值偏貴、多空機率 20%／35%、最大回撤 −78%","side_b":"本次股價 989 元（−11.7%）：FY2027 共識 23.5 倍、FY2028 共識 14.2 倍；多空機率維持 20%／35%，最大回撤區間 −80%～−45%","ruling":"跌幅來自價格而非基本面轉弱，Q2 毛利率 24.8% 與 9 月營收年增 64.7% 仍在上行；Base 五年終值 800 元仍低於現價，評級、估值結論、觀望與多空機率都不變，回撤區間改用範圍表達","evidence_level":"高（價格與共識皆為事實表數字）","settle_metric":"股價對 FY2027 共識 EPS 的倍數","if_then":["若股價跌到 765 元以下且季毛利率≥24%、產地案未起訴公司，重啟研究評估首筆","若股價反彈到 1,200 元以上而 FY2028 共識未上修，維持不追"],"evidence_refs":[]},{"axis":"前份漂移：10-19 之後的新事件","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：陷阱風險中等、護城河持平、五年後成長空間中等、循環股、中循環","side_b":"新事件：楊梅一廠工安死亡、勞檢部分停工（10-13）；處分日本子公司意向書（10-27）；FY2028 共識 EPS 上修 2.88%；10-27 已公布 Q3 財報但事實表未收","ruling":"工安停工公司稱不影響營運、日本子公司處分屬組合瘦身，都不改護城河與循環位置；Q3 財報缺漏是本次最大資料缺口，五欄維持前份結論","evidence_level":"中（Q3 財報缺漏）","settle_metric":"Q3 2026 毛利率與 Q4 展望","if_then":["若 Q3 毛利率低於 24%，循環位置改判晚循環並取消重啟","若 Q3 毛利率≥28% 且 Q4 展望續增，維持中循環判斷"],"evidence_refs":["major_events#1","product_recall_warning#0"]},{"axis":"重啟條件改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價≤765元（約 FY2027 共識 EPS 20倍），且最近一季毛利率仍≥24%","side_b":"股價≤765元（約FY2027共識EPS 18倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","ruling":"價格門檻 765 元不變，FY2027 共識已到 42.01 元，765 元改寫為約 18 倍；另加事件條件：刑事程序已開始、客戶可能重新稽核，價格到了但公司被起訴就不重啟研究、不建倉","evidence_level":"中","settle_metric":"股價、季毛利率、起訴範圍","if_then":["三條件全成立：重跑判斷，通過後首筆建倉 1.5%","價格到了但公司被起訴：不建倉，等客戶稽核結果"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（null）","side_b":"本次設四項：季毛利率連兩季低於 20%、月營收年增連三月低於 10%、產地標示案起訴公司、ABF 報價首度季減；觸發即減碼或清倉","ruling":"前份只有重啟條件、沒有持有中的出場規則；本次補上，未持有時作為取消重啟的條件","evidence_level":"中","settle_metric":"四項停損指標","if_then":["任一項觸發且已持有：減碼一半","起訴公司或報價季減後毛利率再連兩季年減：清倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未記錄唯一致命點（null）","side_b":"2027 年底前 ABF 載板報價首次出現季減（漲價循環結束）","ruling":"Single Thing 改設為報價轉折：情境樹最敏感的是 2028 年後獲利，報價是它的單一開關；產地標示案影響 PCB 與 HDI（合計約 31% 營收），敏感度較小，列風險 R1","evidence_level":"中","settle_metric":"ABF 報價季變動","if_then":["報價首度季減：取消重啟；若持有減碼一半","2027 年各季報價持續調漲：Bull 機率上調重跑判斷"],"evidence_refs":[]},{"axis":"供需：短缺延續 vs 擴產軍備競賽","cause":null,"side_a":"ABF 缺口 2027 年約 20～25%、2028 年 36～42%（Counterpoint、高盛、本土法人），2027 年續為賣方市場","side_b":"欣興 2026 年資本支出三度上修到 537 億元，景碩 2027 年擴 25%，Ibiden 2027 下半年、南電 2029 上半年新產能開出；上一輪 2023 年 Q1 毛利率年減 11.75 個百分點","ruling":"可調和（時點差異）：2027 年前短缺成立，2028～2029 年供給湧出的風險同樣成立；Base 路徑採 2028 年獲利高點、2029～2030 年回落","evidence_level":"中（缺口預估多為二手轉述，資本支出為公司公告）","settle_metric":"ABF 報價季變動與季毛利率年增減","if_then":["若 2027 年各季毛利率仍季增且景碩、南電擴產延後，Bull 機率由 20% 上調到 30%","若 2027 年任一季報價季減，Bear 機率上調到 45%"],"evidence_refs":["supply_demand_durability#0","end_markets#5","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#1","cyclical_prior_downcycle_behavior#0"]},{"axis":"產地標示案：短期事件 vs 客戶分散供應商","cause":null,"side_a":"花旗：ABF 產能全在台灣，調查若限特定廠房屬短期影響，維持買進、目標價 1,500 元","side_b":"刑事搜索兩波、PCB 事業部總經理交保；市場擔心觸發美系客戶合規條款，客戶可能加認證景碩、南電與日系","ruling":"不可裁決至檢方起訴決定：決勝資料（起訴書、客戶稽核結果）今天不存在，證據時間窗沒有蓋住風險窗；在此之前不稱風險已解，列為重啟條件與風險 R1","evidence_level":"中","settle_metric":"起訴範圍（個人或法人）、美國海關動作、主要客戶揭露的供應商變動","if_then":["若只起訴個人且無海關動作，事件條件解除","若起訴公司或主要客戶公開轉單，持有則清倉，未持有則取消重啟"],"evidence_refs":["geo_supply_chain#0","regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2","competitive_share_entrants#1"]},{"axis":"市場定價 vs 循環歷史","cause":null,"side_a":"法說後賣方目標價 1,010～1,500 元、多家買進；FY1 共識三個月上修 21.78%；現價只要 FY2028 共識的 14.2 倍","side_b":"FY2027 共識隱含淨利率約 23%，已高於 2022 年高點約 21%，FY2028 共識要求更高；過去四年毛利率在 13.94%～35.9% 擺動","ruling":"不可調和（方向相反）。選循環歷史：2022 年營益率 27.17% 之後兩年跌到 4.43%，而本輪全產業同步擴產；硬數據點是季毛利率與 ABF 報價。執行：維持觀望不追價。現在就買的最強論證：股價已從 1,120 元回落 11.7%、RSI 38、FY2028 共識只有 14.2 倍、缺口預估到 2028 年擴大、長約預付款降低下行；它不成立的理由是 14.2 倍的分母是高點獲利。反向條件：2027 下半年毛利率仍季增且 FY2028 共識續上修，承認拉長型循環並重跑判斷","evidence_level":"中","settle_metric":"2027 年各季毛利率與 FY2028 共識 EPS 修正方向","if_then":["若 2027 上半年毛利率≥28% 且 FY2028 共識續上修，重跑判斷、Bull 機率上調到 30%","若股價先漲到 1,200 元以上但毛利率未過 26%，不追","若股價跌到 765 元以下而毛利率仍≥24%、產地案未起訴公司，分批反買首筆 1.5%"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"axis":"獲利品質：淨利 vs 營業利益","cause":null,"side_a":"Q2 EPS 8.45 元、淨利 131.1 億元","side_b":"Q2 營業利益只有 66.5 億元，業外約 89 億元（利息、評價轉盈、深圳聯能處分利益）；FY2026 共識 EPS 24.43 元含一次性收益","ruling":"可調和（程度差異）：本業仍在改善（營益率 15.5%），但 FY2026 本益比 40.5 倍的分母高估本業，估值改以 FY2027 錨定","evidence_level":"高","settle_metric":"Q3、Q4 業外收益占稅前淨利比","if_then":["若 Q3 業外占稅前淨利仍超過三成，Base 2027 年 EPS 再下修","若業外回到一成以下且營益率≥18%，維持 Base"],"evidence_refs":[]},{"axis":"管理層展望 vs 外資對 HDI 良率疑慮","cause":null,"side_a":"公司稱 Q3 營收與毛利率續季增，AI 占比下半年升到 65～70%","side_b":"一家美系外資指 AI HDI 與 PCB 初期良率偏低，毛利率展望偏弱","ruling":"可調和（分部差異）：載板占 61%（ABF 52%＋BT 9%）主導毛利率，HDI 良率拖累有限；Q3 財報可驗證，但事實表未收","evidence_level":"中","settle_metric":"Q3 毛利率與 HDI 營收季變動","if_then":["若 Q3 毛利率低於 Q2，採信外資疑慮、Base 2027 年 EPS 下修到 36 元","若 Q3 毛利率≥26%，管理層展望成立"],"evidence_refs":["capital_markets_pricing#2"]}],"triggers":[{"n":1,"text":"股價跌到 765 元以下、最近一季毛利率仍≥24%，且產地標示案未起訴公司：重啟研究，通過後分批建立首筆","type":"估值rearm","maps_to":"H1","metric":"股價、季毛利率、起訴範圍","threshold":"≤765 元且毛利率≥24% 且未起訴公司","action":"重跑判斷後首筆 1.5%","source_freq":"每日股價；每季財報；重大訊息即時","date":null},{"n":2,"text":"補讀 10-27 已公布的 Q3 2026 財報：毛利率低於 24% 則取消重啟、循環位置改判晚循環","type":"假設驗證","maps_to":"H1","metric":"Q3 2026 毛利率","threshold":"<24%","action":"取消重啟、重跑判斷","source_freq":"一次性（Q3 財報已公布）","date":"2026-11"},{"n":3,"text":"ABF 載板報價首次季減","type":"Single Thing","maps_to":"H1","metric":"ABF 報價季變動","threshold":"首次季減","action":"取消重啟；若持有減碼一半","source_freq":"每季法說、同業法說","date":"2027-12-31 前"},{"n":4,"text":"檢方起訴公司本身，或美國海關扣貨、主要客戶公開轉單","type":"清倉","maps_to":"R1","metric":"起訴範圍與客戶動作","threshold":"起訴法人或董事長以上；或任一主要客戶轉單","action":"持有則清倉，未持有則取消重啟","source_freq":"重大訊息即時","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"n":5,"text":"季毛利率連兩季年減","type":"減碼","maps_to":"R2","metric":"季毛利率年增減","threshold":"連兩季年減","action":"減碼一半，再一季年減則清倉","source_freq":"每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"n":6,"text":"楊梅一廠停工擴大或 HDI 良率拖累營益率","type":"風險","maps_to":"R3","metric":"季營益率季變動、月營收月增率","threshold":"營益率季減≥3 個百分點，或月營收連兩月月減","action":"凍結重啟一季","source_freq":"每月營收、每季財報","date":null,"evidence_refs":["major_events#1","product_recall_warning#0","capital_markets_pricing#2"]},{"n":7,"text":"月營收年增率維持 25% 以上到 2027 年中","type":"假設驗證","maps_to":"H2","metric":"月營收年增率","threshold":"≥25%","action":"未達則 H2 削弱、Bull 機率下修","source_freq":"每月 10 日前","date":"2027-07"},{"n":8,"text":"美系 ASIC 載板份額跌破五成","type":"風險","maps_to":"R4","metric":"ASIC 載板份額","threshold":"<50%（2025 年底約 70%）","action":"護城河改判下滑，重跑判斷","source_freq":"法說與產業報導，不定期","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":9,"text":"Q4 2026 法說：2027 年資本支出與報價口徑","type":"複審日期","maps_to":"H1","metric":"2027 年資本支出、毛利率展望","threshold":"資本支出再上修且同業同步擴產","action":"重跑判斷","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"連兩季低於 20%（Q2 2026 為 24.8%）","window":"至 2027 年底","source":"公司季報與法說","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月低於 10%（2026 年 9 月為 +64.7%）","window":"逐月，至 2027 年底","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"產地標示案進展","bear_threshold":"起訴公司或董事長以上，或美國海關扣貨、主要客戶公開轉單","window":"至 2027 年 6 月","source":"公開資訊觀測站重大訊息、地檢署公告","last_status":"warning"},{"metric":"ABF 載板報價","bear_threshold":"公司或同業首次宣布季減","window":"至 2027 年底","source":"法說會與產業報導","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤765元（約FY2027共識EPS 18倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","exec_line":"未觸發前不建倉、不追價；觸發後先重跑判斷，通過才分批建立，首筆 1.5%、總上限 3%；持有中依停損指標減碼或清倉","holding_cap":"3%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2028 年共識 EPS 69.69 元（利潤率高於 2022 年高點）當常態獲利，給 FY2027 共識 23.5 倍；但欣興、景碩、南電、Ibiden 的新產能正好在 2027 下半年到 2029 年開出，上一輪高點後兩年營益率由 27% 跌到 4%","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價≤765 元（約 FY2027 共識 18 倍）且最近一季毛利率≥24%，且產地標示案未起訴公司本身","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2028 年共識 EPS 69.69 元（利潤率高於 2022 年高點）當常態獲利，給 FY2027 共識 23.5 倍；但欣興、景碩、南電、Ibiden 的新產能正好在 2027 下半年到 2029 年開出，上一輪高點後兩年營益率由 27% 跌到 4%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=12.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":["QC-50"]},"thesis":{"H":[{"id":"H1","text":"ABF 載板供不應求延續到 2027 年底，漲價讓季毛利率守在 24% 以上並往 28% 走","2y":"2027 年各季毛利率≥24%，全年≥26%","5y":null,"10y":null,"threshold":"季毛利率≥24%（Q2 2026 為 24.8%）","source":"公司季報與法說會（每季）、月營收（每月）","drift_rule":"以近四季毛利率對 26% 路徑的偏離計：連兩季落後 5% 以上視為削弱，連三季落後 10% 以上視為反轉"},{"id":"H2","text":"AI 需求讓營收維持高成長：2027 年營收達 2,500 億元以上（共識 2,794 億元）","2y":"2027 年營收≥2,500 億元；月營收年增≥25% 到 2027 年中","5y":null,"10y":null,"threshold":"2027 年營收≥2,500 億元","source":"公開資訊觀測站月營收、年報","drift_rule":"近四季營收對 2,500 億元路徑的偏離：連兩季落後 5% 以上視為削弱，連三季落後 10% 以上視為反轉"},{"id":"H3","text":"這一輪循環的谷底比上一輪淺：長約與 AI 占比讓 2026～2030 年平均營益率≥15%，下一個谷底年營益率≥8%（2024 年為 4.43%）","2y":null,"5y":"2026～2030 年平均營益率≥15%；谷底年≥8%","10y":null,"threshold":"五年平均營益率≥15%；谷底年≥8%","source":"年報與季報","drift_rule":"以近四季營益率對 15% 的偏離計：連四季落後 5% 以上視為削弱，連六季落後 10% 以上視為反轉"}],"R":[{"id":"R1","text":"產地標示案擴大：檢方起訴公司本身，或美國海關扣貨、客戶重新稽核後公開轉單","h_ref":"H2","clock":"⚡","threshold":"起訴法人或董事長以上；或任一主要客戶公開轉單","evidence_refs":["regulatory_antitrust#0","major_events#0","lawsuit_class_action#0","sec_investigation_restatement#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"擴產軍備競賽讓供給在 2027 下半年到 2029 年湧出，報價轉跌、毛利率回落，重演 2023～2024 年","h_ref":"H1","clock":"🔥","threshold":"毛利率連兩季年減，或 ABF 報價首度季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"執行與工安：HDI 與 AI PCB 良率偏低、楊梅一廠部分停工、537 億元擴產帶來折舊壓力","h_ref":"H1","clock":"⚡","threshold":"營益率季減≥3 個百分點，或停工擴大到影響月營收","evidence_refs":["capital_markets_pricing#2","major_events#1","product_recall_warning#0"]},{"id":"R4","text":"客戶因治理疑慮分散供應商，美系 ASIC 約七成的份額被南電、景碩、日系分走","h_ref":"H3","clock":"🐢","threshold":"法說或客戶揭露份額跌破 50%","evidence_refs":["competitive_share_entrants#1"]}],"single_thing":{"description":"2027 年底前 ABF 載板報價首次出現季減（漲價循環結束）","why_fatal":"情境樹最敏感的是 2028 年後的獲利水準：共識 2027、2028 年 EPS 42.01、69.69 元，隱含利潤率回到 2022 年高點以上；報價一轉跌，2023 年前例是單季毛利率年減 11.75 個百分點，終端 EPS 會從 Base 的 40 元往 Bear 的 18 元移動，下檔約三分之二","if_happens":"未持有：取消重啟，改等循環谷底訊號；已持有：減碼一半，毛利率再連兩季年減則清倉","how_monitor":"每季法說的報價說法（目前稱滾動式調整）、季毛利率年增減、景碩與南電法說的報價口徑、月營收年增率","probability":"約 20%（12～24 個月）：多家預估 2027、2028 年缺口擴大所以不高，但 2027 下半年 Ibiden 與景碩新產能開出是主要風險窗"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":23.5,"peg_fy2":0.36,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.34,"FY2026E":24.43,"FY2027E":42.01,"FY2028E":69.69},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（新台幣）；FY2025A 取年度財報，共識取 Koyfin 2026-10-31 快照，美元值依當日匯率換算；營收共識 FY2026 有 11 位、FY2027 有 20 位分析師"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"10 月營收公布，並補讀 10-27 已公布的 Q3 財報","impact":"中","watch":"月營收年增率是否維持 50% 以上；Q3 毛利率是否≥24%"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年資本支出","impact":"高","watch":"毛利率是否≥26%、資本支出是否再上修"},{"date":"2027-04","date_precision":"quarter","type":"capacity","event":"光復二廠新產能量產","impact":"中","watch":"折舊上升速度與良率"},{"date":null,"type":"regulatory","event":"產地標示案起訴與否","impact":"高","watch":"起訴範圍是個人還是公司，有無美國海關動作"},{"date":"2027-01","date_precision":"quarter","type":"other","event":"日本子公司出售給 Meiko 的正式合約","impact":"低","watch":"處分價格與損益"}]}
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
