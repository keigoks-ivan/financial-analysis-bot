你是 DD 管線 v20 的判斷層閘（gate），標的 AMKR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（49 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝1991 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查證
- `f_kpi1_gross_margin`（q1_business）｜Gross margin＝18.3 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查證
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝224.7 百萬美元（利益率 11.3%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查證
- `f_kpi3_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝—｜期間與口徑：Q3 2026（公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿：公司不揭露 non-GAAP 營業利益，僅揭露 EBITDA $435M（Q2 $400M、Q3 2025 $340M）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（公告於 2026-10-26））
  - 註記：n/a
- `f_kpi4_diluted_eps_gaap`（q1_business）｜Diluted EPS (GAAP)＝0.76 美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-26））
  - 註記：未查證
- `f_kpi6_management_guidance_q4_2`（q1_business）｜Management guidance Q4 2026＝營收 $1.9–2.0B；毛利率 18.0–19.0%；淨利 $160–185M；EPS $0.65–0.75；營業費用約 $140M；全年 capex 約 $2.5B｜期間與口徑：Q4 2026 指引（公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿＋Q3 2026 法說會逐字稿（numbers.latest_quarter_kpis.items[6]，as_of Q4 2026 指引（公告於 2026-10-26））
  - 註記：FY1 EPS 共識 2.50（dd_numbers_extra consensus_revision，2026-10-31 快照）；Q4 單季共識未查證
- `f_kpi7_advanced_products`（q1_business）｜Advanced products 營收＝1632 百萬美元（占 82.0%）｜期間與口徑：Q3 2026（公告於 2026-10-26）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.amkor.com Q3 2026 press release（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（公告於 2026-10-26））
  - 註記：n/a
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-45.95 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_peer_amkr_gross_margin_pct`（q2_moat）｜AMKR 毛利率＝16.56 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amkr_operating_margin_pct`（q2_moat）｜AMKR 營業利益率＝9.51 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amkr_fcf_margin_pct`（q2_moat）｜AMKR FCF 利潤率＝-2.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3711_tw_gross_margin_pct`（q2_moat）｜3711.TW 毛利率＝20.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3711_tw_operating_margin_pct`（q2_moat）｜3711.TW 營業利益率＝11.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3711_tw_fcf_margin_pct`（q2_moat）｜3711.TW FCF 利潤率＝-11.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_6239_tw_gross_margin_pct`（q2_moat）｜6239.TW 毛利率＝19.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6239.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6239_tw_operating_margin_pct`（q2_moat）｜6239.TW 營業利益率＝12.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6239.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_gross_margin_pct`（q2_moat）｜2449.TW 毛利率＝38.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_operating_margin_pct`（q2_moat）｜2449.TW 營業利益率＝26.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_fcf_margin_pct`（q2_moat）｜2449.TW FCF 利潤率＝-32.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_600584_ss_gross_margin_pct`（q2_moat）｜600584.SS 毛利率＝15.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600584.SS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_600584_ss_operating_margin_pct`（q2_moat）｜600584.SS 營業利益率＝7.15 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600584.SS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_600584_ss_fcf_margin_pct`（q2_moat）｜600584.SS FCF 利潤率＝-13.54 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600584.SS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.5 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝247.81 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.78 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.26 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝7528.43 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝8593.11 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-2.72 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 2.57 → 2.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_free_cash_flow_pp_e`（q4_capital）｜Free cash flow（前九個月，營業現金流減 PP&E 付款，自行計算）＝-368.5 百萬美元｜期間與口徑：2026 年前九個月（截至 2026-09-30，公告於 2026-10-26）；公司未揭露單季 FCF／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿現金流量表：營業現金流 $868.3M、PP&E 付款 $1,236.8M（numbers.latest_quarter_kpis.items[5]，as_of 2026 年前九個月（截至 2026-09-30，公告於 2026-10-26）；公司未揭露單季 FCF）
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝336.08 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 2712.28、現金 2376.2（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.878 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝9812.34 USD m｜期間與口徑：2026-11-03／市值 9476.26 ＋ 淨負債 336.08｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝38.25 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.3 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 2.5，分子＝快照價 38.24｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝15.42 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝35.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝35.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.27 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝54.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝54.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.32 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝53.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝53.9 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.3 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.5 → 2.5）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.78 → 2.78）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.67｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 38.07 / W52 53.61 / W104 38.33 / W250 30.57 / W250 13週斜率 0.92%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝53.61 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝38.33 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝30.57 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出外包封測市場競爭激烈，地緣政治貿易緊張提高了中國業者（中國供中國）的競爭；主要對手為 ASE、JCET、Powertech，另有晶圓代工與 EMS 提供部分先進封裝，IDM 客戶亦評估自家產能。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Competition（as_of 2026-02-20）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：前十大客戶占 2025 年淨銷售 72%；亦可能面對受中國政府支持、資金成本較低的本地業者競爭，客戶可能轉用內部、晶圓代工或合約製造商。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Apple 占 2025 年淨銷售 29.8%、Qualcomm 11.1%，前十大客戶合計 72%；IDM 客戶會拿 Amkor 服務與自家 in-house 能力比較。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素載明 IDM 與晶圓代工客戶可能隨時把外包封測轉回自有產能。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：thesis.R、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前十大客戶占淨銷售 72%；Apple 直接銷售占 29.8%、Qualcomm 11.1%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：公司風險因子自述：失去大客戶、客戶合併、訂單或價格下降可能對業務、流動性與財務產生重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce: TSMC CoWoS supply-demand gap reportedly narrowing from ~20% to ~10% by end-2026 as capacity expands; further improvement likely in 2027.
  - 來源：TrendForce News 2026-06-15（as_of 2026-06-15）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Amkor consumer/Android weakness: Android revenue declined 20% in Q2; Q3 outlook affected by SiP migration to Vietnam, memory supply constraints and customer build changes.
  - 來源：Zacks/Nasdaq Amkor earnings call summaries（as_of 2026-08-01）｜affects：thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素列出出口管制（BIS 規則）限制對部分中國公司銷售，屬產業特定貿易監管。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：Amkor 在中國、日韓、馬來西亞、菲律賓、葡萄牙、新加坡、台灣、越南設廠，客戶與供應商多在美國境外；公司稱美中關係與貿易政策變動、關稅、出口管制已對並可能持續對業務造成不利影響；BIS 規則限制先進運算晶片與設備出口中國，部分非美國競爭對手可能豁免。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 稱 2025 年美國多次宣布關稅與出口管制變動，多數後來暫停或修訂；公司無法預測後續行動，關稅可能影響終端需求而不利於公司。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 競爭段：地緣貿易緊張提高了支援中國在地供應鏈的中國同業競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-20）｜affects：moat_trend
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Amkor 封測廠分布於中國、日本、韓國、馬來西亞、菲律賓、葡萄牙、新加坡、台灣、越南，亞洲為主；美國亞利桑那廠仍在興建中
  - 來源：Amkor Form 10-Q (Q1 2026)（as_of 2026-03-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 指出幾乎所有不動產、廠房與設備位於美國以外，並列示地緣緊張、保護主義導致出口限制與關稅
  - 來源：Amkor Form 10-K FY2025（搜尋摘要轉述）（as_of 2026-02-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因素：中國營運風險因美中關係與貿易政策而可能升高
  - 來源：Amkor Form 10-K FY2023（as_of 2024-02-28）｜affects：thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 發布前市場共識約 Q3 $2.04B、Q4 $2.05B；Q4 guidance 區間 $1.9–2.0B 低於該共識（搜尋摘要轉述，未核原文）
  - 來源：WebSearch 摘要（finviz/Business Wire 等）（as_of 2026-10-26）｜affects：valuation、decision_inputs.bear
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：ASE 2026 為最積極的建廠年，全球六座新封測廠同時動工（美、馬、日、德、高雄）；資本支出報導自約20億美元升至2025年53億、2026年85億美元，2027年預期仍高。
  - 來源：TrendForce News, ASE targets FOPLP mass production by end-2026, launches 15 expansion projects（as_of 2026-06-25）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：ASE 2026 capex 上調 20 億至約 105 億美元，設備 65 億中約 70% 用於先進製程
  - 來源：eu.36kr.com（as_of 2026-07-17）｜affects：thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Amkor Q3 2024 毛利率 14.6%（去年同期 15.5%），Q4 指引 13.5%~15.5%，股價跌 8.8%
  - 來源：itiger: Stock Track | Amkor Technology Plunges 8.8% as Q4 Guidance Disappoints（as_of 2024-10-29）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":99.2,"bear_5y_price":23.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":57.4,"ev5y_pct":53.7,"irr_base_pct":9.5,"asym_ratio":3.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.5,"pe":15.3,"basis":"FY2026E（FY1）共識 EPS 2.50 美元、現價 38.25 美元；終端倍數同樣套在當年度 EPS 上，分母口徑一致"},"eps":{"bull":[3.0,3.7,4.5,5.4,6.2],"base":[2.65,2.9,3.35,3.85,4.3],"bear":[2.3,1.7,1.6,1.95,2.3]},"pe":{"bull":16,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.878,"net_buyback":-0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AMKR_Q2_2026_Earnings_Call_20260727.md
- 2026-07-27｜CFO｜guidance：Q3 營收財測區間（原話："Q3 revenue is expected to"）
- 2026-07-27｜CFO｜guidance：Q3 毛利率財測 18.5%–19.5%（原話："Gross margin is projected to be between 18.5% and 19.5%,"）
- 2026-07-27｜CFO｜guidance：Q3 EPS 財測（原話："resulting in EPS between $0.72"）
- 2026-07-27｜CFO｜guidance：Q3 通訊營收預期季減高個位數，偏離季節性（原話："we expect Communications revenue to decline in the high single digits"）
- 2026-07-27｜CFO｜guidance：Q3 運算營收預期季增近 30%（原話："Computing growth is expected to accelerate to nearly 30% sequentially in Q3,"）
- 2026-07-27｜CFO｜guidance：2026 資本支出維持 25–30 億美元（原話："Our estimated 2026 CapEx spend remains between $2.5 billion and $3 billion."）
- 2026-07-27｜CFO｜margin：Q2 毛利率 16.8%，季增逾 250 bps（原話："Gross margin was 16.8%, expanding over 250 basis points sequentially."）
- 2026-07-27｜CFO｜margin：Q2 毛利率擴張拆解：三分之二稼動率/量，三分之一產品組合（原話："two-thirds of that expansion"）
- 2026-07-27｜CFO｜margin：Q3 毛利率擴張主要來自產品組合（原話："predominantly the impact on that gross margin expansion is related to product"）
- 2026-07-27｜CFO｜margin：Q2 營業費用含 2,100 萬美元不動產出售利得（原話："included a $21 million gain on the sale of real estate."）
- 2026-07-27｜CFO｜margin：Q2 稅率 14%，含 1,400 萬美元離散稅務利益（原話："14% due to $14 million in net discrete tax benefits."）
- 2026-07-27｜CEO｜margin：CEO 說明稼動率：Q1 在 70 幾%、Q2 在高 70 幾%（原話："In Q2, we"）
- 2026-07-27｜CEO｜margin：管理層確認 Arizona 製造負擔將在 2027 成為逆風（原話："we need to be thinking about"）
- 2026-07-27｜CFO｜margin：CFO 稱 2028 毛利率與營業利益率均含 Arizona 低稼動率拖累（原話："ramping underutilized Arizona"）
- 2026-07-27｜CEO｜customer：與 TSMC 簽 10 年先進封裝協議（原話："First, we announced a 10-year advanced packaging agreement with TSMC."）
- 2026-07-27｜CEO｜customer：與 NVIDIA 簽多年策略夥伴協議（原話："We also announced a multi-year strategic partnership"）
- 2026-07-27｜CEO｜customer：NVIDIA 協議為預付款，2027 收到並隨服務返還，期限 5–10 年（原話："this is a prepayment"）
- 2026-07-27｜CFO｜customer：Android 營收 Q2 季減 20%，歸因記憶體供給（原話："Android revenue declined 20% reflecting the impact of"）
- 2026-07-27｜CFO｜risk：Q3 通訊下滑三因素：SiP 移越南、記憶體供給限制、拉貨型態改變（原話："second, ongoing"）
- 2026-07-27｜CEO｜risk：CEO 稱 SiP 移轉造成的逆風不只一季，延續到 Q4 與明年上半年（原話："It's probably going to extend into Q4"）
- 2026-07-27｜CEO｜risk：CEO 稱 Q3 通訊下滑約 50% 為市場因素、50% 為 SiP 移轉（原話："The other 50% would be driven by, again, this SiP move"）
- 2026-07-27｜CEO｜risk：Q4 通訊不預期有一般下半年的明顯拉升（原話："we would expect that communications in general will"）
- 2026-07-27｜CEO｜product：最新資料中心 CPU 專案 Q2 開始放量，下半年持續擴大（原話："our newest data"）
- 2026-07-27｜CEO｜commitment：今年預計各有 4 個 2.5D 與 4 個 HDFO 產品量產（原話："4 2.5D, 4 HDFO products launching this year."）
- 2026-07-27｜CEO｜product：橋接類技術時程屬 2028 年（原話："that would be more of a 2028 type"）
- 2026-07-27｜CEO｜commitment：R&D 占比維持 3%–5%，NVIDIA 協議無階梯式增加（原話："I would expect that level to continue."）
- 2026-07-27｜CFO｜capital_allocation：5 月發行 11.5 億美元 0% 可轉債（原話："we issued $1.15 billion of 0% convertible debt,"）
- 2026-07-27｜CFO｜capital_allocation：6/30 現金 25 億、流動性 36 億、總負債 25 億、負債/EBITDA 1.8x（原話："total liquidity was $3.6 billion."）
- 2026-07-27｜CEO｜capital_allocation：Arizona Phase 1 已被預訂滿載（原話："Our projections now show Phase 1 as fully committed,"）
- 2026-07-27｜CEO｜competition：CEO 稱當前客戶可見度與以往產業週期明顯不同（原話："is meaningfully different"）

### AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md
- 2026-05-21｜Megan Faust｜guidance：CFO 給出 2028 年營收目標 90 億美元，±5 億。（原話："revenue to grow to $9 billion, plus or minus $500 million"）
- 2026-05-21｜Megan Faust｜margin：2028 年毛利率目標 17.5%（±100bp），2025 為 14%。（原話："Gross margins expand to 17.5%, plus"）
- 2026-05-21｜Megan Faust｜guidance：2028 年 EPS 目標 2.50 美元，±0.25。（原話："earnings per share of $2.50, plus or minus $0.25"）
- 2026-05-21｜Megan Faust｜guidance：2030 年目標：營收逾 110 億美元、毛利率逾 22%（EPS 逾 5 美元）。（原話："more than $11 billion in revenue, more than 22% gross margin"）
- 2026-05-21｜Megan Faust｜guidance：管理層對 2028/2030 目標的定位：預期執行並打算超越。（原話："we would plan to beat those."）
- 2026-05-21｜Kevin Engel｜risk：CEO 說明目標模型未內建強烈的景氣下行。（原話："strong cycle in the downward direction."）
- 2026-05-21｜Kevin Engel｜guidance：目標模型僅含亞利桑那第一期，第二期尚未納入。（原話："we didn't put Phase 2 in the model."）
- 2026-05-21｜Kevin Engel｜guidance：2028 年 90 億目標的設定口徑：選的是有把握、可達成的數字。（原話："was achievable, we were very comfortable with."）
- 2026-05-21｜Kevin Engel｜risk：CEO 提到擴產面臨規模化挑戰（含空間）。（原話："We see challenges on scaling."）
- 2026-05-21｜Megan Faust｜guidance：亞利桑那滿載時營收約 10 億美元、毛利率逾 30%。（原話："revenue of around $1 billion and gross margins exceeding"）
- 2026-05-21｜Megan Faust｜capital_allocation：亞利桑那兩期預估總投資 70 億美元。（原話："an estimated total investment of $7 billion."）
- 2026-05-21｜Megan Faust｜commitment：第一期量產時程：2028 年開始、2030 年完全建成。（原話："manufacturing for the first phase is targeted to begin"）
- 2026-05-21｜Megan Faust｜margin：亞利桑那對營業利益的稀釋：2027 年起 1%～2%，視完工與爬坡速度。（原話："We anticipate a 1% to 2% dilution to"）
- 2026-05-21｜Megan Faust｜guidance：亞利桑那預期 2029 年前後損益兩平。（原話："We expect Arizona to reach breakeven around 2029"）
- 2026-05-21｜Megan Faust｜margin：數字口徑：2027–2028 亞利桑那爬坡成本先入營業費用，通過驗證後轉入銷貨成本。（原話："there are initial ramp costs in 2027 and 2028 tied to"）
- 2026-05-21｜Megan Faust｜margin：數字口徑：爬坡成本認列在 OpEx（SG&A）中，與越南廠做法一致。（原話："costs begin in OpEx, specifically in SG&A."）
- 2026-05-21｜Megan Faust｜margin：回答毛利擴張來源：前期以產品組合為主、並帶動稼動率。（原話："more mix impact to margin followed by leverage"）
- 2026-05-21｜Megan Faust｜margin：投資爬坡期的口徑：獲利成長刻意慢於營收成長。（原話："earnings growth is muted relative to revenue growth"）
- 2026-05-21｜Megan Faust｜guidance：數字口徑：2030 目標模型未納入第二座亞利桑那廠。（原話："We have not yet included the second Arizona facility"）
- 2026-05-21｜Megan Faust｜capital_allocation：2026 年資本支出指引 25～30 億美元。（原話："for 2026, we guided $2.5 billion to"）
- 2026-05-21｜Megan Faust｜capital_allocation：資本密集度預期由歷來 12%～13% 升至中高十幾%。（原話："moving up into the mid-teens, maybe mid- to high-teens."）
- 2026-05-21｜Megan Faust｜capital_allocation：歷史資本密集度區間。（原話："We've been very consistent in that 12% to 13%."）
- 2026-05-21｜Megan Faust｜capital_allocation：槓桿現況：含 12 億美元可轉債後，總債務 26 億、總槓桿 2.1 倍。（原話："with $2.6 billion of total debt, our gross leverage is 2.1x."）
- 2026-05-21｜Megan Faust｜capital_allocation：5 月發行 12 億美元可轉債。（原話："$1.2 billion of convertible notes we issued"）
- 2026-05-21｜Megan Faust｜commitment：長期債務／EBITDA 目標 1.5 倍以下。（原話："EBITDA target of 1.5x or below"）
- 2026-05-21｜Megan Faust｜commitment：股東回饋目標：自由現金流的 40%～50%。（原話："Over time, we target a return of 40% to 50%"）
- 2026-05-21｜Megan Faust｜capital_allocation：庫藏股授權上限 3 億美元，可機動使用並抵銷股酬稀釋。（原話："repurchase authorization of up to $300 million"）
- 2026-05-21｜Megan Faust｜commitment：回答線上提問：未考慮暫停或停止股利。（原話："we have not considered pausing or stopping the dividend."）
- 2026-05-21｜Megan Faust｜capital_allocation：資金來源之一：已有客戶以預付款形式承諾。（原話："that were in the form of advanced payments"）
- 2026-05-21｜Doug Scott｜capital_allocation：擴產原則：依需求而非投機。（原話："demand, not speculation."）
- 2026-05-21｜Megan Faust｜risk：亞利桑那第一期的機台尚未全數下單，客戶仍在討論專案性質與規模。（原話："yet ordered all the tools for that first phase."）
- 2026-05-21｜Kevin Engel｜customer：第一期客戶結構多為合約性安排（含裝載協議或預付款）。（原話："them are contractually based structures."）
- 2026-05-21｜Megan Faust｜commitment：第二期時程：管理層表示是何時而非是否。（原話："see Phase 2 as a not if, it's just when."）
- 2026-05-21｜Kevin Engel｜product：先進封裝營收今年預期成長為三倍，且全在運算市場。（原話："a tripling of that advanced"）
- 2026-05-21｜Doug Scott｜product：2.5D 客戶接洽數量。（原話："We now have over a dozen 2.5D engagements."）
- 2026-05-21｜Doug Scott｜customer：首個高密度扇出橋接封裝預計明年為 AMD 量產。（原話："bridge package to ramp next year for our customer AMD."）
- 2026-05-21｜Doug Scott｜product：正在開發三個共封裝光學（CPO）案，合計為十億美元級機會。（原話："these projects are billion-dollar opportunities"）
- 2026-05-21｜Doug Scott｜product：CPO 投資時點的敘事：太早投入會使產線閒置。（原話："when we were first asked to invest in CPO 10 years ago"）
- 2026-05-21｜Doug Scott｜product：對 CoWoS 轉 CoWoP 的態度：定位為快速跟進者而非領頭試產。（原話："but certainly as a fast follower."）
- 2026-05-21｜Kevin Engel｜product：測試占營收目前低十幾%，2029–2030 預期升至中高十幾%。（原話："we're envisioning in the mid- to high-teens"）
- 2026-05-21｜Kevin Engel｜competition：最先進封裝產能緊，台灣以外僅 Amkor 韓國可選。（原話："outside of Taiwan is Amkor in Korea."）
- 2026-05-21｜Megan Faust｜competition：管理層自述為美國唯一擴產中的大規模先進封裝 OSAT。（原話："only scaled advanced packaging OSAT that is expanding"）
- 2026-05-21｜Farshad Haghighi｜customer：Apple COO 影片被用作客戶背書，並稱此模式正部署到美國製造點。（原話："Sabih Khan, the COO at Apple generously shared his vision"）
- 2026-05-21｜Kevin Engel｜customer：與超大規模雲端業者直接溝通增加。（原話："definitely more direct communication with the hyperscalers."）
- 2026-05-21｜Kevin Engel｜customer：汽車為第二快成長市場。（原話："at least today, our second fastest-growing market."）
- 2026-05-21｜Megan Faust｜customer：通訊市場整體成長放緩，靠端側 AI 與換機週期。（原話："continued growth will be driven by on-device AI and refresh"）
- 2026-05-21｜Kevin Engel｜customer：數字口徑：2025 年通訊占營收 46%，運算預期成長快於市場。（原話："In 2025, it represented 46% of our revenue."）
- 2026-05-21｜Farshad Haghighi｜product：高階智慧手機半導體價值預期自 225 美元升至 400 美元。（原話："from $225 today toward $400 over the next few years."）
- 2026-05-21｜Kevin Engel｜product：OSAT 可服務市場（TAM）的估算口徑：每吉瓦約 5 億美元，四至五年成長逾 3 倍。（原話："an increase in TAM of over 3x over the next four to five"）
- 2026-05-21｜Kevin Engel｜risk：管理層強調此為結構性轉變而非景氣循環。（原話："and it's not cyclical."）
- 2026-05-21｜Kevin Engel｜customer：與 Intel 合作 EMIB，預計年底在韓國具備能力。（原話："how we are supporting bringing that technology into Korea"）
- 2026-05-21｜Kevin Engel｜capital_allocation：被問聯邦政府入股：表示沒有相關討論。（原話："there's been no discussions around that."）

### 問答異常語氣（迴避／改口／保留）
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Randy Abrams 問 SiP 移轉是否僅一季時間差｜答法：CEO 先答之後在後續回答改口：移轉逆風並非一季，延伸到 Q4 與明年上半年
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Ben Reitzes 問 Q3 毛利率中 SiP 與稼動率的影響及 Q3 稼動率預期｜答法：CEO 談稼動率定性描述（Q1 70 幾%、Q2 高 70 幾%），未給 Q3 稼動率數字，也未量化 SiP 影響
- AMKR_Q2_2026_Earnings_Call_20260727.md｜問：Steve Barger 問 Q4 毛利率是否季節性上升及 2027 到 2028 目標節奏｜答法：未給 Q4 數字，答依組合與稼動率而定；2027 僅指出美國製造負擔為逆風，未給 2027 數字
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：訂單能見度是否超過兩年、可否量化？｜答法：Doug 只答 'It's over'，Kevin 明確表示 'We won't estimate' 並轉談光學與客戶採用速度，未給期間數字。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：2028 年 90 億目標是否受產能所限（目前已年化約 80 億）？｜答法：Kevin 未直接回答是否產能受限，改談目標是 'achievable numbers'、另有更多機會與空間擴張挑戰。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：亞利桑那第二期的客戶需求時點與資本支出規模？｜答法：Kevin 稱討論 'progressing pretty rapidly' 並說 'stay tuned'；Megan 談時程貼近專案，皆未給時點或資本支出數字。
- AMKR_Analyst_Investor_Day_Amkor_Technology_Inc_20260521.md｜問：2.5D、HDFO、橋接、覆晶與晶圓級中哪些受限、哪些低利用？｜答法：Doug 只說整體先進封裝高稼動並持續投資，未點名哪個領域閒置或受限。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 2 | 5 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 2 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B 衛星候選：thesis 完整（B 級護城河 7/10、AI 先進封裝超級週期、TSMC Arizona partnership unique、Q1 26 EPS Beat 50% 強訊號），但 (a) 估值 🟡 救援後合理但未達 🟢、(b) Pure MA ✅ 強勢但 5/18 shooting star + 連 3 日衝高回落 = 動能末段、(c) 短期 R:R 為負值（共識中位 $73 vs 現價 $65.75 上行有限）= 時機尚不到。等回測 W52 $38-55 區或 Fwd PE 24x $58 區 + Q2-Q3 26 報季 EPS guidance 兌現 + HDFO 首次具體營收揭露後分批進場 3-5% 衛星倉。FY26 capex $2.5-3B 高峰執行進度 + Apple 集中度演變是核心監測點。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 先進封裝超級週期持續，AMKR advanced products mix 持續往 90%+ 移動","columns":{"2Y 驗證點":"FY26-27 advanced products 占比突破 85%；HDFO 開始貢獻可揭露營收","5Y 驗證點":"FY28-30 advanced products 占比 90%+，HDFO 占 advanced products 20%+","10Y 驗證點":"FY32+ advanced products 95%+，傳統 packaging 完全 phase out","具體門檻":"FY26 advanced products ≥ 82%；FY27 ≥ 85%；HDFO H2 26 first revenue","來源":"Amkor IR + sell-side 估算 + 法說會揭露","漂移觸發條件":"連 2 季 advanced products mix 停滯 / 下降 → H1 削弱（QC-35 對齊）"}},{"id":"H2","text":"TSMC Arizona partnership 真實落地，2027-2029 帶來 incremental revenue $500M-$1B/年","columns":{"2Y 驗證點":"2027 Arizona phase 1 完工 + 首批 TSMC 客戶訂單揭露","5Y 驗證點":"2028-2030 Arizona phase 1 + phase 2 ramp，產能利用率達 80%+","10Y 驗證點":"Arizona 多 phase 共 $7B 投資全部完工，成為 AMKR 第二大基地","具體門檻":"2027 mid Arizona phase 1 mechanical completion；2028 中首批 TSMC 客戶訂單揭露","來源":"TSMC 法說會 + Amkor IR + CHIPS Act 補助到位進度","漂移觸發條件":"Arizona 完工延後超過 12 個月，且 TSMC partnership 無新進展 → H2 削弱"}},{"id":"H3","text":"Apple 客戶集中度從 30% 逐步降至 22-25%（不是因為 Apple 流失，而是其他客戶成長）","columns":{"2Y 驗證點":"FY26-27 Computing + Automotive 兩段營收占比合計提升至 35%+","5Y 驗證點":"FY28-30 Computing 段成為第一大段（取代 Communications）","10Y 驗證點":"FY32+ 客戶分布更平衡，no single 客戶 &gt; 25%","具體門檻":"FY26 Computing 占比 ≥ 12%（FY24 ~9%）；FY27 ≥ 18%；FY28 ≥ 25%","來源":"Amkor 10-K 分段揭露 + sell-side 模型","漂移觸發條件":"Apple 占比連 2 年仍 ≥ 30% 且 Computing 占比 &lt; 15% → H3 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Apple iPhone unit 同期見頂 + Apple C2/C3 modem 自研擴大 → Communications 段 quarterly revenue YoY 轉負","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Communications 段 quarterly YoY %","警戒閾值":"連 2 季 YoY &lt; 0% → 觸發減倉"}},{"id":"R2","text":"FY26 capex $2.5-3B 真實執行但 H2 26 / H1 27 需求疲軟 → FY26 / FY27 FCF 連年壓制 / 轉負 → 股利 + buyback 動用 net cash","columns":{"對應假設":"H1 / H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"FY26 全年 FCF + Net cash position","警戒閾值":"FY26 FCF &lt; -$300M 或 Net cash 轉 Net debt &gt; $0.5B → 嚴重 capital discipline 質疑"}},{"id":"R3","text":"2030 年代計算範式轉換（photonics / hybrid bonding 完全取代 2.5D / 3D）+ TSMC 收回 advanced packaging in-house → AMKR 結構性退至 traditional 商品 OSAT","columns":{"對應假設":"H1 / H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"TSMC 法說會關於 SoIC / advanced packaging capex 比例 + AMKR R&amp;D / Revenue 趨勢","警戒閾值":"需 ≥ 50% 機率才砍倉；當前機率 ~15-20%，列入觀察"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":65.75,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"AMKR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Amkor Technology, Inc."},"oneliner":"AI 先進封裝把毛利率拉到 18.3%、運算營收年增 37%，但 2027–29 年資本支出高峰讓自由現金流轉負；現價只反映 2028 年 EPS 約 2.7 美元，等 2027 年 2 月資本支出與客戶預付款覆蓋率揭露再動手。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AMKR_20261103/scenario.json","answers":{"q1_business":{"verdict":"Amkor 賺的是晶片設計商與 IDM 委外的封裝測試加工費，錢卡在先進封裝產能：台灣以外能做 HDFO 與 2.5D 的產能是 Amkor 的定價籌碼，SiP 與手機封裝則是跟著客戶拉貨起落的加工生意。","reasoning":"Q3 2026 營收 19.91 億美元，先進產品 16.32 億、占 82.0%；毛利率 18.3%（年增 400 個基點），營益率 11.3%，EPS 0.76 美元。終端市場：運算與車用工業各年增 37% 創新高；通訊年減 28%，原因是 SiP 由韓國移到越南的時程；消費性季增 10%。Q4 財測營收 19–20 億美元、毛利率 18%–19%、EPS 0.65–0.75。收錢方式：客戶自帶晶片，Amkor 按顆收封裝與測試服務費，基板等材料成本多半轉嫁。折舊負擔重（Q3 EBITDA 4.35 億對營業利益 2.25 億，單季折舊攤銷約 2.1 億），獲利由稼動率與產品組合決定。單點依賴：2025 年 Apple 直接銷售占 29.8%、Qualcomm 占 11.1%，前兩大合計 40.9%，前十大 72%（Q3 2026 降到 66%）；這是集中度風險，不能當護城河證據。產業時鐘：先進封裝在擴張期（運算年增 37%，Omdia 預期封裝瓶頸至少延續到 2027 年），通訊與消費性在收縮。公司有兩種性質的業務：AI 運算封裝是長期成長段，通訊與消費性是週期段，循環位置的判讀套在後者與整體產能週期上。循環位置看資本支出建設循環的六個訊號：資本支出約為折舊的 3 倍，偏晚；稼動率由 70 幾%回升，偏早；預付款與客戶承諾領先資本支出，偏早；客戶信用強但集中，中性；股價 26 週跌 46%，賣方目標價遠高於現價，偏早（但目標價已過時）；出貨量成長領先價格，屬中段。合起來判中循環。各訊號互有矛盾，淨值比事實表也未涵蓋，所以反動能檢查無法全數通過。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_gross_margin","f_kpi2_gaap_operating_income_ma","f_kpi3_non_gaap_operating_incom","f_kpi4_diluted_eps_gaap","f_kpi6_management_guidance_q4_2","f_kpi7_advanced_products","f_week26_return_pct"],"verdict_values":{"revenue_quality":"成長來自運算（資料中心 HDFO CPU、2.5D）與車用工業，兩者 Q3 各年增 37%。通訊（2025 年占營收 46%）年減 28%，消費性受零件短缺拖累。營收品質提升靠的是組合往高價先進封裝移動，但前十大客戶仍占 66%；能見度主要來自多年合約與客戶預付款，金額沒有完整揭露。","unit_econ_note":"加工費模式：材料多半轉嫁，毛利額取決於加工價與稼動率。Q1 稼動率 70 幾%、Q2 高 70 幾%（2026-07-27 CEO），Q3 未揭露。單季折舊攤銷約 2.1 億美元，稼動率一往下走毛利率就掉得快：2023–2025 年毛利率只有 14.0%–14.8%。","archetype":{"primary":"循環/商品","secondary":"EMS/ODM","confidence":"中","fingerprint":"資本支出建設循環：毛利率在 14%–19% 之間擺動，資本支出占營收由 12%–13% 升到 30% 以上，前十大客戶占 66%–72%，收入是代工型加工費"},"industry":{"clock_phase":"II","sd_verdict_source":"屬週期性、將會反轉。先進封裝供需在 2027 年前偏緊：Omdia 這樣預期，Q3 法說也稱封裝成為關鍵瓶頸、客戶在搶 2027–28 年產能。但台積電 CoWoS 供需缺口 2026 年底會收斂到約 10%（TrendForce），日月光 2026 年資本支出上調到約 105 億美元、六座新廠同時動工。供給可逆性中高，2027–28 年封裝報價有回落風險。","bargaining":{"up":"上游：基板、先進矽與記憶體供應吃緊、成本上漲，Amkor 以轉嫁為主（Q3 法說 CEO），議價力中性。","down":"下游：Apple 29.8%、Qualcomm 11.1%、前十大 66%–72%，大客戶議價力強。但 AI 客戶為了鎖住產能，願意預付並簽多年約（NVIDIA 預付款 2027 年入帳、期限 5–10 年），先進封裝這一段的議價暫時偏向 Amkor。","geo":"廠房幾乎全在美國以外（中國、日本、韓國、馬來西亞、菲律賓、葡萄牙、新加坡、台灣、越南）。亞利桑那廠 2027 年底完工、2028 年量產，管理層稱是美國唯一在擴產的規模化先進封裝 OSAT。出口管制限制對部分中國客戶的銷售，非美國競爭者可能豁免。"},"profit_pool_dir":"利潤池往先進封裝集中，但最高價值的一段被台積電自建的 CoWoS 拿走。台積電據報擴大把 CoW 前段外包給封測廠（TrendForce 2026-08），Amkor 分到的是外溢量，以及台灣以外的第二來源角色。同業中營益率最高的達 26.9%；Amkor 測試占營收目前是低十幾%，目標在 2029–30 年升到中高十幾%。","tam_table":[{"item":"OSAT 在 AI 資料中心的可服務市場","value":"每吉瓦約 5 億美元，4–5 年成長 3 倍以上（2026-05-21 投資人日 CEO，屬管理層估算）"},{"item":"2.5D 與 HDFO 平台","value":"2026 年約成長為 3 倍；先進封裝營收今年三倍，且全部在運算市場（投資人日、Q3 法說摘要）"},{"item":"先進封裝產業成長","value":"2026 年約 80%（Onto Innovation 由 50% 上調）"},{"item":"晶片市場","value":"2027 年約 1.9 兆美元、年增約 27%（WSTS 2026 春季預測）"},{"item":"Amkor 先進產品占營收","value":"Q3 2026 為 82.0%（16.32 億美元）"},{"item":"Amkor 通訊占營收","value":"2025 年 46%（投資人日）"},{"item":"滲透率、營業利益池占比的五年變化","value":"事實表未涵蓋，無法判斷利潤池是否淨流出"}]}}},"q2_moat":{"verdict":"護城河持平，等級 C。執行力在進步，但定價力主要來自產能吃緊，屬週期現象，利潤率仍是台系同業最低。客戶預付款與多年合約是新出現的轉換成本，要看 2027–28 年新供給開出後撐不撐得住。","reasoning":"機制有三層：規模化的先進封裝產能；地理稀缺（韓國是台灣以外唯一可選的最先進封裝基地，亞利桑那是美國唯一在擴產的規模化 OSAT）；前期設計參與加上預付款綁定的多年合約。對同業的利差：近四季毛利率 16.56%，比日月光 20.81% 低 4.25 個百分點、比力成 19.12% 低 2.56 個百分點；營益率 9.51%，對比 11.47% 與 12.90%。投入資本事實表未涵蓋，ROIC 利差無法計算。Amkor 自身毛利率由 2025 年 13.99% 升到 Q3 2026 單季 18.3%，但同業同期趨勢事實表未涵蓋，利差有沒有收窄無法證實。執行評 7 分：運算與車用創新高，熊本地震後當季復工；但 Q3 毛利率 18.3% 低於 7 月財測下緣 18.5%，運算季增 25% 也低於指引的近 30%。定價評 5 分：CEO 自述以成本轉嫁為主，SiP 不會帶動毛利率加速；漲價空間來自玩家少、產能緊，日月光也同步漲價 20% 以上，是產業共享的好處，不是 Amkor 專屬。產業態勢是雙向拉鋸。競爭面在惡化：日月光資本支出約為 Amkor 的四倍，中國在地供應鏈業者也受惠。結構面在轉好：客戶預付款、多年合約，台積電擴大外包 CoW 前段。其他結構變數偏負：出口管制讓非美國同業豁免，關稅無法預測。","fact_refs":["f_peer_amkr_gross_margin_pct","f_peer_amkr_operating_margin_pct","f_peer_amkr_fcf_margin_pct","f_peer_3711_tw_gross_margin_pct","f_peer_3711_tw_operating_margin_pct","f_peer_3711_tw_fcf_margin_pct","f_peer_6239_tw_gross_margin_pct","f_peer_6239_tw_operating_margin_pct","f_peer_2449_tw_gross_margin_pct","f_peer_2449_tw_operating_margin_pct","f_peer_2449_tw_fcf_margin_pct","f_peer_600584_ss_gross_margin_pct","f_peer_600584_ss_operating_margin_pct","f_peer_600584_ss_fcf_margin_pct","f_kpi1_gross_margin","f_kpi2_gaap_operating_income_ma","f_consensus_eps_fy1","f_shares_diluted_m"],"verdict_values":{"moat":{"mechanism":"規模化先進封裝產能，加上地理稀缺（韓國是台灣以外的最先進封裝基地、亞利桑那是美國本土唯一的規模化 OSAT），再加上前期設計參與與客戶預付款綁定的多年合約","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面在擴大：毛利率年增 400 個基點，前十大客戶占比由 73% 降到 66%，十幾家客戶簽了預付款。定價面穩定：以成本轉嫁為主，毛利率仍低於日月光與力成。兩者合起來判持平。最大客戶 Apple 的份額方向事實表未涵蓋，所以不標上升。","competitor_notes":[{"name":"3711.TW（日月光）","strategy_note":"規模與利潤率都領先（近四季毛利率 20.81%、營益率 11.47%）。2026 年資本支出約 105 億美元、六座新廠同時動工，是 2027–28 年先進封裝報價的最大變數。目前據報漲價 20% 以上，短期幫 Amkor 撐住價格，長期卻是供給過剩的來源。"},{"name":"6239.TW（力成）","strategy_note":"近四季毛利率 19.12%、營益率 12.90%，都高於 Amkor。業務組合事實表未涵蓋，只當利潤率參照。"},{"name":"2449.TW","strategy_note":"近四季營益率 26.86%，同業最高；自由現金流率 −32.27%，顯示它同樣在大舉擴產。業務組合事實表未涵蓋，當價值鏈上緣參照。"},{"name":"600584.SS（長電科技）","strategy_note":"10-K 點名的中國對手。近四季毛利率 15.83%、營益率 7.15%，略低於 Amkor。它受惠於中國在地供應鏈與出口管制，Amkor 對部分中國客戶的生意可能流向它。"}],"spread_notes":{"summary":"近四季毛利率：Amkor 16.56%，比日月光 20.81% 低 4.25 個百分點，比力成 19.12% 低 2.56 個百分點。營益率：9.51%，比日月光 11.47% 低 1.96 個百分點，比力成 12.90% 低 3.39 個百分點。投入資本事實表未涵蓋，ROIC 利差改用利潤率代替。五家自由現金流率全部為負，Amkor 的 −2.09% 最輕，整個產業在同步擴產。"},"threats":[{"level":"🟡","text":"供給過剩：日月光 2026 年資本支出約 105 億美元、六座新廠同時動工；台積電 CoWoS 缺口 2026 年底收斂到約 10%。同業自由現金流率全數為負（日月光 −11.3%、長電 −13.5%），整個產業同步擴產，2027–28 年封裝報價可能反轉。","p":35,"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","supply_demand_durability#1"]},{"level":"🔴","text":"晶圓廠自建與客戶內製：10-K 載明 IDM 與晶圓代工可以隨時把外包封測轉回自有產能，台積電自建的 CoWoS 拿走最高價值的一段。反向證據是台積電據報擴大把 CoW 前段外包給封測廠。","p":25,"evidence_refs":["customer_second_source#1"]},{"level":"🟡","text":"中國在地供應鏈競爭：地緣貿易緊張讓支援中國自給的中國業者受惠，出口管制下 Amkor 對部分中國客戶的生意可能被接走。","p":40,"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#3"]},{"level":"🟡","text":"封裝架構替代：玻璃基板（Intel 主導，Amkor 是合作夥伴）預計三年內商業化，另有共封裝光學與混合鍵合。Amkor 定位為快速跟進者，技術轉換期間既有 2.5D 產能可能貶值。","p":15,"evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉（周轉率為推定：投入資本事實表未涵蓋，但資本支出占營收 30% 以上、單季折舊約 2.1 億美元，屬資產很重的生意）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者是同一批晶片客戶。AI 運算這一端是真需要：Q3 法說稱先進封裝在系統效能的關鍵路徑上、封裝已成瓶頸，客戶用預付款搶 2027–28 年產能。但 2025 年占營收 46% 的通訊與消費性需求可以延後，記憶體一漲價，Android 低階機需求就縮水。一半剛性、一半週期。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一封裝專案的層級衡量。HDFO 製程超過 300 道步驟、換廠要重新認證，專案進行中很難換；但每一代新產品，客戶都能重新選供應商或轉回自有產能。可觀察的代理變數：NVIDIA 預付款期限 5–10 年，十幾家客戶簽了預付款，亞利桑那第一期已被預訂滿載。漲價後的客戶流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"整條 AI 晶片價值鏈中，台積電（前段製程加 CoWoS）與晶片設計商拿走大部分利潤。Amkor 近四季毛利率 16.56%，是台系封測同業最低，Apple 一家就占營收 29.8%。長期需求存在，不代表封測環節能多分到利潤：現在的漲價來自產能吃緊，供給開出後議價權會回到大客戶手上。"},{"item":"社會容忍度","level":"🟡","text":"這是 B2B 加工費，終端消費者感受不到，沒有民意形成的價格天花板。但美國據點的優勢有一部分建立在政策上（Peoria 廠拿到 CHIPS 法案 4.07 億美元補助，加上在地化政策），屬政策風險；關稅與出口管制的變動，公司自述已經造成、而且可能持續造成不利影響。"}],"roiic":"介於負值與約 15% 之間。2022→2025 年營業利益由約 8.97 億降到約 4.68 億美元（financial_history 年報，FY2022–FY2025），同期仍持續投資，增量報酬為負。2025→2026E 淨利由 3.74 億升到約 6.2 億（共識 EPS 2.50 × 2.478 億股），增量約 2.46 億，除以 2026 年淨再投資約 16.6 億，約 15%；但其中含一次性稅務與處分利益，且投資尚未全數投產，這個數字只能當上緣。","reinvest_rate":"約 270%。2026 年資本支出約 25 億美元，減去年化折舊攤銷約 8.4 億（Q3 EBITDA 4.35 億減營業利益 2.25 億，乘以 4），淨再投資約 16.6 億，除以 2026E 淨利約 6.2 億。營運資金變動事實表未涵蓋，收購淨額為零。超過 100% 的部分由客戶預付款、0% 可轉債（11.5 億美元，2031 年到期）與既有現金支應。","endo_ceiling":12,"formula_note":"內生成長率＝增量報酬 × 再投資率。270% 的再投資率是靠外部資金撐起來的，不能直接相乘。改用自有資金口徑：再投資率上限取 100%，增量報酬取上緣 15% 再打八折（扣掉一次性利益與尚未投產的廠房），得出約 12%/年。"}}}},"q3_growth":{"verdict":"五年後跑道寬。AI 先進封裝的可服務市場 4–5 年擴大 3 倍以上，2030 年後還有共封裝光學（3 個十億美元級專案）、橋接封裝、測試占比上升與亞利桑那第二期。但成長主要靠外部資金擴產撐起來，共識 EPS 增速遠高於內生上界，差距來自毛利率擴張與客戶預付款，不是公司自己賺的現金。","reasoning":"成長來源以量為主（運算 2026 年增 30% 以上、2027 年相近或更高，車用工業年增 37%），組合次之（先進產品占 82%），價格只是成本轉嫁加上產能吃緊下的溫和漲價；沒有併購，回購貢獻可以忽略。共識 EPS：FY2025A 1.50 → FY2026E 2.50 → FY2027E 2.78 → FY2028E 3.26（Koyfin 快照，分析師家數事實表未涵蓋），三年年複合 29.5%。同期營收由 FY2025 的 67.08 億到 FY2027E 的 85.93 億，兩年年複合 13.2%；EPS 同兩年年複合 36.1%，兩者相差 23 個百分點，這是一個衰退信號。內生上界約 12%/年（見競爭優勢題的再投資報酬推導），缺口約 17.5 個百分點，可以歸到三個來源：①毛利率由 14.0% 擴張到 18% 以上的組合效應，可以歸因，但有週期高點風險；②2026 年一次性稅務與不動產處分利益，約占全年 EPS 5%；③外部資金撐起的超額再投資（客戶預付款、0% 可轉債）。缺口不靠回購或收購。另外，共識 FY2028E 3.26 比管理層自己的 2028 目標 2.50±0.25 上緣還高 18.5%，所以情境基準取 2.90。跑道方面：滲透率事實表未涵蓋；第二條曲線（共封裝光學、橋接、玻璃基板、測試）有管理層與產業來源，但都還沒有營收，五年後的跑道寬度有一半建立在管理層說法上。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_advanced_products","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"以量為主、組合次之、價格最少（定性拆分：管理層 Q3 法說稱毛利率擴張主要來自高價先進封裝組合）；沒有併購，也沒有實質回購","runway_years":"≥5（可服務市場 4–5 年成長 3 倍以上是管理層估算；滲透率事實表未涵蓋，無法換算到 30% 滲透率的年數）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界約 12%/年（自有資金口徑，增量報酬上緣 15% 打八折）。共識 FY2025A→FY2028E EPS 年複合 29.5%，缺口約 17.5 個百分點，來自毛利率擴張、一次性利益與外部資金，不是無法歸因。","segments":[{"item":"運算","value":"Q3 2026 年增 37%、季增 25%，創新高；Q4 預期季增低雙位數、年增超過 50%；2026 全年年增 30% 以上，2027 年相近或更高"},{"item":"車用與工業","value":"Q3 年增 37%、季增 7%，創新高（ADAS、車載運算）；Q4 預期季增低個位數"},{"item":"通訊","value":"2025 年占營收 46%；Q3 年減 28%、季減 8%（SiP 由韓國移越南、記憶體缺貨、拉貨型態改變）；Q4 預期季減高個位數，Android 與 iOS 都下滑"},{"item":"消費性","value":"Q3 季增 10%（IoT、家電）；Q4 預期季減中十幾%，降幅大於一般季節性"},{"item":"先進產品合計","value":"Q3 16.32 億美元，占 82.0%"},{"item":"組合與毛利率","value":"Q3 毛利率 18.3%，季增 150 個基點、年增 400 個基點，主因是高價先進封裝組合；匯率與熊本地震合計拖累約 60 個基點"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q3 年增 400 個基點"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"通訊年減 28% 主因是 SiP 搬遷時程；份額數據事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"運算量價齊揚"},{"signal":"EPS 年複合顯著高於營收年複合（差距 >5 個百分點）","lit":true,"evidence":"FY2025→FY2027E EPS 年複合 36.1%，營收 13.2%，相差 23 個百分點"},{"signal":"自由現金流／淨利連 2 年 <0.75","lit":true,"evidence":"2025 年 1.91 億 ÷ 3.74 億 ≈ 0.51；2026 年前九個月自由現金流 −3.685 億"},{"signal":"股酬占營收 >5% 且逐年上升","lit":false,"evidence":"事實表未涵蓋；2022→2025 稀釋股數年增約 0.4%，看不到明顯稀釋"},{"signal":"可服務市場萎縮或被替代技術壓縮","lit":false,"evidence":"可服務市場在擴大；玻璃基板屬 Amkor 參與的技術"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"signal":"維護性資本支出占自由現金流 >60%","lit":false,"evidence":"自由現金流為負，維護性資本支出未揭露，不適用"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"方向相反：正在大舉擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置全押在自建產能：2026 年資本支出約 25 億美元，前九個月自由現金流 −3.685 億，缺口靠客戶預付款、0% 可轉債與帳上現金補；回購與股利只是配角，股東在 2029 年前拿不到成長帶來的現金。","reasoning":"自由現金流／淨利：2023 年 1.45、2024 年 0.97、2025 年 0.51（financial_history 年報），2026 年前九個月轉負（營業現金流 8.683 億減廠房設備付款 12.368 億）。現金去向：絕大部分投入廠房與設備，2026 年約 65%–70% 用在廠房（含亞利桑那）；股利殖利率 0.88%；回購金額事實表未涵蓋（授權上限 3 億美元）；沒有併購。資金來源：0% 可轉債 11.5 億美元（2031 年到期）、十幾家客戶的預付款（金額未完整揭露）、現金及短期投資 24 億，總流動性 34 億。槓桿：負債/EBITDA 1.7 倍，高於管理層長期目標的 1.5 倍以下；淨負債 3.36 億美元（含租賃）。CFO 稱 2027 年資產負債表穩健，2028 年以後要不要增債「還太早說」。股東回饋目標是自由現金流的 40%–50%，但自由現金流為負的期間，這個承諾沒有實質意義。股數：2022→2025 稀釋股數由約 2.46 億增到約 2.49 億，年增約 0.4%，稀釋輕微；可轉債轉股價事實表未涵蓋，2031 年前的潛在稀釋無法量化。","fact_refs":["f_kpi5_free_cash_flow_pp_e","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_peer_amkr_fcf_margin_pct","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 沒有併購完成項目，成長全靠自建產能，不適用"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購金額事實表未涵蓋。授權上限 3 億美元，就算全數執行，也只占市值約 94.8 億的 3.2%；自由現金流為負期間，回購主要用來抵銷稀釋，回購收益率達不到 10 年期殖利率加 2 個百分點"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"以年報淨利除以稀釋 EPS 推得稀釋股數：2022 年約 2.462 億、2025 年約 2.493 億，年增約 0.4%，低於 1.5%；目前股數 2.478 億"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近 12 個月沒有完成任何併購；股東回饋規模小（股利殖利率 0.88%，回購金額事實表未涵蓋）。真正承重的問題是資本支出的報酬，已在競爭優勢題的再投資報酬推導處理"}}}},"q5_valuation":{"verdict":"現價 38.25 美元對未來的要求不高：用 14 倍本益比算，只需要 2028 年 EPS 約 2.73 美元，大約是管理層 2028 目標的上緣，而 Q4 財測年化已經有約 2.80。我相信這個門檻守得住。但本益比低，有一半是因為毛利率在多年高點，市銷率只在自身區間的中位，所以判合理而不是便宜。","reasoning":"倍數：FY2026E 本益比 15.3 倍、FY2027E 13.8 倍、FY2028E 11.7 倍；近四季本益比 15.42 倍，在 4 個年度端點中位於 35 分位；市銷率 1.27 倍（54 分位），EV/S 1.32 倍（54 分位）；五年分位事實表未涵蓋。PEG：FY2026E→FY2028E EPS 年複合 14.2%，15.3 ÷ 14.2 ≈ 1.08。若改用 FY2025A 低基期算出的 29.5%，PEG 是 0.52，會高估便宜程度，所以不採用。同業本益比事實表未涵蓋，不拿跨市場同業當錨。賣方目標價（7 月、Q3 財報前）在 69–90 美元，比現價高 80% 以上，但已經過時：股價 26 週跌了 46%，FY1 共識近 3 個月也下修 2.7%。短期上行空間：基準路徑 FY2028E EPS 2.90 × 14 倍 ＝ 40.6 美元，約 +6%；中期（約三年）FY2030E 3.85 × 14 倍 ＝ 53.9 美元，約 +41%。自由現金流為負，現金流估值用不上。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"本益比口徑：FY2026E 共識 EPS 2.50 美元，對應 15.3 倍；終端倍數同樣套在當年度 EPS 上","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋（同業對照只有利潤率），不拿跨市場同業倍數當錨，改用自身年度端點分位與現值"},"fwd_pe":15.3,"peg":1.08,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"本益比 15.3 倍（FY2026E）、13.8 倍（FY2027E）偏低，單看傾向便宜。但毛利率 18.3% 是 2022 年以來最高（2023–2025 年只有 14.0%–14.8%），市銷率與 EV/S 都在年度端點 54 分位，只是中位；PEG 1.08 落在合理區間；自由現金流為負。合起來判合理。五年分位事實表未涵蓋，不另行推算。","upside_short_pct":6.1,"upside_mid_pct":40.9,"denominator_disputed":false,"denominator_note":"FY2026E 含年內一次性稅務利益（Q2 約 1,400 萬美元）與不動產處分利益（約 2,100 萬美元），合計約占全年 EPS 5%，不改變結論。較大的分歧在 FY2028E：共識 3.26 高於管理層目標 2.50±0.25，情境基準改用 2.90，便宜與否的論證不依賴共識的遠期數字。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把週期高點的利潤率當成新常態。陷阱風險中等：本益比低，但毛利率在多年高點，自由現金流為負，而且 2027–29 年資本支出還要再升。","reasoning":"十類衰退信號亮了兩項：EPS 增速比營收增速高 23 個百分點；自由現金流／淨利連兩年低於 0.75。空方最有力的數字：2027 年光是廠房投資就超過 20 億美元，亞利桑那兩期總額由 5 月的 70 億估到 120 億美元；同業自由現金流率全數為負，整個產業在同步擴產。路徑風險：股價 26 週已跌 46%，RSI 35.7；週線跌破 104 週均線（38.33），但仍在 250 週均線（30.57）上方，離 52 週均線（53.61）約 −29%。2024 年 10 月財測令人失望時，股價單日跌 8.8%。反證的完整論述與裁定見反證紀錄。","fact_refs":["f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi5_free_cash_flow_pp_e","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點利潤率加上資本支出高峰，低本益比可能是假便宜"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.5,"pe":15.3,"basis":"FY2026E（FY1）共識 EPS 2.50 美元、現價 38.25 美元；終端倍數同樣套在當年度 EPS 上，分母口徑一致"},"eps":{"bull":[3.0,3.7,4.5,5.4,6.2],"base":[2.65,2.9,3.35,3.85,4.3],"bear":[2.3,1.7,1.6,1.95,2.3]},"pe":{"bull":16,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.88,"net_buyback":-0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-35,"basis":"從現價 38.25 美元起算。下緣：空方路徑的谷底年（FY2029E）EPS 1.60，乘以 11–13 倍（谷底盈餘的倍數通常會擴張），得 17.6–20.8 美元，約 −46% 到 −54%，取 −55%。上緣：FY2027E 下修到 2.30，倍數壓縮到 10–12 倍，得 23.0–27.6 美元，約 −28% 到 −40%，取 −35%。參照：費半歷史上 5 次回撤幅度 30%–82%（部落格彙整，非權威來源）；本股 26 週已跌 46%，波動大。核心業務守得住：2023–24 年下行期仍有 EPS 1.43–1.46 美元，所以這是要有深回撤的心理準備，不是因為波動就砍倉。","trigger_time":null},"basis":{"bull":"運算在 2027 年後維持 30% 以上成長，亞利桑那 2029 年轉盈，毛利率超過管理層 2030 年 22% 的目標，2030 年 EPS 5.40，高於管理層 5 美元的目標；倍數 16 倍，略高於現值 15.3 倍。","base":"運算 2027 年增約 30%，通訊在 2027 下半年回穩，但折舊、亞利桑那爬坡費用與稅率正常化吃掉一部分組合紅利。FY2028E 2.90，介於管理層目標 2.50±0.25 與共識 3.26 之間；FY2031E 4.30，五年年複合約 11.5%，在內生上界 12% 以內。倍數 14 倍，略低於現值 15.3 倍；同業現值倍數事實表未涵蓋，以自身現值與年度端點 35 分位對照。","bear":"2027–28 年日月光與台積電的新產能開出，封裝報價反轉，旗艦專案部分轉單，亞利桑那低稼動拖累獲利，毛利率回到 2023–25 年的 14%–15%。EPS 谷底 1.60（FY2029E），FY2031E 回到 2.30；倍數 10 倍，對應成長熄火到 5%–10% 時的倍數下緣。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"日月光 2026 年資本支出約 105 億美元、六座新廠同時動工；台積電 CoWoS 缺口 2026 年底收斂到約 10%。2024 年 10 月 Amkor 毛利率年減、財測令人失望，股價單日跌 8.8%。2023–2025 年毛利率只有 14.0%–14.8%。","assumption":"先進封裝產能吃緊延續到 2028 年，旗艦運算專案留在 Amkor。","consequence":"五年後虧損 50% 最可能的劇本：2027–28 年新產能開出、報價反轉，旗艦專案部分轉回台積電或分給日月光；Amkor 正好在資本支出最高峰時遇上稼動率下滑，毛利率回到 14%，EPS 回到 1.5–1.6 美元，倍數 10–12 倍，股價落在 15–19 美元。","ruling":"部分採納：空方機率定 30%，最大回撤下緣取 −55%。不全面採納的理由：十幾家客戶的預付款與 5–10 年期合約，讓 2027–28 年的產能填充有合約支撐；HDFO、2.5D、晶圓凸塊設備也可以互相轉用（Q3 法說 CEO）。這條和 Single Thing 部分重疊：轉單是這個劇本的觸發點，供給過剩是放大器。","watch":"運算營收季增率、日月光與台積電的封裝報價、Amkor 對稼動率的說法、毛利率是否連 2 季年減","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","supply_demand_durability#1","cyclical_prior_downcycle_behavior#1"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年前九個月自由現金流 −3.685 億美元。亞利桑那兩期總投資估計由 5 月投資人日的 70 億美元升到 Q3 法說的 120 億。2027 年光是廠房投資就超過 20 億（亞利桑那最多 18 億、韓國 4–4.5 億、越南 0.5 億），亞利桑那在 2028–29 年見高峰。0% 可轉債 11.5 億美元 2031 年到期。負債/EBITDA 1.7 倍，高於 1.5 倍的目標。","assumption":"客戶預付款能覆蓋大部分廠房投資，新產能的報酬率高於資金成本。","consequence":"AI 封裝成長全部兌現、2030 年營收突破 110 億，但每股自由現金流到 2029 年都是負的。預付款以未來的服務抵扣，等於提前收走了未來營收的現金，加上可轉債轉股稀釋：營收和 EPS 好看，股東實際拿到的現金很少。","ruling":"採納，這是本次最主要的風險，也是觀望的關鍵限制。預付款覆蓋率揭露之前不建倉；觸發器設在負債/EBITDA 超過 2.0 倍、總流動性低於 20 億美元。","watch":"2027 年 2 月的資本支出指引、預付款金額與覆蓋率、負債/EBITDA、總流動性","evidence_refs":[]},{"view":"價格已反映太多","evidence":"本益比 15.3 倍看似便宜，但毛利率 18.3% 是 2022 年以來最高；市銷率 1.27 倍、EV/S 1.32 倍都在年度端點中位；共識 FY2028E 3.26 高於管理層目標 2.50±0.25。","assumption":"高點利潤率可以延續，共識的遠期 EPS 可信。","consequence":"如果毛利率回到 15%，在同樣營收下 EPS 會掉三成以上，現在的 15 倍本益比其實是 20 倍以上。","ruling":"反駁。現價 38.25 ÷ 14 倍 ≈ 2028 年 EPS 2.73 美元，只要求達到管理層目標上緣，不要求共識的 3.26，也完全沒有為 2030 年 5 美元的目標付錢；股價比前份已跌 42%，市場已經對高點利潤率打了折。保留的部分是：便宜與否的論證不能建立在共識的遠期數字上。","watch":"毛利率四季滾動值、FY2027E 共識修正","evidence_refs":[]},{"view":"論點失敗","evidence":"幾乎所有廠房設備都在美國以外，主力在中國、日本、韓國、馬來西亞、菲律賓、越南。公司自述關稅與出口管制已經造成、而且可能持續造成不利影響，也無法預測美國後續的行動；出口管制限制對部分中國公司的銷售，非美國競爭者可能豁免；中國營運風險隨美中關係升高。","assumption":"關稅與出口管制的衝擊可以轉嫁出去，或靠亞利桑那廠對沖。","consequence":"如果對半導體或封裝服務課徵關稅，或擴大出口管制，Amkor 亞洲產能的成本優勢與中國客戶的生意會同時受損，而亞利桑那要到 2028 年才量產。","ruling":"部分採納。不寫政策預測，改設損益層的吸收失敗判定：單季毛利率因關稅或出口管制下降 100 個基點以上，或公司揭露受限營收達 5% 以上，即減碼。","watch":"季報對關稅與出口管制的量化揭露、毛利率變動拆解","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#1","geo_supply_chain#0","geo_supply_chain#2","geo_supply_chain#3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 65.75 → 本次 38.25（-41.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=65.75","side_b":"本次 price_at_dd=38.25","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 65.75 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 65.75 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 65.75 美元：Bull 價 99.2、Bear 價 23，五年期望值 −10.6%，基準年化 −1.7%，不對稱比 0.65","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.65。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 65.75 美元：五年期望值 −10.6%，基準年化 −1.7%，不對稱比 0.65","side_b":"本次情境、股價 38.25 美元：五年期望值 +53.7%，基準年化 9.5%，不對稱比 3.33","ruling":"再換股價、情境不動：起點價下跌 41.8%，五年期望值多 64.3 個百分點，基準年化多 11.2 個百分點，不對稱比由 0.65 升到 3.33。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：訊號與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-05-24，股價 65.75 美元）：訊號 B，估值合理（🟡），等股價回測或財報兌現再分批。","side_b":"本次（股價 38.25 美元，比前份跌 42%）：FY2026E 本益比 15.3 倍、FY2027E 13.8 倍；估值仍判合理（🟡），訊號維持 B。","ruling":"可調和，屬程度差異。倍數下降主要來自股價下跌，但毛利率 18.3% 是 2022 年以來最高，市銷率只在年度端點中位，低本益比有一部分是高點利潤率造成的。所以估值由偏貴回到合理，還沒到便宜。","evidence_level":"事實表價格與共識快照（一手數據）","settle_metric":"Q4 2026 毛利率、FY2027E 共識 EPS 修正","if_then":["若 Q4 毛利率 ≥18% 且 FY2027E 共識未再下修 → 估值結論往便宜移一格","若毛利率連 2 季年減 → 估值改判偏貴，不追"],"evidence_refs":[]},{"axis":"前份漂移：陷阱、護城河趨勢、五年後跑道","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：陷阱風險 🟡；護城河 B 級（7/10）；護城河趨勢與五年後跑道未判。","side_b":"本次：陷阱風險 🟡（亮兩項：EPS 增速比營收增速高 23 個百分點；自由現金流／淨利連兩年低於 0.75）；護城河降為 C 級（執行 7 分、定價 5 分），趨勢持平；五年後跑道寬（🟢）。","ruling":"這次調整由新證據驅動。近四季毛利率 16.56%，低於日月光 20.81% 與力成 19.12%；日月光 2026 年資本支出約 105 億美元；CEO 自述定價以成本轉嫁為主。定價力屬產業共享的週期現象，不是 Amkor 專屬，所以護城河降一級。跑道判寬，是因為本次有可服務市場 4–5 年成長 3 倍以上，以及共封裝光學、橋接封裝等第二曲線的來源，但其中一半是管理層的說法。","evidence_level":"同業財報（yfinance）、產業報導、法說會","settle_metric":"Amkor 與日月光的毛利率差距、2027 年封裝報價方向","if_then":["若 2027 年毛利率差距收斂到 2 個百分點以內 → 定價分回到 6，護城河回到 B","若報價轉跌且毛利率連 2 季年減 → 趨勢改判縮減，減碼"],"evidence_refs":["cyclical_supply_discipline_capacity#3","competitive_share_entrants#0"]},{"axis":"前份漂移：研究框架新增欄位","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份沒有設定公司原型、循環位置、情境機率與最大回撤，裁決與角色欄位空白。","side_b":"本次：原型為循環／商品（資本支出建設循環子型），循環位置為中循環；情境機率為多頭 25%、基準 45%、空頭 30%；最大回撤 −35% 到 −55%；裁決與角色由決策矩陣依本次輸入產生。","ruling":"這是方法變動，不代表基本面方向改變。空頭機率 30%，是因為共識 EPS 增速超過內生上界，空頭機率不得低於 30%。","evidence_level":"研究框架","settle_metric":"無（屬方法欄位）","if_then":["若 2027 年資本支出指引顯示擴產速度放緩、預付款覆蓋過半 → 空頭機率可降到 25%"],"evidence_refs":[]},{"axis":"前份風險門檻已觸發，改設新的減碼門檻","cause":"新證據","prior_field":null,"side_a":"前份：通訊營收連 2 季年減即減倉；2026 全年自由現金流低於 −3 億美元，或淨負債超過 5 億美元，即質疑資本紀律。","side_b":"本次：Q3 通訊年減 28%；2026 前九個月自由現金流已達 −3.685 億美元；淨負債 3.36 億美元（含租賃）。新門檻：通訊連 2 季年減超過 20%，且 2027 上半年 SiP 未回升 → 減碼；負債/EBITDA 超過 2.0 倍，或總流動性低於 20 億美元 → 減碼。","ruling":"前份的減倉條件已部分觸發，但當時沒有持倉，不需要追溯動作。改門檻的理由：通訊年減有一半來自 SiP 搬遷時程（2026-07-27 CEO 稱約 50% 是市場因素、50% 是搬遷），只看年減會把搬遷空窗誤判成需求崩壞，所以改看年減幅度加上回升時點。擴產期自由現金流為負在預期之內，且部分由客戶預付款支應，所以改看槓桿與流動性這兩個真正會逼公司增資的數字。管理層的搬遷歸因不採信也不否定，若 2027 上半年 SiP 未回升，就視為歸因不成立。","evidence_level":"季報、法說會（一手）","settle_metric":"2027 上半年通訊營收、負債/EBITDA","if_then":["若 2027 上半年通訊年減仍超過 20% → 減碼","若負債/EBITDA 回到 1.5 倍以下 → 解除資本紀律疑慮"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"Single Thing 新設（觸發即清倉）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）。","side_b":"本次 Single Thing：旗艦 HDFO CPU 專案或 NVIDIA 資料中心 HDFO 專案，任一被轉單、取消或延後 12 個月以上 → 清倉。","ruling":"前份把長期風險放在 2030 年代的技術典範轉移；本次改用數學上敏感度最大的單一項目。2027 年運算成長主要靠少數關鍵專案，失去其中一個，2028 年 EPS 會由基準的 2.90 掉到空方的 1.70。","evidence_level":"法說會（一手）","settle_metric":"每季運算營收季增率與關鍵專案狀態","if_then":["若發生 → 清倉","若關鍵專案 2027 年按時擴產，且新增第三個以上同規模專案 → Single Thing 機率由 15% 降到 10%"],"evidence_refs":[]},{"axis":"重新進場條件新設（未達條件不追，達到再分批建立）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：等股價回測 52 週均線附近的 38–55 美元區，或前瞻本益比 24 倍約 58 美元區，加上 Q2–Q3 財報兌現、HDFO 營收首次揭露後分批進場（沒有設成正式條件）。","side_b":"本次：2027 年 2 月 Q4 法說時，Q4 毛利率 ≥18%，且 2027 資本支出指引附上客戶預付款覆蓋廠房投資過半 → 重跑研究、分批建立首倉；未達則不追。","ruling":"前份的價格條件已經達到（38.25 美元），Q3 EPS 0.76 也兌現了，但 HDFO 營收沒有單獨揭露。更重要的是，本次的關鍵限制已經從價格換成資本支出的報酬，所以改用事件當錨，不設進場價。","evidence_level":"價格（事實表）、法說會","settle_metric":"2027 年 2 月 Q4 法說的資本支出指引與預付款覆蓋率","if_then":["若條件全部達到 → 重跑研究，分兩批建立首倉","若資本支出指引超過 40 億美元且未揭露預付款覆蓋 → 不追，延到 2027 年 Q1 財報再看"],"evidence_refs":[]},{"axis":"清倉與減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（空白）。","side_b":"本次清倉與減碼指標：運算營收年增率連 2 季低於 20%；單季毛利率連 2 季低於 16.6%；負債/EBITDA 超過 2.0 倍；旗艦運算專案轉單或延後 12 個月以上；總流動性低於 20 億美元。","ruling":"本次論點有三根支柱：運算放量、組合推高毛利率、擴產資金不靠股東。每根支柱各配一個可觀察的門檻，再加上 Single Thing，取代前份只有定性描述的監測點。","evidence_level":"研究框架","settle_metric":"每季季報與法說會","if_then":["任一觸發 → 減碼；旗艦專案條件觸發 → 清倉"],"evidence_refs":[]},{"axis":"管理層財測與實際結果：毛利率與運算成長","cause":"新證據","prior_field":null,"side_a":"2026-07-27 Q2 法說（CFO）：Q3 毛利率 18.5%–19.5%，運算季增近 30%。","side_b":"Q3 實際：毛利率 18.3%，低於財測下緣；運算季增 25%。CFO 歸因匯率與熊本地震，合計約 60 個基點；CEO 歸因 300 多道製程的在製品裝載需要時間，否認是供應受限。","ruling":"可調和。管理層的一次性歸因不採信也不否定，列為未證實、持續監測，並預先登記：Q4 毛利率若再低於財測下緣 18.0%，或運算季增低於指引的低雙位數，就視為一次性歸因不成立，停止加碼。","evidence_level":"法說會逐字稿（一手）","settle_metric":"Q4 2026 毛利率、運算季增率","if_then":["若 Q4 毛利率 ≥18% 且運算季增雙位數 → 歸因成立，執行面評分維持","若 Q4 毛利率低於 18.0% → 停止加碼，情境基準往空方調整"],"evidence_refs":[]},{"axis":"資本密集度：投資人日與 Q3 法說的說法不同","cause":"新證據","prior_field":null,"side_a":"2026-05-21 投資人日（CFO）：資本密集度由歷來的 12%–13% 升到中高十幾%；亞利桑那兩期總投資估 70 億美元，第一期 2027 年中完工。","side_b":"2026-10-26 Q3 法說：亞利桑那兩期估 120 億美元，2027 年最多投入 15%（約 18 億），韓國 4–4.5 億、越南 0.5 億，光是廠房就超過 20 億；第一期完工時間改稱 2027 年底；亞利桑那在 2028–29 年見高峰。分析師指出資本支出已超過營收的 30%。","ruling":"可調和，但方向對股東不利。兩期合計投資放大約七成，完工時點後移約半年（沒有超過 12 個月，亞利桑那假設不判削弱）。裁決以後者為準：情境基準 FY2028E EPS 2.90，低於共識的 3.26。資本支出高峰的資金來源，是本次觀望的關鍵限制。","evidence_level":"投資人日與法說會逐字稿（一手）","settle_metric":"2027 年 2 月的資本支出指引與預付款覆蓋率","if_then":["若 2027 資本支出指引超過 40 億美元且未揭露預付款覆蓋 → 不追；已持有則減碼","若預付款覆蓋 2027 廠房投資過半 → 重新進場條件之一成立","反向：若負債/EBITDA 降到 1.5 倍以下，且自由現金流 2028 年轉正 → 解除資本紀律疑慮"],"evidence_refs":[]},{"axis":"管理層 2028 目標與賣方共識","cause":"新證據","prior_field":null,"side_a":"投資人日：2028 年營收 90±5 億美元、毛利率 17.5%±1、EPS 2.50±0.25；投資期內獲利成長刻意慢於營收；目標模型沒有計入亞利桑那第二期，也沒有計入強烈的景氣下行。","side_b":"共識 FY2027E 2.78、FY2028E 3.26，比管理層 2028 目標上緣高 18.5%；Q3 單季毛利率 18.3%，已經超過 2028 目標。","ruling":"可調和，屬程度差異；本次看法比共識悲觀。管理層目標在毛利率上確實保守，但共識可能低估三件事：2027–28 年亞利桑那爬坡費用先計入營業費用（營業利益率稀釋 1%–2%）；2026 年折舊年增中十幾%，2027 年還會再增；2026 年的一次性稅務利益不會重複。基準取 2.90，介於兩者之間。","evidence_level":"投資人日逐字稿（一手）、Koyfin 共識快照","settle_metric":"2027 年 2 月對 2027 年折舊與營業費用的說法、FY2027E 共識修正","if_then":["若 2027 上半年 EPS 年化 ≥2.9 美元 → 基準上調到共識水準","若 FY2027E 共識下修超過 5% → 停止加碼"],"evidence_refs":[]},{"axis":"Q4 財測與發布前共識","cause":"新證據","prior_field":null,"side_a":"發布前市場共識 Q4 營收約 20.5 億美元（搜尋摘要轉述，未核對原文）。","side_b":"Q4 財測營收 19–20 億美元；但運算 Q4 年增超過 50%，缺口來自通訊與消費性的零件短缺。","ruling":"可調和。缺口在低毛利的通訊與消費性，高毛利的運算照指引走。FY1 共識在兩份快照之間修正 0%、近 3 個月 −2.7%，財測公布後的下修可能還沒完全進入賣方模型，因此凍結加碼到 2027 年 2 月。","evidence_level":"搜尋摘要（二手，未核對原文）、共識快照","settle_metric":"2026 年 11–12 月的 FY1／FY2 共識修正","if_then":["若 FY2027E 共識下修超過 5% → 停止加碼","若共識持平且 Q4 營收落在財測上半段 → 解除凍結"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"台積電：對手還是客戶","cause":"新證據","prior_field":null,"side_a":"10-K：IDM 與晶圓代工可以隨時把外包封測轉回自有產能；台積電自建的 CoWoS 拿走最高價值的一段。","side_b":"台積電簽了 10 年期亞利桑那先進封裝協議，據報擴大把 CoW 前段外包給封測廠。","ruling":"可調和：台積電把產能與人力密集、價值較低的段落外包，最高價值段留在自己手上。對 Amkor 來說，這是出貨量的順風，也是價格的上限。","evidence_level":"10-K、產業報導、法說會","settle_metric":"台積電外包給封測廠的段落範圍、Amkor 亞利桑那客戶結構","if_then":["若台積電把 CoWoS 後段也大量外包 → 護城河趨勢可改判擴大","若台積電在美國自建封裝產能 → 亞利桑那假設削弱"],"evidence_refs":["customer_second_source#1"]},{"axis":"自我攻擊：現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買的理由：股價比前份跌 42%、26 週跌 46%，RSI 35.7；現價除以 14 倍，只要求 2028 年 EPS 2.73 美元，而 Q4 財測年化已有約 2.80；運算 2027 年再成長 30% 以上，客戶簽了多年約並預付款項；前份等待的價格區間已經到了。","side_b":"仍要觀望的理由：唯一卡住的是資本支出的報酬。2027 資本支出指引與預付款覆蓋率要到 2027 年 2 月才揭露，在那之前自由現金流為負、槓桿高於目標，股東經濟能否跟上營收成長，現在無法判斷。","ruling":"在 2027 年 2 月 Q4 法說之前無法下定論。關鍵限制是資本支出的資金來源，重新進場條件就是把這個限制反過來寫：預付款覆蓋 2027 廠房投資過半，且 Q4 毛利率 ≥18%。價格不是這次的限制，所以不設進場價。","evidence_level":"法說會、事實表","settle_metric":"2027 年 2 月 Q4 法說","if_then":["若 Q4 毛利率 ≥18% 且預付款覆蓋 2027 廠房投資過半 → 重跑研究，分兩批建立首倉","若 2027 資本支出指引超過 40 億美元且未揭露預付款覆蓋 → 不追，維持觀望到 2027 年 Q1 財報","反向：若法說前股價續跌、運算營收仍照指引兌現 → 不提前建倉，價格不是這次的限制"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 2 月 Q4 法說：Q4 毛利率 ≥18%，且 2027 資本支出指引附上客戶預付款覆蓋廠房投資過半","type":"估值rearm","maps_to":"H2","metric":"Q4 2026 毛利率；2027 資本支出指引；預付款覆蓋率","threshold":"毛利率 ≥18.0%，且預付款覆蓋 2027 廠房投資 ≥50%","action":"條件全部達到 → 重跑研究，分兩批建立首倉；任一未達 → 不追","source_freq":"法說會（每季）","date":"2027-02"},{"n":2,"text":"運算營收 Q4 2026 年增超過 50%，2027 年各季年增 ≥30%","type":"假設驗證","maps_to":"H1","metric":"運算終端市場營收年增率","threshold":"Q4 2026 >50%；2027 各季 ≥30%","action":"連 2 季低於 25% → 停止加碼；連 3 季低於 20% → 減碼","source_freq":"季報（每季）","date":"2027-02"},{"n":3,"text":"管理層把 Q3 毛利率低於財測下緣歸因於匯率與熊本地震（約 60 個基點）；Q4 毛利率若再低於財測下緣，就視為一次性歸因不成立","type":"風險","maps_to":"H2","metric":"Q4 2026 單季毛利率","threshold":"<18.0%","action":"停止加碼，情境基準往空方調整","source_freq":"季報","date":"2027-02"},{"n":4,"text":"通訊與消費性的拖累延長：SiP 搬遷空窗加上記憶體缺貨","type":"風險","maps_to":"R1","metric":"通訊營收年增率","threshold":"連 2 季年減超過 20%，且 2027 上半年 SiP 未回升","action":"減碼","source_freq":"季報（每季）","date":"2027-07","evidence_refs":["supply_demand_durability#3"]},{"n":5,"text":"擴產資金出現缺口：槓桿或流動性惡化","type":"減碼","maps_to":"R2","metric":"負債/EBITDA；總流動性","threshold":"負債/EBITDA >2.0 倍，或總流動性 <20 億美元","action":"減碼","source_freq":"法說會（每季）","date":null},{"n":6,"text":"旗艦 HDFO CPU 專案或 NVIDIA 資料中心 HDFO 專案被轉單、取消或延後","type":"Single Thing","maps_to":"Single Thing","metric":"關鍵運算專案狀態","threshold":"轉單、取消或延後 ≥12 個月","action":"清倉","source_freq":"法說會、8-K、客戶公告（事件型）","date":null},{"n":7,"text":"封裝報價週期反轉","type":"風險","maps_to":"R4","metric":"先進封裝報價；單季毛利率年增減","threshold":"產業報導指出報價轉跌，且毛利率連 2 季年減","action":"減碼","source_freq":"產業報導＋季報","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#3","supply_demand_durability#1"]},{"n":8,"text":"關稅與出口管制的衝擊吸收失敗","type":"風險","maps_to":"R5","metric":"關稅與出口管制造成的毛利率變動；受限營收占比","threshold":"單季毛利率因此下降 ≥100 個基點，或受限營收 ≥5%","action":"減碼","source_freq":"季報、10-K 風險因子","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#1"]},{"n":9,"text":"Q4 財測低於發布前共識的影響進入賣方模型","type":"風險","maps_to":"H1","metric":"FY2027E 共識 EPS 修正","threshold":"近 3 個月下修超過 5%（目前 FY1 近 3 個月 −2.7%）","action":"停止加碼","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#1"]},{"n":10,"text":"Q4 法說後重跑整份研究","type":"複審日期","maps_to":"H2","metric":"全部論點與情境","threshold":"到期即複審","action":"重跑研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"運算終端市場營收年增率","bear_threshold":"連 2 季 <20%（Q3 2026 為 37%）","window":"2027 Q1–Q4","source":"公司季報新聞稿終端市場拆分","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連 2 季 <16.6%（Q3 2026 為 18.3%）","window":"2027–2028","source":"公司季報","last_status":"ok"},{"metric":"負債/EBITDA","bear_threshold":">2.0 倍（Q3 2026 為 1.7 倍）","window":"每季，至 2029 年","source":"法說會 CFO 揭露","last_status":"ok"},{"metric":"旗艦運算專案（HDFO CPU、NVIDIA 資料中心）","bear_threshold":"轉單、取消或延後 ≥12 個月","window":"2026 Q4–2028 Q4","source":"法說會、8-K、客戶公告","last_status":"ok"},{"metric":"總流動性（現金、短期投資與未動用額度）","bear_threshold":"<20 億美元（Q3 2026 為 34 億）","window":"每季，至 2029 年","source":"法說會 CFO 揭露","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027年2月Q4法說：Q4毛利率≥18%，且2027資本支出指引附上客戶預付款覆蓋廠房投資過半","exec_line":"條件成立後先重跑研究，首倉分兩批：法說後建立第一批，運算季增雙位數再確認後建立第二批；建倉後若股價先跌、但運算照指引兌現，分批反買，不停損；Single Thing 發生即清倉。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2027–29 年的資本支出高峰當成股東失血，但十幾家客戶的預付款（分析師估約 30 億美元）承擔了大部分廠房資金。現價只要求 2028 年 EPS 約 2.73 美元，低於共識的 3.26，約等於管理層目標上緣。市場可能錯在把有合約保護的擴產當成投機性擴產；這一點要等預付款覆蓋率揭露才能證實。","momentum_overheated":false,"cycle_gates_pass":false,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月 Q4 法說：Q4 毛利率 ≥18%、運算季增雙位數兌現，且 2027 資本支出指引附上客戶預付款覆蓋率（至少覆蓋廠房投資的一半）；不設進場價。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"AI 運算先進封裝持續放量，運算成為 Amkor 第一大終端市場：運算營收 2026 年增 30% 以上、2027 年相近或更高，先進產品占營收維持 82% 以上。","2y":"2027 全年運算營收年增 ≥30%；Q4 2026 運算年增超過 50%；網通與資料中心兩個 2.5D 專案自 Q4 2026 起量產；超大規模雲端業者的第二個 HDFO CPU 專案放量","5y":null,"10y":null,"threshold":"運算營收季度年增率 ≥30%；先進產品占營收 ≥82%（Q3 2026 為 82.0%）","source":"公司季報新聞稿的終端市場拆分、法說會（每季）","drift_rule":"運算年增率比門檻低 5 個百分點以上（<25%）連 2 季 → 削弱；低 10 個百分點以上（<20%）連 3 季 → 反轉"},{"id":"H2","text":"產品組合把毛利率結構性墊高，且擴產賺得到報酬：單季毛利率守在 17.5% 以上，亞利桑那 2029 年前後損益兩平，客戶預付款支應大部分廠房投資，負債/EBITDA 回到 1.5 倍以下。","2y":null,"5y":"2028 年毛利率 ≥17.5%（管理層目標），2030 年朝 22% 邁進；亞利桑那第一期 2027 年底完工、2028 年量產、2029 年損益兩平；2029 年以後自由現金流轉正","10y":null,"threshold":"單季毛利率 ≥17.5%（Q3 2026 為 18.3%，Q4 財測 18%–19%）；負債/EBITDA ≤2.0 倍（Q3 為 1.7 倍）","source":"季報、法說會、10-K 現金流量表與預付款揭露","drift_rule":"單季毛利率比 17.5% 低 5% 以上（<16.6%）連 4 季 → 削弱；低 10% 以上（<15.75%）連 6 季 → 反轉；亞利桑那完工延後超過 12 個月 → 削弱"},{"id":"H3","text":"客戶結構分散化加上地理稀缺：前十大客戶占比持續下降、單一客戶低於 25%，台灣以外（韓國）與美國本土的先進封裝產能形成長期溢價。","2y":null,"5y":null,"10y":"2030 年前十大客戶 ≤60%、單一客戶 ≤25%；亞利桑那兩期（約 120 億美元）全數投產，成為第二大基地；運算占營收過半","threshold":"前十大客戶占比 ≤66%（Q3 2026，去年同期 73%）且逐年下降；Apple 直接銷售占比低於 29.8%（2025 年水準）","source":"10-K 客戶集中度揭露（每年）、季報的前十大客戶占比","drift_rule":"前十大客戶占比跨 2 個年度回升 → 削弱；跨 3 個年度回升，或任一客戶超過 30% → 反轉"}],"R":[{"id":"R1","text":"通訊與消費性的拖累超過預期：SiP 由韓國移到越南的空窗、記憶體缺貨與漲價，壓低手機與穿戴裝置出貨。Q4 通訊預期季減高個位數、消費性季減中十幾%，Android 與 iOS 都在下滑。","h_ref":"H2","clock":"⚡","threshold":"通訊營收連 2 季年減超過 20%，且 2027 上半年 SiP 未見回升 → 減碼","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"資本支出黑洞：2027 年資本支出再跳升（光是廠房就超過 20 億美元），亞利桑那總投資估計由 70 億升到 120 億美元、2028–29 年見高峰。自由現金流連年為負，如果預付款不夠，就得增債或稀釋股權。","h_ref":"H2","clock":"🔥","threshold":"負債/EBITDA 超過 2.0 倍（Q3 為 1.7 倍），或總流動性低於 20 億美元（Q3 為 34 億），或 2027 資本支出指引超過 40 億美元且未揭露預付款覆蓋 → 減碼","evidence_refs":[]},{"id":"R3","text":"客戶集中與轉單：Apple 占 29.8%、Qualcomm 占 11.1%，前十大占 66%–72%。IDM 與晶圓廠可以轉回自有產能，失去大客戶或被大客戶降價，會對營收與流動性造成重大影響；中國政府支持、資金成本較低的業者也在搶單。","h_ref":"H3","clock":"🐢","threshold":"任一前五大客戶公告轉單或份額下滑，或前十大占比回升到 72% 以上、同時運算成長放緩 → 減碼","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#0","competitive_share_entrants#1"]},{"id":"R4","text":"封裝報價週期反轉：日月光 2026 年資本支出約 105 億美元、六座新廠動工，台積電 CoWoS 缺口在收斂；2027–28 年新供給開出後漲價反轉，毛利率回到 14%–15%。","h_ref":"H2","clock":"🔥","threshold":"產業報導指出先進封裝報價轉跌，且 Amkor 毛利率連 2 季年減 → 減碼","evidence_refs":["cyclical_supply_discipline_capacity#0","supply_demand_durability#1"]},{"id":"R5","text":"關稅與出口管制的衝擊吸收失敗：廠房幾乎全在美國以外，公司自述無法預測美國的關稅與出口管制政策，非美國競爭者可能豁免。","h_ref":"H3","clock":"🐢","threshold":"單季毛利率因關稅或出口管制下降 ≥100 個基點，或公司揭露受限營收 ≥5% → 減碼","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#1","geo_supply_chain#0","geo_supply_chain#2"]}],"single_thing":{"description":"旗艦 HDFO CPU 專案，或 NVIDIA 資料中心 HDFO 專案（韓國光州新廠與預付款的主要對象），任一被客戶轉單、取消或延後 12 個月以上。","why_fatal":"2027 年運算再成長 30% 以上，主要靠這幾個關鍵專案（Q3 法說 CEO：最大的驅動力是關鍵專案，其他專案規模小得多），韓國擴產與亞利桑那都是為它們蓋的。CEO 說資產可以轉用，但也承認「這個客戶的規模很難補」。EPS 對這件事的敏感度大於任何單一終端市場：一旦失去，2028 年 EPS 會由基準的 2.90 掉到空方路徑的 1.70，而折舊照樣要提。","if_happens":"清倉；情境改走空方路徑（FY2028E 1.70、倍數 10 倍），重跑研究之前不重新建倉。","how_monitor":"每季運算營收季增率，以及管理層對關鍵專案的說法；客戶與台積電、日月光的產能公告；預付款合約的異動（8-K）。","probability":"約 15%（12–24 個月內）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.8,"peg_fy2":0.97,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":1.5,"FY2026E":2.5,"FY2027E":2.78,"FY2028E":3.26},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（公司不揭露 non-GAAP 營業利益）；FY1 為 2026 年度，取 Koyfin 2026-10-31 快照"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與法說：2027 資本支出指引、客戶預付款進度","impact":"高","watch":"資本支出指引、預付款覆蓋率、Q4 毛利率是否 ≥18%"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"韓國松島新的組裝測試大樓完工，擴充測試產能","impact":"中","watch":"2027 上半年車用與資料中心的測試營收"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"亞利桑那第一期廠房完工、開始移入設備，2028 年量產","impact":"高","watch":"是否延後；開始認列的折舊與爬坡費用金額"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"高密度扇出橋接封裝量產（2027 年底到 2028 年）","impact":"中","watch":"客戶是否如期量產、對運算營收的貢獻"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2027–29 年的資本支出高峰當成股東失血，但十幾家客戶的預付款（分析師估約 30 億美元）承擔了大部分廠房資金。現價只要求 2028 年 EPS 約 2.73 美元，低於共識的 3.26，約等於管理層目標上緣。市場可能錯在把有合約保護的擴產當成投機性擴產；這一點要等預付款覆蓋率揭露才能證實。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-45.95, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年 2 月 Q4 法說：Q4 毛利率 ≥18%、運算季增雙位數兌現，且 2027 資本支出指引附上客戶預付款覆蓋率（至少覆蓋廠房投資的一半）；不設進場價。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
