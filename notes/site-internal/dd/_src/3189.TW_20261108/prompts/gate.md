你是 DD 管線 v20 的判斷層閘（gate），標的 3189.TW（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝12496.25 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）；H1 累計 23,601,219 仟元（MOPS，經 Q1+Q2 加總核對相符）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無單季共識
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝26.1 %｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝1670.31 百萬 TWD（利益率 13.4%）｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）；H1 營業利益 2,569,277 仟元（MOPS）（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi6`（q1_business）｜管理層指引（間接，非公司官方數字）＝Q3/Q4 ABF 與 BT 載板均價各季增約 8%；高盛預期 Q3/Q4 營收各季增約 10%、Q3 毛利率 27–29%｜期間與口徑：Q2 2026 法說後（2026-08）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：高盛引述法說內容（媒體轉載 money.udn.com／wantrich.chinatimes.com），未取得公司法說簡報原文（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 法說後（2026-08））
  - 註記：另一法人預估 Q3 營收 QoQ +12.4%、毛利率 27.3%
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-03 date｜期間與口徑：2026-11-03／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-03）
- `f_peer_3189_tw_operating_margin_pct`（q2_moat）｜3189.TW 營業利益率＝10.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_operating_margin_pct`（q2_moat）｜3037.TW 營業利益率＝13.3 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_8046_tw_operating_margin_pct`（q2_moat）｜8046.TW 營業利益率＝12.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8046.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_4062_t_operating_margin_pct`（q2_moat）｜4062.T 營業利益率＝18.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.4062.T.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_3189_tw_gross_margin_pct`（q2_moat）｜3189.TW 毛利率＝23.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3189.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3037_tw_fcf_margin_pct`（q2_moat）｜3037.TW FCF 利潤率＝1.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3037.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝12.88 TWD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝33.12 TWD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝54228.06 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝83740.87 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（13 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_eps`（q4_capital）｜歸屬淨利／稀釋 EPS＝2.56 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（Win 投資快訊記 2.57）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：查無
- `f_kpi4_ocf_capex`（q4_capital）｜自由現金流（OCF−Capex）＝315.26 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：不適用
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝1.2 %｜期間與口徑：Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt/cashflow（TWD，源自公司合併財報）（SBC 20.17 百萬）；僅供參考，Q1 同欄 455 百萬疑含員工酬勞/分類差異，跨季不可比（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30；董事會通過合併財報 2026-07-31，MOPS））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-5093.65 TWD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 16233.89、現金 21327.54（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝526.9 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.226 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝671.0 TWD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝115.69 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝11.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝11.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.22 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.12 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.43 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝46.76 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.17｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝536.32 TWD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝317.06 TWD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝197.51 TWD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：競爭對手欣興在美系 AI ASIC 載板市占據報導超過 70%，Nvidia Blackwell 相關載板市占超過 30%；Ibiden 被視為欣興在高階 ABF 主要對手
  - 來源：經濟日報 money.udn.com（欣興 ASIC 市占）；工商時報 wantrich 2026-06-25（as_of 2026-06-25）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：114年(2025)客戶A占銷貨淨額19.51%(113年10.72%)、客戶B 9.23%(113年9.79%)、客戶C 5.21%；前三大合計約33.95%，其餘66.05%；皆非關係人，變動原因為配合客戶訂單需求。
  - 來源：公開資訊觀測站電子書件 114年股東會年報 主要銷貨客戶表（as_of 2026-05-08）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：T-Glass 缺料是景碩目前最大營運限制，估計每月 10%~15% 營收受限；Nittobo 獨供 T-glass 預計 2027 年第 3 季才有擴產
  - 來源：景碩 3189 載板需求 搜尋結果（聯合報系／券商整理）（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear、triggers
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：凱基估 2025–28 年全球主要 ABF 載板廠資本支出比上一輪高 51%；景碩 235 億元投資自 2027 年起折舊壓力受關注
  - 來源：KGI PCB sector report 2026-07-20 / 景碩 3189 搜尋結果（as_of 2026-07-20）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：味之素 ABF 增層膜是許多載板廠指定的唯一供應商，市占九成以上；ABF 約占載板原物料成本 25%–30%（產業層面，非景碩專屬揭露）。as_of 為約略值，原文日期未確認。
  - 來源：udn 經濟日報，ABF 載板三雄漲勢吸睛 法人解析成本漲為何帶動股價?（引國泰期貨）（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：玻璃核心基板量產時點說法不一：一份分析報告基準情境為 2030 年量產；2026 年 6 月文章估 2027 年底起大規模導入；GlaSSEM（Samsung Electro-Mechanics 與 Sumitomo Chemical 合資）目標 2027 下半年供貨
  - 來源：AAIG Substack: Glass Core Substrate Sector Research; atlaspcb.com glass core substrate news 2026（as_of 2026-06-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：景碩宣布約196億元專案資本支出（另有報導稱235億元），分三年執行，用於楊梅/幼獅廠新廠房擴 ABF；ABF月產能由約4,000萬顆增至5,000萬顆，新增產能2027年陸續開出；高盛稱目標2029年底前月產能翻倍至8,000萬顆。公司表示196億為專案額度，實際支出視客戶需求彈性調整。
  - 來源：搜尋摘要彙整（含 udn、uanalyze、ctee 報導）；各則確切發布日未能逐一確認（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：同業南電宣布2026年資本支出超過新台幣100億元，聚焦AI/HPC先進載板（二手轉述自 Atlas PCB 引 Taiwan News，2026年5月股東會，未經原始來源查證）。
  - 來源：Atlas PCB news: Nan Ya PCB AI substrate expansion 2026（as_of 2026-05-31）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Counterpoint（2023年7月）：Unimicron、景碩、南電2023Q1表現差，景氣下行比預期更糟，載板谷底可能落在2023Q2或Q3。
  - 來源：Counterpoint Research, ABF substrate demand likely recover H2 2023, BT substrate demand remain weak（as_of 2023-07-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：DigiTimes（2023年11月）：全球IC載板市場2023年預估下滑約30%，ABF需求未如預期回升。
  - 來源：DigiTimes 2023-11-21（as_of 2023-11-21）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：優分析：景碩2023年前三季每股虧損0.7元；2023Q4因子公司晶碩支撐而提早走出谷底；ABF載板Q4營收季增約3成、毛利率由10~15%升至25%（單一來源）。
  - 來源：優分析 uanalyze（as_of 2024-04-01）｜affects：decision_inputs.bear、thesis.R、moat_trend

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1536.0,"bear_5y_price":176.0,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-10.6,"ev5y_pct":-4.8,"irr_base_pct":-2.2,"asym_ratio":1.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":12.88,"pe":52.1,"basis":"FY2026E 共識 EPS，判斷日距年底不到兩個月，視同當年度口徑；終端倍數同樣乘在當年度（FY2031E）EPS 上。路徑 Y1 為 FY2027E，Y5 為 FY2031E。"},"eps":{"bull":[37.0,52.0,60.0,62.0,64.0],"base":[29.0,38.0,40.0,33.0,30.0],"bear":[24.0,20.0,9.0,6.0,11.0]},"pe":{"bull":24,"base":20,"bear":16},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.226,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：景碩 大客戶 第二供應商 OR 轉單 2026；景碩 客戶 自製 OR 分散供應商；3189.TW Kinsus Interconnect Technology largest customer second source OR in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","irr_base_pct":-11.4,"ev5y_pct":-40.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.3,"ev5y_pct":-40.2,"irr_base_pct":-11.4,"max_dd_pct":-88,"bull_5y_price":1550,"bear_5y_price":180,"p_bull_pct":20,"p_bear_pct":35,"rearm_trigger":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","price_at_dd":1060.0,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3189.TW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"景碩科技"},"oneliner":"景碩一個月跌了三成七，FY2027 本益比剩 20 倍，但分母是上一輪高點 2.3 倍的獲利，第三季數字也還沒進證據包。按情境算，現價五年機率加權報酬約 −5%，480 元以下才值得重做研究。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3189.TW_20261108/scenario.json","answers":{"q1_business":{"verdict":"景碩賺的是高階 ABF 與 BT 載板的加工錢，外加晶碩的隱形眼鏡獲利。目前的超額利潤來自短缺，錢卡在上游獨供材料與下游少數大客戶之間。","reasoning":"2026 年第二季合併營收 124.96 億元，毛利率 26.1%，營業利益率 13.4%，其中載板營收 103.82 億元。2025 年第四季產品組合為手機 35%、ABF／HPC 24%、消費與記憶體 18%、隱形眼鏡 18%、基地台 5%。公司口徑的 AI 相關營收 2026 年約 10%，2027 年 15%～20%，市場的 AI 敘事目前只對應一小部分營收。第三季財報已在 11 月 3 日公布，但事實表最新一季仍是第二季，也沒有逐字稿，本判斷不含第三季數字。產業時鐘放在過熱段，依據是稼動率約 95%、部分現貨漲逾 30%、長約客戶同意支付產能相關款項、2025–28 年資本支出比上一輪高 51%，不是股價。單點依賴有三個：最大客戶占 19.51%，味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi6","f_earnings_recency"],"verdict_values":{"revenue_quality":"合併營收混了兩門生意。晶碩 2025 年毛利率 52%，把合併毛利率墊高，也讓部分獲利歸少數股東。Quartr 記上半年淨利 25.6 億元，若全歸母公司，以 EPS 3.74 元換算約 684 百萬股，高於 526.9 百萬股，可見這個數字含少數股權。晶碩持股比例事實表未涵蓋。","unit_econ_note":"事實表沒有每顆載板的單價與出貨量。公司稱第二季毛利改善主要來自稼動率。高盛預期第三、四季 ABF 與 BT 均價各季增約 8%，這是間接轉述，不是公司指引。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"FY2023 營收跌 36.8%，EPS 由 FY2022 的 14.57 元降到 FY2024 的 0.11 元；FY2022 至 FY2024 自由現金流連三年為負，資本支出呈波段式擴張。"},"industry":{"clock_phase":"III","sd_verdict_source":"供需判斷：短缺至少延續到 2027 年，屬週期性，2028 年後反轉的風險隨擴產升高。2028 年缺口的各家估計從 16% 到 51%，差距太大，不能當結構性持久的證據；這些估計也只到 2028 年，沒有涵蓋 2031 年的情境終點。來源多為媒體與部落格二手轉述。","bargaining":{"up":"上游弱勢：味之素 ABF 膜市占九成以上，T-glass 由 Nittobo 獨供，擴產要到 2027 年第三季。","down":"短缺期暫時占優：客戶出資設備、同意產能相關付款。2025 年前三大客戶合計約 34%，最大客戶占比由 10.72% 升到 19.51%。","geo":"台灣、蘇州、美國設廠。美國 232 條款是否涵蓋載板未確認，事實表未涵蓋公司的關稅影響。"},"profit_pool_dir":"事實表未涵蓋利潤池歷史，無法判斷方向。","tam_table":{"expanded":false,"reason":"事實表只有供需缺口百分比，沒有 ABF 市場規模、滲透率與五年前的利潤池，無法組成對照；份額也多是法人轉述或公司目標。"}}}},"q2_moat":{"verdict":"護城河方向為穩定（→）。執行力在進步，定價能力仍靠短缺，份額提升還沒有一手資料證明。","reasoning":"機制是高層數 ABF 的製程良率與客戶認證。有利的證據是法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%、ABF 稼動率由 86% 升到 95%；公司目標 Vera CPU 載板 100%、AI GPU 載板 20%，後兩項尚未實現。不利的證據是欣興在美系 AI ASIC 載板據報超過 70%，Nvidia Blackwell 相關超過 30%。利益率也沒有顯示領先：景碩近四季營業利益率 10.12%，低於欣興 13.30%、南電 12.27%、Ibiden 18.53%，而且景碩的合併數字還含高毛利的隱形眼鏡。欣興與 Ibiden 的資料截至九月，景碩截至六月，可比性有限。同業 ROIC 差距因事實表沒有投入資本而算不出。份額未被一手資料證實前，AI 順風只夠支持繼續追蹤，不支持付溢價。","fact_refs":["f_peer_3189_tw_operating_margin_pct","f_peer_3037_tw_operating_margin_pct","f_peer_8046_tw_operating_margin_pct","f_peer_4062_t_operating_margin_pct","f_peer_3189_tw_gross_margin_pct","f_peer_3037_tw_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"高層數 ABF 的製程良率加上客戶認證；認證通過後份額移動很快，目前的定價能力主要來自全產業短缺。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力改善：第二季毛利率由 21.16% 升到 26.09%，CPU 供貨率據法人升至 50%。定價能力沒有擴大的證據，公司自己把毛利改善歸因於稼動率。前次判斷以來沒有新的份額資料，第三季也未納入，方向維持。","competitor_notes":[{"name":"欣興（3037.TW）","strategy_note":"美系 AI ASIC 載板據報超過 70%，是最強的直接對手；營業利益率高景碩 3.2 個百分點，但自由現金流利潤率僅 1.89%，擴產吃掉了現金。"},{"name":"南電（8046.TW）","strategy_note":"2026 年資本支出據轉述超過 100 億元，聚焦 AI／HPC，是新增供給來源；毛利率 16.04% 低於景碩，營業利益率 12.27% 高於景碩。"},{"name":"Ibiden（4062.T）","strategy_note":"高階 ABF 的主要對手，毛利率 33.41%、營業利益率 18.53%，代表這一行較好的報酬水準；自 FY2027 起陸續新增量產。"}],"threats":[{"level":"🟡","text":"欣興與 Ibiden 在高階 AI 載板份額領先，景碩要從後段搶份額，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🔴","text":"玻璃核心基板最快 2027 年底導入，最晚說法 2030 年。Intel 的設計仍保留 ABF 增層，受衝擊的是核心層；事實表沒有景碩的玻璃基板計畫。","p":"30%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"新產能 2027 年起陸續開出，主要廠商資本支出比上一輪高 51%，短缺結束時競爭會轉為價格戰。","p":"35%","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#2"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟡","text":"AI 加速器與伺服器 CPU 必須用高層數 ABF，延後購買的代價高。但公司口徑 AI 相關營收 2026 年只占約 10%，2027 年 15%～20%，手機、PC 與消費性需求仍弱，其餘八成營收的需求基礎沒有同樣強。"},{"item":"決策層級","level":"🟡","text":"客戶換載板供應商要重新認證。法人稱美系 AI 客戶 CPU 供貨率由 10% 升到 50%，說明認證通過後份額移動很快，份額能移進來也能移出去。認證週期與合約年限事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"上游味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass，下游是少數 AI 大廠並出資鎖設備。景碩夾在中間，公司也把第二季毛利改善歸因於稼動率而非漲價，短缺的好處能留下多少還沒有證據。"},{"item":"社會容忍度","level":"🟢","text":"載板是企業間零組件，沒有消費者漲價壓力或民生監管限制。近 12 個月公平會處分為 0 筆，232 條款是否涵蓋載板則未確認。"}],"roiic":"事實表未涵蓋投入資本，算不出數值。方向上，營業利益由 FY2022 約 96 億元降到 FY2025 約 27 億元，四年自由現金流合計 −65 億元，上一輪投入尚未換回更高獲利。","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，算不出。2026 年資本支出有 80 億元與 140 億元兩種說法，FY2025 歸屬淨利只有 16 億元，再投資需求遠超過現有獲利。","endo_ceiling":null,"formula_note":"當期 ROIC 與內生成長上界都需要投入資本、折舊與營運資金，事實表未涵蓋，不以推估補值。"}}}},"q3_growth":{"verdict":"第五年後的跑道為中等（🟡）：ABF 產能可以翻倍到 2029 年，之後沒有已證實的第二條成長曲線。","reasoning":"成長以價格和稼動率為主，產能為輔。共識 FY2026E 12.88 元、FY2027E 33.12 元，FY2028E 事實表未涵蓋，三年 CAGR 算不出。FY2025A 到 FY2027E 的 EPS 年化 213%，營收年化 46%，兩者的差距是利潤率回升，不是再投資複利，情境樹因此按超出內生上界處理。另一個檢驗：公司口徑 2027 年 AI 占 15%～20%，代入共識營收 837 億元，非 AI 營收約 670～712 億元，比 2026 年約 488 億元增加 37%～46%，而手機與 PC 需求仍弱，這段成長大多要靠漲價。可能看錯的地方是公司的 AI 定義或許不含伺服器 CPU，若是如此，量的貢獻會比這裡高。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"FY2027 以價格與稼動率為主。2027 年起 ABF 月產能由約 4,000 萬顆增至 5,000 萬顆，2029 年底目標 8,000 萬顆，是量的來源。併購與回購沒有貢獻。","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表沒有投入資本、折舊與營運資金，內生上界算不出，不填數字。共識 EPS 年化 213% 遠高於營收年化 46%，差距歸因於利潤率擴張，按超出內生上界處理。","segments":[{"item":"手機應用（2025 年第四季）","value":"35%"},{"item":"ABF／HPC（2025 年第四季）","value":"24%"},{"item":"消費性電子與記憶體（2025 年第四季）","value":"18%"},{"item":"隱形眼鏡（2025 年第四季）","value":"18%，2025 年毛利率 52%"},{"item":"基地台（2025 年第四季）","value":"5%"},{"item":"AI 相關營收占比（公司口徑）","value":"2026 年約 10%，2027 年 15%～20%"}],"decay_signals":["亮燈：EPS 增速遠高於營收增速，FY2025A 到 FY2027E 年化 213% 對 46%。","未亮但要看：FY2025 毛利率 21.13%，低於 FY2024 的 28.39%，2026 年第二季已回到 26.1%；去年同季數字事實表未涵蓋，連兩季年減無法確認。","未亮：FY2025 自由現金流為淨利的 1.07 倍；FY2024 為負值，但不是連兩年。","未亮：第二季 SBC 占營收 0.16%。","資料缺口：維護性資本支出比重、產業倍數三年走勢事實表未涵蓋。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置尚未被證明：上一輪四年自由現金流合計 −65 億元，這一輪又要投入 196～235 億元，而淨現金只有 51 億元。","reasoning":"FY2025 自由現金流 17.1 億元，是歸屬淨利 16.0 億元的 1.07 倍，但 FY2022 至 FY2024 連三年為負。第二季自由現金流 3.15 億元。第二季 SBC 占營收 0.16%，占營業利益 1.2%；第一季同欄 4.55 億元疑含員工酬勞，跨季不可比。現金去向四分與債務到期結構事實表未涵蓋。總債務 162 億元、現金 213 億元，相對三年專案偏薄；若計入到 2029 年總規模 600～800 億元（設備由客戶出資），未來幾年要靠獲利兌現或對外籌資。流通股數 526.9 百萬股比 FY2025 由淨利與 EPS 推得的 473 百萬股多 11%，事實表沒有說明是增資、轉換或資料口徑差異。","fact_refs":["f_kpi3_eps","f_kpi4_ocf_capex","f_kpi5_sbc","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月重大訊息與搜尋都沒有併購事項，無從計算已實現報酬。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄與均價。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 合計約 4.75 億元，年化約 9.5 億元，占市值約 0.27%，低於 1.5%。股數比 FY2025 多 11% 的原因未說明，不計入這項。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月重大訊息沒有併購事項；事實表也沒有近三年股利、回購與現金去向分項。"}}}},"q5_valuation":{"verdict":"671 元要划算，33.12 元的 FY2027 共識就不能是高點，2031 年還要維持 33 元以上的 EPS 與 20 倍本益比。我相信 2027 年大幅成長，不相信這個獲利水準能不經下行就延續。","reasoning":"FY2027E 共識隱含歸屬淨利約 174.5 億元（33.12 元乘 526.9 百萬股），占共識營收 20.8%，高於 FY2022 高點的 16.4%。Base 用 FY2031E 30 元乘 20 倍得 600 元，低於現價。短期目標以 FY2027 Base 29 元乘 21 倍得 609 元，中期以 FY2028 Base 38 元乘 18 倍得 684 元。成長熄火測試用 FY2029 Base 40 元：成長降到 15% 給 22 倍得 880 元；降到 10% 給 16 倍得 640 元；降到 5% 給 12 倍得 480 元，三種情況只有第一種高於現價。賣方目標價 FactSet 620 元（6 月）、Investing.com 868～892 元（日期偏舊），最高 1,250 元與最低 450 元相差 2.8 倍，共識不穩，不作為支持依據。同業本益比事實表未涵蓋，終端倍數無法附同業對照，只能對照自身 FY2027E 的 20.3 倍；循環股優先看的股價淨值比也因缺淨值而無法使用。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_rev_consensus_fy2_m","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"本益比，以 FY2027E 共識為主、FY2026E 為輔；循環股本應優先看股價淨值比，但事實表未涵蓋淨值。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或目標價，無法建立倍數對照。"},"fwd_pe":52.1,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價對 FY2026E 是 52.1 倍，對 FY2027E 是 20.3 倍。Base 年化報酬約 −2%，機率加權五年約 −5%，多空報酬比約 1.0，比前次好很多，但仍沒有補償循環風險，所以落在偏貴這一檔，未到最貴。五年分位事實表未涵蓋，只有四個年度端點：本益比第 11.2 百分位因 FY2023、FY2024 EPS 接近零而失真，P/S 與 EV/S 都在最高。三年 PEG 因 FY2028E 共識缺漏算不出；用 FY2025A 低基期算得 0.24，沒有意義；改用 FY2022 高點到 FY2027E 的年化 17.8% 算，約 1.1 倍。","upside_short_pct":-9.2,"upside_mid_pct":1.9,"denominator_disputed":true,"denominator_note":"20.3 倍的分母 33.12 元是上一輪高點 14.57 元的 2.3 倍，隱含歸屬淨利率高於 FY2022。分母是否為景氣高點正是爭點，本益比看起來便宜不能當買進理由。另外 P/S 7.22 倍隱含近四季營收約 490 億元，比截至第二季的約 448 億元多，來源未說明；EV 也沒有計入少數股權。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方有兩個：第三季數字和股價大跌的原因都不在證據包裡；短缺若延續過 2028 年，基準情境就偏低。","reasoning":"股價由前次 1,060 元跌到 671 元，RSI 28.17，26 週報酬仍有 +46.76%，股價也還在 52 週均線 536 元之上。下跌原因無法判斷，所以跌幅不當作安全邊際。這家公司沒有可守的核心：FY2022 至 FY2024 自由現金流連三年為負，FY2023、FY2024 EPS 接近零，應按循環交易紀律處理，不用長抱的波動容忍。價值陷阱風險中等，亮燈的衰退訊號只有 EPS 增速遠高於營收增速一項，但這項正是爭點。附錄的品質分只反映 AI 不會取代載板製程，不代表獲利品質。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_earnings_recency"],"verdict_values":{"trap":{"verdict":"🟡","label":"高點獲利被當成新基期"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":12.88,"pe":52.1,"basis":"FY2026E 共識 EPS，判斷日距年底不到兩個月，視同當年度口徑；終端倍數同樣乘在當年度（FY2031E）EPS 上。路徑 Y1 為 FY2027E，Y5 為 FY2031E。"},"eps":{"bull":[37.0,52.0,60.0,62.0,64.0],"base":[29.0,38.0,40.0,33.0,30.0],"bear":[24.0,20.0,9.0,6.0,11.0]},"pe":{"bull":24,"base":20,"bear":16},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.226,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-80,"hi":-55,"basis":"事實表未涵蓋歷史最大回撤，改用三個價位推：到 104 週均線 317 元約 −53%，到 250 週均線 198 元約 −71%，Bear 終值 176 元約 −74%。上一輪基本面跌幅為 FY2023 營收 −36.8%、EPS 由 14.57 元降到 0.10 元，支持深回撤範圍。","trigger_time":null},"basis":{"bull":"ABF 短缺延續過 2028 年，AI GPU 份額達 20%，月產能 8,000 萬顆被長約填滿。FY2031E 營收約 1,600 億元、歸屬淨利率約 21%，沒有明顯下行；24 倍代表市場不再以循環股看待。","base":"2027 年受 T-glass 限料與新折舊影響，EPS 29 元低於共識；2028–29 年達高點約 40 元，2030 年起新產能使報價回落。FY2031E 營收約 1,200 億元、歸屬淨利率約 13.5%，屬中段水準；20 倍接近目前 FY2027E 的 20.3 倍。同業本益比事實表未涵蓋。","bear":"新產能與 AI 需求消化同時發生，重演 2023 年：報價下跌、稼動率低於 80%，新廠折舊落在低收入上，FY2030E 跌到 6 元，FY2031E 回到 11 元；16 倍來自成長降到 10% 的本益比。機率 35%，不採信多年短缺可延續到終端年，因為各家預估只到 2028 年，且 2028 年缺口預估從 16% 到 51%。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY2023 營收跌 36.8%，EPS 由 14.57 元降到 0.10 元，2023 年前三季每股虧 0.7 元。這一輪主要廠商資本支出比上一輪高 51%，景碩新廠折舊從 2027 年起進損益，同業也在擴產。","assumption":"AI 需求在 2028–29 年持續吸收全產業新增產能。","consequence":"FY2030E EPS 跌到個位數，股價落到 104 週均線以下，五年虧損超過 50%。","ruling":"採納，列為 Bear 35%。與 Single Thing 的機制相同；Single Thing 抓報價第一次轉跌的時點，這裡補上折舊與客戶去庫存的放大效果。","watch":"ABF 稼動率、ABF 季均價、2027 年資本支出。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","supply_demand_durability#5"]},{"view":"論點成功但股東經濟變差","evidence":"味之素 ABF 膜市占九成以上，Nittobo 獨供 T-glass，限料每月影響 10%～15% 營收；最大客戶占比由 10.72% 升到 19.51%，客戶出資設備。","assumption":"短缺帶來的漲價大部分留在景碩。","consequence":"營收與產能都達標，但毛利率停在 30% 左右，新產能被客戶鎖定，現金大多再投入，每股盈餘低於 Base。","ruling":"部分採納。公司把第二季毛利改善歸因於稼動率，漲價的留存比例還沒有證據，列為中期風險。","watch":"ABF 報價上漲期間的合併毛利率變化、股本變動。","evidence_refs":["geo_supply_chain#1","supply_demand_durability#2","customer_concentration_credit#0"]},{"view":"價格已反映太多","evidence":"現價為 FY2027E 的 20.3 倍，共識隱含歸屬淨利率 20.8%，高於 FY2022 的 16.4%；EV/S 7.12 倍為四個年度端點最高；欣興在 AI ASIC 份額超過 70%，景碩的份額目標尚未實現。","assumption":"FY2027E 是新的獲利基期。","consequence":"Base 年化約 −2%，多空報酬比約 1.0，上漲空間補償不了循環風險。","ruling":"採納。下跌 36.7% 改善了報酬，但還不足以進場。","watch":"FY2027 共識 EPS、合併毛利率。","evidence_refs":["competitive_share_entrants#2"]},{"view":"論點失敗","evidence":"最近一次財報日是 11 月 3 日，事實表最新一季仍是第二季，也沒有逐字稿；同期股價由 1,060 元跌到 671 元，原因不在證據包內。","assumption":"FY2027 共識 33.12 元已反映第三季與最新展望。","consequence":"若第三季或展望轉弱，三條路徑都要下修；若第三季優於預期，本判斷偏保守。","ruling":"不可裁決至第三季財報與法說內容納入，在那之前不買進、不加碼。","watch":"第三季合併毛利率、營收季增率、法說對 2027 年報價的說法。","fact_refs":["f_earnings_recency","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1060.0 → 本次 671.0（-36.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1060.0","side_b":"本次 price_at_dd=671.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,060 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,060 元：Bull 價 1,550、Bear 價 180，五年期望值 −40.2%，基準年化 −11.4%，不對稱比 0.3","side_b":"本次情境、股價仍用 1,060 元：Bull 價 1,536、Bear 價 176，五年期望值 −39.7%，基準年化 −10.8%，不對稱比 0.31","ruling":"先換情境、股價不動：五年期望值多 0.5 個百分點，基準年化多 0.6 個百分點。不對稱比由 0.3 變為 0.31。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,060 元：五年期望值 −39.7%，基準年化 −10.8%，不對稱比 0.31","side_b":"本次情境、股價 671 元：五年期望值 −4.8%，基準年化 −2.2%，不對稱比 1.0","ruling":"再換股價、情境不動：起點價下跌 36.7%，五年期望值多 34.9 個百分點，基準年化多 8.5 個百分點，不對稱比由 0.31 升到 1.0。合計五年期望值比前份多 35.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識上修與股價大跌方向相反","cause":null,"prior_field":null,"side_a":"FY2027 共識 EPS 由前次 28.11 元升到 33.12 元，上修 17.8%。","side_b":"股價由 1,060 元跌到 671 元，跌 36.7%，RSI 28.17。","ruling":"證據包沒有第三季數字，也沒有下跌原因，不可裁決至第三季財報納入；在那之前不把跌幅當作便宜的理由。","evidence_level":"低","settle_metric":"2026 年第三季合併毛利率與營收季增率","if_then":["若第三季毛利率 ≥27% 且營收季增 ≥10%：情境不變，股價 ≤480 元才分批反買。","若第三季毛利率 <27% 或 FY2027 共識 EPS 下修超過一成：下修 Base 路徑，不追。"],"evidence_refs":[]},{"axis":"AI 敘事與 AI 營收占比","cause":null,"prior_field":null,"side_a":"賣方把景碩定位為 AI 供應商，FY2027 共識營收 837 億元，年增約 54%。","side_b":"公司口徑 2027 年 AI 相關營收只占 15%～20%，手機、PC 與消費性需求仍弱。","ruling":"兩者要同時成立，非 AI 營收須增加 37%～46%，大部分只能來自漲價，所以 FY2027 的成長屬價格驅動。可能看錯的地方是公司的 AI 定義或許不含伺服器 CPU。","evidence_level":"中","settle_metric":"法說會 AI 營收定義與 2027 年實際占比","if_then":["若 AI 定義已含伺服器 CPU 且 2027 年占比仍低於 20%：維持價格驅動的判斷，不追。","若定義不含 CPU 且含 CPU 後占比超過 40%：上調 Base 的量，重做研究。"],"evidence_refs":[]},{"axis":"多年短缺與擴產潮","cause":null,"prior_field":null,"side_a":"高盛估 ABF 缺口 2026 下半年、2027、2028 年為 14%、34%、51%；真空壓膜機交期排到 2031 年。","side_b":"另一外資估 2026–28 年缺口只有 4%、10%、16%；主要廠商資本支出比上一輪高 51%，景碩、欣興、南電、Ibiden 都在擴產。","ruling":"採信 2027 年仍短缺，不採信可延續到 2031 年。差距屬程度與時點，可以調和：短缺到 2028 年，之後新產能壓低報價。","evidence_level":"中","settle_metric":"ABF 稼動率與 ABF 季均價","if_then":["若 2027 年底稼動率仍 ≥90% 且報價續漲：Bull 機率上調到 30%，重做研究。","若稼動率低於 85% 或報價季減：減碼，已無持股則不進場。"],"evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：同業普遍擴產，未見明確的產能紀律聲明。","side_b":"結構：缺口預估在 2027–28 年擴大，客戶出資鎖產能。其他變數：玻璃核心 2027–2030 年導入，232 條款涵蓋與否未確認。","ruling":"雙向拉鋸。短期結構轉好，2028 年後競爭惡化的機率上升。","evidence_level":"中","settle_metric":"稼動率與 ABF 季均價","if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#2","substitute_technology#1"]},{"axis":"載板毛利率的資料衝突","cause":null,"prior_field":null,"side_a":"財報第二季合併毛利率 26.1%。","side_b":"Quartr 摘要一處寫合併毛利率 12.7%，另一處寫載板毛利率 14%～15%。","ruling":"合併數字採財報，12.7% 不採用。以合併毛利約 32.6 億元、非載板營收 21.1 億元按 2025 年晶碩毛利率 52% 粗算，載板毛利率約 20.8%，與 14%～15% 對不上，載板毛利率先視為未確認。","evidence_level":"低","settle_metric":"公司法說簡報的分部毛利率","if_then":[],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價一個月跌 36.7%，RSI 28.17，FY2027 本益比 20.3 倍；共識還在上修，設備交期排到 2031 年會拖慢新產能。若短缺延續過 2028 年，Base 的 FY2031E 30 元明顯偏低。","side_b":"跌幅不等於安全邊際。賣方共識的問題在成長基準：FY2027 獲利被當成往後的起點，沒有算進一次下行；12 位分析師全部買進，目標價最高與最低相差 2.8 倍。","ruling":"不採納，但保留反向條件。Base 機率不變時，Bull 機率要由 20% 升到約 35%，五年機率加權報酬才有 25%；目前沒有足以支持這個調整的一手證據。","evidence_level":"中","settle_metric":"FY2027 合併毛利率與 ABF 均價連續性","if_then":["若 ABF 均價連四季上漲且 FY2027 毛利率 ≥33%：Bull 機率上調到 30% 以上，重做研究，不等 480 元。","若股價續漲但第三季數字仍未驗證：不追。"],"evidence_refs":[]},{"axis":"估值結論與路徑風險隨股價調整","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前次股價 1,060 元，對 FY2027 共識 28.11 元是 37.7 倍，估值為最貴一檔，最大回撤估 −88%，多空機率 20％與 35％。","side_b":"現價 671 元，對 FY2027 共識 33.12 元是 20.3 倍，估值降一檔，回撤範圍改為 −55% 到 −80%，多空機率維持 20％與 35％。","ruling":"變化主要來自股價，機率不因股價改變。報酬仍不足，維持不進場的結論。","evidence_level":"高","settle_metric":"股價與 FY2027 共識 EPS","if_then":["若股價 ≤480 元且共識 EPS ≥28 元：重做研究，通過後分批反買。","若股價回到 900 元以上而第三季數字未驗證：不追。"],"evidence_refs":[]},{"axis":"基本面欄位維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前次：訊號評等 C、價值陷阱中等、護城河方向穩定、五年後跑道中等、循環股、晚循環。","side_b":"本次新增的證據只有 FY2027 共識上修 17.8%，第三季財報未納入，份額與擴產資料都是前次已有。","ruling":"六欄都不動。共識上修不足以改變循環位置，晚循環的依據是稼動率、報價與擴產，都沒有變化。","evidence_level":"中","settle_metric":"第三季財報與下一次法說","if_then":["若第三季顯示稼動率低於 90% 或報價停漲：循環位置改為過熱頂部，不追。","若第三季毛利率超過 29% 且 2027 年長約比重揭露：護城河定價分上調，重做研究。"],"evidence_refs":[]},{"axis":"估值rearm 進場門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價 ≤600 元（約 FY2027 共識 EPS 的 21 倍），且 FY2027 共識 EPS 未較 28.11 元下修逾一成","side_b":"股價 ≤480 元（約 FY2027 共識 EPS 的 14.5 倍），且 FY2027 共識 EPS 不低於 28 元；觸發後先重做研究","ruling":"舊方法是倍數乘共識，照舊用 21 倍乘新共識得 695 元，現價已符合，等於共識上修就自動放行，而分母是否為高點正是爭點。新門檻改用報酬法：600 元時多空報酬比約 1.3，480 元時約 2.0。這是股價接近舊門檻時才改的，有移動門檻的疑慮，下次複審要記錄：若未到 480 元就反轉上漲，這次改動錯過了多少。","evidence_level":"中","settle_metric":"480 元門檻是否觸發及之後的報酬","if_then":["若股價 ≤480 元且共識 EPS ≥28 元：重做研究，通過後分批反買。","若第三季與 2027 年指引上調 Base 路徑：按新路徑重算門檻，不沿用 480 元。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，沒有舊門檻原文可比。","side_b":"合併季毛利率連兩季季減且低於 24%；FY2027 共識 EPS 低於 23.2 元；ABF 稼動率低於 85%；ABF 季均價出現季減。","ruling":"本次新設減碼與清倉門檻，對應毛利率、共識、稼動率與報價四個指標。","evidence_level":"中","settle_metric":"季報與共識追蹤","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，沒有原文可比。","side_b":"2028 年底前，ABF 載板平均售價出現第一次季減。","ruling":"選報價，是因為它是獲利最大的單一敏感度，比 T-glass 限料或客戶流失的影響更大。","evidence_level":"中","settle_metric":"法說報價說明與合併毛利率","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"把 11 月 3 日公布的第三季財報納入，重新核對毛利率與營收。","type":"假設驗證","maps_to":"H1","metric":"2026 年第三季合併毛利率與營收季增率","threshold":"毛利率低於 27% 或營收季增低於 10%","action":"不追，並下修基準路徑","source_freq":"MOPS 季報，每季","date":"2026-11-30","evidence_refs":[]},{"n":2,"text":"股價跌到足以補償循環風險的價位，共識也沒有崩。","type":"估值rearm","maps_to":"H1","metric":"股價與 FY2027 共識 EPS","threshold":"股價 ≤480 元且共識 EPS ≥28 元","action":"重做研究，通過後分批反買","source_freq":"每日收盤，每月共識","date":null,"evidence_refs":[]},{"n":3,"text":"T-glass 與材料短缺壓住出貨。","type":"風險","maps_to":"R1","metric":"單季營收季增率","threshold":"連兩季低於 5%","action":"不追","source_freq":"月營收與季報","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":4,"text":"ABF 報價第一次轉跌。","type":"Single Thing","maps_to":"H1","metric":"ABF 載板季均價","threshold":"2028 年底前出現季減","action":"減碼","source_freq":"法說與法人報價調查，每季","date":"2028-12-31","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0"]},{"n":5,"text":"擴產開出後稼動率回落。","type":"風險","maps_to":"R2","metric":"ABF 稼動率","threshold":"低於 85%","action":"減碼","source_freq":"法說與法人轉述，每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"n":6,"text":"客戶集中度進一步升高，或 AI GPU 份額沒有到位。","type":"風險","maps_to":"R3","metric":"最大客戶占比與 AI GPU 載板份額","threshold":"最大客戶超過 30%，或 2027 年底 AI GPU 份額低於 10%","action":"停止加碼","source_freq":"年報與法人調查，每年","date":null,"evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"n":7,"text":"玻璃核心進入主要 AI 客戶量產。","type":"風險","maps_to":"R5","metric":"玻璃核心量產導入與景碩方案","threshold":"前三大 AI 客戶有一家宣布量產，且公司仍無相應方案","action":"停止加碼","source_freq":"產業新聞與法說，每季","date":null,"evidence_refs":["substitute_technology#1"]},{"n":8,"text":"共識大幅下修，毛利率同時走弱。","type":"清倉","maps_to":"H1","metric":"FY2027 共識 EPS 與合併季毛利率","threshold":"共識 EPS 低於 23.2 元，且毛利率連兩季季減","action":"清倉","source_freq":"每月共識與季報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"n":9,"text":"AI 相關營收與產能進度驗證。","type":"假設驗證","maps_to":"H2","metric":"AI 相關營收占比與 ABF 月產能","threshold":"2027 年 AI 占比低於 15%，或月產能未達 5,000 萬顆","action":"不追","source_freq":"法說與年報，每半年","date":"2027-12-31","evidence_refs":[]},{"n":10,"text":"全年財報與 2027 年資本支出說明出爐，複審情境與 480 元門檻。","type":"複審日期","maps_to":"H1","metric":"FY2026 財報與 2027 年資本支出","threshold":"到期複審","action":"重做研究","source_freq":"年報與法說","date":"2027-03-31","evidence_refs":[]}],"kill_metrics":[{"metric":"合併季毛利率","bear_threshold":"連兩季季減且低於 24%","window":"未來 4 季","source":"MOPS 季報","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 23.2 元（較 33.12 元下修三成）","window":"未來 12 個月","source":"yfinance earnings_estimate","last_status":"ok"},{"metric":"ABF 稼動率","bear_threshold":"低於 85%","window":"未來 8 季","source":"法說會與法人轉述","last_status":"ok"},{"metric":"ABF 載板季均價","bear_threshold":"出現季減","window":"至 2028 年底","source":"法說與法人報價調查","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"股價 ≤480 元（約 FY2027 共識 EPS 的 14.5 倍），且 FY2027 共識 EPS 不低於 28 元；觸發後先重做研究","exec_line":"現價不追。第三季財報納入前不買進。股價 ≤480 元且 FY2027 共識 EPS ≥28 元時先重做研究，通過後分兩批建立，合計不超過總資金 3%。","holding_cap":"不超過總資金 3%"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤480 元，且第三季財報納入後 FY2027 共識 EPS 不低於 28 元。","prior_verdict":"觀望","prior_role":"追蹤"},"thesis":{"H":[{"id":"H1","text":"2027 年短缺仍在，ABF 與 BT 報價加上稼動率，能把合併毛利率推到上一輪高點的九成。","2y":"FY2027 合併毛利率 ≥33%，歸屬 EPS ≥29 元。","5y":null,"10y":null,"threshold":"FY2027 合併毛利率 ≥33%；FY2027 EPS ≥29 元","source":"MOPS 季報、法說會；以 FY2022 毛利率 37.02% 為對照","drift_rule":"以近四季比對，連兩季偏離 ≥5% 視為削弱，連三季偏離 ≥10% 視為反轉"},{"id":"H2","text":"公司把 CPU 載板的認證優勢擴到 AI GPU 與 ASIC，新增產能在客戶出資與長約下被填滿。","2y":null,"5y":"2029 年底 ABF 月產能至少 7,200 萬顆，稼動率 ≥80%。","10y":null,"threshold":"2027 年 AI 相關營收占比 ≥15%；2029 年底 ABF 月產能 ≥7,200 萬顆且稼動率 ≥80%","source":"法說會、年報、法人份額調查","drift_rule":"連四季落後門檻 ≥5% 視為削弱，連六季落後 ≥10% 視為反轉"},{"id":"H3","text":"下一輪下行時，谷底獲利要明顯高於上一輪，才能證明這不只是一段短缺行情。","2y":null,"5y":"下一個谷底年度營業利益率 ≥8%，全循環自由現金流合計為正。","10y":null,"threshold":"谷底年度營業利益率 ≥8%（FY2023 為 3.95%，FY2024 為 3.43%）","source":"年度財報","drift_rule":"連四季偏離 ≥5% 視為削弱，連六季偏離 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"T-glass 由 Nittobo 獨供，擴產要到 2027 年第三季，限料壓住每月 10%～15% 營收。","h_ref":"H1","clock":"⚡","threshold":"單季營收季增率連兩季低於 5%","evidence_refs":["supply_demand_durability#2"]},{"id":"R2","text":"全產業擴產在 2027–29 年開出，新廠折舊落在回落的報價上，重演 2023 年下行。","h_ref":"H1","clock":"🔥","threshold":"ABF 稼動率低於 85% 或季均價季減","evidence_refs":["supply_demand_durability#5","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"客戶集中度升高，欣興與 Ibiden 在高階 AI 載板領先，份額目標可能落空。","h_ref":"H2","clock":"🔥","threshold":"最大客戶占比超過 30%，或 2027 年底 AI GPU 份額低於 10%","evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"id":"R4","text":"味之素等上游獨供廠商分走短缺的利潤，景碩漲價留不住。","h_ref":"H1","clock":"🔥","threshold":"ABF 報價上漲期間，合併毛利率連兩季季減","evidence_refs":["geo_supply_chain#1"]},{"id":"R5","text":"玻璃核心基板導入後，核心層價值轉移，景碩沒有可見的對應方案。","h_ref":"H3","clock":"🐢","threshold":"前三大 AI 客戶有一家宣布量產，且公司仍無相應方案","evidence_refs":["substitute_technology#1"]}],"single_thing":{"description":"2028 年底前，ABF 載板平均售價出現第一次季減。","why_fatal":"這是獲利最大的單一敏感度。FY2027 共識營收 837 億元，均價少 10% 相當於稅前少約 84 億元，每股約 15.9 元，占 33.12 元的 48%，而成本不會同步下降。這是以全部合併營收粗算，隱形眼鏡不隨載板報價變動，實際影響略低。","if_happens":"景氣轉折獲得確認，共識 EPS 開始下修，本益比同步壓縮，走向 Bear 路徑，FY2030E EPS 可能回到個位數。","how_monitor":"每季法說的報價說明、法人報價調查、合併毛利率季變化，以及欣興與 Ibiden 對稼動率的說法。","probability":"約 35%（未來 24 個月左右）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":20.26,"peg_fy2":0.13,"stress":{"pass":1,"total":3},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-08）"},"eps_meta":{"base_eps_path":{"FY2025A":3.37,"FY2026E":12.88,"FY2027E":33.12,"FY2028E":null},"fy_end_month":12,"eps_basis":"歸屬母公司稀釋 EPS；FY2026E、FY2027E 為 yfinance 共識平均，FY2028E 事實表未涵蓋。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報（11 月 3 日公布）與法說內容納入研究","impact":"高","watch":"合併毛利率是否落在 27%～29%，營收季增是否 ≥10%"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 全年財報與 2027 年資本支出說明","impact":"高","watch":"資本支出 80 億元與 140 億元兩種說法何者成立，新廠折舊時點"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"Nittobo T-glass 擴產開始貢獻","impact":"高","watch":"限料緩解後，景碩營收是否加速，報價是否鬆動"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"楊梅與幼獅新廠 ABF 產能陸續開出，月產能往 5,000 萬顆","impact":"高","watch":"新產能稼動率與折舊對毛利率的影響"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"玻璃核心基板供應商目標開始供貨","impact":"中","watch":"主要 AI 客戶是否導入，景碩有沒有對應方案"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=46.76, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
