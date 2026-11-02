你是 DD 管線 v20 的判斷層閘（gate），標的 AENA（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_total_consolidated_reven`（q1_business）｜Total consolidated revenue (9M)＝5283.9 EUR m｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿 https://www.aena.es/en/press/aena-earns-a-profit-of-1774.7-million-euros-in-the-first-nine-months-of---2026.html（numbers.latest_quarter_kpis.items[0]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_kpi1_ebitda_9m`（q1_business）｜EBITDA (9M)＝3077.9 EUR m｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[1]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_kpi2_net_profit_9m`（q1_business）｜Net profit (9M)＝1774.7 EUR m｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[2]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_kpi6_passengers_group`（q1_business）｜Passengers (Group)＝309.9 m pax｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[6]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_peer_aena_gross_margin_pct`（q2_moat）｜AENA 毛利率＝74.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AENA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aena_operating_margin_pct`（q2_moat）｜AENA 營業利益率＝47.51 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AENA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aena_fcf_margin_pct`（q2_moat）｜AENA FCF 利潤率＝15.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AENA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_asr_operating_margin_pct`（q2_moat）｜ASR 營業利益率＝40.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_asr_fcf_margin_pct`（q2_moat）｜ASR FCF 利潤率＝23.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pac_operating_margin_pct`（q2_moat）｜PAC 營業利益率＝43.29 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PAC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pac_fcf_margin_pct`（q2_moat）｜PAC FCF 利潤率＝14.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PAC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi5_net_financial_debt_net_d`（q1_business）｜Net financial debt / Net debt-to-EBITDA＝5845 EUR m（1.47x EBITDA）｜期間與口徑：2026-09-30，公告於 2026-10-28／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[5]，as_of 2026-09-30，公告於 2026-10-28）
  - 註記：查無
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.74 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.82 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.88 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6903.97 EUR m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7241.12 EUR m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_net_operating_cash_flow_`（q1_business）｜Net operating cash flow (9M)＝2811.3 EUR m｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[3]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_kpi4_investment_paid_capex_au`（q1_business）｜Investment paid (capex, 含 Augusta 51% 股權 343.5)＝1133.5 EUR m｜期間與口徑：9M 2026（截至 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Aena IR 新聞稿（同上）（numbers.latest_quarter_kpis.items[4]，as_of 9M 2026（截至 2026-09-30，公告於 2026-10-28））
  - 註記：查無
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝5376.41 EUR m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 7933.87、現金 2557.46（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1500.0 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.949 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝27.6 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.56 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 1.74，分子＝快照價 27.08｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝13.73 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝14.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝14.7 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.08 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.87 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.78 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-4.4 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 1.82 → 1.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 27.08 / W52 24.94 / W104 22.94 / W250 17.25 / W250 13週斜率 1.31%」
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝21.16 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝68.52｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=False｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Ryanair 因 Aena 2026 年機場費調漲（約 6.5%）宣布夏季 2026 再砍西班牙區域機場 120 萬座位；Valladolid 旅客 -59.5%（至7月）、Santiago -13.3%，Vigo +10.2%、Zaragoza +2.9% 部分抵銷（來源為 Idealista 報導，2025 年資料）
  - 來源：Idealista - Ryanair Spain news: 1.2m seats cut as Aena row intensifies（as_of 2025-09-15）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Aena 對 Ryanair 依賴高：西班牙媒體稱約每 10 位 Aena 機場旅客有 2 位搭 Ryanair；Ryanair 2025 年在 Aena 西班牙機場載客 13.3 百萬人（媒體報導，非 Aena 官方分航空公司揭露）。
  - 來源：Vozpópuli, Ryanair dispara su dominio en los aeropuertos españoles（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：Ryanair 因費率爭議削減西班牙運力（報導稱取消 12 條航線、80 萬座位），Valladolid、Santiago 受衝擊最大；easyJet 等部分填補。
  - 來源：Vozpópuli / Menorca.info 報導（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：CNMC 於 2026-06-02 建議 DORA III（2027-2031）機場費率每年下調 0.59%，Aena 原提案為每年上調 3.82%；WACC 由 9% 降至 7.4%，OPEX 減 741.5 百萬歐元；最終由部長會議決定。
  - 來源：RTVC: La CNMC propone rebajar las tasas aeroportuarias hasta 2031（as_of 2026-06-03）｜affects：valuation、thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026 摘要：2026 客運成長約 3%，H2 能見度有限，受地緣與經濟不確定、燃油避險到期、載客率轉弱影響
  - 來源：Quartr: Aena SME Q2 2026 earnings summary（as_of 2026-07-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：產業層級單點失效：2025年9月 Collins Aerospace 報到系統遭攻擊，單一供應商失效波及多個歐洲機場；OT-ISAC 2026年8月報告將第三方集中風險評為高。未找到 Aena 自身供應商集中揭露
  - 來源：OT-ISAC report (Aug 2026)（as_of 2026-08-31）｜affects：thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：競爭主管機關 CNMC 呼籲政府確保 Aena 在 2031 年前降低機場收費（DORA III 監管不確定性）
  - 來源：thecorner.eu（as_of 2026-06-01）｜affects：thesis.R、valuation、decision_inputs.bear
- `regulated_rate_case_roe#0`（regulated_rate_case_roe｜方向 -｜狀態 ok）：CNMC 2026-06-02 報告建議 DORA III（2027–2031）WACC 由 Aena 主張的 9% 降至 7.44%，平均年費率 -0.59%（Aena 申請 +3.82%）；為建議非定案
  - 來源：CNMC 新聞稿 informe DORA 2026-06-02（經搜尋摘要）（as_of 2026-06-02）｜affects：valuation、thesis.R、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":42.3,"bear_5y_price":19.7,"p_bull_pct":22,"p_bear_pct":30,"upside_5y_pct":10.3,"ev5y_pct":8.1,"irr_base_pct":2.0,"asym_ratio":1.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.74,"pe":15.86,"basis":"FY2026E 共識 EPS 1.74（Koyfin 美元口徑）對判斷日股價 27.6；終端倍數同樣以終端年的當年 EPS 為分母"},"eps":{"bull":[1.87,1.98,2.1,2.22,2.35],"base":[1.82,1.88,1.93,1.98,2.03],"bear":[1.72,1.66,1.62,1.62,1.64]},"pe":{"bull":18,"base":15,"bear":12},"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":3.949,"net_buyback":0},"second_stage":{"bull_cagr_pct":5,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### AENA_2025_Earnings_Call_20260225.md
- 2026-02-25｜CEO｜guidance：CEO 說明 2026 年西班牙客流預估成長 1.3%，稱為自然預估。（原話："increase of 1.3% and to us, this is a natural estimate"）
- 2026-02-25｜CEO｜risk：CEO 說明部分機場接近技術上限，2026 年起特定日子會有容量限制。（原話："face constraints because the infrastructure"）
- 2026-02-25｜CEO｜guidance：CEO 說明政府須在 2026 年 9 月前核定最終 DORA III。（原話："a deadline in September 2026 to approve the definitive DORA III."）
- 2026-02-25｜CEO｜capital_allocation：CEO 說明 DORA III 下受管制資產基礎預計增加逾 55 億歐元。（原話："our regulated assets base in more than EUR 5.5 billion."）
- 2026-02-25｜CEO｜guidance：CEO 說明 DORA III 提案的平均費率每年上調約 0.43 歐元。（原話："is just EUR 0.43 every year."）
- 2026-02-25｜CEO｜commitment：CEO 承諾西班牙機場費率仍將是歐洲最具競爭力。（原話："and this is a commitment that we will"）
- 2026-02-25｜CFO｜margin：CFO 報告 2025 年 EBITDA 利潤率 59.3%，較 2024 年低 90 bp。（原話："EBITDA margin of 59.3%, 90 basis points lower than in 2024."）
- 2026-02-25｜CFO｜margin：CFO 說明排除 IFRIC 12 影響後，集團 EBITDA 利潤率為 61.4%，改善 50 bp。（原話："would have improved by 50 basis points to 61.4%."）
- 2026-02-25｜CFO｜margin：CFO 報告集團營運費用成長 11.1%。（原話："operating expenses at group level grew by 11.1%"）
- 2026-02-25｜CFO｜margin：CFO 說明排除巴西 IFRIC 12 後集團營運費用增幅為 4.9%。（原話："would be 4.9% for the whole group."）
- 2026-02-25｜CFO｜margin：CFO 說明人事費用成長，並表示將持續增加全職人力。（原話："adding more FTEs to the company in many different fronts"）
- 2026-02-25｜CFO｜guidance：CFO 表示人事費用的上升趨勢預期不會改變。（原話："we don't expect a different change in this trend"）
- 2026-02-25｜CFO｜competition：CFO 稱 Aena 每位旅客營運費用在可比機場業者中最低。（原話："we are the lowest by far."）
- 2026-02-25｜CFO｜guidance：CFO 表示營運費用項目將在近期持續受衝擊。（原話："will be impacted in the near future."）
- 2026-02-25｜CFO｜guidance：CFO 對 2026 年折舊攤銷的指引：水準與 2025 年相近。（原話："a very similar level of depreciation and amortization for 2026"）
- 2026-02-25｜CFO｜margin：CFO 說明資產耐用年限調整的折舊節省明年會較低、非經常性。（原話："next year will be a bit lower."）
- 2026-02-25｜CEO｜capital_allocation：CEO 說明 2025 年股利提案為每股 1.09 歐元（毛額）。（原話："payment of a gross dividend of EUR 1.09 per share."）
- 2026-02-25｜CFO｜capital_allocation：CFO 報告集團淨債務對 EBITDA 為 1.46。（原話："net debt to EBITDA ratio of the group stood at 1.46"）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明若計入巴西短期存款，槓桿比率約 1.35–1.36。（原話："the ratio of 1.46 would be around 1.35, 1.36."）
- 2026-02-25｜CEO｜capital_allocation：CEO 提到 2025 年 12 月取得英國 Leeds 與 Newcastle 機場的重要持股。（原話："we acquired a significant participation in the U.K."）
- 2026-02-25｜CEO｜commitment：CEO 表示長期希望西班牙與國際業務有更均衡的結構。（原話："a better balance between Spain and the rest"）
- 2026-02-25｜CFO｜customer：CFO 說明 2025 年西班牙客流成長主要來自國際市場，內需小幅下降。（原話："International markets grow at circa 6%"）
- 2026-02-25｜CFO｜product：CFO 說明商業與不動產收入首度突破 20 億歐元。（原話："this is the first year in which we were able to exceed"）
- 2026-02-25｜CFO｜product：CFO 說明免稅有一個分區營收仍比最低保證租金（MAG）短少約 10%。（原話："And we were short by around 10% in"）
- 2026-02-25｜CFO｜product：CFO 報告 VIP 貴賓室服務總營收成長 31.5% 至 1.04 億歐元。（原話："by 31.5%, reaching to EUR 104 million."）
- 2026-02-25｜CEO｜guidance：管理層表示新廣告標案的財務影響要到 2028 年才反映。（原話："would really happen in 2028"）
- 2026-02-25｜CEO｜guidance：管理層表示巴塞隆納餐飲標案的財務影響將在 2026 年反映。（原話："will be seen in 2026 because of all the MAGs"）
- 2026-02-25｜CEO｜guidance：管理層對 2026 年免稅表現表示有信心，將反映帕爾馬新店開幕。（原話："We are confident that a duty-free line for 2026"）
- 2026-02-25｜CEO｜customer：管理層說明特許零售店受電商衝擊最大。（原話："because of disruption of e-commerce, et cetera."）
- 2026-02-25｜CEO｜margin：管理層說明免稅第四季表現較弱，部分來自年底 MAG 的會計調整。（原話："There might be some accounting adjustment"）
- 2026-02-25｜CFO｜margin：CFO 說明航空收入稀釋金額未來將回收。（原話："will be recovered in a couple of years"）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明 Luton 目前承諾的資本支出以維護為主，限制有限。（原話："So limited CapEx on that front."）
- 2026-02-25｜CFO｜capital_allocation：CFO 說明是否參與 Luton 擴建尚未談定。（原話："it has not been resolved yet."）
- 2026-02-25｜CFO｜commitment：CFO 說明巴西 Congonhas 機場工程預定 2028 年 6 月完成。（原話："deliver all those construction works in June 2028"）
- 2026-02-25｜CEO｜risk：CEO 對政治干預風險表示有信心不會再發生。（原話："I'm very confident that this won't happen again"）
- 2026-02-25｜CFO｜risk：CFO 回答 AI 對客流影響時表示管理層會持續追蹤。（原話："it is something that as a company, we are following"）

### AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260416.md
- 2026-04-16｜Maurici Betriu｜guidance：管理層重述西班牙網絡 2026 年客運量公開預測（原話："traffic increase in Spain is of 1.3% in terms of passengers"）
- 2026-04-16｜Maurici Betriu｜guidance：管理層表示地緣與經濟不確定性消退後須重新評估該預測（原話："we will need to reassess that forecast"）
- 2026-04-16｜Maurici Betriu｜guidance：管理層預期未來數年西班牙客運成長較近年和緩（原話："it is to be expected that there will be more moderate growth"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案載明 2031 年西班牙機場客運量預測（原文數字如此）（原話："a focus of 1.69 billion passengers in"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案營運費用年增率（原話："an increase of OpEx of 3.8% per"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案 WACC（原話："Aena proposes a 9%."）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 提案每位旅客平均費率調升幅度（原話："increasing airport fees for on average by EUR 0.43"）
- 2026-04-16｜Maurici Betriu｜guidance：DORA III 尚待內閣核准，管理層預期會有修改（原話："which probably will undergo some modifications"）
- 2026-04-16｜Maurici Betriu｜guidance：2026 Q1 業績發布時點（原話："we will be presenting the results of the first quarter"）
- 2026-04-16｜Maurici Betriu｜margin：2025 合併 EBITDA margin 口徑：合併而非單體（原話："margin, not the stand-alone margin, was 59.3%"）
- 2026-04-16｜Maurici Betriu｜margin：2025 營運費用年增，列舉驅動項（原話："11% increase versus 2024, driven by personnel, services"）
- 2026-04-16｜Maurici Betriu｜margin：商業與不動產收入首度超過 20 億歐元（原話："Group exceeded EUR 2 billion, which is a significant figure"）
- 2026-04-16｜Maurici Betriu｜margin：不動產收入年增與驅動項（原話："revenues of 10.5%, driven by air cargo activity"）
- 2026-04-16｜Maurici Betriu｜margin：2025 淨利與年增幅（原話："almost EUR 2,136.7 million, 10.5% higher than in 2024"）
- 2026-04-16｜Maurici Betriu｜margin：國際業務占合併 EBITDA 比重（原話："international activity represented more than 10% of"）
- 2026-04-16｜Maurici Betriu｜margin：管理層說明 DORA III 營運費用增加的理由之一：新投資週期（原話："We need more human resources for the new investment cycle"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：DORA III 五年總投資規模（原話："a total investment of nearly EUR 13 billion"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：DORA III 受管制年投資相對 DORA I/II 法定上限的倍數（原話："4.4x the current legal maximum investment of DORA I"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：2025 淨財務負債對 EBITDA（原話："decreased to 1.31x in 2025"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：管理層稱財務體質為新投資週期起點（原話："starting point for the new investment cycle"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：建議 2025 年度股利與年增幅（原話："2025 earnings, 11.7% more than last year"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：發行 10 年期公司債（原話："successful issuance of a 10-year Aena bond in"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：巴西第二特許權債券融資（原話："debenture issue worth BRL 5.3 billion underwritten by"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：國際併購紀律：選擇性新增資產（原話："selective addition of new international assets based on"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：宣布收購 Leeds Bradford 與 Newcastle 持股公司（原話："acquisition of 51% stake in a new holding company that owns"）
- 2026-04-16｜Maurici Betriu｜capital_allocation：取得里約 Galeão 特許權（原話："the award of the 13-year concession for"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層承諾維持 80% 派息率（原話："payout ratio of 80% of net income"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層希望在年底前的策略計畫中確認派息率（原話："we hope to be able to confirm this in the strategic plan"）
- 2026-04-16｜Maurici Betriu｜commitment：管理層對投資計畫與債務成本的信心表述（原話："I am confident that in the coming years, Aena will be able"）
- 2026-04-16｜Maurici Betriu｜commitment：光電計畫 2029 年目標及進度慢於先前說法（原話："produce renewable energy equivalent to 51% of Aena's 2019"）
- 2026-04-16｜Maurici Betriu｜competition：航空公司壓低機場費率的壓力；管理層稱之為不負責任（原話："the irresponsible pressure backed by"）
- 2026-04-16｜Maurici Betriu｜competition：費率修正案曾試圖凍結 DORA III 期間機場費（原話："sought to arbitrarily freeze airport fees"）
- 2026-04-16｜Maurici Betriu｜competition：管理層引用 2015–2025 實質費率降幅（原話："a 37% drop in airport fees in 11 years in real"）
- 2026-04-16｜Maurici Betriu｜customer：管理層引用 IATA 資料：歐洲航空公司每位旅客收入增幅（原話："increased by almost 27%, i.e., EUR 40 per person"）
- 2026-04-16｜Maurici Betriu｜customer：西班牙國內線客運 2025 年幾乎持平（原話："national traffic was virtually flat"）
- 2026-04-16｜Maurici Betriu｜risk：管理層表示部分自治區要求共管機場構成重大風險（原話："pose significant risks for the Spanish airport system"）
- 2026-04-16｜Maurici Betriu｜risk：巴斯克雙邊機場機構僅屬諮詢性質（管理層說法）（原話："is strictly consultative and not a"）
- 2026-04-16｜Maurici Betriu｜risk：西班牙客運成長受部分基礎設施容量限制（原話："constraints in some of Aena's infrastructure that could"）
- 2026-04-16｜Maurici Betriu｜risk：中東戰爭對航空的直接影響目前小（原話："the direct impact of the war in Iran and the Middle East"）
- 2026-04-16｜Maurici Betriu｜risk：DORA III 期間債務上升後對總經變動更敏感（原話："we will be more exposed in the future years to macroeconomic"）
- 2026-04-16｜Maurici Betriu｜risk：累計費率缺口（交通量風險由 Aena 承擔）（原話："Aena bears the so-called traffic risk"）
- 2026-04-16｜Maurici Betriu｜risk：累計收入缺口金額（原話："accumulated by and exceeds EUR 550 million"）
- 2026-04-16｜Maurici Betriu｜product：管理層首度提到 AI 可能聚焦 Aena 管理（原話："AI will focus on the management of Aena"）
- 2026-04-16｜Maurici Betriu｜product：光電計畫速度慢於兩年前說法，歸因外部因素（原話："we said that we would have wanted that"）

### AENA_2026_20260729.md
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：2026 西班牙網絡旅客成長管理層估約 3%（原話："could be around 3% compared with 2025."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管理層稱對 2026 冬季季無能見度（原話："we still don't have visibility on the 2026 winter season"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管理層稱載客率弱於座位運能成長（原話："we are observing weaker load factors"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：荷莫茲危機後旅客轉向西班牙（原話："a diversion of traffic towards Spain has been observed as"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜margin：報告 EBITDA 利潤率 54.5% 對 56.5%（原話："The reported EBITDA margin was 54.5% compared with 56.5%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜margin：排除 IFRIC 12 與 Luton 保險補償後可比 EBITDA 利潤率（原話："the comparable EBITDA margin would have been 56.9%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：DORA III 最終由部長會議核准時程（原話："final DORA by the Council of Ministers by 30 September 2026"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：Rio de Janeiro 機場收購金額（原話："equivalent to approximately EUR 490 million"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜product：首批機場酒店地面權授標（原話："first hotel developments within the Spanish airport network"）
- 2026-07-29｜CFO (Castejon)｜guidance：下半年成本增幅預期與上半年相近（原話："we don't see reasons to have cost increases materially"）
- 2026-07-29｜CFO (Castejon)｜margin：管理層拆解上半年母公司其他營運費用增項（原話："related to maintenance, 21.5% increase"）
- 2026-07-29｜CFO (Castejon)｜margin：商業總業務每旅客成長數字（原話："total business per pax of 5.4% this quarter and 4.7%"）
- 2026-07-29｜CFO (Castejon)｜customer：特許店新標 MAG 較 2025 增幅（原話："The award MAGs implied an increase versus 2025 of 82%"）
- 2026-07-29｜CFO (Castejon)｜customer：F&B 新標 MAG 增幅（原話："MAG increases of 11% for 2027 and 37% for 2028"）
- 2026-07-29｜CFO (Castejon)｜customer：免稅帳列收入大致持平（原話："reported duty-free revenue was broadly flat"）
- 2026-07-29｜CFO (Castejon)｜customer：僅加那利群島免稅標超過 MAG（原話："The one in Canary Islands is above."）
- 2026-07-29｜CFO (Castejon)｜customer：馬德里與加泰隆尼亞免稅仍遠離 MAG（原話："Madrid and Catalonia, we are still far from being able"）
- 2026-07-29｜CFO (Castejon)｜risk：出入境系統可能壓抑地中海沿岸免稅表現（原話："duty-free business might have been impacted"）
- 2026-07-29｜CFO (Castejon)｜customer：VIP 服務定價能力（原話："We still have pricing power in many fronts."）
- 2026-07-29｜CFO (Castejon)｜capital_allocation：非管制 CapEx 約 30 億主要用於停車場擴容（原話："those EUR 3 billion are mainly explained by car parks"）
- 2026-07-29｜CFO (Castejon)｜commitment：股利政策 80% 配息不偏離（原話："dividend policy of 80% of payout"）
- 2026-07-29｜CFO (Castejon)｜commitment：DORA 後才更新股利政策（原話："we'll have a whole new set of plans for the company."）
- 2026-07-29｜CFO (Castejon)｜commitment：不預期信用評級惡化（原話："we are not expecting a deterioration or deviation from the"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：策略計畫年底前完成（原話："we'll be done before the end of the year"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：K、P 因子將在策略計畫前公布（原話："you will know those figures before the strategic plan"）
- 2026-07-29｜CFO (Castejon)｜risk：P 因子不一定能 100% 轉嫁通膨（原話："we are not completely optimistic of being able to"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：CapEx 計畫總額 130 億（原話："our CapEx program will be EUR 13 billion"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：管制 CapEx 超支由 Aena 承擔（原話："if we increase that, it's on our side"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：未投滿 100 億須退回 DORA IV（原話："we'll have to give that money back to"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜guidance：2027 起基期較高但長期成長率受限（原話："we'll start at a higher level in 2027"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜capital_allocation：目前不看新併購（原話："we are not looking at any operation"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：巴塞隆納擴建的行政核准不由 Aena 掌控（原話："many approvals that do not depend on Aena"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：對 Ryanair 公開批評（原話："They are never happy with airport charges."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：Barajas 環境許可容量（原話："to grow up to 120 operations per hour"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜competition：對 easyJet 可能被收購（原話："we are not concerned about that at this"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜risk：新冠 MAG 租金爭議（原話："It's not illegal what we are doing."）
- 2026-07-29｜CFO (Castejon)｜margin：Luton 利潤率下滑原因（原話："the end of the special force majeure"）
- 2026-07-29｜CFO (Castejon)｜margin：ANB 利潤率（原話："the EBITDA margin improved as well, from 58% to 60%"）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：Congonhas 工程完工時程（原話："The completion, as I have said, for the Congonhas airport"）
- 2026-07-29｜CFO (Castejon)｜capital_allocation：淨負債/EBITDA 上升原因含股利（原話："EUR 1.6 billion going to our shareholders."）
- 2026-07-29｜Executive Vice Chairman (Marin)｜commitment：對 DGAC 不施壓（原話："we must not press the regulator in this process"）
- 2026-07-29｜CFO (Castejon)｜risk：商業營運商壞帳準備（原話："bad debt provisions that we have to"）

### AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA III（2027–2031）核定 WACC 為 2.32%（原話："has been finally set at 2.32%"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA III 年均機場收費漲幅 0.33%（原話："the average annual airport charges increase will be 0.33%"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜guidance：DORA 假設西班牙機場網絡 2031 年旅客數達 3.63 億（原話："will reach 363 million passengers in 2031"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：核定受管制投資計畫接近 100 億歐元（原話："regulated investment plan amounts to almost EUR 10 billion"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：含非受管制商業投資，總投資接近 130 億歐元（原話："the total investment will reach almost EUR 13 billion"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：DORA III 受管制成本以2026年固定價格計，2027年19.29億歐元升至2031年20.79億歐元（原話："from EUR 1,929 million in 2027 to EUR 2,079 million in 2031"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：2025年受管制成本為16.5億歐元，DORA III起點重設至19.29億（原話："the figure was EUR 1,650 million"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：管理層解釋成本重設原因：環保、安全、資安規範趨嚴與通膨、基本工資上調（原話："So doing the same costs more money"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜margin：受管制OpEx對ATU比率年增近2%（原話："the ratio of OpEx to ATUs will increase almost 2% annually"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜commitment：新策略計畫（2027–2031）將於年底前發布（原話："before the end of the year, our new strategic plan"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜commitment：董事長預告策略計畫中的財務目標企圖心偏高（原話："I can anticipate will be high in many of the financial targets"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：管理層列出兩大優先事項：OpEx 與 CapEx 執行，並稱兩者與過往 DORA 明顯不同（原話："One is OpEx. Two is the CapEx execution."）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長形容本期 DORA 具挑戰性與高要求（原話："it is challenging, it is demanding"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：董事長稱核定投資使受管制業務價值提高，但需達成各項要求才能實現（原話："Aena's value is higher after the approval of DORA III"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜capital_allocation：管理層表示投資增加將使債務大幅上升（原話："Our debt will increase significantly."）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜product：馬德里與巴塞隆納主要擴建多數在 DORA IV 交付，容量全面釋放在 DORA IV（原話："the whole capacity will be delivered in DORA IV"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜commitment：管理層承諾投資不超過核定的 100 億歐元（原話："We are not going to invest more than it has been approved"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜capital_allocation：彈性工具：各機場只需執行核定投資額的 80%（原話："to comply with 80% of the investment that has been approved"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：策略性投資占 CapEx 計畫 40%–50%，須依時程執行（原話："between 40% and 50% of the CapEx program"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：策略性投資未達標可能受罰，因此超支時先動非策略項目（原話："you can receive a penalty"）
- 2026-09-21｜CFO (Ignacio Castejón)｜risk：已發包的 CapEx 比例仍很低（原話："It's still very low, still very low."）
- 2026-09-21｜CFO (Ignacio Castejón)｜commitment：CFO稱公司工程招標一向要求固定價格（原話："with fixed prices in order to avoid last-minute surprises"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜risk：Tenerife South 航廈標案無人投標，技術部指市場評估的風險高於預期（原話："the risk that the market has assessed in this project"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長承認 Tenerife 流標不是好消息，但稱因國家持股透明度才被公開（原話："it leaves you a bad taste in the mouth"）
- 2026-09-21｜Maurici Lucena (Chairman/CEO)｜risk：董事長稱 Tenerife 流標情況並不令人擔憂（原話："this is not worrying"）
- 2026-09-21｜Javier Marin (Executive Vice Chairman)｜guidance：通膨保護沿用法規定義的 P 因子；過渡期 1% 上限已不適用（原話："Now those limitations do not apply at this moment."）
- 2026-09-21｜CFO (Ignacio Castejón)｜capital_allocation：非受管制 CapEx 的節奏請比照受管制 CapEx 建模，其餘留待策略計畫（原話："expect something similar to regulated CapEx"）
- 2026-09-21｜CFO (Ignacio Castejón)｜risk：CFO稱將檢視公司提交的OpEx假設與核定版差異，並指出有履約不及的高風險項目（原話："a high risk of not being able to perform"）
- 2026-09-21｜Carlos Gallego (IR)｜commitment：下次財報為10月底的2026前9個月業績（原話："at the end of October"）

### 問答異常語氣（迴避／改口／保留）
- AENA_2025_Earnings_Call_20260225.md｜問：JPMorgan 請管理層給出 2026 與 DORA III 期間 OpEx 增幅的量級與分項拆分。｜答法：CFO 回顧 2025 年人事與其他營運費用的成因，說趨勢會延續，但未給 2026 年或 DORA III 的 OpEx 增幅數字。
- AENA_2025_Earnings_Call_20260225.md｜問：BNP 追問 2026 年航空業務 D&A 預期。｜答法：CFO 先回答折舊節省『顯著低於 6,800 萬歐元』，被追問後才改說總 D&A 水準與 2025 年相近，首答與提問口徑不一致。
- AENA_2025_Earnings_Call_20260225.md｜問：UBS 問 DORA III 客流預測是否納入 AI 導致白領失業的風險，以及是否與監管機關討論。｜答法：管理層未直接回答預測是否納入，改談市場情緒，並稱與監管機關的討論保密，不透露細節。
- AENA_2025_Earnings_Call_20260225.md｜問：Santander 問免稅與特許零售店每位旅客營收放緩的趨勢。｜答法：管理層回應偏向解釋（會計調整、淡季、電商），未提供每位旅客營收的具體數字。
- AENA_2026_20260729.md｜問：Bank of America 問 2027 關稅 K 因子與 P 因子最佳估計｜答法：說有內部計算但因程序不能公布，不給數字
- AENA_2026_20260729.md｜問：UBS 問固定加變動股利及 Aena S.M.E 可接受的最高槓桿｜答法：不給槓桿上限數字，推到 DORA 後的策略計畫
- AENA_2026_20260729.md｜問：Santander 問 2028 P 因子是否反映今年約 10% 的西班牙 OpEx 通膨｜答法：表示不願斷言轉嫁，未給估計
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Bernstein：最終核定成本比初始假設低約10%，是否意外、差異在哪、如何控制成本｜答法：CFO 只回答 CapEx 招標部分，OpEx 差異未給數字，延後到策略計畫（請「給我們幾週」）
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Jefferies：非受管制 CapEx 的節奏與零售投資的價值上行時點｜答法：CFO 表示留待策略計畫，只給 CapEx 節奏類似受管制一句，未回答價值上行
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：Deutsche Bank：已發包 CapEx 佔比｜答法：只答「still very low」，未給百分比
- AENA_Shareholder_Analyst_Call_Aena_S_M_E_S_A_20260921.md｜問：BNP：標價高於預期時 100 億總額是否增加或順延至 DORA IV｜答法：回答不超投資，但同時承認價格、部分專案仍有不確定性，並稱可能將部分投資延至 DORA IV

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | none | 0 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |
| regulated_rate_case_roe | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：AENA largest customer second source OR in-house 2026
- **reg_tariff_export**（none）：AENA tariff section 232 2026；AENA export control OR entity list 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"非監管商業 + 巴西驅動非受管制成長，抵消受監管關稅被壓的逆風","columns":{"2Y 驗證點":"商業 RPP > €6.5、巴西 EBITDA 貢獻起量","5Y 驗證點":"商業 RPP ≥ €7.5、巴西成集團 15%+ EBITDA","10Y 驗證點":"非監管收入占比由 ~35% 升至 45%+","具體數字門檻":"商業 RPP ≥ €6.5（FY2025 €6.07 起點）；巴西 2025-2028 capex 投產","信息來源":"AENA FY2025 年報（2026-02-25）；Q1 2026（2026-04-29）；Moodie Davitt 商業追蹤","漂移觸發條件":"連 2 季商業 RPP YoY"}},{"id":"H2","text":"DORA III 政府終裁不惡化到破壞回報——年化關稅路徑 ≥ 持平（非 CNMC 建議的 −0.59%/年）","columns":{"2Y 驗證點":"2026-09-30 部長會議終裁","5Y 驗證點":"2027-2031 IMAP 實際軌跡","10Y 驗證點":"DORA IV（2032+）延續可預測回報","具體數字門檻":"年化 IMAP ≥ 持平；紅線＝","信息來源":"CNMC 官方（cnmc.es）；AENA DORA III 新聞稿；部長會議紀錄","漂移觸發條件":"政府採 CNMC 降價路徑且 AENA/TCI 敗訴無救濟 → 反轉"}},{"id":"H3","text":"估值不進一步 de-rate——股息複利 + 個位數 EPS 成長維持 ~8% 總回報","columns":{"2Y 驗證點":"Fwd PE 守 16-17x、殖利率 4%+","5Y 驗證點":"股息年增 ~5-8%、payout ~70-80%","10Y 驗證點":"DDM 隱含價值隨 rate base 成長","具體數字門檻":"Fwd PE ≥ 15x 且殖利率 4-5%；股息不中止","信息來源":"yfinance 共識；JPM/BofA/Jefferies 評等；歷史殖利率區間","漂移觸發條件":"股息政策中止或 capex 排擠分紅 → 削弱 H3"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"歐元區/西班牙觀光需求衝擊（衰退、地緣、恐攻）→ 月度旅客急跌；疊加 overtourism 政策反制（Barcelona 旅遊稅 2026-04 翻倍至 €10-15/晚、短租 2028 前淘汰、Balearic 尖峰季 €15/晚），壓縮平價/長停旅客消費，直擊 H1 商業 RPP 引擎","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"西班牙月度旅客 YoY（INE + AENA 月報）；商業 RPP 環比","警戒閾值":"連 3 月旅客 YoY −5% → 監控部位；連 3 月 −10% → 減碼"}},{"id":"R2","text":"DORA III 政府終裁採 CNMC 降價路徑（或 PP 凍結案通過）——年化關稅","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"CNMC/部長會議公告；後續 Audiencia Nacional 訴訟 docket","警戒閾值":"年化裁定"}},{"id":"R3","text":"航空去碳化：EU ETS 2026 起航空全額拍賣碳權（免費配額歸零），航司 opex +4-6%，疊加關稅爭議放大航司對邊緣航線的取捨 → 長期歐洲 traffic CAGR 下修","columns":{"對應假設":"H1/H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"EU ETS 航空政策；IATA 長期 traffic 預測；SAF 成本","警戒閾值":"IATA 歐洲 10Y traffic CAGR 下修至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","irr_base_pct":8.0,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":5.7,"ev5y_pct":43.0,"irr_base_pct":8.0,"max_dd_pct":-38.0,"bull_5y_price":49.8,"bear_5y_price":22.1,"p_bull_pct":32.0,"p_bear_pct":23.0,"rearm_trigger":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","price_at_dd":26.94,"archetype":"受監管公用/穩定內需","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"AENA","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Aena S.M.E., S.A."},"oneliner":"DORA III 以年均 +0.33% 費率、准許 WACC 8.32% 落地，監管方向的風險已經解除，剩下的是成本控制與 130 億歐元投資的執行風險。現價約 15.9 倍 FY2026E 本益比，估計 Base 年化報酬約 6%。等年底策略計畫確認 80% 配息，或股價回到 14 倍再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/AENA_20261103/scenario.json","answers":{"q1_business":{"verdict":"Aena 收的是航空公司與旅客的過路錢：受管制機場費，加上把人流變現的商業租金。錢卡在西班牙機場使用權這個節點，但費率天花板由政府決定。","reasoning":"收入分四塊。①受管制航空收入：每旅客費率由五年期 DORA 核定，2027–2031 年均 +0.33%，交通量風險由 Aena 自己承擔（2026-04-16 股東會）。②商業收入：零售、餐飲、免稅以最低保證租金（MAG）標案打底，停車與 VIP 自營；上半年 9.839 億歐元，約占上半年總營收 32.996 億的 30%。③不動產（貨運、物流地上權）：第一季 +16.8%。④國際特許：Luton、巴西 ANB／BOAB、2026-05 併入的 Leeds／Newcastle（51%）、2026-10 交割的 Galeão（100%）；國際業務占 2025 年合併 EBITDA 逾一成。航空、不動產、國際三個分部的金額事實表未收錄。最新數字：前 9 個月營收 5,283.9 百萬歐元、EBITDA 3,077.9 百萬（約 58%）、淨利 1,774.7 百萬；TTM 毛利率 74.65%、營業利益率 47.51%。巴西 Congonhas 的 IFRIC 12 建設收入沒有利潤，會灌大營收、壓低利潤率；第一季排除這部分後，集團營收只成長 6%。單點依賴有兩個：一是最大客戶 Ryanair 占西班牙網絡旅客 19.6%（第一季，量年減 3.4%）；二是費率要由部長會議核定的監管依賴。產業態勢分三面看。競爭面：Ryanair 撤出區域機場運力，easyJet 部分填補，屬局部惡化。結構面：DORA III 核准，Moody's 升 A1、Fitch 升 A+，屬轉好。法規面：CNMC 主張降費、自治區要求共管、曾有凍結費率的修正案，風險仍在。整體判為雙向拉鋸。景氣位置判第三階段：交通量成長由 2025 年上半年 +4.5% 降到 2026 年上半年 +3.7%，馬德里、巴塞隆納自 2027 夏季航季起按航廈管理容量，管理層也說載客率轉弱、燃油避險到期。增速在放慢，但需求沒有反轉。","fact_refs":["f_kpi0_total_consolidated_reven","f_kpi1_ebitda_9m","f_kpi2_net_profit_9m","f_kpi6_passengers_group","f_peer_aena_gross_margin_pct","f_peer_aena_operating_margin_pct"],"verdict_values":{"revenue_quality":"品質高：受管制費率五年鎖定，商業收入有 MAG 保底，能見度高。但交通量風險由公司承擔，IFRIC 12 建設收入沒有利潤，會扭曲營收成長與利潤率。","unit_econ_note":"第一季商業與不動產每旅客營收（排除直線法）€7.6，年增 3.0%；VIP 每旅客 €0.84，年增 27%；停車平均客單價 +5.8%。新標 MAG 方面，特許店較 2025 年 +82%，餐飲 2027 年 +11%、2028 年 +37%。受管制費率 2027–2031 年均 +0.33%。","archetype":{"primary":"受監管公用/穩定內需","secondary":null,"confidence":"高","fingerprint":"政府核定的五年費率框架＋單一國家機場網絡獨佔＋80% 配息＋大型受管制投資週期"},"industry":{"clock_phase":"III","sd_verdict_source":"需求屬結構性持久：由入境觀光帶動，2025 年國際線約 +6%、國內線持平。供給擴張受容量上限與監管核准約束，可逆性低。週期風險落在航空公司的運力與燃油成本，不在機場本身。來源：2026-02-25 年報法說、2026-07-29 半年報法說、Aena 上半年新聞稿。","bargaining":{"up":"上游是工程與維護承包商。CapEx 已發包的比例仍很低，Tenerife South 航廈標案無人投標，維護合約續約時範圍擴大、成本上升，議價力偏向承包商。","down":"下游是航空公司。Ryanair 占西班牙網絡旅客 19.6%；費率雖由政府核定，航空公司仍透過撤運力與遊說施壓（ALA 要求每年降價 4.9%）。","geo":"以西班牙單一國家的監管與政治風險為主，巴西（雷亞爾匯率）與英國特許為輔。"},"profit_pool_dir":"利潤池正由受管制航空段，移往商業（MAG 調升、VIP、停車）、不動產與國際段；受管制段的報酬由准許 WACC 封頂。","tam_table":{"expanded":false,"reason":"受監管機場網絡的成長要看受管制資產基礎、費率與交通量，不適用 TAM 滲透率的框架。交通量路徑另以 DORA III 假設的 2031 年 3.63 億旅客追蹤。"}}}},"q2_moat":{"verdict":"護城河方向持平。法源獨佔沒有鬆動，商業段的定價力在擴大；但受管制段的費率被政治封頂，成本執行也在變差，兩邊相抵。","reasoning":"護城河的機制是政府特許的國家級機場網絡：航線要落地西班牙，就得用 Aena 的機場。這條護城河來自法源，報酬上限也由監管決定。定價面：DORA III 費率年均 +0.33%，介於 Aena 申請的 +3.82% 與 CNMC 建議的 −0.59% 之間；准許 WACC 8.32%，高於 CNMC 主張的 7.44%。WACC 數字取 Quartr 投資人說明摘要；2026-09-21 逐字稿摘錄寫成 2.32%，不在 CNMC 7.44% 與 Aena 9% 之間，判為轉錄誤植。商業面新標 MAG 大幅調升，CFO 在 2026-07-29 也說 VIP 仍有定價力。執行面：第一季西班牙網絡 OpEx +7.9%、人事費用 +12.5%，同期旅客只 +3.2%。核定的受管制成本由 2027 年 19.29 億增至 2031 年 20.79 億（2026 固定價），CFO 承認部分項目有很高的機率做不到。最大客戶 Ryanair 正把運力移出區域機場，最大客戶的份額方向往下，護城河不能判為擴大。同業 ROIC 事實表未涵蓋，改用利潤率比較：Aena 營業利益率 47.51%，高於 PAC 的 43.29% 與 ASR 的 40.81%；FCF 利潤率 15.94%，低於 ASR 的 23.32%，落差主要來自投資週期。評分：執行 7 分、定價 8 分，等級 B。當期 ROIC 屬高利益率、低周轉，但投入資本事實表未涵蓋，無法計算。","fact_refs":["f_peer_aena_gross_margin_pct","f_peer_aena_operating_margin_pct","f_peer_aena_fcf_margin_pct","f_peer_asr_operating_margin_pct","f_peer_asr_fcf_margin_pct","f_peer_pac_operating_margin_pct","f_peer_pac_fcf_margin_pct","f_kpi5_net_financial_debt_net_d"],"verdict_values":{"moat":{"mechanism":"政府特許的國家級機場網絡獨佔，單一營運商、費率受管制；商業段以 MAG 標案把旅客流量變現。護城河來自法源而非競爭，報酬上限也由監管決定。","execution":7,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價擴大：受管制費率 2027–2031 年均 +0.33%、准許 WACC 8.32%，都優於 CNMC 建議；新標 MAG 特許店 +82%、餐飲 2028 年 +37%，VIP 每旅客 +27%。執行縮減：西班牙網絡 OpEx +7.9%、旅客 +3.2%，人事 +12.5%，核定成本比公司提案低約一成。兩者相抵，判為持平。","competitor_notes":[{"name":"ADP.PA","strategy_note":"巴黎機場集團的利潤率事實表無資料。同為受管制歐洲機場，可作監管框架對照：第一季法說中 UBS 提到，法國監管機關表示下期會把燃油衝擊納入交通量與 WACC 假設。數字無法比較。"},{"name":"FHZN.SW","strategy_note":"蘇黎世機場的利潤率事實表無資料。它與 Aena 同場競標 Galeão，是海外特許的直接對手，但 Galeão 最後由 Aena 拿下。"},{"name":"ASR","strategy_note":"營業利益率 40.81%，低於 Aena；FCF 利潤率 23.32%，高於 Aena。Aena 的 FCF 落差主要來自巴西建設期與投資增加，ASR 的投資節奏事實表未涵蓋。"},{"name":"PAC","strategy_note":"營業利益率 43.29%、FCF 利潤率 14.44%，都與 Aena 相近；同樣是受管制費率加商業收入的雙軌結構，但監管國別不同，不宜直接當倍數錨。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率替代；ADP、Flughafen Zürich 兩家的利潤率也缺值。","threats":[{"level":"🟡","text":"Ryanair 撤出區域機場運力：2026 夏季再砍 120 萬座位，Valladolid 旅客 −59.5%（2025 年報導資料）。網絡整體仍在成長，屬點對點攻擊；真正的風險是區域機場的固定成本攤不掉。","p":35,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"level":"🟡","text":"監管與政治壓價：CNMC 建議 DORA III 降費，並呼籲政府確保 2031 年前降費。終裁沒有採納，但 DORA IV 與期中修法仍是壓力。","p":20,"evidence_refs":["regulatory_antitrust#0","end_markets#3","regulated_rate_case_roe#0"]},{"level":"🟡","text":"高鐵替代國內線：鐵路可靠時，馬德里–巴塞隆納、馬德里–馬拉加以高鐵為主。2026 上半年因鐵路故障讓旅客回流航空，屬一次性。","p":25,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"第三方系統單點失效：2025 年 9 月報到系統遭攻擊，波及多個歐洲機場；Aena 自身的供應商集中度未揭露。","p":10,"evidence_refs":["geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（營業利益率 47.51%；投入資本周轉率事實表未涵蓋，依機場資產重的性質判斷）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"三個角色分開看：使用者是旅客，決策者是航空公司（決定航線配置），付款者是旅客（機場費含在票價裡）。入境觀光屬需要而非想要；2026 上半年西班牙旅客 +3.7%，管理層估全年約 +3%。弱點是載客率轉弱與燃油避險到期（2026-07-29 法說）。"},{"item":"決策層級","level":"🟡","text":"替代性要從航空公司「這架飛機放在哪個機場」的層級看。主樞紐與島嶼幾乎沒有替代，區域機場的替代性高：Ryanair 撤運力後，Valladolid 旅客 −59.5%。對旅客而言，替代品只有高鐵，而且只限國內線。"},{"item":"價值鏈分配","level":"🟡","text":"管理層引用 IATA 資料：歐洲航空公司每旅客收入增加約 27%，同期西班牙機場費實質下降 37%（2015–2025，2026-04-16 股東會）。受管制段在價值鏈中分到的份額在縮小；商業段則靠 MAG 標案，把零售承租人的利潤拿回來（特許店 MAG +82%）。"},{"item":"社會容忍度","level":"🔴","text":"屬於高必要、高敏感的類型：費率要部長會議核准，CNMC 主張降費，航空公司要求每年降 4.9%，曾有凍結費率的修正案，自治區也要求共管。管理層自己承諾讓西班牙費率維持歐洲最具競爭力。實際的定價上限是政治上限，低於經濟上限。"}],"roiic":"約 8.3%：受管制增量資本以准許 WACC 8.32% 為上限（稅前或稅後口徑事實表未涵蓋）；若成本超出核定，實際報酬會更低","reinvest_rate":"約 37%（淨利口徑）：留存 20%（配息 80%）＋舉債空間約 17%","endo_ceiling":3.0,"formula_note":"內生成長＝增量報酬 × 再投資率 ≈ 8.3% × 37% ≈ 3.1%，保守取 3.0%。舉債空間的算法：淨負債/EBITDA 由 1.47x 升到 Fitch 預估的 2026–2030 平均約 1.9x，約每年 0.1x EBITDA；以前 9 個月 EBITDA 30.779 億年化約 41 億、淨利年化約 23.5 億估算，約占淨利 17%。D&A 與投入資本事實表未涵蓋，以上是量級估計，不是精算。"}}}},"q3_growth":{"verdict":"五年後的成長跑道屬中等。DORA III 讓受管制資產基礎增加逾 55 億歐元，馬德里、巴塞隆納擴建的容量要到 DORA IV 才完整交付，但擴建核准不由 Aena 掌控，目前看不到可驗證的第二條成長曲線。","reasoning":"成長來源是量、價加上小型併購，沒有回購。量：交通量約年增 2%～3%。DORA 核定 2031 年西班牙網絡 3.63 億旅客；2025 年約 3.22 億（由 2026 年 1.3% 預測對應 3.26 億推回），換算約年增 2%。馬德里、巴塞隆納自 2027 夏季起管理容量。價：受管制費率年均 +0.33%，再加通膨 P 因子；過渡期的 1% 上限已取消，但 CFO 不保證能完全轉嫁通膨。商業 MAG 的調升排到 2028 年。併購：Leeds／Newcastle 自 2026-05 併入、Galeão 自 2026-10 併入，2027 年會有整年效益。共識 EPS：FY2026E 1.74、FY2027E 1.82、FY2028E 1.88，兩年年化 3.9%（Koyfin 快照，分析師家數未載；營收共識分別為 16 與 19 位分析師）。內生天花板約 3.0%（見護城河段），缺口約 0.9pp。缺口可以歸因：一是收購（2027 年 Leeds／Newcastle、Galeão 整年併入），二是 2027 年受管制成本基期重設帶來的一次性抬升，不依賴重新評價。Base 假設 2029 年後 EPS 年增約 2.5%～2.7%。衰退信號亮兩個：區域機場在費率調漲後量縮；投資週期下 FCF/NI 將跌破 0.75（2025 年 0.81，FCF 利潤率由 FY2025 的 27.46% 降到 TTM 的 15.94%）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_passengers_group","f_peer_aena_fcf_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量（交通量年增約 2%～3%，受馬德里、巴塞隆納容量管理限制）＋價（受管制費率 +0.33%／年＋通膨 P 因子；商業 MAG 調升）＋併購（Leeds／Newcastle 51%、Galeão 100%）；無回購","runway_years":"受監管業務不適用滲透率。DORA III 到 2031 年，擴建容量在 DORA IV（2032 年起）交付，可見跑道約 10 年，但擴建核准不由 Aena 掌控","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段的再投資空間：增量報酬約 8.3% × 再投資率約 37% ≈ 3.0%","segments":{"expanded":false,"reason":"分部營收事實表只收錄上半年商業營收 9.839 億（約占上半年總營收 32.996 億的 30%）一項，航空、不動產、國際的金額都沒有收錄。利潤組合的爭點在受管制成本，不在分部組合。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"年度毛利率由 61.06% 升到 70.36%（2022–2025）。季度毛利率事實表未涵蓋；第一季排除 IFRIC 12 的 EBITDA 利潤率 47.4%，對比前一年 47.7%，屬持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"國家網絡獨佔，不適用；最大客戶 Ryanair 移出運力另列為威脅"},{"signal":"提價後銷量下滑","lit":true,"note":"2026 年費率調漲約 6.5% 後，Ryanair 砍區域機場座位，Valladolid −59.5%；網絡整體仍 +3.7%，屬局部現象"},{"signal":"EPS 成長顯著高於營收成長","lit":false,"note":"共識 FY2026E→FY2027E：EPS +4.6%、營收 +4.9%"},{"signal":"FCF/NI 連 2 年低於 0.75","lit":true,"note":"2025 年 0.81，TTM FCF 利潤率降到 15.94%。DORA III 投資年均約 26 億歐元，未來數年會結構性低於 0.75，原因是投資週期而非營運惡化"},{"signal":"SBC/營收高於 5% 且上升","lit":false,"note":"2022–2025 年股數持平，約 15 億股"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"高鐵替代只限國內線；eVTOL 仍在可行性研究階段"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"同業倍數事實表未涵蓋"},{"signal":"維護性 capex 占 FCF 高於 60%","lit":null,"note":"維護與擴張的拆分事實表未涵蓋；第一季 capex 約 3 億，多用於安全與設施改善"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"DORA III 投資近 130 億"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置屬中等。配息率 80%、不做回購、股數持平；併購規模小、時間又新，增量報酬還無法驗證。未來五年投資近 130 億，FCF 付不完配息，差額要靠舉債。","reasoning":"FCF/NI 轉換率：2022 年 1.26、2023 年 0.51、2024 年 0.99、2025 年 0.81，起伏來自投資節奏。SBC 占營收事實表未涵蓋；但以淨利除以稀釋 EPS 推算，2022 年與 2025 年的股數都約 15.0 億股，四年持平。現金去向（2026 年前 9 個月）：營業現金流 2,811.3 百萬歐元；投資付現 1,133.5 百萬（含 Leeds／Newcastle 股權 343.5 百萬）；配息約 1,635 百萬（每股 1.09 歐元 × 15 億股，4 月發放，與 CFO 所說的約 16 億一致）；剩約 0.4 億。Galeão 約 4.9 億歐元在 10 月交割，不在前 9 個月的數字內。9 月底淨財務負債 5,845 百萬，為 EBITDA 的 1.47x，第一季底是 1.32x。2025 年底的槓桿口徑有出入：2026-02-25 CFO 說 1.46x，2026-04-16 股東會說 1.31x，事實表未說明差異來源。DORA III 投資年均約 26 億歐元，是 2025 年 FCF 17.28 億的 1.5 倍，在 80% 配息下，淨負債會持續上升；Fitch 預估 2026–2030 平均約 1.9x。","fact_refs":["f_kpi3_net_operating_cash_flow_","f_kpi4_investment_paid_capex_au","f_kpi5_net_financial_debt_net_d","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Luton、巴西 ANB／BOAB 已併入，國際業務占 2025 年合併 EBITDA 逾一成；ANB 排除 IFRIC 12 後 EBITDA 利潤率 65.7%。但投入資本與收購對價事實表未涵蓋，增量報酬無法與 WACC 比較。Leeds／Newcastle、Galeão 都在 2026 年才交割"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表與逐字稿都沒有回購計畫，股東回報全部走 80% 配息"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"淨利 ÷ 稀釋 EPS：2022 年 9.015 億 ÷ 0.601 ≈ 15.0 億股，2025 年 21.367 億 ÷ 1.42 ≈ 15.05 億股，四年持平；目前股數 15 億，淨稀釋約每年 0%，低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"股東回報以 80% 配息為主，沒有回購。併購（Leeds／Newcastle 51%、Galeão 約 4.9 億歐元）合計約占市值 2%，成長主要來自受管制資產基礎與商業標案，不靠併購撐。"}}}},"q5_valuation":{"verdict":"要有 8% 年化報酬，現價需要 FY2031 EPS 約 2.13（年化約 4%），而且本益比守在 15.9 倍。我們的 Base 只到 2.03，判為偏貴，不追。","reasoning":"這是受監管公用事業，主錨用股息殖利率加股息成長，以及前瞻本益比；PEG 只作參考。前瞻本益比 15.86x（判斷日股價 27.6 ÷ FY2026E 共識 1.74），FY2027E 為 15.16x；EPS 兩年年化 3.9%，PEG 約 4.0。股息殖利率約 3.9%（事實表口徑）。回推需求：8% 年化減掉約 3.9% 殖利率，股價需年化約 4.1%，五年後約 33.7；以 15.86 倍回推，FY2031 EPS 需約 2.13。Base 路徑在 2028 年後因費率 +0.33%、利息與折舊上升而放慢，只到 2.03，終端 15 倍對應約 30.45，估計年化約 6%。P/S 6.08x、EV/S 6.87x 都位於 4 個年度端點的最高點，但部分原因是營業利益率由 32% 升到 47%，所以主看本益比。trailing P/E 13.73x 低於 forward，方向與 EPS 成長相反，疑似幣別或分母口徑混用，不當作承重依據。五年分位所需的高低點事實表未涵蓋。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_ev_s_fwd","f_consensus_rev_3m_fy1_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"股息殖利率＋股息成長為主錨，FY2026E 前瞻本益比為輔；同業倍數事實表未涵蓋","tier":"歐洲受管制機場營運商","peers":{"expanded":false,"reason":"同業本益比與殖利率事實表未涵蓋。同業對照只有利潤率，而且 ADP、Flughafen Zürich 缺值，無法做同層級的倍數錨。"},"fwd_pe":15.86,"peg":4.0,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 15.86x，EPS 兩年年化 3.9%，殖利率約 3.9%。要有 8% 年化，FY2031 EPS 需約 2.13 且倍數不降；Base 為 2.03、終端 15 倍，估計年化約 6%，低於 8%。P/S、EV/S 在 4 個年度端點最高。五年分位事實表未涵蓋。結論偏貴。","upside_short_pct":4.6,"upside_mid_pct":10.3,"denominator_disputed":false,"denominator_note":"分母採 FY2026E 共識 EPS 1.74（事實表標美元口徑，與判斷日股價同幣別）。第二季約 3,000 萬歐元的疫情期 MAG 和解收入屬一次性，約占全年淨利 1%，不構成爭點。另外，trailing P/E 13.73x 低於 forward；股息殖利率 3.949% 恰好等於每股 1.09 歐元 ÷ 27.6，兩者疑似混用歐元與美元，所以不承重。短期上行＝FY2027E 1.82 × 現值 15.86 倍；中期上行＝Base 五年後價格 30.45，不含股息。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方在成本與配息，而不在監管方向。價值陷阱風險屬中等。","reasoning":"最可能看錯的三處，詳見反證紀錄：受管制成本吃掉准許報酬；年底策略計畫下修配息；交通量在容量上限與燃油衝擊下轉弱。衰退信號亮兩個：區域機場漲價後量縮，以及投資週期下 FCF/NI 將跌破 0.75。另有一個訊號方向不明：FY2026E 共識 EPS 三個月下修 4.4%，與營運面上修方向相反，原因事實表未涵蓋。26 週漲 21%；RSI 事實表標示不可用，所以不拿來判斷動能是否過熱。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_kpi5_net_financial_debt_net_d","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"受監管成長兌現，但成本與舉債吃掉股東每股經濟的中度風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.74,"pe":15.86,"basis":"FY2026E 共識 EPS 1.74（Koyfin 美元口徑）對判斷日股價 27.6；終端倍數同樣以終端年的當年 EPS 為分母"},"eps":{"bull":[1.87,1.98,2.1,2.22,2.35],"base":[1.82,1.88,1.93,1.98,2.03],"bear":[1.72,1.66,1.62,1.62,1.64]},"pe":{"bull":18,"base":15,"bear":12},"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":3.9,"net_buyback":0},"second_stage":{"bull_cagr_pct":5,"base_cagr_pct":3},"max_dd":{"lo":-45,"hi":-21,"basis":"上緣 −21%：只有估值回到 12 倍、EPS 照 FY2027E 共識 1.82（約 21.8）。下緣 −45%：交通衝擊年的 EPS 落到 Bear 路徑低點 1.62，本益比壓到 9.5 倍（約 15.4，−44%）。公司歷史最大回撤事實表未涵蓋；前份估的 −38% 落在這個區間內。","trigger_time":null},"basis":{"bull":"交通量年增約 3%（擴建前先用足現有容量），商業 MAG 調升如期，Galeão 與 Leeds／Newcastle 整年貢獻，OpEx 守在核定軌跡；策略計畫目標高於共識，配息維持 80%。終端 18 倍，對應殖利率約 4.4%；同業本益比事實表未涵蓋。","base":"沿用共識 FY2027E 1.82、FY2028E 1.88，之後 EPS 年增約 2.5%～2.7%：費率 +0.33% 加 P 因子、交通量約 2%，利息與折舊上升抵銷部分商業成長。終端 15 倍，略低於現值 15.9 倍與 Jefferies 引用的 2027 年 16.3 倍，反映 2029 年後成長放慢與槓桿上升；同業本益比事實表未涵蓋。","bear":"2027–2028 年燃油或地緣衝擊加上載客率轉弱，交通量低於 DORA 假設；OpEx 超出核定、利息上升，EPS 在 2029 年跌到 1.62 後才緩步回升。策略計畫下修配息或放寬槓桿上限，終端 12 倍（成長熄火，殖利率約 6.7%）。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2026-07-29 法說提到冬季航季沒有能見度、載客率轉弱、燃油避險到期；DORA 期間交通量風險由 Aena 自擔；最大客戶 Ryanair 占 19.6%，且正在撤出區域運力。","assumption":"西班牙旅客年增維持 2%～3%，不出現疫情或燃油危機等級的衝擊。","consequence":"若 2027–2028 年出現燃油或地緣衝擊、旅客年減 5%～10%，而成本已重設在高位，EPS 可能跌到 1.6 附近，本益比壓到 10 倍以下，五年後虧損 40%～50%。","ruling":"部分採納。A1 評等與 1.47x 的淨負債/EBITDA，讓公司撐得過一個衝擊年，−50% 不是五年終點的合理中心，因此放進最大回撤下緣（−45%），不放在 Bear 終點。這個故事與唯一致命點部分重疊：衝擊年最可能逼出配息下修。","watch":"西班牙網絡月度旅客 YoY、載客率、航空燃油價格","evidence_refs":["geo_supply_chain#1","customer_concentration_credit#0"],"fact_refs":["f_kpi5_net_financial_debt_net_d"]},{"view":"論點成功但股東經濟變差","evidence":"核定的受管制成本在 2027–2031 年只增加 7.8%（2026 固定價），CFO 承認部分項目做不到；董事長說債務會大幅上升；第一季債務平均成本升到 2.51%；130 億投資會推高折舊。","assumption":"受管制資產基礎增加逾 55 億歐元、准許 WACC 8.32%，能轉成每股盈餘成長。","consequence":"投資如期完成、交通量也達標，但成本超支，利息與折舊吃掉准許報酬，EPS 年增只剩 1%～2%；FCF 長期付不完配息。股東拿到的是更大的資產，而不是更多的每股現金。","ruling":"採納。Base 已把 2029 年後 EPS 年增壓到約 2.5%，Bear 路徑五年後 EPS 1.64 對應的就是這個故事。","watch":"西班牙網絡 OpEx 年增減旅客年增、淨負債/EBITDA、平均債務成本","evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"],"fact_refs":["f_kpi5_net_financial_debt_net_d"]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 15.86x，EPS 兩年年化 3.9%，PEG 約 4.0；P/S 6.08x、EV/S 6.87x 都在 4 個年度端點的最高點；26 週漲 21%。Jefferies 引用 2027 年本益比 16.3x，TipRanks 平均目標價 €27.56。","assumption":"市場用低成長公用事業約 16 倍的倍數定價，認為 DORA 落地後成長穩定。","consequence":"Base 年化約 6%，低於 8%。若本益比回到 14 倍、EPS 照共識走，兩年後價格約 26.3，價格報酬約 −5%。","ruling":"採納，不追，進場價設在 14 倍 FY2026E（24.4）。P/S 分位偏高，部分反映利潤率由 32% 升到 47%，所以主看本益比。","watch":"FY2026E／FY2027E 共識本益比","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct"]},{"view":"論點失敗","evidence":"CNMC 建議 DORA III 每年降費 0.59%、WACC 7.44%，並呼籲政府確保 2031 年前降費；曾有修正案要凍結 DORA III 期間的機場費；部分自治區要求共管機場，2026-04-16 股東會稱這構成重大風險；Ryanair 公開指責 Aena 壟斷。","assumption":"在政府持股之下，費率仍按法定程序核定，不會被期中修法改寫。","consequence":"若期中凍結費率，或 DORA IV 大幅降費，受管制段報酬會掉到資金成本以下，終端倍數從 15 倍掉到 12 倍以下。","ruling":"短期反駁、長期採納。DORA III 已由部長會議核准，2031 年前的費率路徑已鎖定；CEO 在 2026-02-25 說政治干預不會再發生，這是承諾，不是證據。Base 終端 15 倍略低於現值，Bear 的 12 倍反映這條風險。","watch":"國會的費率相關修正案、自治區共管立法、CNMC 對 DORA IV 的前置報告","evidence_refs":["end_markets#3","regulatory_antitrust#0","regulated_rate_case_roe#0"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 26.94 → 本次 27.6（+2.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=26.94","side_b":"本次 price_at_dd=27.6","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 26.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 26.94 美元：Bull 價 49.8、Bear 價 22.1，五年期望值 +43.0%，基準年化 8.0%，不對稱比 5.7","side_b":"本次情境、股價仍用 26.94 美元：Bull 價 42.3、Bear 價 19.68，五年期望值 +10.7%，基準年化 2.5%，不對稱比 1.55","ruling":"先換情境、股價不動：五年期望值少 32.3 個百分點，基準年化少 5.5 個百分點。不對稱比由 5.7 變為 1.55。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 26.94 美元：五年期望值 +10.7%，基準年化 2.5%，不對稱比 1.55","side_b":"本次情境、股價 27.6 美元：五年期望值 +8.1%，基準年化 2.0%，不對稱比 1.36","ruling":"再換股價、情境不動：起點價上漲 2.4%，五年期望值少 2.6 個百分點，基準年化少 0.5 個百分點，不對稱比由 1.55 降到 1.36。合計五年期望值比前份少 34.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"交通量指引：管理層保守，實際與監管假設偏高","cause":null,"prior_field":null,"side_a":"2026-02-25 CEO 說 2026 年西班牙客流 +1.3% 是自然預估；DORA 提案假設 2027–2031 年年增 1.3%。","side_b":"2026-07-29 執行副董事長改口為約 +3%；上半年實際 +3.7%，CAPA 稱 Aena 低估需求；DORA 核定 2031 年 3.63 億旅客，約年增 2%。","ruling":"可調和，屬程度差異。管理層在費率提案期有低報交通量的誘因；實際偏高對 Aena 有利，因為每旅客費率已鎖定、交通風險自擔。但 2027 夏季起馬德里、巴塞隆納按航廈管理容量，上行有天花板，所以 Base 只用約 2%～3%。","evidence_level":"逐字稿＋公司新聞稿＋CAPA 報導","settle_metric":"2027 年西班牙網絡旅客年增率，對比 2%","if_then":["若 2027 年旅客年增 ≥ 3%，且 OpEx 缺口 ≤ 4pp → 上調 Bull 機率並重跑 DD","若 2027 年旅客年增 < 1% → 停止加碼，Bear 機率提到 35%"],"evidence_refs":["supply_demand_durability#2","end_markets#2"]},{"axis":"營運費用：公司提案假設與核定上限的落差","cause":null,"prior_field":null,"side_a":"2026-04-29 CFO 說 DORA III 提案數字仍有效，但承認油價帶動的通膨當時沒有納入；2026-02-25 CFO 說人事費用上升的趨勢不會改變。","side_b":"2026-09-21 核定受管制成本由 2027 年 19.29 億增至 2031 年 20.79 億（2026 固定價）；Bernstein 指出比原始假設低約一成，CFO 承認部分項目有很高的風險做不到，差異數字延到策略計畫才說明。","ruling":"可調和，但幅度大：兩邊都往上，差在速度。2025 年實際受管制成本 16.5 億，重設到 2027 年的 19.29 億，等於已容納約每年 8% 的成長；之後四年核定只增 7.8%（約每年 1.9%），公司人事費用卻仍是雙位數成長。這是第一個假設成不成立的主戰場，Base 已把 2029 年後 EPS 年增壓到 2.5%～2.7%。","evidence_level":"逐字稿（2026-02-25、04-29、09-21）","settle_metric":"2027 年起西班牙網絡 OpEx 年增減旅客年增","if_then":["若 2027 年起連 4 季 > 4pp → 停止加碼，Bear 機率提到 35%","若連 6 季 > 6pp → 減碼一半","反向條件：若策略計畫的 OpEx 目標不高於核定軌跡，且 2027 上半年缺口 ≤ 2pp → 解除這條警示"],"evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"]},{"axis":"80% 配息承諾與債務大幅上升","cause":null,"prior_field":null,"side_a":"2026-07-29 CFO 說 80% 配息政策不會偏離，新政策要等 DORA 之後的策略計畫；2026-04-16 董事長希望在策略計畫中確認配息率。","side_b":"2026-09-21 董事長說債務會大幅上升；2026-07-29 UBS 問可接受的槓桿上限，管理層不給數字；Fitch 預估 2026–2030 平均淨槓桿約 1.9x（9 月底為 1.47x）。","ruling":"可調和。A1／A+ 評等與 1.9x 的路徑還有空間，維持 80% 的機率較高。但這是唯一致命點，決勝數據在年底的策略計畫，在那之前不可裁決。","evidence_level":"逐字稿＋評等機構","settle_metric":"策略計畫的配息率與淨負債上限","if_then":["若配息率 < 70% 或改以股代息 → 取消進場條件並重跑 DD；已持有則減碼一半","若維持 80% 且淨負債上限 ≤ 2.5x → 解除唯一致命點，進場只剩價格條件"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"投資執行：不超投的承諾與發包進度","cause":null,"prior_field":null,"side_a":"2026-09-21 執行副董事長說不會投超過核定的 100 億；CFO 說工程招標一向要求固定價格。","side_b":"同一場 CFO 說已發包的比例「仍很低」，不給百分比；Tenerife South 航廈流標；策略性投資占 40%～50%，落後會被罰；部分投資可能延到 DORA IV。","ruling":"可調和。投資延後會降低近期的債務與折舊，對短期 EPS 反而有利；但策略性項目落後有罰則，擴建容量延後也會壓抑 DORA IV 的成長。列為中期風險，不改 Base。","evidence_level":"逐字稿 2026-09-21","settle_metric":"年度受管制投資執行率（法定彈性下限 80%）與策略性項目罰款","if_then":["若任一年度策略性投資遭罰，或延到 DORA IV 的金額 > 10 億歐元 → 下修五年後的跑道判斷並停止加碼"],"evidence_refs":[]},{"axis":"共識下修與營運上修方向相反","cause":null,"prior_field":null,"side_a":"FY2026E 共識 EPS 三個月由 1.82 降到 1.74（−4.4%），近兩週再降 0.57%。","side_b":"同期交通量的全年估計由 1.3% 上調到約 3%；前 9 個月淨利 1,774.7 百萬歐元；第二季 EBITDA 只比共識低 0.8%。","ruling":"不可裁決，要等到 2027-02 年報。下修原因事實表未涵蓋，可能包含美元換算或成本預估上調。Bear 第一年 EPS 1.72 已低於現行共識，不再另外下調。","evidence_level":"Koyfin 快照＋公司新聞稿","settle_metric":"FY2026 實際 EPS，對比 1.74","if_then":["若 FY2026 實際 EPS 低於 1.70 → Bear 機率提到 35%，重算終端倍數","若 FY2027E 共識再下修超過 5% → 停止加碼"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"DORA III 終裁每年 +0.33%，優於 CNMC 建議的 −0.59%；WACC 8.32%，高於 CNMC 的 7.44%；Moody's 升 A1、Fitch 升 A+；交通量超出預期；MAG 在 2027–2028 年大幅調升；董事長預告策略計畫的財務目標企圖心高，年底前就是催化劑；殖利率約 4%。","side_b":"現價為 15.9 倍 FY2026E，EPS 兩年年化 3.9%，P/S、EV/S 在 4 個年度端點最高；要有 8% 年化，FY2031 EPS 需約 2.13 且倍數不降，Base 只有 2.03。","ruling":"不追。好消息大多已反映在 7 月之前的漲幅裡（26 週 +21%，7 月以來只 +2.4%），剩下的上行要等策略計畫給出高於共識的 2031 年目標。","evidence_level":"公司新聞稿＋評等機構＋賣方報導","settle_metric":"策略計畫 2031 年淨利目標隱含的 EPS 年化成長","if_then":["若策略計畫的 2031 年淨利目標隱含 EPS 年化 ≥ 5%，且維持 80% 配息 → 重跑 DD，進場價可放寬到 15 倍 FY2027E（約 27.3）","若股價在策略計畫發布前先漲到 30 以上 → 不追"],"evidence_refs":["capital_markets_pricing#0","customer_concentration_credit#3"]},{"axis":"前份觀望的主因（DORA III 終裁）已落地","cause":"新證據","prior_field":["signal","archetype","cycle_position"],"side_a":"前份結論為觀望、追蹤，等待 2026-09-30 前的 DORA III 終裁，要求年化費率 ≥ 持平。","side_b":"2026-09-15 部長會議核准：年均 +0.33%、WACC 8.32%、受管制投資近 100 億。前份第二個假設成立。","ruling":"訊號維持 B，類型維持受監管公用；非循環股，不設景氣位置。監管方向的風險解除，但綁定約束改為估值（Base 年化約 6%）。本輪結論依新輸入重新判定。","evidence_level":"公司新聞稿＋投資人說明","settle_metric":null,"if_then":[],"evidence_refs":["regulated_rate_case_roe#1","regulated_rate_case_roe#2"]},{"axis":"估值結論維持偏貴","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 26.94，估值偏貴。","side_b":"本輪股價 27.6（+2.4%），FY2026E 本益比 15.86x，Base 年化約 6%。","ruling":"估值結論不變。本益比下降來自共識 EPS 上移，不是因為股價變便宜。","evidence_level":"事實表","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤區間調整","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 32%、Bear 23%，最大回撤 −38%。","side_b":"本輪 Bull 22%、Base 48%、Bear 30%；最大回撤 −21% 到 −45%。","ruling":"本輪加做內生天花板檢核：Base EPS 年化 3.1%，略高於天花板 3.0%，Bear 機率因此提高到 30%。DORA 終裁費率已知（+0.33%，低於 Aena 申請的 +3.82%），Bull 失去高費率路徑，散布收窄。最大回撤改給區間，下緣對應交通衝擊年 EPS 1.62 乘以 9.5 倍。","evidence_level":"情境推導","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險升一級，護城河與跑道不變","cause":"新證據","prior_field":["trap","moat_trend","runway_post_y5"],"side_a":"前份：陷阱 🟢、護城河持平、五年後跑道 🟡。","side_b":"本輪：陷阱 🟡（區域機場量縮、FCF/NI 將跌破 0.75、核定成本偏緊、FY2026E 共識三個月 −4.4%）；護城河持平；跑道 🟡（擴建在 DORA IV 交付，但核准不由公司掌控）。","ruling":"陷阱風險升一級，原因是成本與舉債對每股經濟的壓力已有證據，不是監管方向轉壞。商業定價力擴大，抵銷了執行面的變差，所以護城河仍判持平。","evidence_level":"逐字稿＋報導＋事實表","settle_metric":"西班牙網絡 OpEx 缺口、FCF/NI","if_then":["若 2027 年 FCF/NI 低於 0.5 且 EPS 未達共識 → 陷阱判斷升為 🔴，停止加碼"],"evidence_refs":["competitive_share_entrants#0","regulated_rate_case_roe#0"]},{"axis":"進場條件重設","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"DORA III 政府終裁允許 ≥ 持平關稅路徑（2026-09-30 前）且訴訟風險釐清，或股價回落至 €24 以下（Fwd PE ≤15x）","side_b":"股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）且年底策略計畫維持 80% 配息率，兩者同時成立才重跑 DD 決定進場首倉","ruling":"前份進場條件的 DORA 那一半已在 2026-09-15 觸發（+0.33% ≥ 持平），訴訟風險事實表未涵蓋；價格那一半沒有觸發（現價 27.6）。監管不確定性解除後，綁定約束改為估值與配息政策，進場首倉改成價格與策略計畫兩個條件同時成立。倍數門檻由 15 倍降到 14 倍，因為 DORA 費率已知偏低、2029 年後成長放慢，要到 14 倍才有約 8%～9% 的年化報酬。","evidence_level":"公司新聞稿＋事實表","settle_metric":"股價與策略計畫配息率","if_then":[],"evidence_refs":["regulated_rate_case_roe#2"]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"2027–2031 策略計畫（預計 2026 年底前發布）把配息率由 80% 下修到 70% 以下，或改為以股代息，用來支應約 130 億歐元的投資","ruling":"前份最大的二元事件是 DORA III 終裁，已經落地。本輪最大的單一敏感項改為策略計畫的配息率：總回報約三分之二來自股息，配息率由 80% 降到 65%，等於股息少將近兩成，直接打到靠殖利率支撐的本益比。若發生，取消進場條件並重跑 DD；已持有則減碼一半。","evidence_level":"逐字稿 2026-04-16、07-29、09-21","settle_metric":"策略計畫配息率","if_then":["若配息率 < 70% → 減碼一半，未持有則取消進場條件"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）","side_b":"本輪設五條：配息率 < 70%；2027 年起 OpEx 缺口連 4 季 > 4pp；月度旅客連 3 個月 ≤ −10%；淨負債/EBITDA > 2.5x；Ryanair 占比 < 17%","ruling":"前份只在風險敘述裡帶門檻，本輪把門檻集中成每季可以核對的指標。任一條觸發，已持有就減碼一半；配息率與月度旅客兩條同時觸發則清倉。","evidence_level":"方法調整","settle_metric":null,"if_then":["任一條觸發 → 減碼一半","配息率與月度旅客兩條同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"風險門檻的退休與替換","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份 R1：連 3 月旅客 YoY −5% 監控、連 3 月 −10% 減碼。R2：DORA III 終裁採 CNMC 降價路徑，年化費率低於持平。R3：EU ETS 航空碳權全額拍賣，IATA 歐洲 10 年交通 CAGR 下修。","side_b":"R1 門檻原樣保留（−5% 監控、−10% 減碼）。R2 退休：終裁為 +0.33%，門檻確定不會成立。R3 改為長期的政治與社會容忍度風險；交通量的長期門檻，改看 DORA 假設的 2031 年 3.63 億旅客。","ruling":"R2 退休，理由是事件已結算，而且方向對 Aena 有利。ETS 本輪沒有新證據，前份門檻原文已截斷、無法核對；既然交通量風險由公司自擔，改用更直接的 DORA 旅客路徑來監測。R1 的減碼門檻不變。","evidence_level":"公司新聞稿＋前份判斷","settle_metric":null,"if_then":[],"evidence_refs":["regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"年底策略計畫若把配息率降到 70% 以下，或改以股代息，唯一致命點成立","type":"Single Thing","maps_to":"H3","metric":"2027–2031 策略計畫配息率","threshold":"< 70% 或改以股代息","action":"未持有：取消進場條件並重跑 DD；已持有：減碼一半","source_freq":"Aena 策略計畫，一次性（預計 2026 年底前）","date":"2026-12-31","evidence_refs":["customer_concentration_credit#2"]},{"n":2,"text":"股價回到 14 倍 FY2026E，且策略計畫維持 80% 配息，才重跑 DD","type":"估值rearm","maps_to":"H3","metric":"股價 ÷ FY2026E 共識 EPS；策略計畫配息率","threshold":"股價 ≤ 24.4 且配息率 ≥ 80%","action":"重跑 DD，確認後建立首筆小部位","source_freq":"股價每日；策略計畫一次性","date":null,"evidence_refs":[]},{"n":3,"text":"受管制成本重設後，西班牙網絡營運費用的成長若持續明顯快過旅客，准許報酬會被吃掉","type":"假設驗證","maps_to":"H1","metric":"西班牙網絡 OpEx 年增減西班牙旅客年增","threshold":"2027 年起連 4 季 > 4pp；連 6 季 > 6pp","action":"連 4 季：停止加碼；連 6 季：減碼一半","source_freq":"Aena 季報，每季","date":"2027-07-31","evidence_refs":["regulated_rate_case_roe#0"]},{"n":4,"text":"商業與不動產每旅客營收成長若低於 3%，非受管制段撐不起 EPS","type":"假設驗證","maps_to":"H2","metric":"商業與不動產每旅客營收（排除直線法調整）年增","threshold":"連 2 季 < +3%","action":"停止加碼","source_freq":"Aena 季報，每季","date":"2027-04-30","evidence_refs":[]},{"n":5,"text":"西班牙旅客的月度年增轉負，而交通量風險由公司自擔","type":"風險","maps_to":"R1","metric":"西班牙網絡月度旅客 YoY","threshold":"連 3 個月 ≤ −5% 監控；連 3 個月 ≤ −10% 減碼","action":"≤ −10%：減碼一半；未持有則凍結進場條件，直到旅客回正","source_freq":"Aena 月度交通量，每月","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":6,"text":"最大客戶 Ryanair 持續撤出運力","type":"風險","maps_to":"R3","metric":"Ryanair 占西班牙網絡旅客比重與年增","threshold":"占比 < 17% 或單季年減 > 10%","action":"停止加碼，重算區域機場成本攤提對 EPS 的影響","source_freq":"Aena 季報分航空公司交通量，每季","date":null,"evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":7,"text":"投資週期把槓桿推過評等容忍區","type":"減碼","maps_to":"H3","metric":"淨負債/EBITDA；Moody's／Fitch 評等","threshold":"> 2.5x，或任一家評等降到 A 級以下","action":"減碼一半","source_freq":"Aena 季報；評等公告","date":null,"evidence_refs":[]},{"n":8,"text":"期中修法凍結費率，或自治區共管機場入法","type":"清倉","maps_to":"R4","metric":"國會費率凍結修正案、機場共管立法","threshold":"任一案完成立法程序","action":"清倉；未持有則移除進場條件","source_freq":"國會議程，事件型","date":null,"evidence_refs":["end_markets#3","regulatory_antitrust#0"]},{"n":9,"text":"FY2026 年報與策略計畫發布後複審","type":"複審日期","maps_to":null,"metric":"FY2026 EPS 對比 1.74；2027 年交通量與 OpEx 指引","threshold":"到期即複審","action":"重跑 DD","source_freq":"一次性","date":"2027-03-15","evidence_refs":[]}],"kill_metrics":[{"metric":"2027–2031 策略計畫配息率","bear_threshold":"< 70% 或改以股代息","window":"2026-12 策略計畫發布","source":"Aena 策略計畫","last_status":"unknown"},{"metric":"西班牙網絡 OpEx 年增減西班牙旅客年增","bear_threshold":"2027 年起連 4 季 > 4pp","window":"2027Q1–2028Q4","source":"Aena 季報","last_status":"warning"},{"metric":"西班牙網絡月度旅客 YoY","bear_threshold":"連 3 個月 ≤ −10%","window":"每月滾動","source":"Aena 月度交通量","last_status":"ok"},{"metric":"淨負債/EBITDA","bear_threshold":"> 2.5x","window":"每季","source":"Aena 季報","last_status":"ok"},{"metric":"Ryanair 占西班牙網絡旅客比重","bear_threshold":"< 17%","window":"每季","source":"Aena 季報分航空公司交通量","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）且年底策略計畫維持 80% 配息率，兩者同時成立才重跑 DD 決定首倉","exec_line":"觀望，不追。綁定約束是估值：估計 Base 年化約 6%，低於 8%；策略計畫的配息率是唯一致命點。兩者都過關，才重跑 DD 決定首倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等年底策略計畫確認配息率 ≥ 80%，且股價 ≤ 24.4（FY2026E 共識本益比 ≤ 14 倍）；兩者同時成立才重跑 DD","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"DORA III 的受管制段按核定兌現：2027 年成本重設後，西班牙網絡營運費用的成長不會明顯快過旅客與核定成本軌跡，策略性投資也按時程執行。","2y":null,"5y":"2031 年受管制成本實際值，超出核定的 20.79 億歐元（2026 固定價）不到 5%","10y":null,"threshold":"2027 年起，西班牙網絡 OpEx 年增減旅客年增 ≤ 4pp；各機場投資執行率 ≥ 80%（法定彈性下限）","source":"Aena 季報西班牙網絡成本表；DORA III 年度執行資料；2026-09-21 投資人說明會","drift_rule":"缺口超過 4pp 連 4 季＝削弱；超過 6pp 連 6 季＝反轉"},{"id":"H2","text":"非受管制段（商業、不動產、國際）帶動集團 EPS 年增 ≥ 3%，抵銷受管制費率年均只有 +0.33% 的逆風。","2y":"新標 MAG（特許店 +82%、餐飲 2027 年 +11%／2028 年 +37%）如期入帳；商業與不動產每旅客營收以 2026 年第一季的 €7.6 為起點，每年 ≥ +3%","5y":null,"10y":null,"threshold":"商業與不動產每旅客營收（排除直線法）年增 ≥ 3%；FY2027 EPS ≥ 共識 1.82 的 95%","source":"Aena 季報商業段揭露；Koyfin 共識快照","drift_rule":"連 2 季低於門檻 5% 以上＝削弱；連 3 季低於門檻 10% 以上＝反轉"},{"id":"H3","text":"130 億歐元的投資週期，不犧牲股東的現金回報：配息率維持 80%，槓桿與評等守得住。","2y":null,"5y":"2027–2031 年配息率維持 80%，淨負債/EBITDA 不超過 2.5x，評等維持 A 級","10y":null,"threshold":"配息率 ≥ 80%；淨負債/EBITDA ≤ 2.5x（Fitch 預估 2026–2030 平均約 1.9x）；Moody's／Fitch 維持 A 級","source":"2026 年底策略計畫；Aena 季報淨負債；Moody's、Fitch 評等公告","drift_rule":"槓桿連 4 季高於 Fitch 路徑 5% 以上＝削弱；配息率下修＝反轉"}],"R":[{"id":"R1","text":"燃油避險到期、載客率轉弱、地緣衝突，讓西班牙交通量轉弱；交通量風險由公司自擔，會同時打到受管制收入與商業收入。","h_ref":"H2","clock":"⚡","threshold":"西班牙網絡月度旅客 YoY 連 3 個月 ≤ −5% 監控；連 3 個月 ≤ −10% 減碼","evidence_refs":["geo_supply_chain#1"]},{"id":"R2","text":"核定成本比公司提案低約一成，CFO 承認部分項目做不到；人事費用連年雙位數成長，會吃掉准許報酬。","h_ref":"H1","clock":"🔥","threshold":"2027 年起，西班牙網絡 OpEx 年增減旅客年增，連 4 季 > 4pp","evidence_refs":["regulated_rate_case_roe#0","regulatory_antitrust#0"]},{"id":"R3","text":"最大客戶 Ryanair（占 19.6%，第一季量年減 3.4%）持續撤出區域機場運力；區域機場的固定成本攤不掉，商業收入也跟著流失。","h_ref":"H1","clock":"🔥","threshold":"Ryanair 占西班牙網絡旅客比重 < 17%，或單季年減 > 10%","evidence_refs":["competitive_share_entrants#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"政治與社會容忍度：CNMC 主張降費、曾有凍結費率的修正案、自治區要求共管，期中修法或 DORA IV 大幅降費，會壓縮受管制報酬。","h_ref":"H3","clock":"🐢","threshold":"費率凍結或共管完成立法；或 CNMC 在 DORA IV 前置報告中主張 WACC 低於 7.5%","evidence_refs":["end_markets#3","regulatory_antitrust#0"]},{"id":"R5","text":"投資執行落後：Tenerife South 流標、已發包比例仍很低、巴塞隆納擴建核准不由 Aena 掌控；策略性項目落後會被罰，擴建容量也會延後。","h_ref":"H1","clock":"🔥","threshold":"任一年度策略性投資遭罰，或延到 DORA IV 的金額 > 10 億歐元","evidence_refs":[]}],"single_thing":{"description":"2027–2031 策略計畫（預計 2026 年底前發布）把配息率由 80% 下修到 70% 以下，或改為以股代息，用來支應約 130 億歐元的投資。","why_fatal":"本檔的總回報約三分之二來自股息（殖利率約 4%，EPS 年化約 3%）。配息率由 80% 降到 65%，等於股息少將近兩成；靠殖利率支撐的本益比會失去錨，終端倍數要改看 12 倍一帶，五年價格報酬由正轉負。","if_happens":"未持有：取消進場條件並重跑 DD。已持有：減碼一半，在新配息政策下的殖利率回到 5% 以上之前不回補。","how_monitor":"看策略計畫的財務目標（配息率、淨負債上限、2031 年淨利目標）。對照基準：2026-07-29 CFO 說新計畫出來前 80% 配息不偏離，以及 Fitch 平均槓桿約 1.9x 的假設。","probability":"12 個月內約 20%。管理層承諾 80% 配息，董事長也預告目標企圖心高；但管理層已承認債務會大幅上升，並拒絕回答可接受的槓桿上限。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.16,"peg_fy2":3.8,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.42,"FY2026E":1.74,"FY2027E":1.82,"FY2028E":1.88},"fy_end_month":12,"eps_basis":"共識 EPS 為 Koyfin 快照，事實表標美元口徑，與判斷日股價同幣別。FY2025A 的 1.42 是年報歐元稀釋 EPS，幣別不同，不宜直接拿來和共識算成長率；三年共識成長以 FY2026E→FY2028E 的年化約 3.9% 為準。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"2027–2031 策略計畫發布（配息率、淨負債上限、2031 年財務目標）","impact":"高","watch":"配息率是否 ≥ 80%；2031 年淨利目標隱含的 EPS 年化成長"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"公布 2027 年費率的 K 因子與 P 因子","impact":"中","watch":"P 因子能否轉嫁 2026 年約 10% 的西班牙 OpEx 通膨"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 年報與 2027 年交通量指引","impact":"中","watch":"FY2026 EPS 對比 1.74；2027 年交通量與 OpEx 指引"},{"date":"2027-03","date_precision":"month","type":"regulatory","event":"DORA III 第一年費率生效（依往年 3 月 1 日調費的慣例）","impact":"中","watch":"費率調整後航空公司的運力配置，特別是 Ryanair 在區域機場的動向"},{"date":"2027-03","date_precision":"month","type":"capacity","event":"馬德里、巴塞隆納自 2027 夏季航季起按航廈管理容量","impact":"中","watch":"兩大樞紐旅客成長是否被壓到 2% 以下"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=21.16, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='受監管公用/穩定內需', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：reg_tariff_export（關稅／出口管制）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
